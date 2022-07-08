"""
Adapted from ViGEm source
"""

from enum import IntFlag, IntEnum
from ctypes import Structure, Union, c_short, c_ushort, c_ubyte


c_byte = c_ubyte  # because BYTE is actually unsigned char


class VIGEM_TARGET_TYPE(IntFlag):
    """
    Represents the desired target type for the emulated device.
    NOTE: 1 skipped on purpose to maintain compatibility
    """
    Xbox360Wired = 0  # Microsoft Xbox 360 Controller (wired)
    DualShock4Wired = 2  # Sony DualShock 4 (wired)


class XUSB_BUTTON(IntFlag):
    """
    Possible XUSB report buttons.
    """
    XUSB_GAMEPAD_DPAD_UP = 0x0001
    XUSB_GAMEPAD_DPAD_DOWN = 0x0002
    XUSB_GAMEPAD_DPAD_LEFT = 0x0004
    XUSB_GAMEPAD_DPAD_RIGHT = 0x0008
    XUSB_GAMEPAD_START = 0x0010
    XUSB_GAMEPAD_BACK = 0x0020
    XUSB_GAMEPAD_LEFT_THUMB = 0x0040
    XUSB_GAMEPAD_RIGHT_THUMB = 0x0080
    XUSB_GAMEPAD_LEFT_SHOULDER = 0x0100
    XUSB_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XUSB_GAMEPAD_GUIDE = 0x0400
    XUSB_GAMEPAD_A = 0x1000
    XUSB_GAMEPAD_B = 0x2000
    XUSB_GAMEPAD_X = 0x4000
    XUSB_GAMEPAD_Y = 0x8000


class XUSB_REPORT(Structure):
    """
    Represents an XINPUT_GAMEPAD-compatible report structure.
    """
    _fields_ = [("wButtons", c_ushort),
                ("bLeftTrigger", c_byte),
                ("bRightTrigger", c_byte),
                ("sThumbLX", c_short),
                ("sThumbLY", c_short),
                ("sThumbRX", c_short),
                ("sThumbRY", c_short)]


class DS4_LIGHTBAR_COLOR(Structure):
    """
    The color value (RGB) of a DualShock 4 Lightbar
    """
    _fields_ = [("Red", c_ubyte),  # Red part of the Lightbar (0-255).
                ("Green", c_ubyte),  # Green part of the Lightbar (0-255).
                ("Blue", c_ubyte)]  # Blue part of the Lightbar (0-255).


class DS4_BUTTONS(IntFlag):
    """
    DualShock 4 digital buttons
    """
    DS4_BUTTON_THUMB_RIGHT = 1 << 15
    DS4_BUTTON_THUMB_LEFT = 1 << 14
    DS4_BUTTON_OPTIONS = 1 << 13
    DS4_BUTTON_SHARE = 1 << 12
    DS4_BUTTON_TRIGGER_RIGHT = 1 << 11
    DS4_BUTTON_TRIGGER_LEFT = 1 << 10
    DS4_BUTTON_SHOULDER_RIGHT = 1 << 9
    DS4_BUTTON_SHOULDER_LEFT = 1 << 8
    DS4_BUTTON_TRIANGLE = 1 << 7
    DS4_BUTTON_CIRCLE = 1 << 6
    DS4_BUTTON_CROSS = 1 << 5
    DS4_BUTTON_SQUARE = 1 << 4


class DS4_SPECIAL_BUTTONS(IntFlag):
    """
    DualShock 4 special buttons
    """
    DS4_SPECIAL_BUTTON_PS = 1 << 0
    DS4_SPECIAL_BUTTON_TOUCHPAD = 1 << 1


class DS4_DPAD_DIRECTIONS(IntEnum):
    """
    DualShock 4 directional pad (HAT) values
    """
    DS4_BUTTON_DPAD_NONE = 0x8
    DS4_BUTTON_DPAD_NORTHWEST = 0x7
    DS4_BUTTON_DPAD_WEST = 0x6
    DS4_BUTTON_DPAD_SOUTHWEST = 0x5
    DS4_BUTTON_DPAD_SOUTH = 0x4
    DS4_BUTTON_DPAD_SOUTHEAST = 0x3
    DS4_BUTTON_DPAD_EAST = 0x2
    DS4_BUTTON_DPAD_NORTHEAST = 0x1
    DS4_BUTTON_DPAD_NORTH = 0x0


