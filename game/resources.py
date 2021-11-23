import pyglet
import pathlib
import pygame

pyglet.resource.path = ["gfx"]
pyglet.resource.reindex()
pygame.mixer.init()

def center(img):
	img.anchor_x = img.width/2
	img.anchor_y = img.height/2
	return img


bullet = center(pyglet.resource.image("bullet.png"))
player = center(pyglet.resource.image("player.png"))
icon = pyglet.image.load("gfx/player.png")
ground = center(pyglet.resource.image("ground.png"))
station = center(pyglet.resource.image("station.png"))
gui = pyglet.resource.image("GUI_background.png")
gui_button = pyglet.resource.image("button_background.png")
fuelstate = pyglet.resource.image("Fuelstate.png")
fuelstate_frame = pyglet.resource.image("Fuelstate frame.png")
rocks =[center(pyglet.resource.image("/".join(str(i).split('gfx\\')[1].split("\\")))) for i in pathlib.Path("gfx/terrain/rocks").iterdir() if str(i).endswith(".png") ]
gems =[center(pyglet.resource.image("/".join(str(i).split('gfx\\')[1].split("\\")))) for i in pathlib.Path("gfx/terrain/gems").iterdir() if str(i).endswith(".png") ]
craters =[center(pyglet.resource.image("/".join(str(i).split('gfx\\')[1].split("\\")))) for i in pathlib.Path("gfx/terrain/craters").iterdir() if str(i).endswith(".png") ]

pyglet.resource.add_font("Orbitron.ttf")

def play(asset):
	pygame.mixer.music.load("sfx/" + asset + ".mp3")
	pygame.mixer.music.play()