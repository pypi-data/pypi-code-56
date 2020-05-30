#!/usr/bin/env python3


from glob import glob
from binascii import unhexlify, hexlify
import numpy as np
import os
import mmap
import struct
import logging


class ParsingException(Exception):
    pass


logger = logging.getLogger('parseLogger')


def get_data_format(mfile):
    finnig_header = b'\x01\xA1'+"Finnigan".encode("UTF-16")[2:]
    mfile.seek(0)
    if mfile.read(len(finnig_header)) == finnig_header:
        logger.info("Detected Finnigan .raw file header...")
        mfile.seek(mfile.tell()+16)
        if mfile.read(2) == b'\x08\x00':
            file_format = struct.unpack("<h", mfile.read(2))[0]
            logger.debug("Data format version is {}".format(file_format))
            return file_format
        else:
            raise ParsingException(
                "[ERROR] File is unsupported, please submit your spectrum"
                "to the developer of this library")

    else:
        raise ParsingException(
                "[ERROR] File was not recognized"
                "as Finnigan .raw file!!")


def load_tmp_file(tmp_folder):
    def read_tmp_file(tmp_file):
        inp = open(tmp_file, mode="rb")
        data = inp.read()
        inp.close()
        return data
    tmp_files = sorted(glob(tmp_folder+"/*"),
                       key=lambda tmpf: os.stat(tmpf).st_mtime,
                       reverse=True)
    for file in tmp_files:
        if read_tmp_file(file).find(unhexlify("ffffffff0100")) == 8:
            logger.info("Found temp file"+file)
            temp_data = open(file, "rb")
            return temp_data
    raise ParsingException("[ERROR] Valid .tmp file was not found")


def get_chromatogram(mfile, look_from, data_form, tmp_folder, no_of_scans):
    pos = find_chrom_primer(mfile, look_from, data_form)
    temp_found = False
    if pos == int(-1):
        logger.warning("Did not find scan times in the original file\n"
                       "Looks like the scanning is in progress,"
                       "searching for the temp file")
        mfile = load_tmp_file(tmp_folder)
        mfile.seek(8)
        temp_found = True
    else:
        mfile.seek(pos+4)
    times = []
    intensities = []
    if data_form in {47, 63}:
        h_len = 72
        fmt = "<4s3idd"
        delim = "ffffffff"
        tpos = -2
        ipos = -1
    elif data_form == 57:
        h_len = 72
        fmt = "<4si8s6d4si"
        delim = "00000000"
        tpos = 3
        ipos = 4
    elif data_form == 66:
        h_len = 88
        fmt = "<4s3idd"
        delim = "ffffffff"
        tpos = -2
        ipos = -1
    else:
        raise ParsingException("[ERROR] unknown Machine Type {}, exiting NOW!"
                               .format(data_form))

    logger.info("Extracting scan times")

    fmt_size = struct.calcsize(fmt)
    next_measure = 1
    while 1:
        header = mfile.read(h_len)
        val = struct.unpack(fmt, header[:fmt_size])
        if data_form == 57 and val[0][2:] == struct.pack(
                "<h", 1+struct.unpack("<xxh", unhexlify(delim))[0]):
            delim = hexlify(struct.pack("<xxh", 1+struct.unpack(
                            "<xxh", unhexlify(delim))[0]))
        if (val[0] == unhexlify(delim) and val[1] == next_measure):
            times.append(val[tpos])
            intensities.append(val[ipos])
            logger.debug("time of the scan #{} is {:.6} seconds"
                         .format(val[1], val[tpos]*60))
            next_measure += 1
        else:
            break
    if temp_found:
        logger.info("Cutting out chromatogram")
        times = times[:no_of_scans]
        intensities = intensities[:no_of_scans]
    if len(times) != no_of_scans:
        logger.critical("Number of times: {}, number of scans {}".format(
                        len(times), no_of_scans))
        raise ParsingException(
            "[ERROR] Number of times does not fit to number of scans")
    return np.array([times, intensities], dtype=np.float32)


