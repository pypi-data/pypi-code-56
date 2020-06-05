import os

AUDIO_DIR_STR = "audio"
WAV_SUFFIX_STR = ".wav"
OGG_SUFFIX_STR = ".ogg"
DEFAULT_AUDIO_PATH_STR = "415328__eardeer__slumberfoam.wav"

testing_bool = False


def get_base_dir() -> str:
    # PLEASE NOTE: This gives us the ct dir, not the project dir. The reason is that we are trying
    # to make this work with setup.py and PyPI

    # TODO: If we are running the application with "python3 -m ct" the base dir will be
    # something like /___/python3/dist-packages
    first_str = os.path.abspath(__file__)
    # -__file__ is the file that started the application, in other words mindfulness-at-the-computer.py
    #######second_str = os.path.dirname(first_str)
    base_dir_str = os.path.dirname(first_str)
    return base_dir_str


def get_audio_path(i_file_name: str = "") -> str:
    audio_files_path_str = os.path.join(get_base_dir(), AUDIO_DIR_STR)
    os.makedirs(audio_files_path_str, exist_ok=True)
    if i_file_name:
        audio_files_path_str = os.path.join(audio_files_path_str, i_file_name)
    return audio_files_path_str

