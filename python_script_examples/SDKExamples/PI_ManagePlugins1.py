"""
ManagePlugins.py

Ported to Python by Sandy Barbour - 28/04/2005

This example demonstrates how to interact with X-Plane by reading and writing
data.  This example creates menus items that change the nav-1 radio frequency.
"""

from XPLMDefs import *
from XPLMPlugin import *
from XPLMMenus import *
from XPLMUtilities import *

class PythonInterface:
	def XPluginStart(self):
		global myMenu
		self.Name = "ManagePlugins1"
		self.Sig =  "SandyBarbour.Python.ManagePlugins1"
		self.Desc = "A plugin that manages other plugins."

		mySubMenuItem = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Manage Plugins 1", 0, 1)
		self.MyMenuHandlerCB = self.MyMenuHandlerCallback
		self.myMenu = XPLMCreateMenu(self, "Manage Plugins 1", XPLMFindPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB,	0)
		XPLMAppendMenuItem(self.myMenu, "Disable Others", 0, 1)
		XPLMAppendMenuItem(self.myMenu, "Enable All", 1, 1)
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
		# This is the menu handler.  We will go through each plugin.
		for n in range(0 , XPLMCountPlugins()-1):
			plugin = XPLMGetNthPlugin(n)
			me = XPLMGetMyID()

			"""
			Check to see if the plugin is us.  If so, don't
			disable ourselves!
			"""
			str = "plugin=%d,me=%d\n" % (plugin, me)
			XPLMDebugString(str);
			if (plugin != me):
				# Disable based on the item ref for the menu.
				if (inItemRef == 0):
					XPLMDisablePlugin(plugin)
				else:
					XPLMEnablePlugin(plugin)
		pass
