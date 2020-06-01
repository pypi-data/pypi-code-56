# Copyright (C) 2019 Intek Institute.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Intek Institute or one of its subsidiaries.  You shall not disclose
# this confidential information and shall use it only in accordance
# with the terms of the license agreement or other applicable
# agreement you entered into with Intek Institute.
#
# INTEK INSTITUTE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  INTEK
# INSTITUTE SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY
# LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS
# SOFTWARE OR ITS DERIVATIVES.

import collections
import pathlib
import random
import sys

from PIL import Image
from PIL import ImageDraw
import numpy


class Sprite:
    """
    Represent the identification and the position of a sprite packed in a
    picture with other sprites.

    A sprite is identified with a unique label (a strictly positive
    integer).

    The location of a sprite is defined with a bounding box (top-left and
    bottom-right) of the contour of the sprite.
    """
    def __init__(self, sprite_sheet, label, x1, y1, x2, y2):
        """
        Build a new `Sprite` object.

        The coordinates of the top-left and bottom-right corners of the sprite
        are related to the top-left corner of the picture this sprite is
        packed in.


        :param sprite_sheet: A `SpriteSheet` object this sprite belongs to.

        :param label: Label of this sprite. This label MUST be unique among
            all the sprites packed in a picture.

        :param x1: Abscissa of the top-left corner.

        :param y1: Ordinate of the top-left corner of the bounding box of this
            sprite.

        :param x2: Abscissa of the bottom-right corner of the bounding box of
            this sprite.

        :param y2: Ordinate of the bottom-left corner of the bounding box of
            this sprite.


        :raise ValueError: If the specified coordinates of the sprite's
            bounding box are invalid.  These coordinates MUST all be positive
            integer values; the coordinates of the top-left corner MUST be on
            the top or the left of the coordinates of the bottom-right corner.

        :raise TypeError: If the specified arguments are not of the expected
            type.
        """
        if not isinstance(label, int):
            raise TypeError("Invalid label type")

        if label < 0:
            raise ValueError("Invalid label")

        if any([not isinstance(arg, int) for arg in (x1, y1, x2, y2)]):
            raise TypeError("Invalid coordinates type")

        if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > x2 or y1 > y2:
            raise ValueError('Invalid coordinates')

        self.__sprite_sheet = sprite_sheet

        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        self.__height = None
        self.__width = None
        self.__surface_area = None
        self.__density = None

    @property
    def bottom_right(self):
        return self.__x2, self.__y2

    @property
    def height(self):
        if self.__height is None:
            self.__height = self.__y2 - self.__y1 + 1

        return self.__height

    @property
    def label(self):
        return self.__label

    @property
    def surface_area(self):
        """
        Return the surface area of the sprite's bounding box.


        :return: Area that the sprite's rectangle bounding box occupies.
        """
        if self.__surface_area is None:
            self.__surface_area = self.width * self.height

        return self.__surface_area

    @property
    def top_left(self):
        return self.__x1, self.__y1

    @property
    def width(self):
        if self.__width is None:
            self.__width = self.__x2 - self.__x1 + 1

        return self.__width

    @property
    def density(self):
        if self.__density is None:
            pixels = sum([
                self.__sprite_sheet.label_map[y][x] == self.__label
                for y in range(self.__y1, self.__y2 + 1)
                for x in range(self.__x1, self.__x2 + 1)])

            self.__density = pixels / self.surface_area

        return self.__density


