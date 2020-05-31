"""
Defines atcli's main functionality.
"""

# !/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import audioop
import json
import math
import multiprocessing
import os
import subprocess
import sys
import tempfile
import wave
from typing import List, Pattern, Optional

import requests

from atcli.SRTParser import SRTParser

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
from googleapiclient.discovery import build
from progressbar import ProgressBar, Percentage, Bar, ETA

from atcli.constants import (
    LANGUAGE_CODES, GOOGLE_SPEECH_API_KEY, GOOGLE_SPEECH_API_URL,
)
from atcli.formatters import FORMATTERS

DEFAULT_SUBTITLE_FORMAT = 'srt'
DEFAULT_CONCURRENCY = 10
DEFAULT_SRC_LANGUAGE = 'en-US'
DEFAULT_DST_LANGUAGE = 'en-US'


def percentile(arr, percent):
    """
    Calculate the given percentile of arr.
    """
    arr = sorted(arr)
    index = (len(arr) - 1) * percent
    floor = math.floor(index)
    ceil = math.ceil(index)
    if floor == ceil:
        return arr[int(index)]
    low_value = arr[int(floor)] * (ceil - index)
    high_value = arr[int(ceil)] * (index - floor)
    return low_value + high_value


class FLACConverter(object):  # pylint: disable=too-few-public-methods
    """
    Class for converting a region of an input audio or video file into a FLAC audio file
    """

    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path = source_path
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            # delete=False necessary for running on Windows
            temp = tempfile.NamedTemporaryFile(suffix='.flac', delete=False)
            program_ffmpeg = which("ffmpeg")
            command = [str(program_ffmpeg), "-ss", str(start), "-t", str(end - start),
                       "-y", "-i", self.source_path,
                       "-loglevel", "error", temp.name]
            use_shell = True if os.name == "nt" else False
            subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)
            read_data = temp.read()
            temp.close()
            os.unlink(temp.name)
            return read_data

        except KeyboardInterrupt:
            return None


class SpeechRecognizer(object):  # pylint: disable=too-few-public-methods
    """
    Class for performing speech-to-text for an input FLAC file.
    """

    def __init__(self, language="en", rate=44100, retries=3, api_key=GOOGLE_SPEECH_API_KEY):
        self.language = language
        self.rate = rate
        self.api_key = api_key
        self.retries = retries

    def __call__(self, data):
        try:
            for _ in range(self.retries):
                url = GOOGLE_SPEECH_API_URL.format(lang=self.language, key=self.api_key)
                headers = {"Content-Type": "audio/x-flac; rate=%d" % self.rate}

                try:
                    resp = requests.post(url, data=data, headers=headers)
                    # print(resp.content)
                except requests.exceptions.ConnectionError:
                    continue

                for line in resp.content.decode('utf-8').split("\n"):
                    try:
                        line = json.loads(line)
                        line = line['result'][0]['alternative'][0]['transcript']
                        return line[:1].upper() + line[1:]
                    except IndexError:
                        # no result
                        continue
                    except JSONDecodeError:
                        continue

        except KeyboardInterrupt:
            return None


class Translator(object):  # pylint: disable=too-few-public-methods
    """
    Class for translating a sentence from a one language to another.
    """

    def __init__(self, language, api_key, src, dst):
        self.language = language
        self.api_key = api_key
        self.service = build('translate', 'v2',
                             developerKey=self.api_key)
        self.src = src
        self.dst = dst

    def __call__(self, sentence):
        try:
            if not sentence:
                return None

            result = self.service.translations().list(  # pylint: disable=no-member
                source=self.src,
                target=self.dst,
                q=[sentence]
            ).execute()

            if 'translations' in result and result['translations'] and \
                    'translatedText' in result['translations'][0]:
                return result['translations'][0]['translatedText']

            return None

        except KeyboardInterrupt:
            return None


def which(program):
    """
    Return the path for a given executable.
    """

    def is_exe(file_path):
        """
        Checks whether a file is executable.
        """
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    # necessary to run on Windows
    if os.name == "nt":
        program += ".exe"
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        # looks for file in the script execution folder before checking on system path
        current_dir = os.getcwd()
        local_program = os.path.join(current_dir, program)
        if is_exe(local_program):
            return local_program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
    return None


def extract_audio(filename, channels=1, rate=16000):
    """
    Extract audio from an input file to a temporary WAV file.
    """
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(filename):
        print("The given file does not exist: {}".format(filename))
        raise Exception("Invalid filepath: {}".format(filename))
    program_ffmpeg = which("ffmpeg")
    if not program_ffmpeg:
        print("ffmpeg: Executable not found on machine.")
        raise Exception("Dependency not found: ffmpeg")
    command = [str(program_ffmpeg), "-y", "-i", filename,
               "-ac", str(channels), "-ar", str(rate),
               "-loglevel", "error", temp.name]
    use_shell = True if os.name == "nt" else False
    subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)
    return temp.name, rate


