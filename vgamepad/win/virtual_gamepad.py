"""
VGamepad API (Windows)
"""

import vgamepad.win.vigem_commons as vcom
import vgamepad.win.vigem_client as vcli
import ctypes
from ctypes import CFUNCTYPE, c_void_p, c_ubyte
from abc import ABC, abstractmethod
from inspect import signature  # Check if user defined callback function is legal


def check_err(err):
    if err != vcom.VIGEM_ERRORS.VIGEM_ERROR_NONE:
        raise Exception(vcom.VIGEM_ERRORS(err).name)


def dummy_callback(client, target, large_motor, small_motor, led_number, user_data):
    """
    Pattern for callback functions to be registered as notifications

    :param client: vigem bus ID
    :param target: vigem device ID
    :param large_motor: integer in [0, 255] representing the state of the large motor
    :param small_motor: integer in [0, 255] representing the state of the small motor
    :param led_number: integer in [0, 255] representing the state of the LED ring
    :param user_data: placeholder, do not use
    """
    pass


class VBus:
    """
    Virtual USB bus (ViGEmBus)
    """
    def __init__(self):
        self._busp = vcli.vigem_alloc()
        check_err(vcli.vigem_connect(self._busp))

    def get_busp(self):
        return self._busp

    def __del__(self):
        vcli.vigem_disconnect(self._busp)
        vcli.vigem_free(self._busp)


# We instantiate a single global VBus for all controllers
VBUS = VBus()


class VGamepad(ABC):
    def __init__(self):
        self.vbus = VBUS
        self._busp = self.vbus.get_busp()
        self._devicep = self.target_alloc()
        self.CMPFUNC = CFUNCTYPE(None, c_void_p, c_void_p, c_ubyte, c_ubyte, c_ubyte, c_void_p)
        self.cmp_func = None
        vcli.vigem_target_add(self._busp, self._devicep)
        assert vcli.vigem_target_is_attached(self._devicep), "The virtual device could not connect to ViGEmBus."

    def __del__(self):
        vcli.vigem_target_remove(self._busp, self._devicep)
        vcli.vigem_target_free(self._devicep)

    def get_vid(self):
        """
        :return: the vendor ID of the virtual device
        """
        return vcli.vigem_target_get_vid(self._devicep)

    def get_pid(self):
        """
        :return: the product ID of the virtual device
        """
        return vcli.vigem_target_get_pid(self._devicep)

    def set_vid(self, vid):
        """
        :param: the new vendor ID of the virtual device
        """
        vcli.vigem_target_set_vid(self._devicep, vid)

    def set_pid(self, pid):
        """
        :param: the new product ID of the virtual device
        """
        vcli.vigem_target_get_pid(self._devicep, pid)

    def get_index(self):
        """
        :return: the internally used index of the target device
        """
        return vcli.vigem_target_get_index(self._devicep)

    def get_type(self):
        """
        :return: the type of the object (e.g. VIGEM_TARGET_TYPE.Xbox360Wired)
        """
        return vcli.vigem_target_get_type(self._devicep)

    @abstractmethod
    def target_alloc(self):
        """
        :return: the pointer to an allocated ViGEm device (e.g. vcli.vigem_target_x360_alloc())
        """
        pass


