import math
import game

def distance( pos1, pos2 ):
	return math.sqrt( abs(pos1[0]-pos2[0]) ** 2 + abs( pos1[1] - pos2[1] ) ** 2 )

def diameter(obj):
	return distance( (0,0), (obj.width,obj.height) )

def really_check_collision( obj1, obj2 ):
	a = abs( obj1.x - obj2.x )
	b = abs(obj2.y - obj1.y)
	c = distance( obj1.position, obj2.position) 
	if c > (diameter(obj1)/2 + diameter(obj2)/2) or b > (abs(obj1.height/2)+abs(obj2.height/2)) or a>(abs(obj1.width/2) + abs(obj2.width/2)):
		return False
	if not a==0 and not b==0:
		d = abs( obj2.width/2)
		g = abs(obj1.height/2)
		f = (c*d)/a
		i = (g*c)/b
	else:
		if b==0:
			return ( abs(obj1.width/2 + obj2.width/2) ) >= c
		elif a ==0:
			return ( abs(obj1.height/2 + obj2.height/2) ) >= c
		else:
			return True
	judgement = (i+f) >= c
		
	return judgement
	
def check_collision(obj1, obj2):
	if obj1.y < obj2.y :
		return really_check_collision(obj1, obj2)
	return really_check_collision(obj2, obj1)
	