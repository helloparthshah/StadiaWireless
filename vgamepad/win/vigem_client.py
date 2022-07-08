"""
Adapted from ViGEm source
"""

import platform
from pathlib import Path
from ctypes import CDLL, POINTER, CFUNCTYPE, c_void_p, c_uint, c_ushort, c_ulong, c_bool, c_ubyte
from vgamepad.win.vigem_commons import XUSB_REPORT, DS4_REPORT, DS4_REPORT_EX, VIGEM_TARGET_TYPE

if platform.architecture()[0] == "64bit":
    arch = "x64"
else:
    arch = "x86"

pathClient = Path(__file__).parent.absolute() / "vigem" / "client" / arch / "ViGEmClient.dll"
vigemClient = CDLL(str(pathClient))


"""
Allocates an object representing a driver connection
@returns    A PVIGEM_CLIENT object
"""
vigem_alloc = vigemClient.vigem_alloc
vigem_alloc.argtypes = ()
vigem_alloc.restype = c_void_p

"""
Frees up memory used by the driver connection object
@param      vigem   The PVIGEM_CLIENT object.
"""
vigem_free = vigemClient.vigem_free
vigem_free.argtypes = (c_void_p, )
vigem_free.restype = None

"""
Initializes the driver object and establishes a connection to the emulation bus driver.
Returns an error if no compatible bus device has been found.
@param 	    vigem	The PVIGEM_CLIENT object.
@returns	A VIGEM_ERROR.
"""
vigem_connect = vigemClient.vigem_connect
vigem_connect.argtypes = (c_void_p, )
vigem_connect.restype = c_uint

"""
Disconnects from the bus device and resets the driver object state. The driver object
may be reused again after calling this function. When called, all targets which may
still be connected will be destroyed automatically. Be aware, that allocated target
objects won't be automatically freed, this has to be taken care of by the caller.
@param      vigem	The PVIGEM_CLIENT object.
"""
vigem_disconnect = vigemClient.vigem_disconnect
vigem_disconnect.argtypes = (c_void_p, )
vigem_disconnect.restype = None

"""
Allocates an object representing an Xbox 360 Controller device.
@returns	A PVIGEM_TARGET representing an Xbox 360 Controller device.
"""
vigem_target_x360_alloc = vigemClient.vigem_target_x360_alloc
vigem_target_x360_alloc.argtypes = ()
vigem_target_x360_alloc.restype = c_void_p

"""
Allocates an object representing a DualShock 4 Controller device.
@returns	A PVIGEM_TARGET representing a DualShock 4 Controller device.
"""
vigem_target_ds4_alloc = vigemClient.vigem_target_ds4_alloc
vigem_target_ds4_alloc.argtypes = ()
vigem_target_ds4_alloc.restype = c_void_p

"""
Frees up memory used by the target device object. This does not automatically remove
the associated device from the bus, if present. If the target device doesn't get
removed before this call, the device becomes orphaned until the owning process is
terminated.
@param 	    target	The target device object.
"""
vigem_target_free = vigemClient.vigem_target_free
vigem_target_free.argtypes = (c_void_p, )
vigem_target_free.restype = None

"""
Adds a provided target device to the bus driver, which is equal to a device plug-in
event of a physical hardware device. This function blocks until the target device is
in full operational mode.
@param 	    vigem 	The driver connection object.
@param 	    target	The target device object.
@returns	A VIGEM_ERROR.
"""
vigem_target_add = vigemClient.vigem_target_add
vigem_target_add.argtypes = (c_void_p, c_void_p)
vigem_target_add.restype = c_uint

"""
Removes a provided target device from the bus driver, which is equal to a device
unplug event of a physical hardware device. The target device object may be reused
after this function is called. If this function is never called on target device
objects, they will be removed from the bus when the owning process terminates.
@param 	    vigem 	The driver connection object.
@param 	    target	The target device object.
@returns	A VIGEM_ERROR.
"""
vigem_target_remove = vigemClient.vigem_target_remove
vigem_target_remove.argtypes = (c_void_p, c_void_p)
vigem_target_remove.restype = c_uint

"""
Overrides the default Vendor ID value with the provided one.
@param 	    target	The target device object.
@param 	    vid   	The Vendor ID to set.
"""
vigem_target_set_vid = vigemClient.vigem_target_set_vid
vigem_target_set_vid.argtypes = (c_void_p, c_ushort)
vigem_target_set_vid.restype = None

"""
Overrides the default Product ID value with the provided one.
@param 	    target	The target device object.
@param 	    pid   	The Product ID to set.
"""
vigem_target_set_pid = vigemClient.vigem_target_set_pid
vigem_target_set_pid.argtypes = (c_void_p, c_ushort)
vigem_target_set_pid.restype = None

"""
Returns the Vendor ID of the provided target device object.
@param 	    target	The target device object.
@returns	The Vendor ID.
"""
vigem_target_get_vid = vigemClient.vigem_target_get_vid
vigem_target_get_vid.argtypes = (c_void_p, )
vigem_target_get_vid.restype = c_ushort

"""
Returns the Product ID of the provided target device object.
@param 	    target	The target device object.
@returns	The Product ID.
"""
vigem_target_get_pid = vigemClient.vigem_target_get_pid
vigem_target_get_pid.argtypes = (c_void_p, )
vigem_target_get_pid.restype = c_ushort

