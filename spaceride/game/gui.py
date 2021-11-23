import pyglet
import game

class Button:	
	def __init__(self, text, x, y, foreground, background, width = 200, height = 50, batch = None, ):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.background = pyglet.sprite.Sprite(img = game.resources.gui_button, x = self.x, y = self.y, batch = batch, group = background)
		self.foreground = pyglet.text.Label( text = text, x  = x + width/2, y = y + height/2, anchor_x = "center", anchor_y = "center", batch = batch, font_name = "Orbitron", group = foreground )
	def ishovered(self, pos):
		return self.x < pos[0] and pos[0] < self.x + self.width and self.y < pos[1] and pos[1] < self.y + self.height
		
	def update(self, text):
		self.foreground.text = text
		
class GUI:
	def __init__(self, buttons,window, enabled = True):
		self.buttons = []
		self.window = window
		self.batch = pyglet.graphics.Batch()
		self.background = pyglet.sprite.Sprite(img = game.resources.gui, x = -1, y = -600, batch = self.batch, group = pyglet.graphics.OrderedGroup(0))
		button_background = pyglet.graphics.OrderedGroup(1)
		button_foreground = pyglet.graphics.OrderedGroup(2)
		for i, button in enumerate(buttons):
			self.buttons.append(Button(button, x = 300, y = -220  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
		self.enabled = enabled
		
	def handle_mouse_motion(self, x, y, dx, dy):
		for i in self.buttons:
			if i.ishovered( (x,y-600) ):
				self.window.set_mouse_cursor( self.window.get_system_mouse_cursor(self.window.CURSOR_HAND) )
				return pyglet.event.EVENT_HANDLED
		self.window.set_mouse_cursor( self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT) )
		return pyglet.event.EVENT_HANDLED
		
	def handle_mouse_press(self, x, y):
		if self.enabled:
			for i,b in enumerate(self.buttons):
				if b.ishovered( (x,y - 600) ):
					return i
		return None
		
	def draw(self):
		pyglet.gl.glScalef(1,-1, 1)
		self.batch.draw()
		pyglet.gl.glScalef(1,-1, 1)
	
class UpgradeGUI(GUI):
	def __init__(self, window, enabled = True, levels = [0]*5):
		buttons = ["Left engine", "Right engine", "Left gun", "Right gun", "Cabin"]
		self.buttons = []
		self.labels = []
		self.window = window
		self.batch = pyglet.graphics.Batch()
		global money
		self.background = pyglet.sprite.Sprite(img = game.resources.gui, x = -1, y = -600, batch = self.batch, group = pyglet.graphics.OrderedGroup(0))
		button_background = pyglet.graphics.OrderedGroup(1)
		button_foreground = pyglet.graphics.OrderedGroup(2)
		self.buttons.append(Button(text = "Back", x = 80, y = -130 , batch = self.batch, background = button_background, foreground = button_foreground))
		for i, button in enumerate(buttons):
			if levels[i] < 10:
				self.buttons.append(Button(text = "%i$" % ((levels[i]+1) * 100)  , x = 500, y = -200  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
			else:
				self.buttons.append(Button(text = "MAX", x = 500, y = -200  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
			name = pyglet.text.Label(text = button, x = 90, y = -180  - 70 * i  , batch = self.batch, group = button_foreground, font_name = "Orbitron" )
			info = pyglet.text.Label( text = "%i/10" % levels[i], x = 100 + name.content_width, y = -180  - 70 * i  , batch = self.batch, group = button_foreground, font_name = "Orbitron" )
			self.labels.extend([name, info])
		self.labels.append( pyglet.text.Label( text = "%i$" % game.money, y = -90, x = 600, batch = self.batch, group = button_foreground, font_name = "Orbitron" ) )
		self.enabled = enabled
		
	def update(self, index, level, amount):
		self.labels[index*2+1].text = "%i/10" % level
		if level < 10:
			self.buttons[index+1].update("%i$" % amount)
		else:
			self.buttons[index+1].update("MAX")
	def update_balance(self, balance):
		self.labels[-1].text = "%i$" % balance
		
class RepairGUI(GUI):
	def __init__(self, window, enabled = True, states = [100]*5):
		buttons = ["Left engine", "Right engine", "Left gun", "Right gun", "Cabin"]
		self.buttons = []
		self.labels = []
		self.window = window
		self.batch = pyglet.graphics.Batch()
		global money
		self.background = pyglet.sprite.Sprite(img = game.resources.gui, x = -1, y = -600, batch = self.batch, group = pyglet.graphics.OrderedGroup(0))
		button_background = pyglet.graphics.OrderedGroup(1)
		button_foreground = pyglet.graphics.OrderedGroup(2)
		self.buttons.append(Button(text = "Back", x = 80, y = -130 , batch = self.batch, background = button_background, foreground = button_foreground) )
		self.labels.append( pyglet.text.Label( text = "DIY", x = 390, y = -130, batch = self.batch,group = button_foreground, font_name = "Orbitron" ) )
		self.labels.append( pyglet.text.Label( text = "Profesional", x = 570, y = -130, batch = self.batch,group = button_foreground, font_name = "Orbitron" ) )
		self.labels.append( pyglet.text.Label( text = "%i$"%game.money, x = 600, y = -90, batch = self.batch,group = button_foreground, font_name = "Orbitron" ) )
		for i, button in enumerate(buttons):
			if states[i] < 30:
				self.buttons.append(Button(text = "Repair", x = 300, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
				self.buttons.append(Button(text = "200$", x = 520, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
			elif states[i] == 100:
				self.buttons.append(Button(text = "Repaired", x = 300, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
				self.buttons.append(Button(text = "Repaired", x = 520, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
			elif states[i] < 100 and states[i] >= 30:
				self.buttons.append(Button(text = "Unavailable", x = 300, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
				self.buttons.append(Button(text = "100$", x = 520, y = -210  - 70 * i  , batch = self.batch, background = button_background, foreground = button_foreground ) )
			name = pyglet.text.Label(text = button, x = 100, y = -190  - 70 * i  , batch = self.batch, group = button_foreground, font_name = "Orbitron" )
			info = pyglet.text.Label( text = "%i%%" % states[i], x = 110 + name.content_width, y = -190  - 70 * i  , batch = self.batch, group = button_foreground, font_name = "Orbitron" )
			self.labels.extend([name, info])
			
	def update(self, index, state):
		self.labels[index * 2 + 4].text = "%i%%" % state
		if state < 30:
			self.buttons[index*2+1].update(text = "Repair")
			self.buttons[index*2+2].update(text = "200$")
		elif state == 100:
			self.buttons[index*2+1].update(text = "Repaired" )
			self.buttons[index*2+2].update(text = "Repaired" )
		elif state < 100 and state >= 30:
			self.buttons[index*2+1].update(text = "Unavailable")
			self.buttons[index*2+2].update(text = "100$")
		self.labels[2].text = "%i$"% game.money