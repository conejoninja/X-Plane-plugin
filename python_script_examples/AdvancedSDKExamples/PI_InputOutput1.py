"""
Input / Output example
Written by Sandy Barbour - 29/02/2004
Ported to Python by Sandy Barbour - 01/05/2005

This examples shows how to get input data from Xplane.
It also shows how to control Xplane by sending output data to it.

In this case it controls N1 depending on the throttle value.

It also shows the use of Menus and Widgets.
"""

from XPLMDefs import *
from XPLMUtilities import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMMenus import *
from XPWidgetDefs import *
from XPWidgets import *
from XPStandardWidgets import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "InputOutput1"
		self.Sig =  "SandyBarbour.Python.InputOutput1"
		self.Desc = "A plug-in that handles data Input/Output."

		self.MAX_NUMBER_ENGINES = 8
		self.MAX_INPUT_DATA_ITEMS = 2
		self.MAX_OUTPUT_DATA_ITEMS = 1

		# Use lists for the datarefs, makes it easier to add extra datarefs
		InputDataRefDescriptions = ["sim/flightmodel/engine/ENGN_thro", "sim/aircraft/engine/acf_num_engines"]
		OutputDataRefDescriptions = ["sim/flightmodel/engine/ENGN_N1_"]
		self.DataRefDesc = ["1", "2", "3", "4", "5", "6", "7", "8"]

		# Create our menu
		Item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - Input/Output 1", 0, 1)
		self.InputOutputMenuHandlerCB = self.InputOutputMenuHandler
		self.Id = XPLMCreateMenu(self, "Input/Output 1", XPLMFindPluginsMenu(), Item, self.InputOutputMenuHandlerCB, 0)
		XPLMAppendMenuItem(self.Id, "Data", 1, 1)

		# Flag to tell us if the widget is being displayed.
		self.MenuItem1 = 0

		# Get our dataref handles here
		self.InputDataRef = []
		for Item in range(self.MAX_INPUT_DATA_ITEMS):
			self.InputDataRef.append(XPLMFindDataRef(InputDataRefDescriptions[Item]))

		self.OutputDataRef = []
		for Item in range(self.MAX_OUTPUT_DATA_ITEMS):
			self.OutputDataRef.append(XPLMFindDataRef(OutputDataRefDescriptions[Item]))

		# Register our FL callbadk with initial callback freq of 1 second
		self.InputOutputLoopCB = self.InputOutputLoopCallback
		XPLMRegisterFlightLoopCallback(self, self.InputOutputLoopCB, 1.0, 0)

		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		# Unregister the callback
		XPLMUnregisterFlightLoopCallback(self, self.InputOutputLoopCB, 0)

		if (self.MenuItem1 == 1):
			XPDestroyWidget(self, self.InputOutputWidget, 1)
			self.MenuItem1 = 0

		XPLMDestroyMenu(self, self.Id)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def InputOutputLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		if (self.MenuItem1 == 0): # Don't process if widget not visible
			return 1.0

		# Only deal with the actual engines that we have
		self.NumberOfEngines = XPLMGetDatai(self.InputDataRef[1])

		# Get our throttle positions for each engine
		self.Throttle = []
		count = XPLMGetDatavf(self.InputDataRef[0], self.Throttle, 0, self.NumberOfEngines)

		# Get our current N1 for each engine
		self.CurrentN1 = []
		count = XPLMGetDatavf(self.OutputDataRef[0], self.CurrentN1, 0, self.NumberOfEngines)

		for Item in range(self.MAX_NUMBER_ENGINES):
			XPSetWidgetDescriptor(self.InputEdit[Item], "")
			XPSetWidgetDescriptor(self.OutputEdit[Item], "")

		# Process each engine
		self.NewN1 = []
		for Item in range(self.NumberOfEngines):
			# Default to New = Current
			self.NewN1.append(self.CurrentN1[Item])

			"""
			Special processing can go here depending on input value
			For this example just limit N1 to 80% if throttle > 50%
			"""
			if (self.Throttle[Item] > 0.5):
				if (self.CurrentN1[Item] > 80.0):
					self.NewN1[Item] = 80.0

			# This updates the first widget column with the throttle values
			XPSetWidgetDescriptor(self.InputEdit[Item], str(self.Throttle[Item]))

			# This updates the second widget column with the N1 values
			XPSetWidgetDescriptor(self.OutputEdit[Item], str(self.NewN1[Item]))

		# Set the new N1 values for each engine
		XPLMSetDatavf(self.OutputDataRef[0], self.NewN1, 0, self.NumberOfEngines)

		# This means call us ever 10ms.
		return 1.0

	def InputOutputMenuHandler(self, inMenuRef, inItemRef):
		# If menu selected create our widget dialog
		if (inItemRef == 1):
			if (self.MenuItem1 == 0):
				self.CreateInputOutputWidget(300, 550, 350, 350)
				self.MenuItem1 = 1
			else:
				if(not XPIsWidgetVisible(self.InputOutputWidget)):
					XPShowWidget(self.InputOutputWidget)
		pass

	"""
	This will create our widget dialog.
	I have made all child widgets relative to the input paramter.
	This makes it easy to position the dialog
	"""
	def CreateInputOutputWidget(self, x, y, w, h):
		x2 = x + w
		y2 = y - h

		# Create the Main Widget window
		self.InputOutputWidget = XPCreateWidget(x, y, x2, y2, 1, "Python - Input/Output Example 1 by Sandy Barbour", 1,	0, xpWidgetClass_MainWindow)

		# Add Close Box decorations to the Main Widget
		XPSetWidgetProperty(self.InputOutputWidget, xpProperty_MainWindowHasCloseBoxes, 1)

		# Create the Sub Widget window
		InputOutputWindow = XPCreateWidget(x+50, y-50, x2-50, y2+50, 1,	"",	0, self.InputOutputWidget, xpWidgetClass_SubWindow)

		# Set the style to sub window
		XPSetWidgetProperty(InputOutputWindow, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)

		# For each engine
		InputText = []
		self.InputEdit = []
		self.OutputEdit = []
		for Item in range(self.MAX_NUMBER_ENGINES):
			# Create a text widget
			InputText.append(XPCreateWidget(x+60, y-(60 + (Item*30)), x+90, y-(82 + (Item*30)), 1,	self.DataRefDesc[Item],  0, self.InputOutputWidget, xpWidgetClass_Caption))

			# Create an edit widget for the throttle value
			self.InputEdit.append(XPCreateWidget(x+100, y-(60 + (Item*30)), x+180, y-(82 + (Item*30)), 1, "", 0, self.InputOutputWidget,	xpWidgetClass_TextField))

			# Set it to be text entry
			XPSetWidgetProperty(self.InputEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

			# Create an edit widget for the N1 value
			self.OutputEdit.append(XPCreateWidget(x+190, y-(60 + (Item*30)), x+270, y-(82 + (Item*30)),	1, "", 0, self.InputOutputWidget, xpWidgetClass_TextField))

			# Set it to be text entry
			XPSetWidgetProperty(self.OutputEdit[Item], xpProperty_TextFieldType, xpTextEntryField)

		# Register our widget handler
		self.InputOutputHandlerCB = self.InputOutputHandler
		XPAddWidgetCallback(self, self.InputOutputWidget, self.InputOutputHandlerCB)
		pass

	def InputOutputHandler(self, inMessage, inWidget,	inParam1, inParam2):
		if (inMessage == xpMessage_CloseButtonPushed):
			if (self.MenuItem1 == 1):
				XPHideWidget(self.InputOutputWidget)
			return 1

		return 0
		pass
