"""
KeySniffer.c

Ported to Python by Sandy Barbour - 28/04/2005

KeySniffer shows the use of key sniffers to intercept and process raw
keystrokes.  This one creates a window where all data about the keystroke
is displayed.

Key strokes have two sets of character data.  The ASCII key code is a valid
ASCII value.  This value discriminates between the A key with and without shift
(e.g. 'A' and 'a') but does not discriminate between numbers on the main
keyboard vs. numeric keypad.  Virtual key codes tell exactly what physical key
was pressed (e.g. top-row-0 vs. num-pad-0) but do not change by modifier keys.
Modifier keys are returned separately.

ASCII codes are good for handling text entry; virtual key codes are good for
setting up key commands (since they allow for separate binding of the numeric
key pad).
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMUtilities import *

class PythonInterface:
        def XPluginStart(self):
                # First set up our plugin info.
                self.Name = "KeySniffer1"
                self.Sig =  "SandyBarbour.Python.KeySniffer1"
                self.Desc = "An example sniffing keys."
                self.Char = 65
                self.VirtualKey = 0
                self.Flags = 0

                # Now create a new window.  Pass in our three callbacks.
                self.DrawWindowCB = self.MyDrawWindowCallback
                self.KeyCB = self.MyHandleKeyCallback
                self.MouseClickCB = self.MyHandleMouseClickCallback
                self.Window = XPLMCreateWindow(
                                                self,
                                                50, 750, 350, 700,
                                                1,
                                                self.DrawWindowCB,
                                                self.KeyCB,
                                                self.MouseClickCB,
                                                0)

                # Finally register our key sniffer.
                self.MyKeySnifferCB = self.MyKeySniffer
                XPLMRegisterKeySniffer(self, self.MyKeySnifferCB, 1,    0)
                return self.Name, self.Sig, self.Desc

        def XPluginStop(self):
                XPLMUnregisterKeySniffer(self, self.MyKeySnifferCB, 1,  0)
                XPLMDestroyWindow(self, self.Window)

        def XPluginEnable(self):
                return 1

        def XPluginDisable(self):
                pass

        def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
                pass

        """
        MyDrawWindowCallback

        This routine draws the window, showing the last keyboard stroke to be
        recorded by our sniffer.
        """
        def MyDrawWindowCallback(self, inWindowID, inRefcon):
                # First get our window's location.
                lLeft = [];     lTop = []; lRight = []; lBottom = []
                XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
                left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])

                # Draw a translucent dark box as our window outline.
                gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)

                color = 1.0, 1.0, 1.0

                if (self.Flags & xplm_ShiftFlag):
                        Shift = 'S'
                else:
                        Shift = ' '
                if (self.Flags & xplm_OptionAltFlag):
                        OptionAlt = 'A'
                else:
                        OptionAlt = ' '
                if (self.Flags & xplm_ControlFlag):
                        Control = 'C'
                else:
                        Control = ' '
                if (self.Flags & xplm_DownFlag):
                        Down = 'D'
                else:
                        Down = ' '
                if (self.Flags & xplm_UpFlag):
                        Up = 'U'
                else:
                        Up = ' '

                """
                Take the last key stroke and form a descriptive string.
                Note that ASCII values may be printed directly.  Virtual key
                codes are not ASCII and cannot be, but the utility function
                XPLMGetVirtualKeyDescription provides a human-readable string
                for each key.  These strings may be multicharacter, e.g. 'ENTER'
                or 'NUMPAD-0'.
                """

                Desc = XPLMGetVirtualKeyDescription(self.VirtualKey)
                if (self.Char == 0):
                        MyString = "%d %c | %d %s (%c %c %c %c %c)" % (self.Char, '0', self.VirtualKey, Desc, Shift, OptionAlt, Control, Down, Up)
                else:
                        MyString = "%d %c | %d %s (%c %c %c %c %c)" % (self.Char, self.Char, self.VirtualKey, Desc, Shift, OptionAlt, Control, Down, Up)

                # Draw the string into the window.
                gResult = XPLMDrawString(color, left + 5, top - 20, MyString, 0, xplmFont_Basic)

        def MyHandleKeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
                pass

        def MyHandleMouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
                return 1

        """
        MyKeySniffer

        This routnine receives keystrokes from the simulator as they are pressed.
        A separate message is received for each key press and release as well as
        keys being held down.
        """
        def MyKeySniffer(self, inChar, inFlags, inVirtualKey, inRefcon):

                # First record the key data.
                self.VirtualKey = inVirtualKey
                self.Flags = inFlags
                self.Char = inChar

                """
                Return 1 to pass the keystroke to plugin windows and X-Plane.
                Returning 0 would consume the keystroke.
                """
                return 1