class SpriteSheet:
    """
    Represent a sprite sheet that consists of multiple sprites in one
    image.

    Sprite sheets pack multiple sprites into a single picture.  Using
    sprite sheet, video game developers create sprite sheet animation
    representing one or several animation sequences while only loading a
    single file.
    """
    # List of the supported image modes.
    SUPPORTED_IMAGE_MODES = ('1', 'L', 'RGB', 'RGBA')

    # Relative coordinates of the neighbor pixels.
    #
    # +----------+----------+----------+
    # | (-1, -1) | (0, -1)  | (1, -1)  |
    # +----------+----------+----------+
    # | (-1, 0)  |    X     |
    # +----------+----------+
    NEIGHBOR_PIXEL_RELATIVE_COORDINATES = ((-1, -1), (0, -1), (1, -1), (-1, 0))

    def __init__(self, fd, background_color=None, name=None):
        """
        Build a new `SpriteSheet` object.


        :param fd: An image file, either:

            * the name and path (a string) that references an image file in the
              local file system;

            * a `pathlib.Path` object that references an image file in the local
              file system ;

            * a file object that MUST implement `read()`, `seek()`, and `tell()`
              methods, and be opened in binary mode;

            * a `PIL.Image` object.

        :param background_color: The background color (i.e., transparent color)
            of the image.  The type of `background_color` argument depends on
            the images' mode:

            * an integer if the mode is grayscale;

            * a tuple `(red, green, blue)` of integers if the mode is `RGB`;

            * a tuple `(red, green, blue, alpha)` of integers if the mode is
             `RGBA`. The `alpha` element is optional. If not defined, while the
             image mode is `RGBA`, the constructor considers the `alpha`
             element to be `255`.

        :param name: A human-readable name given to this sprite sheet.
        """
        self.__image = Image.open(fd) if isinstance(fd, (str, pathlib.Path)) else fd

        if self.__image.mode not in SpriteSheet.SUPPORTED_IMAGE_MODES:
            raise ValueError(f"'The image mode '{self.__image.mode}' is not supported")

        self.__is_pixel_value_8bits = self.__image.mode in ('1', 'L')

        self.__background_color = background_color  # Lazy loading by the read-only property `background_color`.
        self.__name = name

        # Table of label equivalence (a dictionary) to keep note of which labels
        # refer to the same sprite when two parts of a sprite eventually connect.
        # If a pixel has multiple neighbors with different labels, the algorithm
        # assigns for that pixel the first label found and indicate that all
        # the other ones are equivalent. The filled table contains every label
        # (the key) in the image and the labels (the associated value) from
        # their surrounding neighbors too.
        self.__linked_labels = {}

        self.__sprites = None
        self.__label_map = None

    def __link_labels(self, label1, label2):
        """
        Link the two specified labels that identify connected parts of a same
        sprite.


        :param label1: A first label.

        :param label2: An second label equivalent to the first label passed to
            this function.
        """
        unified_labels = self.__linked_labels[label1]
        unified_labels.update(self.__linked_labels[label2])

        for label in unified_labels:
            self.__linked_labels[label] = unified_labels

    def __merge_linked_labels(self):
        """
        Merge the equivalence labels together and unify all the connected
        fragments of a sprite to one sprite.


        :return: A tuple `(sprites, labels)` where:

            * `sprites`: A collection of key-value pairs (a dictionary) where each
              key-value pair maps the key (the label of a sprite) to its associated
              value (a `Sprite` object).  Each connected fragment of a sprite has
              been unified to one sprite.

            * `label_map`: A 2D array of integers of equal dimension (width and
              height) as the original image where the sprites are packed in.  This
              array maps each pixel of the original image to the label of the sprite
              this pixel corresponds to, or `0` if this pixel doesn't belong to a
              sprite (e.g., transparent color).
        """
        # Reduce each group of equivalence labels (each referencing connected
        # parts of a sprite) to one label only, the first in the list.
        primary_labels = {}
        for label, equivalence_labels in self.__linked_labels.items():
            # Retrieve the fist element of the Python set.
            primary_labels[label] = next(iter(equivalence_labels))

        # Create a new a 2D array of integers that maps each pixel of the to
        # the unified label of the sprite this pixel corresponds to, or `0` if
        # this pixel doesn't belong to a sprite (e.g., transparent color).
        unified_label_map = [
            [label and primary_labels[label] for label in row]
            for row in self.__label_map]

        # Determine the list of pixels mapped to each unique label.
        label_pixels_coordinates = collections.defaultdict(list)
        for y, row in enumerate(unified_label_map):
            for x, label in enumerate(row):
                if label:
                    label_pixels_coordinates[label].append((x, y))

        # Build the list of sprites (which connected parts have been reunified)
        # and calculate their respective bounding box.
        sprites = {}

        for label in label_pixels_coordinates:
            x1 = y1 = sys.maxsize
            x2 = y2 = 0

            for x, y in label_pixels_coordinates[label]:
                if x < x1: x1 = x
                if x > x2: x2 = x
                if y < y1: y1 = y
                if y > y2: y2 = y

            sprites[label] = Sprite(self, label, x1, y1, x2, y2)

        return sprites, unified_label_map

    @property
    def background_color(self):
        """
        Return the background color of the sprite sheet's image.


        :return: The background color (i.e., transparent color)
            of the image.  The type of `background_color` argument depends on
            the images' mode:

            * an integer if the mode is grayscale;

            * a tuple `(red, green, blue)` of integers if the mode is `RGB`;

            * a tuple `(red, green, blue, alpha)` of integers if the mode is
             `RGBA`. The `alpha` element is optional. If not defined, while the
             image mode is `RGBA`, the constructor considers the `alpha`
             element to be `255`.
        """
        if self.__background_color is None:
            self.__background_color = self.find_most_common_color(self.__image)

        return self.__background_color

    def create_sprite_labels_image(self, background_color=None, bounding_box_color=None, labels=None, seed=None):
        """
        Create a new image, drawing the masks of the sprites at the exact same
        position that the sprites were in the original image.

        The function draws each sprite mask with a random uniform color (one
        color per sprite mask). The function also draws a rectangle (bounding
        box) around each sprite mask, of the same color used for drawing the
        sprite mask.


        :param background_color: Either a tuple `(R, G, B)` or a tuple
            `(R, G, B, A)`) that identifies the color to use as the background
            of the image to create. If this argument is not passed to the
            function, the default value `(255, 255, 255)`.

        :param bounding_box_color:  Either a tuple `(R, G, B)` or a tuple
            `(R, G, B, A)`) that identifies the color to use as the bounding
            boxes If omitted, the function uses the color of the corresponding
            sprite mask.

        :param labels: The restricted list of sprite labels to draw bounding
            boxes.  If not defined, the function draws the bounding boxes of
            all the sprite labels.

        :param seed: Seed value to initialize the pseudo-random generator with.
            If omitted, the function initializes the generator with the
            current system time.  Specifying an initial seed value allows to
            draw sprite masks with the same random colors.


        :return: An `Image` object.


        :raise ValueError: if the specified background color is not a tuple
            `(R, G, B)`, neither a tuple `(R, G, B, A)`.
        """
        if self.__sprites is None:
            self.find_sprites()

        if background_color and (not isinstance(background_color, tuple) or not 3 <= len(background_color) <= 4):
            raise ValueError('Invalid background color')

        if background_color is None:
            background_color = (255, 255, 255)

        # Randomly generate RGB colors for each sprite label using the specified
        # color (or White, if not defined) for the background.
        sprite_label_colors = {0: background_color}

        random.seed(seed)

        for label in self.__sprites:
            sprite_label_colors[label] = tuple([random.randint(64, 200) for c in range(len(background_color))])

        # Build the image with the sprite label's color.
        pixels = numpy.asarray([
            [sprite_label_colors[label] for label in row]
            for row in self.__label_map],
            dtype=numpy.uint8)

        image = Image.fromarray(pixels, 'RGB' if len(background_color) == 3 else 'RGBA')

        # Draw the bounding boxes surrounding the sprites restricted to the
        # specified list of labels.
        draw = ImageDraw.Draw(image)

        for label in labels or self.__sprites:
            sprite = self.__sprites[label]
            color = bounding_box_color or sprite_label_colors[label]
            draw.rectangle((sprite.top_left, sprite.bottom_right), outline=color, width=1)

        return image

    @staticmethod
    def find_most_common_color(image):
        """
        Return the color that is the most common in the given image.


        :param image: A `PIL.Image` object.


        :return: An integer or a tuple of integers (one for each band red, green,
            blue, and possibly alpha) representing the color that is the most
            common in the given image.
        """
        if image.mode not in SpriteSheet.SUPPORTED_IMAGE_MODES:
            raise ValueError(f"'The image mode '{image.mode}' is not supported")

        # Retrieve the list of colors used in this image.
        #
        # The default maximum number limit of colors is 256 colors.  We
        # explicitly to the maximum possible colors in the image, which is
        # the total number of pixels in this image.
        colors_count = image.getcolors(image.width * image.height)

        # Sort pixel value usages by decreasing order to retrieve the most common
        # pixel value.
        most_common_color_count, most_common_color = max(colors_count, key=lambda color_count: color_count[0])

        # @note: Previous implementation of this function, in case the method
        #     `getcolors` would restrict the number of colors to a hard limit.
        #
        # if image.mode == 'L':
        #     # Retrieve the list of colors used in this image.
        #     #
        #     # @note: Because this method is limited to a maximum number of colors
        #     #     (256), this method can only be used for non-RGB image (grayscale).
        #     colors_count = image.getcolors()
        #
        #     # Sort pixel value usages by decreasing order to retrieve the most common
        #     # pixel value.
        #     sorted_colors_count = sorted(colors_count, key=lambda color_count: color_count[0], reverse=True)
        #     most_common_color_count, most_common_color = sorted_colors_count[0]
        #
        # else:
        #     # Count the number of times each unique pixel value is used in the
        #     # image.
        #     #
        #     # The numpy array of a PIL image, composed of multiple bands, is a 3D
        #     # array: an array of rows of this image, a sub-array of columns for this
        #     # row, and a sub-array of the band values of the pixel for this column
        #     # and this row.
        #     #
        #     # We need to flatten this array to a 2D array: an array of band values
        #     # of each pixel of this image.
        #     #
        #     # @note: We could have used the following similar code, but it's 30%
        #     #    slower (more likely the time to reshape the initial array).
        #     #
        #     #    ```python
        #     #    flatten_colors = numpy.asarray(image) \
        #     #        .flatten() \
        #     #        .reshape((image.width * image.height, len(image.getbands())))
        #     #    pixel_counter = collections.Counter(zip(*flatten_colors))
        #     #    ```
        #
        #     # Split this image into individual bands; for example, splitting an "RGB"
        #     # image creates three new images each containing a copy of one of the
        #     # original bands (red, green, blue). Then build a list of numpy arrays of
        #     # these image bands with flatten values.
        #     color_channels = [
        #         numpy.asarray(image_band).flatten()
        #         for image_band in image.split()]
        #
        #     # Recompose pixel colors with its respective components taken from each
        #     # image band.
        #     flatten_colors = zip(*color_channels)
        #
        #     # Count the number of times each unique color is used in the image and
        #     # retrieve the most common color.
        #     pixel_counter = collections.Counter(flatten_colors)
        #
        #     most_common_color_counts = pixel_counter.most_common(1)
        #     most_common_color, most_common_color_count = most_common_color_counts[0]

        return most_common_color

    def find_sprites(self):
        """
        Return a collection of sprites that are packed in the sprite sheet's
        image, and an array that maps each pixel of the original image to the
        label of the sprite this pixel corresponds to.


        :return: A tuple `(sprites, label_map)` where:

            * `sprites`: A collection of key-value pairs (a dictionary) where each
              key-value pair maps the key (the label of a sprite) to its associated
              value (a `Sprite` object).  Each connected fragment of a sprite has
              been unified to one sprite.

            * `label_map`: A 2D array of integers of equal dimension (width and
              height) as the original image where the sprites are packed in.  This
              array maps each pixel of the original image to the label of the sprite
              this pixel corresponds to, or `0` if this pixel doesn't belong to a
              sprite (e.g., transparent color).
        """
        if self.__sprites is None:
            # Lazy load the background color if not already specified.
            background_color = self.background_color

            # Convert the image into an array for faster access.
            pixels = numpy.asarray(self.__image)

            # Create a 2D array of integers of equal dimension (width and height) as
            # the image passed to the function. This array maps each pixel of the to
            # the label of the sprite this pixel corresponds to, or `0` if this
            # pixel doesn't belong to a sprite (e.g., transparent color).
            image_width, image_height = self.__image.size
            self.__label_map = numpy.asarray([[0] * image_width] * image_height)

            # Generator of label identifiers to map with pixels that are part of a
            # sprite (e.g., pixel that are not considered as transparent, that do
            # not belong to the background color).
            current_label = 0

            for y in range(image_height):
                for x in range(image_width):
                    # Ignore transparent pixel (i.e., pixel which value corresponds to the
                    # background color).
                    #
                    # @note: The code of this test is a lot faster than using the function
                    #     `numpy.array_equal`:
                    #
                    #     ```python
                    #     >>> timeit.timeit(stmt='tuple(pixels) == transparent_color', setup='import numpy; pixels = numpy.asarray([0, 0, 0]); transparent_color = (255,255,255)', number=1000000)
                    #     1.4233526739990339
                    #     >>> timeit.timeit(stmt='numpy.array_equal(pixels, transparent_color)', setup='import numpy; pixels = numpy.asarray([0, 0, 0]); transparent_color = [255,255,255]', number=1000000)
                    #     7.9941349439977785
                    if pixels[y][x] != background_color if self.__is_pixel_value_8bits else tuple(pixels[y][x]) != background_color:
                        # Label associated to this pixel. Initially no label.
                        pixel_label = 0

                        for dx, dy in self.NEIGHBOR_PIXEL_RELATIVE_COORDINATES:
                            neighbor_pixel_x, neighbor_pixel_y = x + dx, y + dy

                            # Check whether a neighbor pixel belongs to a sprite.
                            if 0 <= neighbor_pixel_x < image_width and neighbor_pixel_y >= 0 and self.__label_map[neighbor_pixel_y][neighbor_pixel_x] > 0:
                                # If the current pixel has been already associated to a label, check
                                # whether the neighbor pixel has the same label, and if not, link these
                                # labels and their equivalent labels all together.
                                if pixel_label and pixel_label != self.__label_map[neighbor_pixel_y][neighbor_pixel_x] and \
                                   self.__label_map[neighbor_pixel_y][neighbor_pixel_x] not in self.__linked_labels[pixel_label]:
                                    self.__link_labels(pixel_label, self.__label_map[neighbor_pixel_y][neighbor_pixel_x])

                                pixel_label = self.__label_map[neighbor_pixel_y][neighbor_pixel_x]

                        # If the pixel is not connected to a neighbor pixel, generate a new
                        # label.  Map the pixel to the associated label.
                        if pixel_label:
                            self.__label_map[y][x] = pixel_label
                        else:
                            current_label += 1
                            self.__linked_labels[current_label] = set([current_label])
                            self.__label_map[y][x] = current_label

            self.__sprites, self.__label_map = self.__merge_linked_labels()

        return self.__sprites.values(), self.__label_map

    @property
    def image(self):
        """
        Return the image this sprite sheet has been built from.

        The caller MUST NOT write in this image.


        :return: A `PIL.Image` object.
        """
        return self.__image

    @property
    def label_map(self):
        return self.__label_map

    @property
    def name(self):
        return self.__name
