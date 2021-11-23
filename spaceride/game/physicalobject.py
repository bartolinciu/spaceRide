import pyglet
import game
import random

class PhysicalObject(pyglet.sprite.Sprite):
	def __init__(self, imgs, speed=0, *args, **kwargs ):
		super(PhysicalObject, self).__init__(img = imgs[random.randint(0, len(imgs)-1)], *args, **kwargs)
		self.speed=speed
		self.destroyed = False
		self.fresh = True
		
	def update(self, dt):
		self.y+=self.speed * dt
		if (self.y + self.height/2 > game.window_height or self.y - self.height/2 < 0) and not self.fresh:
			self.destroyed = True
		if self.y > 0:
			self.fresh = False
		
	def handle_collision(self, obj):
		if isinstance(obj, (game.bullet.Bullet, game.player.Part)) and obj.good:
			self.destroyed = True
