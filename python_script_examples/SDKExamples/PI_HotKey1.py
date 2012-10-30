"""
HotKey.py

Ported to Python by Sandy Barbour - 28/04/2005

This code shows how to implement a trivial hot key.  A hot key is a mappable command
key the user can press; in this case, this plugin maps F1 being pressed down to getting
the sim to say stuff.
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMUtilities import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "HotKey1"
		self.Sig =  "SandyBarbour.Python.HotKey1"
		self.Desc = "An example using a hotkey."

		"""
		Setting up a hot key is quite easy; we simply register a callback.
		We also provide a text description so that the plugin manager can
		list the hot key in the hot key mapping dialog box.
		"""

		self.MyHotKeyCB = self.MyHotKeyCallback
		self.HotKey = XPLMRegisterHotKey(self, XPLM_VK_F1, xplm_DownFlag, "Says 'Hello World 1'", self.MyHotKeyCB, 0)
		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		XPLMUnregisterHotKey(self, self.HotKey)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def MyHotKeyCallback(self, inRefcon):
		"""
		This is our hot key handler.  Note that we don't know what key stroke
		was pressed!  We can identify our hot key by the 'refcon' value though.
		This is because our hot key could have been remapped by the user and we
		wouldn't know it.
		"""
		XPLMSpeakString("Hello World 1!")
		pass

