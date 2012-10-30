"""
Position Example

Written by Sandy Barbour - 26/05/2004

Ported to Python by Sandy Barbour - 10/05/2005

This examples shows how to change the aircraft attitude.
Should be used with the override plugin.
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMMenus import *
from XPLMUtilities import *
from XPWidgetDefs import *
from XPWidgets import *
from XPStandardWidgets import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "Position1"
		self.Sig =  "SandyBarbour.Python.Position1"
		self.Desc = "A plug-in that changes the aircraft attitude."

		self.MAX_ITEMS = 11

		# Use lists for the datarefs, makes it easier to add extra datarefs
		self.DataRefString = ["sim/flightmodel/position/local_x", "sim/flightmodel/position/local_y", "sim/flightmodel/position/local_z",
										"sim/flightmodel/position/lat_ref", "sim/flightmodel/position/lon_ref",	"sim/flightmodel/position/theta",
										"sim/flightmodel/position/phi", "sim/flightmodel/position/psi",
										"sim/flightmodel/position/latitude", "sim/flightmodel/position/longitude", "sim/flightmodel/position/elevation"]

		self.DataRefDesc = ["Local x", "Local y", "Local z", "Lat Ref", "Lon Ref", "Theta", "Phi", "Psi"]
		self.Description = ["Latitude", "Longitude", "Elevation"]

		# Create our menu
		Item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Position 1", 0, 1)
		self.PositionMenuHandlerCB = self.PositionMenuHandler
		self.Id = XPLMCreateMenu(self, "Position1", XPLMFindPluginsMenu(), Item, self.PositionMenuHandlerCB, 0)
		XPLMAppendMenuItem(self.Id, "Position1", 1, 1)

		# Flag to tell us if the widget is being displayed.
		self.MenuItem1 = 0

		# Get our dataref handles here
		self.PositionDataRef = []
		for Item in range(self.MAX_ITEMS):
			self.PositionDataRef.append(XPLMFindDataRef(self.DataRefString[Item]))

		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		if (self.MenuItem1 == 1):
			XPDestroyWidget(self, self.PositionWidget, 1)
			self.MenuItem1 = 0

		XPLMDestroyMenu(self, self.Id)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def PositionMenuHandler(self, inMenuRef, inItemRef):
		# If menu selected create our widget dialog
		if (inItemRef == 1):
			if (self.MenuItem1 == 0):
				self.CreatePosition(300, 600, 300, 550)
				self.MenuItem1 = 1
			else:
				if(not XPIsWidgetVisible(self.PositionWidget)):
					XPShowWidget(self.PositionWidget)
		pass

	"""
	This will create our widget dialog.
	I have made all child widgets relative to the input paramter.
	This makes it easy to position the dialog
	"""
	def CreatePosition(self, x, y, w, h):
		FloatValue = []
		for Item in range(self.MAX_ITEMS):
			FloatValue.append(XPLMGetDataf(self.PositionDataRef[Item]))

		# X, Y, Z, Lat, Lon, Alt
		DoubleValue = [0.0, 0.0, 0.0]
		DoubleValue[0], DoubleValue[1], DoubleValue[2] = XPLMLocalToWorld(FloatValue[0], FloatValue[1], FloatValue[2])
		DoubleValue[2] *= 3.28

		x2 = x + w
		y2 = y - h
		PositionText = []

		# Create the Main Widget window
		self.PositionWidget = XPCreateWidget(x, y, x2, y2, 1, "Python - Position Example 1 by Sandy Barbour", 1,	0, xpWidgetClass_MainWindow)

		# Add Close Box decorations to the Main Widget
		XPSetWidgetProperty(self.PositionWidget, xpProperty_MainWindowHasCloseBoxes, 1)

		# Create the Sub Widget window
		PositionWindow = XPCreateWidget(x+50, y-50, x2-50, y2+50, 1,	"",	0, self.PositionWidget, xpWidgetClass_SubWindow)

		# Set the style to sub window
		XPSetWidgetProperty(PositionWindow, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)


		self.PositionEdit = []
		self.UpArrow = []
		self.DownArrow = []
		self.Position2Edit = []

		for Item in range(self.MAX_ITEMS-3):

			PositionText.append(XPCreateWidget(x+60, y-(70 + (Item*30)), x+115, y-(92 + (Item*30)),
								1,				 		# Visible
								self.DataRefDesc[Item],	# desc
								0,				 		# root
								self.PositionWidget,
								xpWidgetClass_Caption))

			buffer = "%f" % (FloatValue[Item])
			self.PositionEdit.append(XPCreateWidget(x+120, y-(70 + (Item*30)), x+210, y-(92 + (Item*30)),
								1, buffer, 0, self.PositionWidget,
								xpWidgetClass_TextField))

			XPSetWidgetProperty(self.PositionEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

			self.UpArrow.append(XPCreateWidget(x+212, y-(66 + (Item*30)), x+224, y-(81 + (Item*30)),
								1, "", 0, self.PositionWidget,
								xpWidgetClass_Button))

			XPSetWidgetProperty(self.UpArrow[Item], xpProperty_ButtonType, xpLittleUpArrow)

			self.DownArrow.append(XPCreateWidget(x+212, y-(81 + (Item*30)), x+224, y-(96 + (Item*30)),
								1, "", 0, self.PositionWidget,
								xpWidgetClass_Button))

			XPSetWidgetProperty(self.DownArrow[Item], xpProperty_ButtonType, xpLittleDownArrow)

		self.PositionApplyButton = XPCreateWidget(x+50, y-310, x+140, y-332,
						1, "Apply Data", 0, self.PositionWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.PositionApplyButton, xpProperty_ButtonType, xpPushButton)

		self.LatLonRefApplyButton = XPCreateWidget(x+145, y-310, x+240, y-332,
						1, "Apply LatLonRef", 0, self.PositionWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.LatLonRefApplyButton, xpProperty_ButtonType, xpPushButton)

		Position2Text = []
		for Item in range(3):

			Position2Text.append(XPCreateWidget(x+60, y-(350 + (Item*30)), x+115, y-(372 + (Item*30)),
								1,				 		# Visible
								self.Description[Item],	# desc
								0,				 		# root
								self.PositionWidget,
								xpWidgetClass_Caption))

			buffer = "%lf" % (DoubleValue[Item])
			self.Position2Edit.append(XPCreateWidget(x+120, y-(350 + (Item*30)), x+210, y-(372 + (Item*30)),
								1, buffer, 0, self.PositionWidget,
								xpWidgetClass_TextField))

			XPSetWidgetProperty(self.PositionEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

		self.LatLonAltApplyButton = XPCreateWidget(x+70, y-440, x+220, y-462,
							1, "Apply LatLonAlt", 0, self.PositionWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.LatLonAltApplyButton, xpProperty_ButtonType, xpPushButton)

		self.ReloadSceneryButton = XPCreateWidget(x+70, y-465, x+220, y-487,
							1, "Reload Scenery", 0, self.PositionWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.ReloadSceneryButton, xpProperty_ButtonType, xpPushButton)

		# Register our widget handler
		self.PositionHandlerCB = self.PositionHandler
		XPAddWidgetCallback(self, self.PositionWidget, self.PositionHandlerCB)
		pass

	def PositionHandler(self, inMessage, inWidget,	inParam1, inParam2):

		FloatValue = []

		for Item in range(self.MAX_ITEMS):
			FloatValue.append( XPLMGetDataf(self.PositionDataRef[Item]))

		if (inMessage == xpMessage_CloseButtonPushed):
			if (self.MenuItem1 == 1):
				XPHideWidget(self.PositionWidget)
			return 1

		if (inMessage == xpMsg_PushButtonPressed):

			if (inParam1 == self.PositionApplyButton):
				self.ApplyValues()
				return 1

			if (inParam1 == self.LatLonRefApplyButton):
				self.ApplyLatLonRefValues()
				return 1

			if (inParam1 == self.LatLonAltApplyButton):
				self.ApplyLatLonAltValues()
				return 1

			if (inParam1 == self.ReloadSceneryButton):
				XPLMReloadScenery()
				return 1

			for Item in range(self.MAX_ITEMS-3):
				if (inParam1 == self.UpArrow[Item]):
					FloatValue[Item] += 1.0
					buffer = "%f" % (FloatValue[Item])
					XPSetWidgetDescriptor(self.PositionEdit[Item], buffer)
					XPLMSetDataf(self.PositionDataRef[Item], FloatValue[Item])
					return 1

			for Item in range(self.MAX_ITEMS-3):
				if (inParam1 == self.DownArrow[Item]):
					FloatValue[Item] -= 1.0
					buffer = "%f" % (FloatValue[Item])
					XPSetWidgetDescriptor(self.PositionEdit[Item], buffer)
					XPLMSetDataf(self.PositionDataRef[Item], FloatValue[Item])
					return 1

		return 0

	def ApplyValues(self):
		for Item in range(self.MAX_ITEMS-3):
			buffer = []
			XPGetWidgetDescriptor(self.PositionEdit[Item], buffer, 512)
			XPLMSetDataf(self.PositionDataRef[Item], float(buffer[0]))

		pass

	def ApplyLatLonRefValues(self):
		buffer = []
		XPGetWidgetDescriptor(self.PositionEdit[3], buffer, 512)
		FloatValue = float(buffer[0])
		XPLMSetDataf(self.PositionDataRef[3], FloatValue)

		buffer = []
		XPGetWidgetDescriptor(self.PositionEdit[4], buffer, 512)
		FloatValue = float(buffer[0])
		XPLMSetDataf(self.PositionDataRef[4], FloatValue)

		pass

	def ApplyLatLonAltValues(self):
		# This gets the lat/lon/alt from the widget text fields
		FloatValue = [0.0, 0.0, 0.0]
		for Item in range(3):
			buffer = []
			XPGetWidgetDescriptor(self.Position2Edit[Item], buffer, 512)
			FloatValue[Item] = float(buffer[0])

		# Lat, Lon, Alt, X, Y, Z
		DoubleValue = [0.0, 0.0, 0.0]
		DoubleValue[0], DoubleValue[1], DoubleValue[2] = XPLMWorldToLocal(FloatValue[0], FloatValue[1], FloatValue[2] / 3.28)

		for Item in range(3):
			# This writes out the lat/lon/alt from the widget text fields back to the datarefs
			XPLMSetDataf(self.PositionDataRef[Item+8], FloatValue[Item])
			# This writes out the x,y,z datarefs after conversion from lat/lon/alt back to the datarefs
			XPLMSetDataf(self.PositionDataRef[Item], DoubleValue[Item])

		self.ApplyLatLonRefValues()

		pass

