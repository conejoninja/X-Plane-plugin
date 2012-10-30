"""
TimedProcessing.c

Ported to Python by Sandy Barbour - 28/04/2005

This example plugin demonstrates how to use the timed processing callbacks
to continuously record sim data to disk.

This technique can be used to record data to disk or to the network.  Unlike
UDP data output, we can increase our frequency to capture data every single
sim frame.  (This example records once per second.)

Use the timed processing APIs to do any periodic or asynchronous action in
your plugin.
"""

from XPLMDefs import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *

class PythonInterface:
	def XPluginStart(self):
		global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl
		self.Name = "TimedProcessing1"
		self.Sig =  "SandyBarbour.Python.TimedProcessing1"
		self.Desc = "A plugin that records sim data."

		"""
		Open a file to write to.  We locate the X-System directory
		and then concatenate our file name.  This makes us save in
		the X-System directory.  Open the file.
		"""
		self.outputPath = XPLMGetSystemPath() + "timedprocessing1.txt"
		self.OutputFile = open(self.outputPath, 'w')

		""" Find the data refs we want to record."""
		self.PlaneLat = XPLMFindDataRef("sim/flightmodel/position/latitude")
		self.PlaneLon = XPLMFindDataRef("sim/flightmodel/position/longitude")
		self.PlaneEl = XPLMFindDataRef("sim/flightmodel/position/elevation")

		"""
		Register our callback for once a second.  Positive intervals
		are in seconds, negative are the negative of sim frames.  Zero
		registers but does not schedule a callback for time.
		"""
		self.FlightLoopCB = self.FlightLoopCallback
		XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 1.0, 0)
		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		# Unregister the callback
		XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)

		# Close the file
		self.OutputFile.close()
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		# The actual callback.  First we read the sim's time and the data.
		elapsed = XPLMGetElapsedTime()
		lat = XPLMGetDataf(self.PlaneLat)
		lon = XPLMGetDataf(self.PlaneLon)
		el = XPLMGetDataf(self.PlaneEl)

		# Write the data to a file.
		buf = "Time=%f, lat=%f,lon=%f,el=%f.\n" % (elapsed, lat, lon, el)
		self.OutputFile.write(buf)

		# Return 1.0 to indicate that we want to be called again in 1 second.
		return 1.0;
