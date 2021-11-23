import pyglet
import game

class indicator:
	def __init__(self, name, batch, font_size, font_name, x, y, width):
		self.width = width
		self.x = x
		self.name = pyglet.text.Label(text = name + ":", x = x, y = y, font_size = font_size, font_name = font_name, batch = batch)
		self.state = pyglet.text.Label(text = "%i%%" % 100,font_size = font_size, font_name = font_name, batch = batch, y = y )
		self.state.x = x + width - self.state.content_width
	def update(self, state):
		self.state.text = "%i%%" % state
		self.state.x = self.x + self.width - self.state.content_width
class fuelindicator:
	def __init__(self, max, x, y, batch):
		self.max = max
		self.label = pyglet.text.Label(text = "Fuel ", y = y, x = x, batch = batch,font_size = 20, font_name = "Orbitron")
		self.frame = pyglet.sprite.Sprite(img = game.resources.fuelstate_frame , x = x + self.label.content_width, y = y, batch = batch)
		self.bar = pyglet.sprite.Sprite(img = game.resources.fuelstate, x = x + 2 + self.label.content_width, y=y + 2, batch = batch)
		self.org_width = self.bar.width
	def update(self, state):
		img = self.bar.image
		img.width = self.org_width * (state / self.max)
		img.texture.width = self.org_width * (state / self.max)
		self.bar.image = img
class HUD:
	def __init__(self):
		batch = pyglet.graphics.Batch()
		self.batch = batch
		self.leftengine = indicator(name = "Left engine",x = 10, y=-30,batch = batch, width = 300, font_size = 20, font_name = "Orbitron")
		self.rightengine = indicator(name = "Right engine",x = 10, y=-60,batch = batch,width = 300, font_size = 20, font_name = "Orbitron")
		self.leftgun = indicator(name = "Left gun",x = 10, y=-90,batch = batch,width = 300, font_size = 20, font_name = "Orbitron")
		self.rightgun = indicator(name = "Right gun",x = 10, y=-120,batch = batch,width = 300, font_size = 20, font_name = "Orbitron")
		self.cabin = indicator(name = "Cabin",x = 10, y=-150,batch = batch,width = 300, font_size = 20, font_name = "Orbitron")
		self.fuel = fuelindicator(max = 50, x = 570 , y = -40, batch = batch)
	def update(self, state):
		for i in state:
			self.__getattribute__(i).update(state[i])
	
	def draw(self):
		pyglet.gl.glScalef(1,-1, 1)
		self.batch.draw()
		pyglet.gl.glScalef(1,-1, 1)