from utils import mapBetweenRanges
from evdev import InputDevice, ecodes, list_devices


class RemoteControl(object):
    gamepad = None
    robot = None
    # Initial state of speed on each wheel
    x_speed = 0
    y_speed = 0

    def __init__(self, robot):
        print "Starting RemoteControl..."
        self.robot = robot
        self.try_connect_gamepad()

    def try_connect_gamepad(self):
        devices = map(InputDevice, list_devices())
        for device in devices:
            if device.name.lower() == 'gamepad':
                # prints out device info at start
                self.gamepad = device
                print(self.gamepad)

    def update(self):
        if self.gamepad is None:
            # If there is no gamepad, check if one got connected...
            self.try_connect_gamepad()
        else:
            try:
                # read and process every message
                for event in self.gamepad.read_loop():
                    self.updateMotors(event)
            except:
                print "Gamepad disconnected."
                self.gamepad = None

    def updateMotors(self, event):
        # joystick goes from 0 to 255,
        # we need to convert this to two values from -100 to 100,
        # that is what the Robot accepts

        if event.type == ecodes.EV_ABS:
            # if event.code == ecodes.ABS_X:
            #     print('ABS_X : ' + str(event.value))
            if event.code == ecodes.ABS_Z:
                print('ABS_Z : ' + str(event.value))
                self.x_speed = int(mapBetweenRanges(event.value, 255, 0, -100, 100))
                self.robot.move(self.x_speed, self.y_speed)

            #elif event.code == ecodes.ABS_Y:
            elif event.code == ecodes.ABS_RZ:
                # print('ABS_Y : ' + str(event.value))
                print('ABS_RZ : ' + str(event.value))
                self.y_speed = int(mapBetweenRanges(event.value, 255, 0, -100, 100))
                self.robot.move(self.x_speed, self.y_speed)
