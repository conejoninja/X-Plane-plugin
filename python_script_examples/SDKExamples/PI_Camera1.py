"""
Camera.py

Ported to Python by Sandy Barbour - 28/04/2005

This plugin registers a new view with the sim that orbits the aircraft.  We do this by:

1. Registering a hotkey to engage the view.
2. Setting the view to external when we are engaged.
3. Registering a new camera control funcioin that ends when a new view is picked.
"""

import math
from XPLMDefs import *
from XPLMDisplay import *
from XPLMUtilities import *
from XPLMCamera import *
from XPLMDataAccess import *
from XPLMDisplay import *
from SandyBarbourUtilities import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "Camera1"
		self.Sig =  "SandyBarbour.Python.Camera1"
		self.Desc = "An example using the camera module."

		# Prefetch the sim variables we will use.
		self.PlaneX = XPLMFindDataRef("sim/flightmodel/position/local_x");
		self.PlaneY = XPLMFindDataRef("sim/flightmodel/position/local_y");
		self.PlaneZ = XPLMFindDataRef("sim/flightmodel/position/local_z");

		# Register our hot key for the new view.
		self.MyHotKeyCB = self.MyHotKeyCallback
		self.HotKey = XPLMRegisterHotKey(self, XPLM_VK_F8, xplm_DownFlag, "Circling External View 1", self.MyHotKeyCB, 0)
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
		This is the hotkey callback.  First we simulate a joystick press and
		release to put us in 'free view 1'.  This guarantees that no panels
		are showing and we are an external view.
		"""
		XPLMCommandButtonPress(xplm_joy_v_fr1)
		XPLMCommandButtonRelease(xplm_joy_v_fr1)

		# Now we control the camera until the view changes.
		self.MyOrbitPlaneFuncCB = self.MyOrbitPlaneFunc
		XPLMControlCamera(self, xplm_ControlCameraUntilViewChanges, self.MyOrbitPlaneFuncCB, 0)
		pass

	"""
	MyOrbitPlaneFunc

	This is the actual camera control function, the real worker of the plugin.  It is
	called each time X-Plane needs to draw a frame.
	"""
	def	MyOrbitPlaneFunc(self, outCameraPosition, inIsLosingControl, inRefcon):
		if (inIsLosingControl):
			XPLMDontControlCamera(self)

		if (outCameraPosition and not inIsLosingControl):
			SandyBarbourClearDisplay()
			SandyBarbourDisplay("Python CameraCallback 1 Start")
			SandyBarbourDisplay("outCameraPosition :- "+ str(outCameraPosition))
			SandyBarbourDisplay("inIsLosingControl :- "+ str(inIsLosingControl))
			SandyBarbourDisplay("inRefcon :- "+ str(inRefcon))
			SandyBarbourDisplay("x       :- "+ str(outCameraPosition[0]))
			SandyBarbourDisplay("y       :- "+ str(outCameraPosition[1]))
			SandyBarbourDisplay("z       :- "+ str(outCameraPosition[2]))
			SandyBarbourDisplay("pitch   :- "+ str(outCameraPosition[3]))
			SandyBarbourDisplay("heading :- "+ str(outCameraPosition[4]))
			SandyBarbourDisplay("roll    :- "+ str(outCameraPosition[5]))
			SandyBarbourDisplay("zoom    :- "+ str(outCameraPosition[6]))
			"""
			First get the screen size and mouse location.  We will use this to decide
			what part of the orbit we are in.  The mouse will move us up-down and around.
			"""
			w = []; h = []; x = []; y = []
			XPLMGetScreenSize(w, h)
			XPLMGetMouseLocation(x, y)
			heading = 360.0 * float(x[0]) / float(w[0])
			pitch = 20.0 * ((float(y[0])/float(h[0]) * 2.0) - 1.0)

			"""
			Now calculate where the camera should be positioned to be 200
			meters from the plane and pointing at the plane at the pitch and
			heading we wanted above.
			"""
			dx = -200.0 * math.sin(heading * 3.1415 / 180.0)
			dz = 200.0 * math.cos(heading * 3.1415 / 180.0)
			dy = -200 * math.tan(pitch * 3.1415 / 180.0)
			SandyBarbourDisplay("dx    :- "+ str(dx))
			SandyBarbourDisplay("dy    :- "+ str(dy))
			SandyBarbourDisplay("dz    :- "+ str(dz))

			# Fill out the camera position info.
			outCameraPosition[0] = XPLMGetDataf(self.PlaneX) + dx;
			outCameraPosition[1] = XPLMGetDataf(self.PlaneY) + dy;
			outCameraPosition[2] = XPLMGetDataf(self.PlaneZ) + dz;
			outCameraPosition[3] = pitch;
			outCameraPosition[4] = heading;
			outCameraPosition[5] = 0;
		return 1
