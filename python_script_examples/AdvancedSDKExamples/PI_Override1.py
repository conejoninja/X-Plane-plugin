"""
Override Example

Written by Sandy Barbour - 26/05/2004

Ported to Python by Sandy Barbour - 11/05/2005

This examples shows how to apply various overrides.
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
		self.Name = "Override"
		self.Sig =  "SandyBarbour.Python.Override"
		self.Desc = "A plug-in that Overrides Xplane."

		self.NumberOfOverrides = 20
		self.MenuItem1 = 0

		self.DataRefGroup = "sim/operation/override/"
		self.DataRefDesc  = ["override_planepath", "override_joystick", "override_artstab",
						"override_flightcontrol", "override_gearbrake", "override_navneedles",
						"override_adf", "override_dme", "override_gps", "override_flightdir", "override_annunciators",
						"override_autopilot","override_pfc_autopilot_lites",
						"override_joystick_heading", "override_joystick_pitch",
						"override_joystick_roll", "override_throttles",
						"override_groundplane", "disable_cockpit_object", "disable_twosided_fuselage"]

		# Create our menu
		Item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Override Xplane 1", 0, 1)
		self.OverrideMenuHandlerCB = self.OverrideMenuHandler
		self.Id = XPLMCreateMenu(self, "Override", XPLMFindPluginsMenu(), Item, self.OverrideMenuHandlerCB,	0)
		XPLMAppendMenuItem(self.Id, "Enable/Disable Override", 1, 1)

		# Flag to tell us if the widget is being displayed.
		self.MenuItem1 = 0

		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		if (self.MenuItem1 == 1):
			XPDestroyWidget(self, self.OverrideWidget, 1)
			self.MenuItem1 = 0

		XPLMDestroyMenu(self, self.Id)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def OverrideMenuHandler(self, inMenuRef, inItemRef):
		# If menu selected create our widget dialog
		if (inItemRef == 1):
			if (self.MenuItem1 == 0):
				self.OverrideScreenNumber = 0
				self.CreateOverride(300, 550, 350, 380)
				self.MenuItem1 = 1
			else:
				if(not XPIsWidgetVisible(self.OverrideWidget)):
					XPShowWidget(self.OverrideWidget)
		pass

	"""
	This will create our widget dialog.
	I have made all child widgets relative to the input paramter.
	This makes it easy to position the dialog
	"""
	def CreateOverride(self, x, y, w, h):
		x2 = x + w
		y2 = y - h
		WindowCentre = int(x+w/2)

		self.GetDataRefIds()

		self.OverrideWidget = XPCreateWidget(x, y, x2, y2,
						1, "Python - Xplane Override 1", 1, 0,
						xpWidgetClass_MainWindow)

		XPSetWidgetProperty(self.OverrideWidget, xpProperty_MainWindowHasCloseBoxes, 1)

		self.OverridePanel = XPCreateWidget(x+50, y-50, x2-50, y2+50,
						1, "", 0, self.OverrideWidget,
						xpWidgetClass_SubWindow)

		XPSetWidgetProperty(self.OverridePanel, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)


		self.OverridePreviousButton = XPCreateWidget(WindowCentre-80, y2+24, WindowCentre-10, y2+2,
						1, "Previous", 0, self.OverrideWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.OverridePreviousButton, xpProperty_ButtonType, xpPushButton)

		self.OverrideNextButton = XPCreateWidget(WindowCentre+10, y2+24, WindowCentre+80, y2+2,
						1, "Next", 0, self.OverrideWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.OverrideNextButton, xpProperty_ButtonType, xpPushButton)

		self.OverrideEdit = []
		for Item in range(8):
			yOffset = (45+28+(Item*30))
			self.OverrideEdit.append(XPCreateWidget(x+60, y-yOffset, x+60+200, y-yOffset-20,
						1, "", 0, self.OverrideWidget,
						xpWidgetClass_TextField))
			XPSetWidgetProperty(self.OverrideEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

		self.OverrideCheckBox = []
		for Item in range(8):
			yOffset = (45+28+(Item*30))
			self.OverrideCheckBox.append(XPCreateWidget(x+260, y-yOffset, x+260+22, y-yOffset-20,
						1, "", 0, self.OverrideWidget,
						xpWidgetClass_Button))

			XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonType, xpRadioButton)
			XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox)
			XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonState, 1)

		self.RefreshOverride()

		self.OverrideHandlerCB = self.OverrideHandler
		XPAddWidgetCallback(self, self.OverrideWidget, self.OverrideHandlerCB)

		pass

	def OverrideHandler(self, inMessage, inWidget,	inParam1, inParam2):
		if (inMessage == xpMessage_CloseButtonPushed):
			if (self.MenuItem1 == 1):
				XPHideWidget(self.OverrideWidget)
			return 1

		if (inMessage == xpMsg_PushButtonPressed):

			if (inParam1 == self.OverridePreviousButton):
				self.OverrideScreenNumber-=1
				if (self.OverrideScreenNumber<0):
					self.OverrideScreenNumber = 0
				self.RefreshOverride()
				return 1

			if (inParam1 == self.OverrideNextButton):
				self.OverrideScreenNumber+=1
				if (self.OverrideScreenNumber>self.MaxScreenNumber):
					self.OverrideScreenNumber = self.MaxScreenNumber
				self.RefreshOverride()
				return 1

		if (inMessage == xpMsg_ButtonStateChanged):
			for Item in range(8):
				if (Item+(self.OverrideScreenNumber*8) < self.NumberOfOverrides):
					if (self.DataRefID[Item+(self.OverrideScreenNumber*8)]):
						State = XPGetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonState, 0)
						self.SetDataRefState(self.DataRefID[Item+(self.OverrideScreenNumber*8)], State)
			return 1

		return 0

	def RefreshOverride(self):

		for Item in range(8):
			if ((Item+(self.OverrideScreenNumber*8)) < self.NumberOfOverrides):
				if (self.DataRefID[Item+(self.OverrideScreenNumber*8)]):
					XPSetWidgetDescriptor(self.OverrideEdit[Item], self.DataRefDesc[Item+(self.OverrideScreenNumber*8)])
					if (self.GetDataRefState(self.DataRefID[Item+(self.OverrideScreenNumber*8)])):
						XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonState, 1)
					else:
						XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonState, 0)
					XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_Enabled, 1)
			else:
				XPSetWidgetDescriptor(self.OverrideEdit[Item], "")
				XPSetWidgetProperty(self.OverrideCheckBox[Item], xpProperty_ButtonState, 0)

		if (self.OverrideScreenNumber == 0):
			XPSetWidgetProperty(self.OverridePreviousButton, xpProperty_Enabled, 0)
		else:
			XPSetWidgetProperty(self.OverridePreviousButton, xpProperty_Enabled, 1)
			XPSetWidgetDescriptor(self.OverridePreviousButton, "Previous")

		if (self.OverrideScreenNumber == self.MaxScreenNumber):
			XPSetWidgetProperty(self.OverrideNextButton, xpProperty_Enabled, 0)
		else:
			XPSetWidgetProperty(self.OverrideNextButton, xpProperty_Enabled, 1)
			XPSetWidgetDescriptor(self.OverrideNextButton, "Next")

		pass

	def GetDataRefIds(self):
		self.DataRefID = []
		for Item in range(self.NumberOfOverrides):
			TempDataRefID = XPLMFindDataRef(self.DataRefGroup + str(self.DataRefDesc[Item]))
			if (Item == 0):
				self.SpecialDataRef = TempDataRefID
			self.DataRefID.append(TempDataRefID)

		self.MaxScreenNumber = (self.NumberOfOverrides-1) / 8

		pass

	def GetDataRefState(self, DataRefID):
		if (DataRefID == self.SpecialDataRef):
			self.IntVals = []
			XPLMGetDatavi(DataRefID, self.IntVals, 0, 8)
			DataRefi = self.IntVals[0]
		else:
			DataRefi = XPLMGetDatai(DataRefID)

		return DataRefi

	def SetDataRefState(self, DataRefID, State):
		if (DataRefID == self.SpecialDataRef):
			IntVals = [State, 0, 0, 0, 0, 0, 0, 0]
			XPLMSetDatavi(DataRefID, IntVals, 0, 8)
		else:
			XPLMSetDatai(DataRefID, State)

		pass
