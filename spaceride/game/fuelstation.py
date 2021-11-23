import game

class FuelStation(game.fuelobject.FuelObject):
	def __init__(self, *args, **kwargs):
		super(FuelStation, self).__init__(imgs = [game.resources.station], *args, **kwargs)
		self.combustion = -25
			