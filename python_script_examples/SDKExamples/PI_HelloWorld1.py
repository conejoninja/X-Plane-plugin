"""
HellWorld.py

Ported to Python by Sandy Barbour - 28/04/2005

This plugin implements the canonical first program.  In this case, we will
create a window that has the text hello-world in it.  As an added bonus
the  text will change to 'This is a plugin' while the mouse is held down
in the window.

This plugin demonstrates creating a window and writing mouse and drawing
callbacks for that window.
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *

class PythonInterface:
	"""
	XPluginStart

	Our start routine registers our window and does any other initialization we
	must do.
	"""
	def XPluginStart(self):
		"""
		First we must fill in the passed in buffers to describe our
		plugin to the plugin-system."""
		self.Name = "HelloWorld1"
		self.Sig =  "SandyBarbour.Python.HelloWorld1"
		self.Desc = "A test plugin for the Python Interface."
		self.Clicked = 0
		"""
		Now we create a window.  We pass in a rectangle in left, top,
		right, bottom screen coordinates.  We pass in three callbacks."""
		self.DrawWindowCB = self.DrawWindowCallback
		self.KeyCB = self.KeyCallback
		self.MouseClickCB = self.MouseClickCallback
		self.WindowId = XPLMCreateWindow(self, 50, 600, 300, 400, 1, self.DrawWindowCB, self.KeyCB, self.MouseClickCB, 0)
		return self.Name, self.Sig, self.Desc

	"""
	XPluginStop

	Our cleanup routine deallocates our window.
	"""
	def XPluginStop(self):
		XPLMDestroyWindow(self, self.WindowId)
		pass

	"""
	XPluginEnable.

	We don't do any enable-specific initialization, but we must return 1 to indicate
	that we may be enabled at this time.
	"""
	def XPluginEnable(self):
		return 1

	"""
	XPluginDisable

	We do not need to do anything when we are disabled, but we must provide the handler.
	"""
	def XPluginDisable(self):
		pass


	"""
	XPluginReceiveMessage

	We don't have to do anything in our receive message handler, but we must provide one.
	"""
	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass


	"""
	MyDrawingWindowCallback

	This callback does the work of drawing our window once per sim cycle each time
	it is needed.  It dynamically changes the text depending on the saved mouse
	status.  Note that we don't have to tell X-Plane to redraw us when our text
	changes; we are redrawn by the sim continuously.
	"""
	def DrawWindowCallback(self, inWindowID, inRefcon):
		# First we get the location of the window passed in to us.
		lLeft = [];	lTop = []; lRight = [];	lBottom = []
		XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
		left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])
		"""
		We now use an XPLMGraphics routine to draw a translucent dark
		rectangle that is our window's shape.
		"""
		gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
		color = 1.0, 1.0, 1.0

		if self.Clicked :
			Desc = "I'm a plugin 1"
		else:
			Desc = "Hello World 1"

		"""
		Finally we draw the text into the window, also using XPLMGraphics
		routines.  The NULL indicates no word wrapping.
		"""
		gResult = XPLMDrawString(color, left + 5, top - 20, Desc, 0, xplmFont_Basic)
		pass

	"""
	MyHandleKeyCallback

	Our key handling callback does nothing in this plugin.  This is ok;
	we simply don't use keyboard input.
	"""
	def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
		pass

	"""
	MyHandleMouseClickCallback

	Our mouse click callback toggles the status of our mouse variable
	as the mouse is clicked.  We then update our text on the next sim
	cycle.
	"""
	def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
		"""
		If we get a down or up, toggle our status click.  We will
		never get a down without an up if we accept the down.
		"""
		if ((inMouse == xplm_MouseDown) or (inMouse == xplm_MouseUp)):
			self.Clicked = 1 - self.Clicked

		"""
		Returning 1 tells X-Plane that we 'accepted' the click; otherwise
		it would be passed to the next window behind us.  If we accept
		the click we get mouse moved and mouse up callbacks, if we don't
		we do not get any more callbacks.  It is worth noting that we
		will receive mouse moved and mouse up even if the mouse is dragged
		out of our window's box as long as the click started in our window's
		box.
		"""
		return 1
