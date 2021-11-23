import game
import random

class Crater(game.fuelobject.FuelObject):
	def __init__(self, *args, **kwargs):
		super(Crater,self).__init__(imgs=game.resources.craters, *args, **kwargs)
		self.combustion = game.resources.craters.index(self.image)+1
		