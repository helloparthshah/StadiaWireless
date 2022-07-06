import asyncio
from websockets import serve
import vgamepad as vg
import json
import os
import socket

port = os.environ.get('PORT', '80')
gamepad = vg.VX360Gamepad()


async def handler(websocket):
    async for message in websocket:
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


async def main():
    print(socket.gethostbyname(socket.gethostname()))
    with open('ip.js', 'w') as f:
        f.write("let ip=\"" + socket.gethostbyname(socket.gethostname())+"\";")
    print("Connecting to: " + '0.0.0.0' + ":" + str(port))
    async with serve(handler, '0.0.0.0', port):
        await asyncio.Future()

asyncio.run(main())
