import game

class Bullet( game.physicalobject.PhysicalObject ):
	def __init__(self, *args, **kwargs):
		super(Bullet, self).__init__( imgs = [game.resources.bullet], speed = -game.speed, *args, **kwargs )
		self.good = True
		
	def handle_collision(self, obj):
		if not isinstance(obj, (Bullet, game.player.Player, game.player.Part, game.fuelobject.FuelObject)):
			self.destroyed = True
