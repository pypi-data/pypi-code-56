'''
Created on 2019年3月26日

@author: bkd

压缩脚本
'''
from shutil import make_archive as ma
from os.path import join, dirname, isfile, normpath
from os import chdir, walk
import zipfile
import logging

logger = logging.getLogger(__name__)


class createZipFile:
    def execute(self, app, sp):
        path = sp["path"]
        cur_file = sp["fileList"][0]
        curItem = join(path, cur_file)
        logger.info("压缩:" + curItem)

        filelist = []
        if isfile(curItem):
            filelist.append(curItem)
        else:
            filelist.append(curItem)
            for root, dirs, files in walk(curItem):
                for d in dirs:
                    filelist.append(normpath(join(root, d)))
                for name in files:
                    filelist.append(normpath(join(root, name)))

        zf = zipfile.ZipFile(curItem + ".zip", "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(path):]
            # logger.info arcname
            zf.write(tar, arcname)
        zf.close()
