# Stadia Wireless
![image](https://j.gifs.com/28oNLW.gif)

Stadia Wireless enables you to use your stadia controller wirelessly. Not just with stadia, but with any game.

## Stadia has been shut dowm

![image](https://user-images.githubusercontent.com/35399171/214456250-032f3d2a-7615-449e-a6f4-137a607c4dd0.png)

Stadia was [shut down](https://stadia.google.com/gg/) on January 18, 2023.

Google released a [web tool](https://stadia.google.com/controller) which is available until December 31, 2023 to switch the controller from the normal wifi mode to using Bluetooth LE.

## How to use Stadia Wireless
[Demo](https://www.youtube.com/watch?v=tBFfNh7ldqo&ab_channel=ParthShah)

First, you need to install python3 if you don't already have it.
[Python Install Guide](https://realpython.com/installing-python/)

Download the latest release from the [releases](https://github.com/helloparthshah/StadiaWireless/releases/)

Directly run the server by downloading the pre installed zip file and running server.exe

You'll see a icon in the System Tray and right clicking on it will show you the website you'll need to access.

Open the webpage on your phone, connect your controller to your phone through usb and enjoy!

*TIP: In order to make it easier to open the webpage, you can open up the webpage in chrome by clicking on the link and sending it to your device or generating a QR code.*

## FAQ

- I encountered a `VIGEM_ERROR_BUS_NOT_FOUND` error

Try installing `vgamepad` by executing `pip install vgamepad`
If that still doesn't work then try installing https://vigem.org/Downloads/

- Website says "No Controller Connected"

Make sure the controller is not connected to the Stadia app

- I modified the code and want to create a release.

I used pyinstaller to generate the releases. Run the command
```
pyinstaller --noconfirm --onedir --windowed --icon "D:/Projects/pythonProjects/StadiaWireless/logo.ico" --add-data "D:/Projects/pythonProjects/StadiaWireless/static;static/" --add-data "D:/Projects/pythonProjects/StadiaWireless/templates;templates/" --add-data "D:/Projects/pythonProjects/StadiaWireless/vgamepad;vgamepad/"  "D:/Projects/pythonProjects/StadiaWireless/server.py"
```
and replace the paths with your paths

- Linux and macOS versions?

I'm still looking into how to emulate controllers in Linux and macOs. For now, I'm thinking of using evdev for Linux and foohid for macos.
