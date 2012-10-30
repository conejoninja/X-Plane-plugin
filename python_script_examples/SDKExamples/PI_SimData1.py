"""
SimData.py

Ported to Python by Sandy Barbour - 28/04/2005

This example demonstrates how to interact with X-Plane by reading and writing
data.  This example creates menus items that change the nav-1 radio frequency.
"""

from XPLMDefs import *
from XPLMMenus import *
from XPLMDataAccess import *

class PythonInterface:
        def XPluginStart(self):
                self.Name = "SimData1"
                self.Sig =  "SandyBarbour.Python.SimData1"
                self.Desc = "A plugin that changes sim data."

                mySubMenuItem = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Sim Data 1", 0, 1)
                self.MyMenuHandlerCB = self.MyMenuHandlerCallback
                self.myMenu = XPLMCreateMenu(self, "Sim Data", XPLMFindPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB,    0)
                XPLMAppendMenuItem(self.myMenu, "Decrement Nav1", -1000, 1)
                XPLMAppendMenuItem(self.myMenu, "Increment Nav1", +1000, 1)
                self.DataRef = XPLMFindDataRef("sim/cockpit/radios/nav1_freq_hz")
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
                This is our handler for the menu item.  Our inItemRef is the refcon
                we registered in our XPLMAppendMenuItem calls.  It is either +1000 or
                -1000 depending on which menu item is picked.
                """
                if (self.DataRef != 0):
                        """
                        We read the data ref, add the increment and set it again.
                        This changes the nav frequency.
                        """
                        XPLMSetDatai(self.DataRef, XPLMGetDatai(self.DataRef) + inItemRef)
                pass
