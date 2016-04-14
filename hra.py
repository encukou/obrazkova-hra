import random

import pyglet
window = pyglet.window.Window()

COLUMNS = 8
ROWS = 8

SPACING = 20

IMG_PATH = 'assets/animal-pack/PNG/Square without details/{}.png'
ACTIVE_PATH = 'assets/animal-pack/PNG/Square (outline)/{}.png'
ANIMAL_INFO = (
    ('snake', 25),
    ('penguin', 0),
    ('elephant', 0),
    ('monkey', 0),
    ('giraffe', -45),
    ('panda', -25),
    ('pig', -15),
    ('hippo', -10),
    ('parrot', 0),
    ('rabbit', -65),
)

def image_load(animal_name, path, offset):
    img = pyglet.image.load(path.format(animal_name))
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2 + offset
    return img

pictures = [image_load(name, IMG_PATH, 0)
            for name, offset in ANIMAL_INFO]
active_pictures = [image_load(name, ACTIVE_PATH, offset)
                   for name, offset in ANIMAL_INFO]

def get_tile_size(window):
    return min(window.width / COLUMNS,
               window.height / ROWS)


def logical_to_screen(logical_x, logical_y, window):
    tile_size = get_tile_size(window)
    start_x = (window.width - tile_size * COLUMNS) / 2
    start_y = (window.height - tile_size * ROWS) / 2
    screen_x = start_x + (logical_x + 0.5) * tile_size
    screen_y = start_y + (logical_y + 0.5) * tile_size
    return screen_x, screen_y


def screen_to_logical(screen_x, screen_y, window):
    tile_size = get_tile_size(window)
    start_x = (window.width - tile_size * COLUMNS) / 2
    start_y = (window.height - tile_size * ROWS) / 2
    logical_x = (screen_x - start_x) / tile_size - 0.5
    logical_y = (screen_y - start_y) / tile_size - 0.5
    return logical_x, logical_y


class Tile:
    def __init__(self):
        self.value = random.randrange(10)
        self.sprite = pyglet.sprite.Sprite(pictures[self.value])

    def draw(self, x, y, window, selected):
        if selected:
            self.sprite.image = active_pictures[self.value]
        else:
            self.sprite.image = pictures[self.value]
        tile_size = get_tile_size(window)
        img_width = pictures[0].width
        screen_x, screen_y = logical_to_screen(x, y, window)
        self.sprite.x = screen_x
        self.sprite.y = screen_y
        self.sprite.scale = (tile_size - SPACING) / img_width
        self.sprite.draw()


class Board:
    def __init__(self):
        self.content = [[Tile() for i in range(ROWS)]
                        for j in range(COLUMNS)]
        self.last_mouse_pos = 0, 0

    def draw(self, window):
        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                selected = (x, y) == board.last_mouse_pos
                if not selected:
                    tile.draw(x, y, window, selected)

        x, y = board.last_mouse_pos
        if 0 <= x < COLUMNS and 0 <= y < ROWS:
            tile = self.content[x][y]
            tile.draw(x, y, window, True)

board = Board()

@window.event
def on_text(text):
    print(text)

@window.event
def on_draw():
    window.clear()
    board.draw(window)

@window.event
def on_mouse_motion(x, y, dx, dy):
    logical_x, logical_y = screen_to_logical(x, y, window)
    logical_x = round(logical_x)
    logical_y = round(logical_y)
    board.last_mouse_pos = logical_x, logical_y

#def tik(t):
    #print(t)

#pyglet.clock.schedule_interval(tik, 1/30)

pyglet.app.run()
print('Hotovo!')
