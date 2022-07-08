var noSleep = new NoSleep();

document.addEventListener(
	'click',
	function enableNoSleep() {
		document.removeEventListener('click', enableNoSleep, false);
		noSleep.enable();
	},
	false
);
const sections = {
	pending: document.getElementById('Pending'),
	active: document.getElementById('Active'),
};

let gamepadIndex;
window.addEventListener('gamepadconnected', (event) => {
	noSleep.enable();
	gamepadIndex = event.gamepad.index;
});

const buttons = {
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
};

let connected = false;
const url = window.location.href.replace('http', 'ws');
let socket = new WebSocket(url + '/controller');
socket.onopen = function (e) {
	connected = true;
	console.log('[open] Connection established');
};

const vibrate = async (data) => {
	if (navigator.getGamepads()[gamepadIndex].vibrationActuator)
		await navigator.getGamepads()[gamepadIndex].vibrationActuator.playEffect('dual-rumble', {
			startDelay: 0,
			duration: 500,
			weakMagnitude: data.sm / 255,
			strongMagnitude: data.lm / 255,
		});
};

socket.onmessage = function (event) {
	console.log(`[message] Data received from server: ${event.data}`);
	let data = JSON.parse(event.data);
	console.log(data.lm);
	console.log(data.sm);
	// vibrate controller
	if (gamepadIndex !== undefined) {
		vibrate(data).then(() => {
			if (data.lm > 0 || data.sm > 0) {
				vibrate(data);
			}
		});
	}
};

socket.onclose = function (event) {
	connected = false;
	if (event.wasClean) {
		console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
	} else {
		console.log('[close] Connection died');
	}
};

socket.onerror = function (error) {
	console.log(`[error] ${error.message}`);
};

const update = () => {
	if (gamepadIndex !== undefined) {
		// a gamepad is connected and has an index
		const myGamepad = navigator.getGamepads()[gamepadIndex];
		buttons['lx'] = myGamepad.axes[0];
		buttons['ly'] = myGamepad.axes[1];
		buttons['rx'] = myGamepad.axes[2];
		buttons['ry'] = myGamepad.axes[3];
		sections.pending.classList.remove('visible');
		sections.active.classList.add('visible');
		myGamepad.buttons
			.map((e) => e.pressed)
			.forEach((isPressed, buttonIndex) => {
				if (buttonIndex == 6 || buttonIndex == 7) {
					buttons[buttonIndex] = myGamepad.buttons[buttonIndex].value;
				} else if (isPressed) {
					buttons[buttonIndex] = true;
				} else {
					buttons[buttonIndex] = false;
				}
			});
		UpdateDisplay();
		socket.send(JSON.stringify(buttons));
	} else {
		sections.active.classList.remove('visible');
		sections.pending.classList.add('visible');
	}
};

const loop = () => {
	update();
	requestAnimationFrame(loop);
};
loop();

// Display Management

const buttonElems = {
		0: document.getElementById('ButtonA'),
		1: document.getElementById('ButtonB'),
		2: document.getElementById('ButtonX'),
		3: document.getElementById('ButtonY'),
		4: document.getElementById('ShoulderLeft'),
		5: document.getElementById('ShoulderRight'),
		6: document.getElementById('TriggerLeft'),
		7: document.getElementById('TriggerRight'),
		8: document.getElementById('ButtonOptions'),
		9: document.getElementById('ButtonMenu'),
		10: document.getElementById('ButtonLeftStick'),
		11: document.getElementById('ButtonRightStick'),
		12: document.getElementById('DpadUp'),
		13: document.getElementById('DpadDown'),
		14: document.getElementById('DpadLeft'),
		15: document.getElementById('DpadRight'),
		16: document.getElementById('ButtonStadia'),
		17: document.getElementById('ButtonAssistant'),
		18: document.getElementById('ButtonCapture'),
		LStick: document.getElementById('StickLeft'),
		RStick: document.getElementById('StickRight'),
	},
	stickValues = {
		LStick: 0,
		RStick: 0,
	};

function UpdateDisplay() {
	for (let buttonIndex = 0; buttonIndex < 19; buttonIndex++) {
		const buttonValue = buttons[buttonIndex];
		if (buttonElems[buttonIndex]) {
			if (buttonIndex == 6 || buttonIndex == 7) {
				buttonElems[buttonIndex].style.strokeDashoffset = 338 - buttonValue * 338;
				continue;
			}
			if (buttonValue) {
				buttonElems[buttonIndex].classList.add('active');
				continue;
			}
			buttonElems[buttonIndex].classList.remove('active');
		} else {
			console.log(buttonIndex);
		}
	}
	buttonElems.LStick.style.transform = 'translate(' + buttons['lx'] + '%, ' + buttons.['ly'] + '%)';
	buttonElems.RStick.style.transform = 'translate(' + buttons['rx'] + '%, ' + buttons.['ry'] + '%)';
}