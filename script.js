var noSleep = new NoSleep();

/* document.addEventListener('touchstart', function enableNoSleep() {
    document.removeEventListener('touchstart', enableNoSleep, false);
    noSleep.enable();
}, false);
 */
let gamepadIndex;
window.addEventListener('gamepadconnected', (event) => {
    noSleep.enable();
    gamepadIndex = event.gamepad.index;
});

let buttons = {
    0: false,
    1: false,
    2: false,
    3: false,
    4: false,
    5: false,
    6: 0,
    7: 0,
    8: false,
    9: false,
    10: false,
    11: false,
    12: false,
    13: false,
    14: false,
    15: false,
    16: false,
    17: false,
    18: false,
    "lx": 0,
    "ly": 0,
    "rx": 0,
    "ry": 0,
}


let connected = false;
let socket = new WebSocket("ws://" + ip);
socket.onopen = function (e) {
    connected = true;
    console.log("[open] Connection established");
};

socket.onmessage = function (event) {
    console.log(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function (event) {
    connected = false;
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

socket.onerror = function (error) {
    console.log(`[error] ${error.message}`);
};


setInterval(() => {
    if (gamepadIndex !== undefined) {
        // a gamepad is connected and has an index
        const myGamepad = navigator.getGamepads()[gamepadIndex];
        buttons["lx"] = myGamepad.axes[0];
        buttons["ly"] = myGamepad.axes[1];
        buttons["rx"] = myGamepad.axes[2];
        buttons["ry"] = myGamepad.axes[3];
        document.body.innerHTML = ""; // reset page
        myGamepad.buttons.map(e => e.pressed).forEach((isPressed, buttonIndex) => {
            if (buttonIndex == 6 || buttonIndex == 7) {
                buttons[buttonIndex] = myGamepad.buttons[buttonIndex].value;
            }
            else if (isPressed) {
                buttons[buttonIndex] = true;

                // button is pressed; indicate this on the page
                document.body.innerHTML += `<h1>Button ${buttonIndex} is pressed</h1>`;
            } else {
                buttons[buttonIndex] = false;
            }
        })
        socket.send(JSON.stringify(buttons));
    }
}, 1)