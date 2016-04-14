import random

import pyglet
window = pyglet.window.Window()

COLUMNS = 8
ROWS = 8

SPACING = 20

IMG_PATH = 'assets/animal-pack/PNG/Square without details/{}.png'
ANIMAL_NAMES = ('snake', 'penguin', 'elephant', 'monkey',
                'giraffe', 'panda', 'pig', 'hippo', 'parrot',
                'rabbit')

def image_load(animal_name):
    img = pyglet.image.load(IMG_PATH.format(animal_name))
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    return img

obrazky = [image_load(name) for name in ANIMAL_NAMES]

def get_tile_size(window):
    return min(window.width / COLUMNS,
               window.height / ROWS)


def logical_to_screen(x, y, window):
    tile_size = get_tile_size(window)
    start_x = (window.width - tile_size * COLUMNS) / 2
    start_y = (window.height - tile_size * ROWS) / 2
    screen_x = start_x + (x + 0.5) * tile_size
    screen_y = start_y + (y + 0.5) * tile_size
    return screen_x, screen_y


class Tile:
    def __init__(self):
        self.value = random.randrange(6)
        self.sprite = pyglet.sprite.Sprite(obrazky[self.value])

    def draw(self, x, y, window):
        tile_size = get_tile_size(window)
        img_width = self.sprite.image.width
        screen_x, screen_y = logical_to_screen(x, y, window)
        self.sprite.x = screen_x
        self.sprite.y = screen_y
        self.sprite.scale = (tile_size - SPACING) / img_width
        self.sprite.draw()


class Board:
    def __init__(self):
        self.content = [[Tile() for i in range(ROWS)]
                        for j in range(COLUMNS)]

    def draw(self, window):
        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                tile.draw(x, y, window)

board = Board()

@window.event
def on_text(text):
    print(text)

@window.event
def on_draw():
    window.clear()
    board.draw(window)

def tik(t):
    print(t)

pyglet.clock.schedule_interval(tik, 1/30)

pyglet.app.run()
print('Hotovo!')
