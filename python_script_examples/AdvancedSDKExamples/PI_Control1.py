"""
Control Example

Written by Sandy Barbour - 26/05/2004

Ported to Python by Sandy Barbour - 10/05/2005

This examples shows how to move the aircraft control surfaces.
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
		self.Name = "Control1"
		self.Sig =  "SandyBarbour.Python.Control1"
		self.Desc = "A plug-in that move the control surfaces."
		self.MAX_ITEMS = 12
		# Use lists for the datarefs, makes it easier to add extra datarefs
		DataRefString = ["sim/joystick/yolk_pitch_ratio", "sim/joystick/yolk_roll_ratio", "sim/joystick/yolk_heading_ratio",
						"sim/joystick/artstab_pitch_ratio", "sim/joystick/artstab_roll_ratio", "sim/joystick/artstab_heading_ratio",
						"sim/joystick/FC_ptch", "sim/joystick/FC_roll", "sim/joystick/FC_hdng",
						"sim/flightmodel/weight/m_fuel1", "sim/flightmodel/weight/m_fuel2", "sim/flightmodel/weight/m_fuel3"]

		self.DataRefDesc = ["Yolk Pitch", "Yolk Roll", "Yolk Heading", "AS Pitch", "AS Roll", "AS Heading", "FC Pitch", "FC Roll", "FC Heading", "Fuel 1", "Fuel 2", "Fuel 3"]

		self.IncrementValue = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 10.0, 10.0, 10.0]

		# Create our menu
		Item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Control 1", 0, 1)
		self.ControMenuHandlerCB = self.ControMenuHandler
		self.Id = XPLMCreateMenu(self, "Control1", XPLMFindPluginsMenu(), Item, self.ControMenuHandlerCB,	0)
		XPLMAppendMenuItem(self.Id, "Control1", 1, 1)

		# Flag to tell us if the widget is being displayed.
		self.MenuItem1 = 0

		# Get our dataref handles here
		self.ControlDataRef = []
		for self.Item in range(self.MAX_ITEMS):
			self.ControlDataRef.append(XPLMFindDataRef(DataRefString[self.Item]))

		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		if (self.MenuItem1 == 1):
			XPDestroyWidget(self, self.ControlWidget, 1)
			MenuItem1 = 0

		XPLMDestroyMenu(self, self.Id)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def ControMenuHandler(self, inMenuRef, inItemRef):
		# If menu selected create our widget dialog
		if (inItemRef == 1):
			if (self.MenuItem1 == 0):
				self.CreateControl(300, 550, 350, 530)
				self.MenuItem1 = 1
			else:
				if(not XPIsWidgetVisible(self.ControlWidget)):
					XPShowWidget(self.ControlWidget)
		pass

	"""
	This will create our widget dialog.
	I have made all child widgets relative to the input paramter.
	This makes it easy to position the dialog
	"""
	def CreateControl(self, x, y, w, h):

		FloatValue = []
		for self.Item in range(self.MAX_ITEMS):
			FloatValue.append(XPLMGetDataf(self.ControlDataRef[self.Item]))

		x2 = x + w
		y2 = y - h

		# Create the Main Widget window
		self.ControlWidget = XPCreateWidget(x, y, x2, y2, 1, "Python - Control 1 Example by Sandy Barbour", 1,	0, xpWidgetClass_MainWindow)

		# Add Close Box decorations to the Main Widget
		XPSetWidgetProperty(self.ControlWidget, xpProperty_MainWindowHasCloseBoxes, 1)

		# Create the Sub Widget window
		ControlWindow = XPCreateWidget(x+50, y-50, x2-50, y2+50, 1,	"",	0, self.ControlWidget, xpWidgetClass_SubWindow)

		# Set the style to sub window
		XPSetWidgetProperty(ControlWindow, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)

		ControlText = []
		self.ControlEdit = []
		self.UpArrow = []
		self.DownArrow = []

		for Item in range(self.MAX_ITEMS):

			ControlText.append(XPCreateWidget(x+60, y-(70 + (Item*30)), x+115, y-(92 + (Item*30)),
								1,					   	# Visible
								self.DataRefDesc[Item],	# desc
								0,					   	# root
								self.ControlWidget,
								xpWidgetClass_Caption))

			buffer = "%f" % (FloatValue[Item])
			self.ControlEdit.append(XPCreateWidget(x+160, y-(70 + (Item*30)), x+250, y-(92 + (Item*30)),
								1, buffer, 0, self.ControlWidget,
								xpWidgetClass_TextField))

			XPSetWidgetProperty(self.ControlEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

			self.UpArrow.append(XPCreateWidget(x+252, y-(66 + (Item*30)), x+264, y-(81 + (Item*30)),
								1, "", 0, self.ControlWidget,
								xpWidgetClass_Button))

			XPSetWidgetProperty(self.UpArrow[Item], xpProperty_ButtonType, xpLittleUpArrow)

			self.DownArrow.append(XPCreateWidget(x+252, y-(81 + (Item*30)), x+264, y-(96 + (Item*30)),
								1, "", 0, self.ControlWidget,
								xpWidgetClass_Button))

			XPSetWidgetProperty(self.DownArrow[Item], xpProperty_ButtonType, xpLittleDownArrow)

		self.ControlApplyButton = XPCreateWidget(x+120, y-440, x+210, y-462,
						1, "Apply Data", 0, self.ControlWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.ControlApplyButton, xpProperty_ButtonType, xpPushButton);

		# Register our widget handler
		self.ControlHandlerCB = self.ControlHandler
		XPAddWidgetCallback(self, self.ControlWidget, self.ControlHandlerCB)
		pass

	def ControlHandler(self, inMessage, inWidget,	inParam1, inParam2):

		FloatValue = []

		for Item in range(self.MAX_ITEMS):
			FloatValue.append( XPLMGetDataf(self.ControlDataRef[Item]))

		if (inMessage == xpMessage_CloseButtonPushed):
			if (self.MenuItem1 == 1):
				XPHideWidget(self.ControlWidget)
			return 1

		if (inMessage == xpMsg_PushButtonPressed):

			if (inParam1 == self.ControlApplyButton):
				self.ApplyValues()
				return 1

			for Item in range(self.MAX_ITEMS):
				if (inParam1 == self.UpArrow[Item]):
					FloatValue[Item] += self.IncrementValue[Item]
					buffer = "%f" % (FloatValue[Item])
					XPSetWidgetDescriptor(self.ControlEdit[Item], buffer)
					XPLMSetDataf(self.ControlDataRef[Item], FloatValue[Item])
					return 1

			for Item in range(self.MAX_ITEMS):
				if (inParam1 == self.DownArrow[Item]):
					FloatValue[Item] -= self.IncrementValue[Item];
					buffer = "%f" % (FloatValue[Item])
					XPSetWidgetDescriptor(self.ControlEdit[Item], buffer);
					XPLMSetDataf(self.ControlDataRef[Item], FloatValue[Item]);
					return 1;

		return 0

	def ApplyValues(self):
		for Item in range(self.MAX_ITEMS):
			buffer = []
			XPGetWidgetDescriptor(self.ControlEdit[Item], buffer, 512)
			XPLMSetDataf(self.ControlDataRef[Item], float(buffer[0]))

		pass
