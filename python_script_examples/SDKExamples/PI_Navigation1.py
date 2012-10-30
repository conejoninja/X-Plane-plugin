"""

Navigation.py

Ported to Python by Sandy Barbour - 28/04/2005

This example demonstrates how to use the FMC and the navigation databases in
X-Plane.
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMMenus import *
from XPLMUtilities import *
from XPLMNavigation import *
from XPLMDataAccess import *

nearestAirport = 1
programFMC = 2

class PythonInterface:
        def XPluginStart(self):
                global myMenu
                self.Name = "Navigation1"
                self.Sig =  "SandyBarbour.Python.Navigation1"
                self.Desc = "A plugin that controls the FMC."
                mySubMenuItem = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Navigation 1", 0, 1)
                self.MyMenuHandlerCB = self.MyMenuHandlerCallback
                self.myMenu = XPLMCreateMenu(self, "Navigation1", XPLMFindPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB,   0)
                XPLMAppendMenuItem(self.myMenu, "Say nearest airport", nearestAirport, 1)
                XPLMAppendMenuItem(self.myMenu, "Program FMC", programFMC, 1)
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
                if (inItemRef == nearestAirport):
                        # First find the plane's position.
                        lat = [XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/latitude"))]
                        lon = [XPLMGetDataf(XPLMFindDataRef("sim/flightmodel/position/longitude"))]
                        # Find the nearest airport to us.
                        ref = XPLMFindNavAid(None, None, lat[0], lon[0], None, xplm_Nav_Airport)
                        if (ref != XPLM_NAV_NOT_FOUND):
                                id = []
                                name = []
                                XPLMGetNavAidInfo(ref, None, lat, lon, None, None, None, id, name, None)
                                buf = "The nearest airport is %s, %s" % (str(id[0]), str(name[0]))
                                XPLMSpeakString(buf);
                                XPLMDebugString(buf);
                        else:
                                XPLMSpeakString("No airports were found!")
                                XPLMDebugString("No airports were found!\n");

                if (inItemRef == programFMC):
                        """
                        This code programs the flight management computer.  We simply set each entry to a navaid
                        that we find by searching by name or ID.
                        """
                        XPLMSetFMSEntryInfo(0, XPLMFindNavAid(None, "KBOS", None, None, None, xplm_Nav_Airport), 3000)
                        XPLMSetFMSEntryInfo(1, XPLMFindNavAid(None, "LUCOS", None, None, None, xplm_Nav_Fix), 20000)
                        XPLMSetFMSEntryInfo(2, XPLMFindNavAid(None, "SEY", None, None, None, xplm_Nav_VOR), 20000)
                        XPLMSetFMSEntryInfo(3, XPLMFindNavAid(None, "PARCH", None, None, None, xplm_Nav_Fix), 20000)
                        XPLMSetFMSEntryInfo(4, XPLMFindNavAid(None, "CCC", None, None, None, xplm_Nav_VOR), 12000)
                        XPLMSetFMSEntryInfo(5, XPLMFindNavAid(None, "ROBER", None, None, None, xplm_Nav_Fix), 9000)
                        XPLMSetFMSEntryInfo(6, XPLMFindNavAid(None, "KJFK", None, None, None, xplm_Nav_Airport), 3000)
                        XPLMClearFMSEntry(7)
                        XPLMClearFMSEntry(8)
                pass
