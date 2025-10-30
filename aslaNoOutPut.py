import ctypes
import ctypes.util
import pyaudio
import sys

if sys.platform.startswith("linux"):
    # Load ALSA library
    asound = ctypes.cdll.LoadLibrary(ctypes.util.find_library('asound'))

    # Define a no-op error handler
    def py_error_handler(filename, line, function, err, fmt):
        pass

    # Convert Python function to C callback
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                          ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    # Tell ALSA to use the no-op error handler
    asound.snd_lib_error_set_handler(c_error_handler)