def find_chrom_primer(mfile, look_from, data_form):
    mfile.seek(look_from)
    if data_form in {47, 63, 66}:
        time_header = unhexlify("00000000ffffffff01000000")
        pos = mfile.find(time_header)
    elif data_form == 57:
        time_header = unhexlify("0000000000000000010000000E00000002000000")
        pos = mfile.find(time_header)
    else:
        raise ParsingException("[ERROR] unknown data_form {}, exiting NOW!"
                               .format(data_form))
    return pos


def ext_scan_heads(mfile, data_form):
    positions = []
    primer_pos = find_scan_primer(mfile, data_form)
    mfile.seek(primer_pos)
    positionsarr, first_marr, last_marr, steparr, matrixlenarr =\
        [], [], [], [], []
    if data_form in {47, 57, 63}:
        fmt = "<IffdI"
        first_run = True
        next_measure = 1
        file_len = len(mfile)
        while True:
            next_pos = mfile.find(unhexlify("ffffffffffffffff"))-24
            if next_pos == (-1-24):
                logger.info("EOF! All scan heads have been acquired...")
                break
            mfile.seek(next_pos)
            header = mfile.read(struct.calcsize(fmt))
            rel_start_pos, first_m, last_m, step, arr_len \
                = struct.unpack(fmt, header)

            logger.info("Mapping header of the scan #{}"
                        .format(next_measure))
            next_measure += 1
            arr_len = arr_len-4
            params = (first_m, last_m, step, arr_len)
            if first_run:
                first_run = False
                old_params = params
            if params != old_params:
                logger.debug("parameters change detected,"
                             "adding acquisition parameters array")
                for parameter, pararray in (
                        (positions, positionsarr), (old_params[0], first_marr),
                        (old_params[1], last_marr), (old_params[2], steparr),
                        (old_params[3], matrixlenarr)):
                    pararray.append(parameter)
                old_params = params
                positions = []
            positions.append((primer_pos+rel_start_pos, arr_len))
            first_run = False
            old_params = params

            if (mfile.tell() + 20) < file_len:
                mfile.seek(20, 1)
            else:
                logger.warning("EOF! all scan heads acquired")
                logger.warning("Looks like measuring is in progress"
                               "or file is corrupted.")
                last_p = mfile.tell()
                break
            last_p = mfile.tell()

    elif data_form == 66:
        fmt = "<4xI24xffdd4xi4xi"
        fmt_size = struct.calcsize(fmt)
        first_run = True
        logger.info("Mapping headers")
        next_measure = 1
        while True:
            header = mfile.read(fmt_size)
            logger.info("Mapping header of the scan #{}"
                        .format(next_measure))
            next_measure += 1
            if len(header) != fmt_size:
                logger.warning("EOF! All scan heads acquired")
                logger.warning("Looks like measuring is in progress"
                               "or file is corrupted.")
                last_p = mfile.tell()
                break

            if struct.unpack(fmt, header)[1] == 0:
                last_p = mfile.tell()
                logger.info("EOF! All scan heads mapped, last mapping skipped")
                break

            tot_len, first_m, last_m, first_m_d, step, arr32_len, arr_len2 \
                = struct.unpack(fmt, header)
            arr_len = arr32_len*4
            params = (first_m, last_m, step, arr_len)
            start_pos = mfile.tell()
            if first_run:
                first_run = False
                old_params = params
            if params != old_params:
                logger.warning("parameters change detected,"
                               "adding acquisition parameters array")
                for parameter, pararray in (
                        (positions, positionsarr), (old_params[0], first_marr),
                        (old_params[1], last_marr), (old_params[2], steparr),
                        (old_params[3], matrixlenarr)):
                    pararray.append(parameter)
                old_params = params
                positions = []
            positions.append((start_pos, arr_len))
            mfile.seek(start_pos+arr_len)
    else:
        raise ParsingException("[ERROR] unknown data_form {},"
                               "exiting NOW!".format(data_form))

    logger.debug("Writing the last set of acquisition parameters")
    for parameter, pararray in (
            (positions, positionsarr), (first_m, first_marr),
            (last_m, last_marr), (step, steparr),
            (arr_len, matrixlenarr)):
        pararray.append(parameter)
    return positionsarr, first_marr, last_marr, steparr, matrixlenarr,\
        data_form, last_p