def find_speech_regions(filename, frame_width=4096, min_region_size=0.5,
                        max_region_size=6):  # pylint: disable=too-many-locals
    """
    Perform voice activity detection on a given audio file.
    """
    reader = wave.open(filename)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()
    chunk_duration = float(frame_width) / rate

    n_chunks = int(math.ceil(reader.getnframes() * 1.0 / frame_width))
    energies = []

    for _ in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.2)

    elapsed_time = 0

    regions = []
    region_start = None

    for energy in energies:
        is_silence = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size

        if (max_exceeded or is_silence) and region_start:
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                region_start = None

        elif (not region_start) and (not is_silence):
            region_start = elapsed_time
        elapsed_time += chunk_duration
    return regions


def generate_subtitles(  # pylint: disable=too-many-locals,too-many-arguments
        source_path,
        output=None,
        concurrency=DEFAULT_CONCURRENCY,
        src_language=DEFAULT_SRC_LANGUAGE,
        dst_language=DEFAULT_DST_LANGUAGE,
        subtitle_file_format=DEFAULT_SUBTITLE_FORMAT,
        api_key=None,
        generate_txt=False
):
    """
    Given an input audio/video file, generate subtitles in the specified language and format.
    """



    audio_filename, audio_rate = extract_audio(source_path)

    regions = find_speech_regions(audio_filename)

    pool = multiprocessing.Pool(concurrency)
    converter = FLACConverter(source_path=audio_filename)
    recognizer = SpeechRecognizer(language=src_language, rate=audio_rate,
                                  api_key=GOOGLE_SPEECH_API_KEY)

    transcripts = []
    if regions:
        try:
            widgets = ["Converting speech regions to FLAC files: ", Percentage(), ' ', Bar(), ' ',
                       ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
            extracted_regions = []
            for i, extracted_region in enumerate(pool.imap(converter, regions)):
                extracted_regions.append(extracted_region)
                pbar.update(i)
            pbar.finish()

            widgets = ["Performing speech recognition: ", Percentage(), ' ', Bar(), ' ', ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()

            for i, transcript in enumerate(pool.imap(recognizer, extracted_regions)):
                transcripts.append(transcript)
                pbar.update(i)
            pbar.finish()

            if src_language.split("-")[0] != dst_language.split("-")[0]:
                if api_key:
                    google_translate_api_key = api_key
                    translator = Translator(dst_language, google_translate_api_key,
                                            dst=dst_language,
                                            src=src_language)
                    prompt = "Translating from {0} to {1}: ".format(src_language, dst_language)
                    widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                    pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
                    translated_transcripts = []
                    for i, transcript in enumerate(pool.imap(translator, transcripts)):
                        translated_transcripts.append(transcript)
                        pbar.update(i)
                    pbar.finish()
                    transcripts = translated_transcripts
                else:
                    print(
                        "Error: Subtitle translation requires specified Google Translate API key. "
                        "See --help for further information."
                    )
                    return 1

        except KeyboardInterrupt:
            pbar.finish()
            pool.terminate()
            pool.join()
            print("Cancelling transcription")
            raise

    timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
    formatter = FORMATTERS.get(subtitle_file_format)
    formatted_subtitles = formatter(timed_subtitles)

    dest = output

    if not dest:
        base = os.path.splitext(source_path)[0]
        dest = "{base}.{format}".format(base=base, format=subtitle_file_format)

    with open(dest, 'wb') as output_file:
        output_file.write(formatted_subtitles.encode("utf-8"))

    if generate_txt:
        SRTParser.extractTextFromSRT(str(dest))
    os.remove(audio_filename)

    return dest


def validate(args):
    """
    Check that the CLI arguments passed to atcli are valid.
    """
    if args.format not in FORMATTERS:
        print(
            "Subtitle format not supported. "
            "Run with --list-formats to see all supported formats."
        )
        return False

    # if args.src_language not in LANGUAGE_CODES.keys():
    #     print(
    #         "Source language not supported. "
    #         "Run with --list-languages to see all supported languages."
    #     )
    #     return False
    #
    # if args.dst_language not in LANGUAGE_CODES.keys():
    #     print(
    #         "Destination language not supported. "
    #         "Run with --list-languages to see all supported languages."
    #     )
    #     return False

    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False

    return True


def main():
    """
    Run atcli as a command-line program.
    """
    #
    # # bug on macos, disable multiprocessing
    # multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the video or audio file to subtitle",
                        nargs='?')
    parser.add_argument('-C', '--concurrency', help="Number of concurrent API requests to make",
                        type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument('-o', '--output',
                        help="Output path for subtitles (by default, subtitles are saved in \
                        the same directory and name as the source path)")
    parser.add_argument('-F', '--format', help="Destination subtitle format",
                        default=DEFAULT_SUBTITLE_FORMAT)
    parser.add_argument('-S', '--src-language', help="Language spoken in source file",
                        default=DEFAULT_SRC_LANGUAGE)
    parser.add_argument('-D', '--dst-language', help="Desired language for the subtitles",
                        default=DEFAULT_DST_LANGUAGE)
    parser.add_argument('-K', '--api-key',
                        help="The Google Translate API key to be used. \
                        (Required for subtitle translation)")
    parser.add_argument('--list-formats', help="List all available subtitle formats",
                        action='store_true')
    parser.add_argument('--list-languages', help="List all available source/destination languages",
                        action='store_true')
    parser.add_argument('-t', '--generate_txt', help='create a more human readable txt file in addition to the srt',
                        action='store_true')
    args = parser.parse_args()

    if args.list_formats:
        print("List of formats:")
        for subtitle_format in FORMATTERS:
            print("{format}".format(format=subtitle_format))
        return 0

    if args.list_languages:
        print("List of all languages:")
        for code, language in sorted(LANGUAGE_CODES.items()):
            print("{code}\t{language}".format(code=code, language=language))
        return 0

    if not validate(args):
        return 1

    if os.name != "nt" and "Darwin" in os.uname():
        # the default unix fork method does not work on Mac OS
        # need to use forkserver
        start_method = multiprocessing.get_start_method(allow_none=True)
        if 'forkserver' != start_method:
            # multiprocessing.set_start_method('forkserver')
            multiprocessing.set_start_method('spawn')

    file_queue = set()

    input_is_dir = os.path.isdir(args.source_path)
    if input_is_dir:
        print("input is directory, scanning files for candidates")
        cValidator = CandidateValidator()
        for root, dirs, files in os.walk(top=args.source_path):
            for file in files:
                current_file = os.path.join(root, file)
                if cValidator(current_file):
                    file_queue.add(current_file)
    else:
        file_queue.add(args.source_path)

    # # TESTING, REMOVE THIS:
    # import random
    # file_queue = [random.choice(list(file_queue))]

    try:
        # print(file_queue)
        for item in file_queue:
            try:
                pass
                # print(item)
                subtitle_file_path = generate_subtitles(
                    source_path=item,
                    concurrency=args.concurrency,
                    src_language=args.src_language,
                    dst_language=args.dst_language,
                    api_key=args.api_key,
                    subtitle_file_format=args.format,
                    output=args.output,
                    generate_txt=args.generate_txt
                )
                print("Subtitles file created at {}".format(subtitle_file_path))
            except KeyboardInterrupt:
                raise

            except Exception as ex:
                print(f'exception! \n {ex}')
                raise
    except KeyboardInterrupt:
        return 1
    except Exception as ex:
        print(ex)
        return 1
    return 0


class CandidateValidator(object):
    valid_filetypes: List[Pattern[str]]

    def __init__(self):
        import re
        self.valid_filetypes = [
            re.compile(r'.+\.mp4$'),
            re.compile(r'.+\.mkv$')
        ]

    def __call__(self, input_file) -> Optional[bool]:
        try:
            for pattern in self.valid_filetypes:
                if pattern.match(input_file):
                    # check if subtitle file already exists

                    if os.path.exists(self._change_ext(input_file, '.srt')):
                        print(f'skipping {self._change_ext(input_file, ".srt")} exists, skipping')
                        return False
                    elif os.path.exists(self._change_ext(input_file, '.transcript')):
                        print(f'skipping {self._change_ext(input_file, ".transcript")} exists, skipping')
                        return False
                    elif os.path.exists(self._change_ext(input_file, '.txt')):
                        print(f'skipping {self._change_ext(input_file, ".txt")} exists, skipping')
                        return False
                    else:
                        return True
                else:
                    continue
            # if no match by end of list, then return false
            return False
            # start, end = region
            # start = max(0, start - self.include_before)
            # end += self.include_after
            # # delete=False necessary for running on Windows
            # temp = tempfile.NamedTemporaryFile(suffix='.flac', delete=False)
            # program_ffprobe = which("ffprobe")
            # command = [str(program_ffprobe), "-ss", str(start), "-t", str(end - start),
            #            "-y", "-i", self.source_path,
            #            "-loglevel", "error", temp.name]
            # use_shell = True if os.name == "nt" else False
            # subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)
            # read_data = temp.read()
            # temp.close()
            # os.unlink(temp.name)
            # return read_data
        except KeyboardInterrupt:
            return

    def _change_ext(self, file: str, new_ext: str):
        ext_parts = os.path.splitext(file)
        ext = ext_parts[len(ext_parts) - 1]  # get the last element of list (extension)
        # base_parts = ext_parts[0:len(ext_parts) - 1 ]
        basepath = ext_parts[0]
        return str(basepath + new_ext)


if __name__ == '__main__':
    # main()
    sys.exit(main())
# if __name__ == '__main__':
# sys.exit(main())
