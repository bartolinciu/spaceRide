import game

class Gem( game.obstacle.Obstacle ):
	def __init__(self, *args, **kwargs):
		super(Gem, self).__init__(imgs = game.resources.gems,*args, **kwargs)
	
	def handle_collision(self,obj):
		super(Gem, self).handle_collision(obj)
		if isinstance(obj, game.bullet.Bullet):
			game.add_money( {0:10, 1:5, 2:15}[int(game.resources.gems.index(self.image)/4)] ) 