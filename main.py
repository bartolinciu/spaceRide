import pyglet
import game
import random
import time

window = pyglet.window.Window(caption = "Space Ride", width = 800, height = 600)
window.set_location( int(window.screen.width/2-400), int(window.screen.height/2-300) )
window.set_icon(game.resources.icon)
main_batch = pyglet.graphics.Batch()
ground_group = pyglet.graphics.OrderedGroup(0)
terrain_group = pyglet.graphics.OrderedGroup(1)
bullets_group = pyglet.graphics.OrderedGroup(2)
ground_img = pyglet.sprite.Sprite(img = game.resources.ground, x = 400, y=300, batch = main_batch, group = ground_group)

ground_img.scale = 40
game_objs = []
player = None
craters = 0
craters_limit = 5
craters_time = 0.0
pause = False
deathscreen = False
reason = pyglet.text.Label( text = "", x = 400, y = -300, anchor_y = "center", anchor_x = "center", font_name = "Orbitron", font_size = 30 )
hud = game.hud.HUD()
game.init()

def Exit():
	game.save()
	quit()

@window.event
def on_close():
	Exit()
	
@window.event
def on_key_press(symbol, modifiers):
	global pause
	global deathscreen
	
	if deathscreen:
		Gui.enabled = True
	else:
		if symbol == pyglet.window.key.ESCAPE:
			if pause:
				pause = False
				Gui.enabled = False
				pyglet.clock.schedule_once(update, 1/120.0)
				pyglet.clock.schedule_interval( spawn_station, 10 )
				pyglet.clock.schedule_interval( spawn_obstacles, 1/2 )
			else:
				if not Gui.enabled:
					pause = True
					Gui.enabled = True
		
	return pyglet.event.EVENT_HANDLED
		
	
@window.event
def on_mouse_motion(*args, **kwargs):
	if Gui.enabled:
		return Gui.handle_mouse_motion(*args, **kwargs)

		
@window.event
def on_draw():
	window.clear()
	if not Gui.enabled:
		main_batch.draw()
		player.draw()
		hud.draw()
		pyglet.gl.glScalef(1,-1, 1)
		reason.text = player.reason
		reason.draw()
		pyglet.gl.glScalef(1,-1, 1)
	else:
		Gui.draw()
		

def spawn_obstacles(dt):
	global craters
	global craters_time
	global craters_limit
	n = random.randint(0, 5)
	for i in range(n):
		x = random.randint(60, 740)
		not_good = True
		while not_good:
			obj = game.spawn( ([game.rock.Rock] * 100 + [game.gem.Gem]*25 +  [game.crater.Crater] * 10)[random.randint(0,134)], y = -50, x = x, batch = main_batch, speed = game.speed, push = False, group = terrain_group  )
			not_good = False
			for i in game.new_objs + game_objs:
				if game.utils.check_collision(obj,i):
					not_good = True
					if x < 730:
						x += 10
					else:
						return
			if isinstance(obj, game.crater.Crater) and not not_good:
				if craters >= craters_limit:
					not_good = True
				else:
					craters +=1
		game.new_objs.append(obj)
	if craters_time > 5:
		craters_time = 0.0
		craters = 0
	craters_time += dt
		
def spawn_station(dt):
	x = random.randint(60, 540)
	not_good = True
	while not_good:
		obj = game.spawn( game.fuelstation.FuelStation, y = -50, x = x, batch = main_batch, speed = game.speed, push = False  )
		not_good = False
		for i in game.new_objs + game_objs:
			if game.utils.check_collision(obj,i):
				not_good = True
				if x < 530:
					x += 10
				else:
					return
	game.new_objs.append(obj)
	
