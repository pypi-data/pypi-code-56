from .bam import D64BAM
from .block import Block
from .dos_image import DOSImage


class D64Image(DOSImage):

    DOS_VERSION = ord('2')
    DOS_FORMAT = ord('A')
    MAX_TRACK = 35
    DIR_TRACK = 18
    INTERLEAVE = 10
    DIR_INTERLEAVE = 3
    TRACK_SECTOR_MAX = ((21, (1, 17)), (19, (18, 24)), (18, (25, 30)), (17, (31, 35)))
    IMAGE_SIZES = (174848, 175531)

    def __init__(self, filename):
        self.bam = D64BAM(self)
        super().__init__(filename)

    def alloc_next_block(self, track, sector, directory=False):
        return self._alloc_next_block(track, sector, self.DIR_INTERLEAVE if directory else self.INTERLEAVE)

    @classmethod
    def create(cls, filepath, disk_name, disk_id):
        """Create an empty disk image."""
        super().create(filepath)

        image = cls(filepath)
        try:
            image.open('r+b')

            # block 18/0 contains the BAM and various identifying fields
            bam_block = Block(image, cls.DIR_TRACK, 0)
            bam_block.set(0x90, b'\xa0' * 0x1b)
            image.name = disk_name
            image.id = disk_id
            image.dos_type = ((cls.DOS_FORMAT, cls.DOS_FORMAT))
            image.dos_version = cls.DOS_VERSION

            # populate the BAM with all free blocks
            for sectors, range_ in cls.TRACK_SECTOR_MAX:
                for t in range(range_[0], range_[1]+1):
                    bits_free = '1' * sectors
                    image.bam.set_entry(t, sectors, bits_free)

            # block 18/1 contains 8 empty directory entries
            dir_block = Block(image, cls.DIR_TRACK, 1)
            dir_block.data_size = 0xfe

            # link BAM block to directory block
            bam_block.set_next_block(dir_block)

            # allocate both blocks
            image.bam.set_allocated(cls.DIR_TRACK, 0)
            image.bam.set_allocated(cls.DIR_TRACK, 1)
        finally:
            image.close()
