import pyglet
window = pyglet.window.Window()

obrazek = pyglet.image.load('assets/animal-pack/PNG/Square without details/penguin.png')
sprite = pyglet.sprite.Sprite(obrazek)
sprite.y_speed = 400

@window.event
def on_text(text):
    print(text)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

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
