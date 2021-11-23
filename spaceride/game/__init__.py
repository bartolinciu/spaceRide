from game import resources,physicalobject,fuelobject,obstacle,utils,rock,gem,crater,player,bullet,fuelstation,gui,hud
import struct

window_height = 600
window_width = 800
speed = 50
new_objs = []
levels = [0]*5
states = [100]*5
self_made_repairs=[False]*5
money = 0
pending_money = 0

def add_money(amount):
	global pending_money
	pending_money += amount

def spawn( classname, handler = False,push = True, window = None, *args, **kwargs ):
	obj = classname(*args, **kwargs)
	obj.scale = -1
	if handler:
		window.push_handlers(obj.keys)
	if push:
		new_objs.extend( [obj] )
	return obj
	
def init():
	global money
	global levels
	global states
	global self_made_repairs
	try:
		with open("savefile.dat", "rb") as f:
			data = f.read()
		money,*levels_raw = struct.unpack("i5H", data)
		for i,k in enumerate(levels_raw):
			states[i] = k&0xff
			levels[i] = (k>>8) & 0x7f
			self_made_repairs[i] = k>>15
	except FileNotFoundError:
		return
		
def save():
	global money
	global levels
	global states
	global self_made_repairs
	levels_packed = [ ((k<<8) | (states[i]&0xff) | self_made_repairs[i]<<15)&0xffff for i,k in enumerate(levels)]
	with open("savefile.dat", "wb") as f:
		f.write( struct.pack("i5H", money, *levels_packed ) )