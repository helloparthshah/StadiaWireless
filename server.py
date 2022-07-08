from flask import Flask, render_template, request
from flask_sock import Sock
import socket
import vgamepad as vg
import json
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
import threading
import ctypes
import datetime

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
sock = Sock(app)
gamepad = None

notif = None


def create_image():
    # Open logo.png
    image = Image.open("logo.png")
    # Resize the image heigh 64 and preserve the aspect ratio
    image.thumbnail((64, 64), Image.ANTIALIAS)
    return image


@sock.route('/controller')
def controller(ws):
    def my_callback(client, target, large_motor, small_motor, led_number, user_data):
        notif = {
            'lm': large_motor,
            'sm': small_motor,
            'led': led_number,
            'time': str(datetime.datetime.now())
        }
        ws.send(json.dumps(notif))
    global gamepad
    if gamepad == None:
        gamepad = vg.VX360Gamepad()
    gamepad.register_notification(callback_function=my_callback)
    while True:
        if not ws.connected:
            gamepad.close()
            gamepad = None
            break
        message = ws.receive()
        if message.startswith('{'):
            message = json.loads(message)
            gamepad.left_joystick(
                int(message['lx']*32767), -int(message['ly']*32767))
            gamepad.right_joystick(
                int(message['rx']*32767), -int(message['ry']*32767))
            if message['0'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            elif message['0'] == False:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            if message['1'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            elif message['1'] == False:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            if message['2'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            elif message['2'] == False:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            if message['3'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            elif message['3'] == False:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            if message['4'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            elif message['4'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            if message['5'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            elif message['5'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            gamepad.left_trigger(int(message['6']*255))
            gamepad.right_trigger(int(message['7']*255))
            if message['8'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
            elif message['8'] == False:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
            if message['9'] == True:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            elif message['9'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            if message['10'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            elif message['10'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            if message['11'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            elif message['11'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            if message['12'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            elif message['12'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            if message['13'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            elif message['13'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            if message['14'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            elif message['14'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            if message['15'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            elif message['15'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            if message['16'] == True:
                gamepad.press_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
            elif message['16'] == False:
                gamepad.release_button(
                    button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
            gamepad.update()


@app.route('/')
def index():
    return render_template('index.html')


hostname = socket.gethostname()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 0))
port = sock.getsockname()[1]
sock.close()


def runServer():
    print("Open this webpage in your mobile: http://"+hostname+':'+str(port))
    app.run(host='0.0.0.0', port=port)


class thread_with_exception(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):

        # target function of the thread class
        try:
            runServer()
        finally:
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


t = thread_with_exception('thread_with_exception')
t.start()


def exit(icon):
    global t
    t.raise_exception()
    t.join()
    icon.visible = False
    icon.stop()


def startIcon():
    import webbrowser
    icon('test', Image.open('logo.ico'), menu=menu(
        item(
            'http://'+hostname+':'+str(port),
            action=lambda: webbrowser.open('http://'+hostname+':'+str(port))
        ),
        item('http://'+socket.gethostbyname(socket.gethostname())+':'+str(port),
             action=lambda: webbrowser.open('http://'+socket.gethostbyname(socket.gethostname())+':'+str(port))),
        item(
            'Exit',
            action=exit
        )
    )).run()


startIcon()
