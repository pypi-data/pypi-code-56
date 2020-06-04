import time
import hashlib
import random
import struct

from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from .fit import fitting
from .conf import Glyph, NameStrings



class Generate:
    def __init__(self, path: str, glyphNames: list = None):
        self.glyph = Glyph(glyphNames)

        self.__origin_font = TTFont(path)
        self.__hhea = {
            'ascent': self.__origin_font['hhea'].ascent,
            'descent': self.__origin_font['hhea'].descent
        }

        self.__glyphCoordinates_map = self._wash()

        self.map = {}
        self.__judge = True
        self._record_path = ""

    def _wash(self) -> dict:
        # origin_cmap = self.__origin_font.getBestCmap()
        # reserve_origin_cmap = dict(zip(origin_cmap.values(), origin_cmap.keys()))

        GlyphCoordinates_map = {}
        for i in self.glyph.glyph_names[1:]:
            print(i, self.__origin_font['glyf'][i].coordinates)
            GlyphCoordinates_map[i] = self.__origin_font['glyf'][i].coordinates

        return GlyphCoordinates_map




    def _genCodes(self) -> list:
         return random.sample(range(0xE000, 0xF8FF), len(self.glyph.rand_names))

    def build(self, savePath: str = None, *args, **kwargs) -> tuple:
        if self.__judge == True:
            self.__judge = False
            self._record_path = savePath

        glyphs, metrics, cmap, record = {}, {}, {}, {}
        codes = self._genCodes()
        nameStrings = NameStrings(*args, **kwargs)

        glyph_set = self.__origin_font.getGlyphSet()
        pen = TTGlyphPen(glyph_set)
        
        for i, (gn, rn) in enumerate(zip(self.glyph.glyph_names, self.glyph.rand_names)):
            glyph_set[gn].draw(pen)
 
            # list(self.__glyphCoordinates_map[gn])
            if i != 0:
                pen.points = fitting(list(self.__glyphCoordinates_map[gn]))
                print(pen.points)

            # pen._addPoint((100, 200), 0)
            glyphs[rn] = pen.glyph()
            metrics[rn] = self.__origin_font['hmtx'][gn]

            if i == 0:
                continue

            cmap[codes[i]] = rn
            # cmap[codes[3 * i + 1]] = rn
            # cmap[codes[3 * i + 2]] = rn
            # print(hex(codes[3 * i]), rn, gn)
            record[gn] = hex(codes[i])
        
        fb = FontBuilder(self.__origin_font['head'].unitsPerEm, isTTF=True)

        fb.setupGlyphOrder(self.glyph.rand_names)
        fb.setupCharacterMap(cmap)
        fb.setupGlyf(glyphs)
        fb.setupHorizontalMetrics(metrics)
        fb.setupHorizontalHeader(**self.__hhea)
        fb.setupNameTable(nameStrings)
        fb.setupOS2()
        fb.setupPost()


        hash_time = hashlib.md5(str(time.time() * 1000).encode()).hexdigest()[8:24]
        returnPath = savePath if savePath != None else f"{hash_time}.ttf"

        fb.save(returnPath)
        self.map[returnPath] = record

        return returnPath, record

    def record(self):
        index = self._record_path.find('/')
        if index == -1:
            path = "./"
        elif index == (1 or 2):
            end_index = len(self._record_path) - len(self._record_path.split('/')[-1])
            path = self._record_path[0:end_index]
        else:
            raise 'path error!'

        import json
        with open(f'{path}map.json', 'w') as f:
            f.write(json.dumps(self.map))




class Generates(Generate):
    def __init__(self, path: str, glyphNames: list = None):
        super().__init__(path, glyphNames=glyphNames)

        self.maps = {}


    def _call(self, savePath: str):
        return super().build(savePath=savePath)

    def build(self, savePaths: list = None) -> dict:
        import multiprocessing

        try:
            from concurrent.futures import ProcessPoolExecutor
        except ImportError:
            from concurrent.futures.process import ProcessPoolExecutor


        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = executor.map(self._call, savePaths)
            for f in futures:
                self.maps[f[0]] = f[1]

            return self.maps
    
    def record(self):
        index = self._record_path.find('/')
        if index == -1:
            path = "./"
        elif index == (1 or 2):
            end_index = len(self._record_path) - len(self._record_path.split('/')[-1])
            path = self._record_path[0:end_index]
        else:
            raise 'path error!'

        import json
        with open(f'{path}map.json', 'w') as f:
            f.write(json.dumps(self.maps))