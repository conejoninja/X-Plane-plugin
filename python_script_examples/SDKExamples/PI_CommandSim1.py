"""
CommandSim.py

Ported to Python by Sandy Barbour - 28/04/2005

This function demonstrates how to send commands to the sim.  Commands allow you to simulate
any keystroke or joystick button press or release.
"""

from XPLMDefs import *
from XPLMMenus import *
from XPLMUtilities import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "CommandSim1"
		self.Sig =  "SandyBarbour.Python.CommandSim1"
		self.Desc = "An example of sending commands."

		mySubMenuItem = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Command Sim 1", 0, 1)
		self.MyMenuHandlerCB = self.MyMenuHandlerCallback
		self.myMenu = XPLMCreateMenu(self, "Command Sim 1", XPLMFindPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB,	0)

		"""
		For each command, we set the item refcon to be the key command ID we wnat
		to run.   Our callback will use this item refcon to do the right command.
		This allows us to write only one callback for the menu.
		"""
		XPLMAppendMenuItem(self.myMenu, "Pause", xplm_key_pause, 1)
		XPLMAppendMenuItem(self.myMenu, "Reverse Thrust", xplm_key_revthrust, 1)
		XPLMAppendMenuItem(self.myMenu, "Jettison", xplm_key_jettison, 1)
		XPLMAppendMenuItem(self.myMenu, "Brakes (Regular)", xplm_key_brakesreg, 1)
		XPLMAppendMenuItem(self.myMenu, "Brakes (Full)",  xplm_key_brakesmax, 1)
		XPLMAppendMenuItem(self.myMenu, "Landing Gear",  xplm_key_gear, 1)
		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		XPLMDestroyMenu(self, self.myMenu)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def MyMenuHandlerCallback(self, inMenuRef, inItemRef):
		"""
		This is the menu callback.  We simply turn the item ref back
		into a command ID and tell the sim to do it.
		"""
		XPLMCommandKeyStroke(inItemRef)
		pass

