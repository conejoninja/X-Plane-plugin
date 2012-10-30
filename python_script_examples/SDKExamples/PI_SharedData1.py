"""
ShareData.py

Ported to Python by Sandy Barbour - 03/05/2005

This is an example plugin that demonstrates how to share data, both owned
by a plugin and shared.

Data can be published in two ways: a plugin can publish data it owns.
In this case, it provides callbacks to read (and optionally write) the
data.  As other plugins access the data ref, the SDK calls back the
accessors.

Data can also be shared.  In this case, the SDK allocates the memory
for the data.  Each plugin that shares it registers a callback that is
called by the SDK when any plugin writes the data.

We use the xplanesdk namespace to allocate unique data refs.  When creating
your own datarefs, make sure to prefix the data ref with a domain unique to
your organization.  'sim' is the domain for the main simulator.
"""

from XPLMDefs import *
from XPLMDataAccess import *
from XPLMUtilities import *
from XPLMGraphics import *
from XPLMDisplay import *

class PythonInterface:
        def XPluginStart(self):
                self.Name = "SharedData1"
                self.Sig =  "SandyBarbour.Python.SharedData1"
                self.Desc = "A plugin that shares a data ref."
                self.DrawWindowCB = self.DrawWindowCallback
                self.KeyCB = self.KeyCallback
                self.MouseClickCB = self.MouseClickCallback
                self.Window = XPLMCreateWindow(self, 50, 600, 300, 400, 1, self.DrawWindowCB, self.KeyCB, self.MouseClickCB, 0)

                """
                Register our owned data.  Note that we pass two sets of
                function callbacks for two data types and leave the rest blank.
                """
                self.MyGetDatafCB = self.MyGetDatafCallback
                self.MySetDatafCB = self.MySetDatafCallback
                self.MyGetDatadCB = self.MyGetDatadCallback
                self.MySetDatadCB = self.MySetDatadCallback
                self.OwnedDataRef = XPLMRegisterDataAccessor(
                                                                        self,
                                                                        "xplanesdk/examples/sharedata/number1",
                                                                        xplmType_Float + xplmType_Double,       # The types we support
                                                                        1,                                      # Writable
                                                                        0, 0,                                   # No accessors for ints
                                                                        self.MyGetDatafCB, self.MySetDatafCB,   # Accessors for floats
                                                                        self.MyGetDatadCB, self.MySetDatadCB,   # Accessors for doubles
                                                                        0, 0,                                   # No accessors for int arrays
                                                                        0, 0,                                   # No accessors for float arrays
                                                                        0, 0,                                   # No accessors for raw data
                                                                        0, 0)                                   # Refcons not used

                """
                Subscribe to shared data.  If no one else has made it, this will
                cause the SDK to allocate the data.
                """
                self.MyDataChangedCB = self.MyDataChangedCallback
                RetVal = XPLMShareData(self, "xplanesdk/examples/sharedata/sharedint1", xplmType_Int,   self.MyDataChangedCB, 0)
                self.SharedDataRef = XPLMFindDataRef("xplanesdk/examples/sharedata/sharedint1")
                self.Buffer = "ShareData 1 - SharedDataRef := %x\n" % self.SharedDataRef
                XPLMDebugString(self.Buffer)
                print(self.Buffer)

                return self.Name, self.Sig, self.Desc

        def XPluginStop(self):
                XPLMDestroyWindow(self, self.Window)
                if (self.OwnedDataRef):
                        XPLMUnregisterDataAccessor(self, self.OwnedDataRef)
                RetVal = XPLMUnshareData(self, "xplanesdk/examples/sharedata/sharedint1", xplmType_Int, self.MyDataChangedCB, 0)
                pass

        def XPluginEnable(self):
                return 1

        def XPluginDisable(self):
                pass

        def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
                pass

        def DrawWindowCallback(self, inWindowID, inRefcon):
                lLeft = [];     lTop = []; lRight = []; lBottom = []
                XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
                left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])
                gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
                color = 1.0, 1.0, 1.0
                gResult = XPLMDrawString(color, left + 5, top - 20, "Click Here", 0, xplmFont_Basic)
                pass

        def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
                pass

        def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
                if (inMouse == xplm_MouseDown):
                        AccessorDataRef = XPLMFindDataRef("xplanesdk/examples/sharedata/number1")
                        XPLMSetDataf(AccessorDataRef, 1.2345)
                        DataRefFloat = XPLMGetDataf(AccessorDataRef)
                        print("DataRefFloat 1 = " + str(DataRefFloat) + str("\n"))
                        XPLMSetDatad(AccessorDataRef, 9.87654321234)
                        DataRefDouble = XPLMGetDatad(AccessorDataRef)
                        print("DataRefDouble 1 = " + str(DataRefDouble) + str("\n"))
                return 1

        """
        This is the callback for our shared data.  Right now we do not react
        to our shared data being chagned.
        """

        def MyDataChangedCallback(self, inRefcon):
                pass

        """
        These callbacks are called by the SDK to read and write the sim.
        We provide two sets of callbacks allowing our data to appear as
        float and double.  This is done for didactic purposes; multityped
        data is provided as a backward compatibility solution and probably
        should not be used in initial designs as a convenience to client
        code.
        """

        def MyGetDatafCallback(self, inRefcon):
                return self.OwnedFloatData

        def MySetDatafCallback(self, inRefcon, inValue):
                self.OwnedFloatData = inValue
                pass

        def MyGetDatadCallback(self, inRefcon):
                return self.OwnedDoubleData;

        def MySetDatadCallback(self, inRefcon, inValue):
                self.OwnedDoubleData = inValue;
                pass



















