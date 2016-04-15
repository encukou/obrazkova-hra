import random

import pyglet
window = pyglet.window.Window()

COLUMNS = 8
ROWS = 8

SPACING = 20
MOVE_SPEED = 5
EXPLODE_SPEED = 3

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
def image_load(filename, offset):
    img = pyglet.image.load(filename)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2 + offset
    return img

pictures = [image_load(IMG_PATH.format(name), 0)
            for name, offset in ANIMAL_INFO]
active_pictures = [image_load(ACTIVE_PATH.format(name), offset)
                   for name, offset in ANIMAL_INFO]

active_bg_img = image_load('assets/puzzle-pack-2/PNG/Tiles grey/tileGrey_01.png', 0)
bg_sprite = pyglet.sprite.Sprite(active_bg_img)

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
        self.animation = None
        self.reset_value()

    def reset_value(self):
        self.value = random.randrange(10)
        self.sprite = pyglet.sprite.Sprite(pictures[self.value])

    def draw(self, x, y, window, selected=False):
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
        if self.animation:
            self.animation.draw(self, x, y, window)
        else:
            self.sprite.draw()

    def update(self, t):
        if self.animation:
            result = self.animation.update(t)
            if result:
                self.animation = None
            return result


class Board:
    def __init__(self):
        self.content = [[Tile() for i in range(ROWS)]
                        for j in range(COLUMNS)]
        self.last_mouse_pos = 0, 0
        self.selected_tile = None
        self.extra_tiles = set()

        found_area = True
        while found_area:
            found_area = False
            for x, column in enumerate(self.content):
                for y, tile in enumerate(column):
                    area = self.check_area(x, y)
                    if len(area) >= 3:
                        tile.reset_value()
                        found_area = True
                        break

    def draw(self, window):
        if self.selected_tile is not None:
            logical_x, logical_y = self.selected_tile
            x, y = logical_to_screen(logical_x, logical_y, window)
            bg_sprite.x = x
            bg_sprite.y = y
            bg_sprite.color = 150, 150, 255
            bg_sprite.draw()

        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                selected = (x, y) == board.last_mouse_pos
                if not selected:
                    tile.draw(x, y, window, selected)

        x, y = board.last_mouse_pos
        if 0 <= x < COLUMNS and 0 <= y < ROWS:
            tile = self.content[x][y]
            tile.draw(x, y, window, True)

        for x, y, tile in self.extra_tiles:
            tile.draw(x, y, window)

    def action(self, x, y):
        if 0 <= x < COLUMNS and 0 <= y < ROWS:
            current_tile = self.content[x][y]
            if current_tile.animation:
                return
            if self.selected_tile is None:
                self.selected_tile = x, y
            elif self.selected_tile == (x, y):
                self.selected_tile = None
            else:
                other_x, other_y = self.selected_tile
                self.content[x][y], self.content[other_x][other_y] = (
                    self.content[other_x][other_y], self.content[x][y])
                self.content[x][y].animation = MoveAnimation(other_x, other_y)
                self.content[other_x][other_y].animation = MoveAnimation(x, y)
                self.selected_tile = None

    def update(self, t):
        tiles_to_check = set()
        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                result = tile.update(t)
                if result:
                    self.check_and_remove_area(x, y)

        for x, y, tile in list(self.extra_tiles):
            result = tile.update(t)
            if result:
                self.extra_tiles.remove((x, y, tile))

    def check_area(self, x, y):
        area = set()
        to_check = {(x, y)}
        value = self.content[x][y].value
        while to_check:
            x, y = to_check.pop()
            area.add((x, y))
            for x, y in (x+1, y), (x-1, y), (x, y+1), (x, y-1):
                if ((x, y) not in area and
                        0 <= x < COLUMNS and 0 <= y < ROWS and
                        self.content[x][y].value == value and
                        not self.content[x][y].animation):
                    to_check.add((x, y))
        return area

    def check_and_remove_area(self, x, y):
        area = self.check_area(x, y)
        if len(area) >= 3:
            for x in range(COLUMNS):
                removed = 0
                for y in range(ROWS):
                    while (x, y + removed) in area:
                        removed += 1
                    if (x, y) in area:
                        self.extra_tiles.add((x, y, self.content[x][y]))
                        self.content[x][y].animation = ExplodeAnimation()
                    if removed:
                        if y + removed < ROWS:
                            self.content[x][y] = self.content[x][y + removed]
                        else:
                            tile = Tile()
                            self.content[x][y] = tile
                        self.content[x][y].animation = MoveAnimation(
                            x, y + removed, speed=1/removed)


class MoveAnimation:
    def __init__(self, start_x, start_y, speed=1):
        self.start_x = start_x
        self.start_y = start_y
        self.pos = 0
        self.speed = speed

    def update(self, t):
        self.pos += t * MOVE_SPEED * self.speed
        if self.pos > 1:
            return True

    def draw(self, tile, x, y, window):
        logical_x = x * self.pos + self.start_x * (1 - self.pos)
        logical_y = y * self.pos + self.start_y * (1 - self.pos)
        tile.sprite.x, tile.sprite.y = logical_to_screen(logical_x, logical_y, window)
        tile.sprite.draw()


class ExplodeAnimation:
    def __init__(self):
        self.pos = 0

    def update(self, t):
        self.pos += t * EXPLODE_SPEED
        if self.pos > 1:
            return True

    def draw(self, tile, x, y, window):
        tile.sprite.scale *= 1 + self.pos * 2
        tile.sprite.opacity = 255 * (1 - self.pos)
        tile.sprite.draw()


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

@window.event
def on_mouse_press(x, y, button, modifiers):
    logical_x, logical_y = screen_to_logical(x, y, window)
    logical_x = round(logical_x)
    logical_y = round(logical_y)
    board.action(logical_x, logical_y)

pyglet.clock.schedule_interval(board.update, 1/30)

pyglet.app.run()
