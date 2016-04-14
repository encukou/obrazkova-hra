import random

import pyglet
window = pyglet.window.Window()

COLUMNS = 8
ROWS = 8

SPACING = 20

obrazek = pyglet.image.load('assets/animal-pack/PNG/Square without details/penguin.png')
obrazek.anchor_x = obrazek.width // 2
obrazek.anchor_y = obrazek.height // 2
sprite = pyglet.sprite.Sprite(obrazek)
sprite.y_speed = 400


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


class Board:
    def __init__(self):
        self.content = [[random.randrange(8) for i in range(ROWS)]
                        for j in range(COLUMNS)]

    def draw(self, window):
        tile_size = get_tile_size(window)
        for x, column in enumerate(self.content):
            for y, num in enumerate(column):
                screen_x, screen_y = logical_to_screen(x, y, window)
                sprite.x = screen_x
                sprite.y = screen_y
                sprite.scale = (tile_size - SPACING) / obrazek.width
                sprite.draw()

board = Board()

@window.event
def on_text(text):
    print(text)

@window.event
def on_draw():
    window.clear()
    board.draw(window)

def tik(t):
    sprite.x += 100 * t
    sprite.y += sprite.y_speed * t
    sprite.y_speed -= 400 * t
    if sprite.y < 0:
        sprite.y_speed = -sprite.y_speed
    print(t)

pyglet.clock.schedule_interval(tik, 1/30)

pyglet.app.run()
print('Hotovo!')