def find_scan_primer(mfile, data_form):
    if data_form == 57:
        #  position of primer is present just after the date and time
        while 1:
            pos = mfile.find(unhexlify("01000000"))
            if pos == int(-1):
                raise ParsingException(
                    "[ERROR] expected date and time not found in the file,"
                    " unknown .raw file format")
            mfile.seek(pos+4)
            fmt = "<8h"
            year, month, dow, dom, h, m, s, ms = struct.unpack(
                    fmt, mfile.read(struct.calcsize(fmt)))
            if year > 1980 and 0 < month <= 12 and 0 < dow <= 7 and\
                    0 < dom <= 31 and 0 <= h < 24 and 0 <= m < 60 and\
                    0 <= s < 60 and 0 <= ms < 1000:
                break
        mfile.seek(pos+24)
        primer_pos = struct.unpack("<i", mfile.read(4))[0] + 4
    elif data_form in {47, 63}:
        #  going to the first delimiter
        pos = mfile.find(unhexlify("ffffffffffffffff"))+32
        if pos == int(-1):
            raise ParsingException(
                "[ERROR] expected delimiter is not present in file,"
                " unknown .raw file format")

        mfile.seek(pos)
        logger.info("Safety check: The year of acquisition was {} ?"
                    .format(str(np.frombuffer(mfile.read(2), dtype=np.int16))))
        fmt = "<IffdI"
        #  skipping date&time
        mfile.seek(pos+20)
        primer_pos = struct.unpack("<i", mfile.read(4))[0] + 4
    elif data_form == 66:
        #  going to the first delimiter
        pos = mfile.find(unhexlify("ffffffffffffffff"))+32
        if pos == int(-1):
            raise ParsingException(
                "[ERROR] expected delimiter is not present in file,"
                " unknown .raw file format")
        mfile.seek(pos)
        logger.info("Safety check: The year of acquisition was {} ?"
                    .format(str(np.frombuffer(mfile.read(2), dtype=np.int16))))
        fmt = "<4xI24xffdd4xi4xi"
        mfile.seek(pos+804)
        primer_pos = struct.unpack("<i", mfile.read(4))[0]
    else:
        raise ParsingException(
                "[ERROR] unknown data_form {}, exiting NOW!".format(data_form))

    return primer_pos


def load_raw(raw_file,
             tmp_glob=r"C:/ProgramData/Thermo Scientific/Temp/*.tmp"):
    inf = open(raw_file, "rb")
    mf = mmap.mmap(inf.fileno(), 0, access=mmap.ACCESS_READ)
    data_format = get_data_format(mf)
    positionsarr, first_marr, last_marr, steparr, matrixlenarr, data_form,\
        last_p = ext_scan_heads(mf, data_format)
    segments = [len(segment) for segment in positionsarr]

    chromatogram = get_chromatogram(
            mf, last_p, data_form, tmp_glob, np.sum(segments))

    acqnum = 0
    spectra = []
    for i in range(len(segments)):
        acqnumstart = acqnum
        no_of_members = int(matrixlenarr[i])/4
        masses = first_marr[i]+np.arange(
                no_of_members, dtype=np.float32)*steparr[i]
        matrix = np.empty((len(positionsarr[i]), int(
            positionsarr[i][0][1]/4)), dtype=np.float32)
        for x, (pos, arr_len) in enumerate(positionsarr[i]):
            mf.seek(pos)
            logger.info("Extracting the spectrum of the scan #{}"
                        .format(acqnum+1))
            acqnum += 1
            if data_form in {47, 57, 63}:
                values = np.frombuffer(mf.read(matrixlenarr[i]),
                                       dtype=np.uint32)
                # old format is weird Int.
                # It need to be reformed before pasted into matrix.
                matrix[x] = values-0x80000000
            elif data_form == 66:
                values = np.frombuffer(mf.read(matrixlenarr[i]),
                                       dtype=np.float32)
                matrix[x] = values
            else:
                raise ParsingException("[ERROR] Data type not defined")
        chromsection = chromatogram.T[acqnumstart:acqnum].T
        spectra.append([chromsection, masses, matrix])
    inf.close()
    logger.info("Parsing done, hopefully in correct way")
    return spectra


#  working cajzls, delete when finishing
if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel("DEBUG")
    file_list = ["TSQ.raw", "LCQ.raw", "LTQ.raw", "MAX.raw"]
    for i in file_list:
        print(i)
        load_raw(i)
