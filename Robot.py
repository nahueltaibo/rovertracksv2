import time
import atexit
import math
from utils import mapBetweenRanges
from Adafruit_MotorHAT import Adafruit_MotorHAT


class Robot(object):
    def __init__(self, addr=0x60, left_id=1, right_id=3, left_trim=0, right_trim=0, stop_at_exit=True):
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - left_id: The ID of the left motor, default is 1.
         - right_id: The ID of the right motor, default is 2.
         - left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Adafruit_MotorHAT(addr)
        self._left = self._mh.getMotor(left_id)
        self._right = self._mh.getMotor(right_id)
        self._left_trim = left_trim
        self._right_trim = right_trim
        # Start with motors turned off.
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._left_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._left.setSpeed(speed)

    def _right_speed(self, speed):
        """Set the speed of the right motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._right_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._right.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def right(self, speed, seconds=None):
        """Spin to the right at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def left(self, speed, seconds=None):
        """Spin to the left at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def move(self, x_speed, y_speed):
        """This methods acceps x, and y between -100 and 100
        Think of those values as the percentage were each joystick axis is positioned
        -100 = stick fully back (or left)
        0 = stick in center resting
        100 = stick fuly forward (or right)
        :param x_speed: x joystick position (-100 to 100)
        :param y_speed: y joystick position (-100 to 100)
        """
        assert -100 <= x_speed <= 100, 'x_peed must be a value between -100 and 100 inclusive!'
        assert -100 <= y_speed <= 100, 'y_peed must be a value between -100 and 100 inclusive!'

        # if any of the speeds is None, then set the value associated with no movement
        left_speed, right_speed = self.joystickToDiff(x_speed, y_speed, -255, 255)

        # Set motor speed and move both forward.
        self._left_speed(int(abs(left_speed)))
        if left_speed >= 0:
            self._left.run(Adafruit_MotorHAT.FORWARD)
        else:
            self._left.run(Adafruit_MotorHAT.BACKWARD)

        self._right_speed(int(abs(right_speed)))
        if right_speed >= 0:
            self._right.run(Adafruit_MotorHAT.FORWARD)
        else:
            self._right.run(Adafruit_MotorHAT.BACKWARD)

    def joystickToDiff(self, x, y, minSpeed, maxSpeed):
        """
        This methods acceps x, and y between -100 and 100
        Think of those values as the percentage were each joystick axis is positioned
        -100 = stick fully back (or left)
        0 = stick in center resting
        100 = stick fuly forward (or right)
        :param x: position of the joystick's x axis (between -100 and 100)
        :param y: position of the joystick's y axis (between -100 and 100)
        :param minSpeed: minimum speed supported by the wheel
        :param maxSpeed: maximum speed supported by the wheel
        :return: The pair of speed values to send to left and right wheels
        """
        assert -100 <= x <= 100, 'x_peed must be a value between -100 and 100 inclusive!'
        assert -100 <= y <= 100, 'y_peed must be a value between -100 and 100 inclusive!'

        # If in_x and in_y are 0, then there is not much to calculate...
        if x == 0 and y == 0:
            return 0, 0

        # First Compute the angle in deg
        # First hypotenuse
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(math.fabs(x) / z)

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the coeff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
        turn = round(turn * 100, 0) / 100

        # And max of y or x is the movement
        mov = max(math.fabs(y), math.fabs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = mov
            rawRight = turn
        else:
            rawRight = mov
            rawLeft = turn

        # Reverse polarity
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0 - rawRight

        # Map the values from the work range (-100 to 100)
        # onto the requested output range (minSpeed to maxSpeed)
        rightOut = mapBetweenRanges(rawRight, -100, 100, minSpeed, maxSpeed)
        leftOut = mapBetweenRanges(rawLeft, -100, 100, minSpeed, maxSpeed)

        return rightOut, leftOut