class VX360Gamepad(VGamepad):
    """
    Virtual XBox360 gamepad
    """
    def __init__(self):
        super().__init__()
        self.report = self.get_default_report()
        self.update()

    def get_default_report(self):
        return vcom.XUSB_REPORT(
            wButtons=0,
            bLeftTrigger=0,
            bRightTrigger=0,
            sThumbLX=0,
            sThumbLY=0,
            sThumbRX=0,
            sThumbRY=0)

    def reset(self):
        """
        Resets the report to the default state
        """
        self.report = self.get_default_report()

    def press_button(self, button):
        """
        Presses a button (no effect if already pressed)
        All possible buttons are in XUSB_BUTTON

        :param: a XUSB_BUTTON field, e.g. XUSB_BUTTON.XUSB_GAMEPAD_X
        """
        self.report.wButtons = self.report.wButtons | button

    def release_button(self, button):
        """
        Releases a button (no effect if already released)
        All possible buttons are in XUSB_BUTTON

        :param: a XUSB_BUTTON field, e.g. XUSB_BUTTON.XUSB_GAMEPAD_X
        """
        self.report.wButtons = self.report.wButtons & ~button

    def left_trigger(self, value):
        """
        Sets the value of the left trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self.report.bLeftTrigger = value

    def right_trigger(self, value):
        """
        Sets the value of the right trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self.report.bRightTrigger = value

    def left_trigger_float(self, value_float):
        """
        Sets the value of the left trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.left_trigger(round(value_float * 255))

    def right_trigger_float(self, value_float):
        """
        Sets the value of the right trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.right_trigger(round(value_float * 255))

    def left_joystick(self, x_value, y_value):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self.report.sThumbLX = x_value
        self.report.sThumbLY = y_value

    def right_joystick(self, x_value, y_value):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self.report.sThumbRX = x_value
        self.report.sThumbRY = y_value

    def left_joystick_float(self, x_value_float, y_value_float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.left_joystick(round(x_value_float * 32767), round(y_value_float * 32767))

    def right_joystick_float(self, x_value_float, y_value_float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.right_joystick(round(x_value_float * 32767), round(y_value_float * 32767))

    def update(self):
        """
        Sends the current report (i.e. commands) to the virtual device
        """
        check_err(vcli.vigem_target_x360_update(self._busp, self._devicep, self.report))

    def register_notification(self, callback_function):
        """
        Registers a callback function that can handle force feedback, leds, etc.

        :param: a function of the form: my_func(client, target, large_motor, small_motor, led_number, user_data)
        """
        if not signature(callback_function) == signature(dummy_callback):
            raise TypeError("Needed callback function signature: {}, but got: {}".format(signature(dummy_callback), signature(callback_function)))
        self.cmp_func = self.CMPFUNC(callback_function)  # keep its reference, otherwise the program will crash when a callback is made.
        check_err(vcli.vigem_target_x360_register_notification(self._busp, self._devicep, self.cmp_func, None))

    def unregister_notification(self):
        """
        Unregisters a previously registered callback function.
        """
        vcli.vigem_target_x360_unregister_notification(self._devicep)

    def target_alloc(self):
        return vcli.vigem_target_x360_alloc()


class VDS4Gamepad(VGamepad):
    """
    Virtual DualShock 4 gamepad
    """

    def __init__(self):
        super().__init__()
        self.report = self.get_default_report()
        self.update()

    def get_default_report(self):
        rep = vcom.DS4_REPORT(
            bThumbLX=0,
            bThumbLY=0,
            bThumbRX=0,
            bThumbRY=0,
            wButtons=0,
            bSpecial=0,
            bTriggerL=0,
            bTriggerR=0)
        vcom.DS4_REPORT_INIT(rep)
        return rep

    def reset(self):
        """
        Resets the report to the default state
        """
        self.report = self.get_default_report()

    def press_button(self, button):
        """
        Presses a button (no effect if already pressed)
        All possible buttons are in DS4_BUTTONS

        :param: a DS4_BUTTONS field, e.g. DS4_BUTTONS.DS4_BUTTON_TRIANGLE
        """
        self.report.wButtons = self.report.wButtons | button

    def release_button(self, button):
        """
        Releases a button (no effect if already released)
        All possible buttons are in DS4_BUTTONS

        :param: a DS4_BUTTONS field, e.g. DS4_BUTTONS.DS4_BUTTON_TRIANGLE
        """
        self.report.wButtons = self.report.wButtons & ~button

    def press_special_button(self, special_button):
        """
        Presses a special button (no effect if already pressed)
        All possible buttons are in DS4_SPECIAL_BUTTONS

        :param: a DS4_SPECIAL_BUTTONS field, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        self.report.bSpecial = self.report.bSpecial | special_button

    def release_special_button(self, special_button):
        """
        Releases a special button (no effect if already released)
        All possible buttons are in DS4_SPECIAL_BUTTONS

        :param: a DS4_SPECIAL_BUTTONS field, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        self.report.bSpecial = self.report.bSpecial & ~special_button

    def left_trigger(self, value):
        """
        Sets the value of the left trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self.report.bTriggerL = value

    def right_trigger(self, value):
        """
        Sets the value of the right trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self.report.bTriggerR = value

    def left_trigger_float(self, value_float):
        """
        Sets the value of the left trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.left_trigger(round(value_float * 255))

    def right_trigger_float(self, value_float):
        """
        Sets the value of the right trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.right_trigger(round(value_float * 255))

    def left_joystick(self, x_value, y_value):
        """
        Sets the values of the X and Y axis for the left joystick
        Note: compared to the API, the Y axis are multiplied by -1 for consistency with X360

        :param: integer between 0 and 255 (128 = neutral position)
        """
        self.report.bThumbLX = x_value
        self.report.bThumbLY = - y_value

    def right_joystick(self, x_value, y_value):
        """
        Sets the values of the X and Y axis for the right joystick
        Note: compared to the API, the Y axis are multiplied by -1 for consistency with X360

        :param: integer between 0 and 255 (128 = neutral position)
        """
        self.report.bThumbRX = x_value
        self.report.bThumbRY = - y_value

    def left_joystick_float(self, x_value_float, y_value_float):
        """
        Sets the values of the X and Y axis for the left joystick
        Note: compared to the API, the Y axis are multiplied by -1 for consistency with X360

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.left_joystick(128 + round(x_value_float * 127), 128 + round(y_value_float * 127))

    def right_joystick_float(self, x_value_float, y_value_float):
        """
        Sets the values of the X and Y axis for the right joystick
        Note: compared to the API, the Y axis are multiplied by -1 for consistency with X360

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.right_joystick(128 + round(x_value_float * 127), 128 + round(y_value_float * 127))

    def directional_pad(self, direction):
        """
        Sets the direction of the directional pad (hat)
        All possible directions are in DS4_DPAD_DIRECTIONS

        :param: a DS4_DPAD_DIRECTIONS field, e.g. DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST
        """
        vcom.DS4_SET_DPAD(self.report, direction)

    def update(self):
        """
        Sends the current report (i.e. commands) to the virtual device
        """
        check_err(vcli.vigem_target_ds4_update(self._busp, self._devicep, self.report))

    def update_extended_report(self, extended_report):
        """
        Enables using DS4_REPORT_EX instead of DS4_REPORT (advanced users only)
        If you don't know what this is about, you can safely ignore this function

        :param: a DS4_REPORT_EX
        """
        check_err(vcli.vigem_target_ds4_update_ex_ptr(self._busp, self._devicep, ctypes.byref(extended_report)))

    def register_notification(self, callback_function):
        """
        Registers a callback function that can handle force feedback, leds, etc.

        :param: a function of the form: my_func(client, target, large_motor, small_motor, led_number, user_data)
        """
        if not signature(callback_function) == signature(dummy_callback):
            raise TypeError("Needed callback function signature: {}, but got: {}".format(signature(dummy_callback), signature(callback_function)))
        self.cmp_func = self.CMPFUNC(callback_function)
        check_err(vcli.vigem_target_ds4_register_notification(self._busp, self._devicep, self.cmp_func, None))

    def unregister_notification(self):
        """
        Unregisters a previously registered callback function.
        """
        vcli.vigem_target_ds4_unregister_notification(self._devicep)

    def target_alloc(self):
        return vcli.vigem_target_ds4_alloc()
