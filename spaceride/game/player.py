import game
import pyglet

class Part:
	def __init__( self, x, y, width, height, scale, parent = None, level = 0 ):
		self.parent = parent
		self.x = x
		self.y = y
		self.width = width*scale
		self.height = height*scale
		self.good = True
		self.state = 100
		self.position = (self.x, self.y)
		self.level = level
		
	def handle_collision(self, obj=None):
		self.state -= (13 - self.level)
		if self.state < 0:
			self.good = False
			self.state =0
	
	def upgrade(self):
		self.level += 1


class Gun(Part):
	def __init__(self, batch, bullets_group, *args, **kwargs):
		super(Gun, self).__init__(width = 17, height = 126, *args, **kwargs)	
		self.batch = batch
		self.bullets_group = bullets_group
		
	def shoot(self):
		if self.good:
			game.spawn( game.bullet.Bullet, x = self.x , y = self.y-self.height/2, batch = self.batch, group = self.bullets_group )
			game.resources.play("laser")
			


class Engine(Part):
	def __init__(self, *args, **kwargs):
		super(Engine,self).__init__(width = 67, height = 91, *args, **kwargs)
	
	def handle_collision(self, *args, **kwargs):
		if self.good:
			super(Engine,self).handle_collision(*args, **kwargs)
			self.parent.combustion+=0.125
	
class Cabin(Part):
	def __init__(self, *args, **kwargs):
		super(Cabin, self).__init__( width = 42, height = 151, *args, **kwargs )
		
	def handle_collision(self, *args, **kwargs):
		super(Cabin, self).handle_collision( *args,**kwargs )
		if not self.good:
			self.parent.destroyed = True
			self.parent.reason = "Cabin destroyed"
		
		
class Player(pyglet.sprite.Sprite):
	def __init__(self, fuel, maxfuel, batch, bullets_group, levels = [0]*5, states = [100]*5, *args, **kwargs):
		super(Player,self).__init__(img = game.resources.player, *args, **kwargs)
		self.fuel = fuel
		self.leftgun = Gun(x = self.x - 97, y = self.y, scale = self.scale, parent = self, batch = batch, bullets_group = bullets_group)
		self.rightgun = Gun( x = self.x + 97, y = self.y, scale = self.scale, parent = self, batch = batch, bullets_group = bullets_group )
		self.leftengine = Engine( x = self.x - 33, y = self.y + 36, scale = self.scale, parent = self  )
		self.rightengine = Engine( x = self.x + 33, y = self.y + 36, scale = self.scale, parent = self  )
		self.cabin = Cabin( x = self.x, y = self.y + 10, scale = self.scale, parent = self )
		self.parts = [ self.leftengine, self.rightengine, self.leftgun, self.rightgun, self.cabin ]
		for i,part in enumerate(self.parts):
			part.level = levels[i]
			part.state = states[i]
		self.keys = pyglet.window.key.KeyStateHandler()
		global speed
		self.combustion = 1 * (game.speed/50)
		self.destroyed = False
		self.reason = ""
		self.last_shot = 0.0
		self.maxfuel = maxfuel
		
	def update(self, dt):
		self.fuel-=self.combustion * dt
		global speed
		self.combusion = game.speed
		if self.fuel < 0:
			self.destroyed = True
			self.reason = "Out of fuel"
		if self.keys[pyglet.window.key.LEFT]:
			if self.x > 0 + abs(self.width/2):
				self.x -= 10
				for i in self.parts:
					i.x-=10
					i.position = (i.x, i.y)
				
		if self.keys[pyglet.window.key.RIGHT]:
			if self.x < 797 - abs(self.width/2):
				self.x += 10
				for i in self.parts:
					i.x+=10
					i.position = (i.x, i.y)
		
		if self.keys[pyglet.window.key.SPACE]:
			if self.last_shot > 1/2:
				self.leftgun.shoot()
				self.rightgun.shoot()
				self.last_shot = 0.0
		self.last_shot += dt
			
		
		if not self.leftengine.good and not self.rightengine.good:
			self.destroyed = True
			self.reason = "Engines down"
			
	def upgrade(self,index):
		self.parts[index].upgrade()
	
	def handle_collision(self,obj):
		if type(obj) == game.bullet.Bullet:
			return
		else:	
			for i in self.parts:
				if game.utils.check_collision(i, obj):
					if isinstance( obj, game.fuelobject.FuelObject ):
						if obj.active:
							self.fuel -= obj.combustion
							if self.fuel > self.maxfuel:
								self.fuel = self.maxfuel
							game.resources.play("refuel")
					else:
						i.handle_collision(obj)
					obj.handle_collision(i)
	def state(self):
		return {"leftengine":self.leftengine.state, "rightengine":self.rightengine.state, "leftgun":self.leftgun.state, "rightgun":self.rightgun.state, "cabin": self.cabin.state, "fuel":self.fuel }