def update(dt):
	global deathscreen
	game_objs.extend(game.new_objs)
	game.new_objs.clear()
	for obj in game_objs:
		obj.update(dt)
	global speed
	speed += 0.011
	for i,obj1 in enumerate(game_objs):
		for obj2 in game_objs[i+1:]:
			if game.utils.check_collision(obj1, obj2):
				obj1.handle_collision(obj2)
				obj2.handle_collision(obj1)

	for obj in [ obj for obj in game_objs if obj.destroyed ]:
		game_objs.remove(obj)
		
	hud.update(player.state())
	
	if not player.destroyed and not pause:
		pyglet.clock.schedule_once(update, 1/120.0)
	else:
		pyglet.clock.unschedule(spawn_obstacles)
		pyglet.clock.unschedule(spawn_station)
		Gui.enabled = True
		if player.destroyed:
			game.resources.play("game_over")
			deathscreen = True
			Gui.enabled = False
			global states
			player_states = player.state()
			for i,k in enumerate(player_states):
				if k is "fuel":
					continue
				game.states[i] = player_states[k]
			global self_made_repairs
			game.self_made_repairs = [False] * 5 
			global money
			global pending_money
			game.money += game.pending_money
			
		
def new_game():
	global player
	global craters
	global craters_time
	global pause
	global speed
	global deathscreen
	deathscreen = False
	speed= 50
	window.set_mouse_cursor( window.get_system_mouse_cursor(window.CURSOR_DEFAULT) )
	player = game.spawn(game.player.Player, fuel = 50,maxfuel = 50, levels=game.levels, states = game.states, x = 400, y = 500, handler = True, window = window, batch = main_batch, bullets_group = bullets_group )
	game_objs.clear()
	craters = 0
	craters_time = 0.0
	pause = False
	pyglet.clock.schedule_once(update, 1/120.0)
	pyglet.clock.schedule_interval( spawn_station, 10 )
	pyglet.clock.schedule_interval( spawn_obstacles, 1/2 )
	Gui.enabled = False
	
	

guis = [
	game.gui.GUI(["New Game","Repairs", "Upgrades", "Exit"], window, enabled = False),
	game.gui.UpgradeGUI( window, enabled = False, levels = game.levels),
	game.gui.RepairGUI( window, enabled = False, states = game.states )
	]
Gui = guis[0]

def switch_gui(index):
	global Gui
	global button_handlers
	button_handlers = gui_handlers[index]
	Gui.enabled = False
	Gui = guis[index]
	Gui.enabled = True
	if index == 2:
		for part in range(5):
			Gui.update(part, game.states[part])
	
def upgrade(index):
	global money
	global levels
	if game.levels[index] < 10 and game.money >=(game.levels[index]+1) * 100 and game.states[index] == 100:
		game.money-=(game.levels[index]+1) * 100  
		game.levels[index] +=1
		Gui.update(index = index, level=game.levels[index], amount = (game.levels[index]+1) * 100   )
		Gui.update_balance(balance = game.money)
	
def repair(part, self_made):
	global states
	global self_made_repairs
	global money
	if not self_made:
		cost = {0:100, 1:200}[game.states[part] < 30]
		if game.money >= cost:
			game.states[part] = 100
			game.money -= {0:100, 1:200}[game.states[part] < 30]
	else:
		if game.states[part] < 30 and not game.self_made_repairs[part]:
			game.states[part] = random.randint(20,30)
			game.self_made_repairs[part] = True
	Gui.update(part, game.states[part])
	
gui_handlers = [
	[ new_game,(switch_gui, 2), (switch_gui, 1),Exit ],
	[ (switch_gui, 0), (upgrade, 0), (upgrade, 1), (upgrade, 2), (upgrade, 3), (upgrade, 4)],
	[ (switch_gui, 0)] + [ (repair, int((i-2)/2), i%2) for i in range(1,12) ]
	]
	
button_handlers = gui_handlers[0]

@window.event
def on_mouse_press(x,y,button,modifiers):
	if button == pyglet.window.mouse.LEFT:
		button_index = Gui.handle_mouse_press(x,y)
		if not button_index == None:
			handler = button_handlers[button_index]
			if not isinstance(handler, tuple):
				handler()
			else:
				handler[0](*handler[1:])
		return pyglet.event.EVENT_HANDLED
	
	

if __name__ == "__main__":
	pyglet.gl.glTranslatef(1, 600, 1)
	pyglet.gl.glScalef(1,-1, 1)
	Gui.enabled=True
	pyglet.app.run()
