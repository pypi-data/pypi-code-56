"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version syncs the grid to the sprite list in one go using resync_grid_with_sprites.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites
"""
import arcade

# Set how many rows and columns we will have
ROW_COUNT = 15
COLUMN_COUNT = 15

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Example"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()

        # Create a list of solid-color sprites to represent each grid location
        for row in range(COLUMN_COUNT):
            for column in range(ROW_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

    def resync_grid_with_sprites(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # We need to convert our two dimensional grid to our
                # one-dimensional sprite list. For example a 10x10 grid might have
                # row 2, column 8 mapped to location 28. (Zero-basing throws things
                # off, but you get the idea.)
                # ALTERNATIVELY you could set self.grid_sprite_list[pos].texture
                # to different textures to change the image instead of the color.
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            # Flip the location between 1 and 0.
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            else:
                self.grid[row][column] = 0

        self.resync_grid_with_sprites()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
