#!/usr/bin/python
import time
import Robot
from RemoteControl import RemoteControl

robot = Robot.Robot(left_id=1, right_id=3, left_trim=0, right_trim=0)
remoteControl = RemoteControl(robot)


def main():
    print "Starting Move2..."
    while True:
        remoteControl.update()
        time.sleep(1)


if __name__ == "__main__":
    main()
