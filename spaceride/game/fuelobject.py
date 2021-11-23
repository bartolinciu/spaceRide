import game

class FuelObject(game.physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(FuelObject, self).__init__(*args, **kwargs)
		self.active = True
		
	def handle_collision(self, obj):
		if isinstance(obj, game.player.Part):
			self.active=False