class DS4_REPORT(Structure):
    """
    DualShock 4 HID Input report
    """
    _fields_ = [("bThumbLX", c_byte),
                ("bThumbLY", c_byte),
                ("bThumbRX", c_byte),
                ("bThumbRY", c_byte),
                ("wButtons", c_ushort),
                ("bSpecial", c_byte),
                ("bTriggerL", c_byte),
                ("bTriggerR", c_byte)]


def DS4_SET_DPAD(report, dpad):
    report.wButtons &= ~0xF
    report.wButtons |= dpad  # TODO cast USHORT?


def DS4_REPORT_INIT(report):
    report.bThumbLX = 0x80
    report.bThumbLY = 0x80
    report.bThumbRX = 0x80
    report.bThumbRY = 0x80
    DS4_SET_DPAD(report, DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE)


class DS4_TOUCH(Structure):
    """
    DualShock 4 HID Touchpad structure
    """
    _fields_ = [("bPacketCounter", c_byte),  # timestamp / packet counter associated with touch event
                ("bIsUpTrackingNum1", c_byte),  # 0 means down; active low
                # unique to each finger down, so for a lift and repress the value is incremented
                ("bTouchData1", c_byte * 3),  # Two 12 bits values (for X and Y)
                # middle byte holds last 4 bits of X and the starting
                ("bIsUpTrackingNum2", c_byte),  # second touch data immediately follows data of first
                ("bTouchData2", c_ushort * 3)]  # resolution is 1920x943


class DS4_SUB_REPORT_EX(Structure):
    _fields_ = [("bThumbLX", c_byte),
                ("bThumbLY", c_byte),
                ("bThumbRX", c_byte),
                ("bThumbRY", c_byte),
                ("wButtons", c_ushort),
                ("bSpecial", c_byte),
                ("bTriggerL", c_byte),
                ("bTriggerR", c_byte),
                ("wTimestamp", c_ushort),
                ("bBatteryLvl", c_byte),
                ("wGyroX", c_short),
                ("wGyroY", c_short),
                ("wGyroZ", c_short),
                ("wAccelX", c_short),
                ("wAccelY", c_short),
                ("wAccelZ", c_short),
                ("_bUnknown1", c_byte * 5),
                ("bBatteryLvlSpecial", c_byte),
                # really should have a enum to show everything that this can represent (USB charging, battery level; EXT, headset, microphone connected)
                ("_bUnknown2", c_byte * 2),
                ("bTouchPacketsN", c_byte),  # 0x00 to 0x03 (USB max)
                ("sCurrentTouch", DS4_TOUCH),
                ("sPreviousTouch", DS4_TOUCH * 2)]


class DS4_REPORT_EX(Union):
    """
    DualShock 4 v1 complete HID Input report
    """
    _fields_ = [("Report", DS4_SUB_REPORT_EX),
                ("ReportBuffer", c_ubyte * 63)]


class VIGEM_ERRORS(IntEnum):
    """
    Values that represent ViGEm errors
    """
    VIGEM_ERROR_NONE = 0x20000000
    VIGEM_ERROR_BUS_NOT_FOUND = 0xE0000001
    VIGEM_ERROR_NO_FREE_SLOT = 0xE0000002
    VIGEM_ERROR_INVALID_TARGET = 0xE0000003
    VIGEM_ERROR_REMOVAL_FAILED = 0xE0000004
    VIGEM_ERROR_ALREADY_CONNECTED = 0xE0000005
    VIGEM_ERROR_TARGET_UNINITIALIZED = 0xE0000006
    VIGEM_ERROR_TARGET_NOT_PLUGGED_IN = 0xE0000007
    VIGEM_ERROR_BUS_VERSION_MISMATCH = 0xE0000008
    VIGEM_ERROR_BUS_ACCESS_FAILED = 0xE0000009
    VIGEM_ERROR_CALLBACK_ALREADY_REGISTERED = 0xE0000010
    VIGEM_ERROR_CALLBACK_NOT_FOUND = 0xE0000011
    VIGEM_ERROR_BUS_ALREADY_CONNECTED = 0xE0000012
    VIGEM_ERROR_BUS_INVALID_HANDLE = 0xE0000013
    VIGEM_ERROR_XUSB_USERINDEX_OUT_OF_RANGE = 0xE0000014
    VIGEM_ERROR_INVALID_PARAMETER = 0xE0000015
    VIGEM_ERROR_NOT_SUPPORTED = 0xE0000016


# TODO: add the missing types (C callback functions)