"""
Sends a state report to the provided target device.
@param 	    vigem 	The driver connection object.
@param 	    target	The target device object.
@param 	    report	The report to send to the target device.
@returns	A VIGEM_ERROR.
"""
vigem_target_x360_update = vigemClient.vigem_target_x360_update
vigem_target_x360_update.argtypes = (c_void_p, c_void_p, XUSB_REPORT)
vigem_target_x360_update.restype = c_uint

"""
Sends a state report to the provided target device.
@param 	    vigem 	The driver connection object.
@param 	    target	The target device object.
@param 	    report	The report to send to the target device.
@returns	A VIGEM_ERROR.
"""
vigem_target_ds4_update = vigemClient.vigem_target_ds4_update
vigem_target_ds4_update.argtypes = (c_void_p, c_void_p, DS4_REPORT)
vigem_target_ds4_update.restype = c_uint

"""
Note: this is a function not present in the master branch of vigem client.
This fixes https://github.com/yannbouteiller/vgamepad/issues/5.
When ctypes supports Union passed by value, this function will be removed.

Sends a full size state report to the provided target device.
@param 	    vigem 	    The driver connection object.
@param 	    target	    The target device object.
@param 	    report_ptr	A pointer to the report buffer.
@returns	A VIGEM_ERROR.
"""
vigem_target_ds4_update_ex_ptr = vigemClient.vigem_target_ds4_update_ex_ptr
vigem_target_ds4_update_ex_ptr.argtypes = (c_void_p, c_void_p, POINTER(DS4_REPORT_EX))
vigem_target_ds4_update_ex_ptr.restype = c_uint

"""
Returns the internal index (serial number) the bus driver assigned to the provided
target device object. Note that this value is specific to the inner workings of
the bus driver, it does not reflect related values like player index or device
arrival order experienced by other APIs. It may be used to identify the target
device object for its lifetime. This value becomes invalid once the target
device is removed from the bus and may change on the next addition of the
device.
@param 	    target	The target device object.
@returns	The internally used index of the target device.
"""
vigem_target_get_index = vigemClient.vigem_target_get_index
vigem_target_get_index.argtypes = (c_void_p, )
vigem_target_get_index.restype = c_ulong

"""
Returns the type of the provided target device object.
@param 	    target	The target device object.
@returns	A VIGEM_TARGET_TYPE.
"""
vigem_target_get_type = vigemClient.vigem_target_get_type
vigem_target_get_type.argtypes = (c_void_p, )
vigem_target_get_type.restype = VIGEM_TARGET_TYPE

"""
Returns TRUE if the provided target device object is currently attached to the bus,
FALSE otherwise.
@param 	    target	The target device object.
@returns	TRUE if device is attached to the bus, FALSE otherwise.
"""
vigem_target_is_attached = vigemClient.vigem_target_is_attached
vigem_target_is_attached.argtypes = (c_void_p, )
vigem_target_is_attached.restype = c_bool

"""
Returns the user index of the emulated Xenon device. This value correspondents to the
(zero-based) index number representing the player number via LED present on a
physical controller and is compatible to the dwUserIndex property of the
XInput* APIs.
@param 	    vigem 	The driver connection object.
@param 	    target	The target device object.
@param 	    index 	The (zero-based) user index of the Xenon device. (PULONG)
@returns	A VIGEM_ERROR.
"""
vigem_target_x360_get_user_index = vigemClient.vigem_target_x360_get_user_index
vigem_target_x360_get_user_index.argtypes = (c_void_p, c_void_p, c_void_p)
vigem_target_x360_get_user_index.restype = c_uint

"""
Registers a function which gets called, when LED index or vibration state changes
occur on the provided target device. This function fails if the provided
target device isn't fully operational or in an erroneous state.
@param 	vigem			The driver connection object.
@param 	target			The target device object.
@param 	notification	The notification callback.
@param 	userData		The user data passed to the notification callback.
@returns	A VIGEM_ERROR.
"""
vigem_target_x360_register_notification = vigemClient.vigem_target_x360_register_notification
vigem_target_x360_register_notification.argtypes = (c_void_p, c_void_p, c_void_p, c_void_p)
vigem_target_x360_register_notification.restype = c_uint

"""
Removes a previously registered callback function from the provided target object.
@param 	target	The target device object.
"""
vigem_target_x360_unregister_notification = vigemClient.vigem_target_x360_unregister_notification
vigem_target_x360_unregister_notification.argtypes = (c_void_p, )
vigem_target_x360_unregister_notification.restype = None

"""
Registers a function which gets called, when LightBar or vibration state changes
occur on the provided target device. This function fails if the provided
target device isn't fully operational or in an erroneous state.
@param 	vigem			The driver connection object.
@param 	target			The target device object.
@param 	notification	The notification callback.
@param 	userData		The user data passed to the notification callback.
@returns	A VIGEM_ERROR.
"""
vigem_target_ds4_register_notification = vigemClient.vigem_target_ds4_register_notification
vigem_target_ds4_register_notification.argtypes = (c_void_p, c_void_p, c_void_p, c_void_p)
vigem_target_ds4_register_notification.restype = c_uint

"""
Removes a previously registered callback function from the provided target object.
@param 	target	The target device object.
"""
vigem_target_ds4_unregister_notification = vigemClient.vigem_target_ds4_unregister_notification
vigem_target_ds4_unregister_notification.argtypes = (c_void_p, )
vigem_target_ds4_unregister_notification.restype = None
