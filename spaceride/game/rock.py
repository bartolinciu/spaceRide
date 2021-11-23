import game

class Rock(game.obstacle.Obstacle):
	def __init__(self, *args, **kwargs):
		super(Rock, self).__init__(imgs = game.resources.rocks, *args, **kwargs)