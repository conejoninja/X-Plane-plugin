"""
FMSUtility example

Written by Sandy Barbour - 21/01/2005
Ported to Python by Sandy Barbour - 04/05/2005

This examples shows how to access the FMS.
"""

from XPLMDefs import *
from XPLMMenus import *
from XPLMNavigation import *
from XPWidgetDefs import *
from XPWidgets import *
from XPStandardWidgets import *

class PythonInterface:
	def XPluginStart(self):
		self.Name = "FMSUtility1"
		self.Sig =  "SandyBarbour.Python.FMSUtility1"
		self.Desc = "A plug-in that accesses the FMS."

		self.MAX_NAV_TYPES = 13
		self.MenuItem1 = 0
		self.NavTypeLinePosition = 0

		self.NavTypeLookup = [["Unknown",		xplm_Nav_Unknown],
        			         ["Airport",		xplm_Nav_Airport],
            	    		 ["NDB",			xplm_Nav_NDB],
			    	         ["VOR",			xplm_Nav_VOR],
        		    	     ["ILS",			xplm_Nav_ILS],
		                	 ["Localizer",		xplm_Nav_Localizer],
	        		         ["Glide Slope",	xplm_Nav_GlideSlope],
			                 ["Outer Marker",	xplm_Nav_OuterMarker],
        			         ["Middle Marker",	xplm_Nav_MiddleMarker],
		    	             ["Inner Marker",	xplm_Nav_InnerMarker],
        			         ["Fix",			xplm_Nav_Fix],
		            	     ["DME",			xplm_Nav_DME],
        		        	 ["Lat/Lon",		xplm_Nav_LatLon]]

		# Create our menu
		Item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Python - FMSUtility 1", 0, 1)
		self.FMSUtilityMenuHandlerCB = self.FMSUtilityMenuHandler
		self.Id = XPLMCreateMenu(self, "FMSUtility 1", XPLMFindPluginsMenu(), Item, self.FMSUtilityMenuHandlerCB,	0)
		XPLMAppendMenuItem(self.Id, "Utility Panel", 1, 1)

		return self.Name, self.Sig, self.Desc

	def XPluginStop(self):
		if (self.MenuItem1 == 1):
			XPDestroyWidget(self, self.FMSUtilityWidget, 1)
			self.MenuItem1 = 0

		XPLMDestroyMenu(self, self.Id)
		pass

	def XPluginEnable(self):
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		pass

	def FMSUtilityMenuHandler(self, inMenuRef, inItemRef):
		# If menu selected create our widget dialog
		if (inItemRef == 1):
			if (self.MenuItem1 == 0):
				self.CreateFMSUtilityWidget(221, 640, 420, 290)
				self.MenuItem1 = 1
			else:
				if(not XPIsWidgetVisible(self.FMSUtilityWidget)):
					XPShowWidget(self.FMSUtilityWidget)
		pass

	"""
	This will create our widget dialog.
	I have made all child widgets relative to the input paramter.
	This makes it easy to position the dialog
	"""
	def CreateFMSUtilityWidget(self, x, y, w, h):
		x2 = x + w
		y2 = y - h
		Buffer = "Python - FMS Example 1 by Sandy Barbour - 2005"

		# Create the Main Widget window
		self.FMSUtilityWidget = XPCreateWidget(x, y, x2, y2, 1, Buffer, 1,	0, xpWidgetClass_MainWindow)

		# Add Close Box decorations to the Main Widget
		XPSetWidgetProperty(self.FMSUtilityWidget, xpProperty_MainWindowHasCloseBoxes, 1)

		# Create the Sub Widget1 window
		FMSUtilityWindow1 = XPCreateWidget(x+10, y-30, x+160, y2+10,
							1,		# Visible
							"",		# desc
							0,		# root
							self.FMSUtilityWidget,
							xpWidgetClass_SubWindow)

		# Set the style to sub window
		XPSetWidgetProperty(FMSUtilityWindow1, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)

		# Create the Sub Widget2 window
		FMSUtilityWindow2 = XPCreateWidget(x+170, y-30, x2-10, y2+10,
							1,		# Visible
							"",		# desc
							0,		# root
							self.FMSUtilityWidget,
							xpWidgetClass_SubWindow)

		# Set the style to sub window
		XPSetWidgetProperty(FMSUtilityWindow2, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow)

		# Entry Index
		self.GetEntryIndexButton = XPCreateWidget(x+20, y-40, x+110, y-62,
							1, " Get Entry Index", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.GetEntryIndexButton, xpProperty_ButtonType, xpPushButton)

		self.EntryIndexEdit = XPCreateWidget(x+120, y-40, x+150, y-62,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.EntryIndexEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.EntryIndexEdit, xpProperty_Enabled, 1)

		self.SetEntryIndexButton = XPCreateWidget(x+20, y-70, x+110, y-92,
							1, " Set Entry Index", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.SetEntryIndexButton, xpProperty_ButtonType, xpPushButton)

		# Destination Index
		self.GetDestinationEntryButton = XPCreateWidget(x+20, y-100, x+110, y-122,
		 					1, " Get Dest Index", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.GetDestinationEntryButton, xpProperty_ButtonType, xpPushButton)

		self.DestinationEntryIndexEdit = XPCreateWidget(x+120, y-100, x+150, y-122,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.DestinationEntryIndexEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.DestinationEntryIndexEdit, xpProperty_Enabled, 1)

		self.SetDestinationEntryButton = XPCreateWidget(x+20, y-130, x+110, y-152,
						1, " Set Dest Index", 0, self.FMSUtilityWidget,
						xpWidgetClass_Button)

		XPSetWidgetProperty(self.SetDestinationEntryButton, xpProperty_ButtonType, xpPushButton)

		# Number of Entries
		self.GetNumberOfEntriesButton = XPCreateWidget(x+20, y-160, x+110, y-182,
							1, " Get No. Entries", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.GetNumberOfEntriesButton, xpProperty_ButtonType, xpPushButton)

		self.GetNumberOfEntriesText = XPCreateWidget(x+120, y-160, x+150, y-182,
							1, "", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.GetNumberOfEntriesText, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.GetNumberOfEntriesText, xpProperty_Enabled, 0)

		# Clear Entry
		self.ClearEntryButton = XPCreateWidget(x+20, y-190, x+110, y-212,
							1, " Clear Entry", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.ClearEntryButton, xpProperty_ButtonType, xpPushButton)

		# Index (Segment - 1)
		IndexCaption = XPCreateWidget(x+180, y-40, x+230, y-62,
							1, "Index", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.IndexEdit = XPCreateWidget(x+240, y-40, x+290, y-62,
							1, "", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.IndexEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.IndexEdit, xpProperty_Enabled, 1)

		SegmentCaption = XPCreateWidget(x+300, y-40, x+350, y-62,
							1, "Segment", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.SegmentCaption2 = XPCreateWidget(x+360, y-40, x+410, y-62,
							1, "", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		# Airport ID
		AirportIDCaption = XPCreateWidget(x+180, y-70, x+230, y-92,
							1, "Airport ID", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.AirportIDEdit = XPCreateWidget(x+240, y-70, x+290, y-92,
							1, "----", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.AirportIDEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.AirportIDEdit, xpProperty_Enabled, 1)

		# Altitude
		AltitudeCaption = XPCreateWidget(x+180, y-100, x+230, y-122,
							1, "Altitude", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.AltitudeEdit = XPCreateWidget(x+240, y-100, x+290, y-122,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.AltitudeEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.AltitudeEdit, xpProperty_Enabled, 1)

		# Nav Type
		NavTypeCaption = XPCreateWidget(x+180, y-130, x+230, y-152,
							1, "Nav Type", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		Buffer = "%s" % (self.NavTypeLookup[0][0])
		self.NavTypeEdit = XPCreateWidget(x+240, y-130, x+340, y-152,
							1, Buffer, 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.NavTypeEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.NavTypeEdit, xpProperty_Enabled, 0)

		# Used for selecting Nav Type
		self.UpArrow = XPCreateWidget(x+340, y-130, x+362, y-141,
									1, "", 0, self.FMSUtilityWidget,
									xpWidgetClass_Button)

		XPSetWidgetProperty(self.UpArrow, xpProperty_ButtonType, xpLittleUpArrow)

		# Used for selecting Nav Type
		self.DownArrow = XPCreateWidget(x+340, y-141, x+362, y-152,
									1, "", 0, self.FMSUtilityWidget,
									xpWidgetClass_Button)

		XPSetWidgetProperty(self.DownArrow, xpProperty_ButtonType, xpLittleDownArrow)

		self.NavTypeText = XPCreateWidget(x+362, y-130, x+400, y-152,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.NavTypeText, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.NavTypeText, xpProperty_Enabled, 0)

		# Get FMS Entry Info
		self.GetFMSEntryButton = XPCreateWidget(x+180, y-160, x+270, y-182,
							1, " Get FMS Entry", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.GetFMSEntryButton, xpProperty_ButtonType, xpPushButton)

		# Set FMS Entry Info
		self.SetFMSEntryButton = XPCreateWidget(x+280, y-160, x+370, y-182,
							1, " Set FMS Entry", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.SetFMSEntryButton, xpProperty_ButtonType, xpPushButton)

		# Lat / Lon
		LatCaption = XPCreateWidget(x+180, y-190, x+230, y-212,
							1, "Latitude", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.LatEdit = XPCreateWidget(x+240, y-190, x+310, y-212,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.LatEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.LatEdit, xpProperty_Enabled, 1)

		LonCaption = XPCreateWidget(x+180, y-220, x+230, y-242,
							1, "Longitude", 0, self.FMSUtilityWidget,
							xpWidgetClass_Caption)

		self.LonEdit = XPCreateWidget(x+240, y-220, x+310, y-242,
							1, "0", 0, self.FMSUtilityWidget,
							xpWidgetClass_TextField)

		XPSetWidgetProperty(self.LonEdit, xpProperty_TextFieldType, xpTextEntryField)
		XPSetWidgetProperty(self.LonEdit, xpProperty_Enabled, 1)

		self.SetLatLonButton = XPCreateWidget(x+180, y-250, x+270, y-272,
							1, " Set Lat/Lon", 0, self.FMSUtilityWidget,
							xpWidgetClass_Button)

		XPSetWidgetProperty(self.SetLatLonButton, xpProperty_ButtonType, xpPushButton)

		# Register our widget handler
		self.FMSUtilityHandlerCB = self.FMSUtilityHandler
		XPAddWidgetCallback(self, self.FMSUtilityWidget, self.FMSUtilityHandlerCB)
		pass

	def FMSUtilityHandler(self, inMessage, inWidget,	inParam1, inParam2):
		if (inMessage == xpMessage_CloseButtonPushed):
			if (self.MenuItem1 == 1):
				XPHideWidget(self.FMSUtilityWidget)
			return 1

		# Handle any button pushes
		if (inMessage == xpMsg_PushButtonPressed):
			# Most of these handlers get a value.
			# It then has to be converted to a string.
			# This is because "XPSetWidgetDescriptor" expects a string as its second parameter.
			if (inParam1 == self.ClearEntryButton):
				XPLMClearFMSEntry(XPLMGetDisplayedFMSEntry())
				return 1

			if (inParam1 == self.GetEntryIndexButton):
				Index = XPLMGetDisplayedFMSEntry()
				XPSetWidgetDescriptor(self.EntryIndexEdit, str(Index))
				return 1

			if (inParam1 == self.SetEntryIndexButton):
				Buffer = []
				XPGetWidgetDescriptor(self.EntryIndexEdit, Buffer, 256)
				lIndex = Buffer[0]
				sIndex = str(lIndex)
				Index = int(sIndex)
				XPLMSetDisplayedFMSEntry(Index)
				return 1

			if (inParam1 == self.GetDestinationEntryButton):
				Index = XPLMGetDestinationFMSEntry()
				XPSetWidgetDescriptor(self.DestinationEntryIndexEdit, str(Index))
				return 1

			if (inParam1 == self.SetDestinationEntryButton):
				Buffer = []
				XPGetWidgetDescriptor(self.DestinationEntryIndexEdit, Buffer, 256)
				Index = int(str(Buffer[0]))
				XPLMSetDestinationFMSEntry(Index)
				return 1

			if (inParam1 == self.GetNumberOfEntriesButton):
				Count = XPLMCountFMSEntries()
				XPSetWidgetDescriptor(self.GetNumberOfEntriesText, str(Count))
				return 1

			if (inParam1 == self.GetFMSEntryButton):
				Index = XPLMGetDisplayedFMSEntry()
				outType = []; outID = []; outRef = []; outAltitude = []; outLat = []; outLon = []
				XPLMGetFMSEntryInfo(Index, outType, outID, outRef, outAltitude, outLat, outLon)
				XPSetWidgetDescriptor(self.IndexEdit, str(Index))
				XPSetWidgetDescriptor(self.SegmentCaption2, str(Index+1))

				if (outType[0] == xplm_Nav_LatLon):
					XPSetWidgetDescriptor(self.AirportIDEdit, "----")
				else:
					XPSetWidgetDescriptor(self.AirportIDEdit, str(outID[0]))

				XPSetWidgetDescriptor(self.AltitudeEdit, str(outAltitude[0]))
				XPSetWidgetDescriptor(self.NavTypeEdit, self.NavTypeLookup[self.GetCBIndex(outType[0])][0])
				Buffer =  "%d" % (self.NavTypeLookup[self.GetCBIndex(outType[0])][1])
				XPSetWidgetDescriptor(self.NavTypeText, Buffer)
				XPSetWidgetDescriptor(self.LatEdit, str(outLat[0]))
				XPSetWidgetDescriptor(self.LonEdit, str(outLon[0]))
				return 1

			if (inParam1 == self.SetFMSEntryButton):
				Buffer = []
				XPGetWidgetDescriptor(self.IndexEdit, Buffer, 256)
				Index = int(str(Buffer[0]))
				XPSetWidgetDescriptor(self.SegmentCaption2, str(Index+1))
				Buffer = []
				XPGetWidgetDescriptor(self.AltitudeEdit, Buffer, 256)
				Altitude = int(str(Buffer[0]))
				Buffer = []
				XPGetWidgetDescriptor(self.NavTypeText, Buffer, 256)
				NavType = int(str(Buffer[0]))
				Buffer = []
				XPGetWidgetDescriptor(self.AirportIDEdit, Buffer, 256)
				IDFragment = str(Buffer[0])
				XPLMSetFMSEntryInfo(Index, XPLMFindNavAid(None, IDFragment, None, None, None, NavType), Altitude)
				return 1

			if (inParam1 == self.SetLatLonButton):
				Buffer = []
				XPGetWidgetDescriptor(self.IndexEdit, Buffer, 256)
				Index = int(str(Buffer[0]))
				XPSetWidgetDescriptor(self.SegmentCaption2, str(Index+1))
				Buffer = []
				XPGetWidgetDescriptor(self.AltitudeEdit, Buffer, 256)
				Altitude  = int(str(Buffer[0]))
				Buffer = []
				XPGetWidgetDescriptor(self.LatEdit, Buffer, 256)
				Lat = float(str(Buffer[0]))
				Buffer = []
				XPGetWidgetDescriptor(self.LonEdit, Buffer, 256)
				Lon = float(str(Buffer[0]))
				XPLMSetFMSEntryLatLon(Index, Lat, Lon, Altitude)
				return 1

			# Up Arrow is used to modify the NavTypeLookup Array Index
			if (inParam1 == self.UpArrow):
				self.NavTypeLinePosition -= 1
				if (self.NavTypeLinePosition < 0):
					self.NavTypeLinePosition = self.MAX_NAV_TYPES-1
				XPSetWidgetDescriptor(self.NavTypeEdit, self.NavTypeLookup[self.NavTypeLinePosition][0])
				XPSetWidgetDescriptor(self.NavTypeText, str(self.NavTypeLookup[self.NavTypeLinePosition][1]))
				return 1

			# Down Arrow is used to modify the NavTypeLookup Array Index
			if (inParam1 == self.DownArrow):
				self.NavTypeLinePosition += 1
				if (self.NavTypeLinePosition > self.MAX_NAV_TYPES-1):
					self.NavTypeLinePosition = 0
				XPSetWidgetDescriptor(self.NavTypeEdit, self.NavTypeLookup[self.NavTypeLinePosition][0])
				XPSetWidgetDescriptor(self.NavTypeText, str(self.NavTypeLookup[self.NavTypeLinePosition][1]))
				return 1

		return 0
		pass

	# This function takes an XPLMNavType and
	# returns the index into the NavTypeLookup array.
	# We can then use that index to access the description or enum.
	def GetCBIndex(self, Type):
		CBIndex = 0
		Index = 0

		while Index < self.MAX_NAV_TYPES:
			if (self.NavTypeLookup[Index][1] == Type):
				CBIndex = Index
				break

			Index += 1

		return CBIndex

