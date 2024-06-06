# 🤖 UGOT Robot Auto Demo

## Introduction
Welcome to the **UGOT Robot Auto Demo**! This project showcases the autonomous control of the UBTech UGOT Robot in a soccer game scenario. The robot can independently lock onto and kick a ball, demonstrating a small but significant part of the UGOT soccer game.

## Control Methods
- **Manual Command Selection Control**
- **Full Autonomous Mode**

## Features
### Command Set Control
*Easy to expand!*
- Commands implement methods declared under the `Command` class.
- Inspired by the WPILib command set control logic from the FIRST Robotics Competition.

### Webpage Control Panel
*Integrated with a local server, communicates via WebSocket*
- **Manual Command Selection Buttons**
- **Video Stream Preview**
- **PID Tuning with Reaction Curve**
  - Maintains data from the past 50 ticks of the program run.
- PS: this front end webpage might look terrible, as I am not a frontend person, it is just usable, lol

### Computer Vision
- **YOLOv8 Model**
  - Trained with a customized dataset of ping-pong balls and goals used in the UGOT soccer game.
- **Monocam Distance and Angle Measure Algorithm**
  - No depth camera or depth prediction model is involved.
  - Algorithm located in `utils.get_relative_position.py`.

## 🎥 Video Demo
*Coming soon...*

## 🤩 Get Started
1. Installed all the required packages
2. Make sure that the UGOT robot is connected to the same WiFi as your computer
3. Config the IP of the robot in the `config.py` file
4. Open a terminal and go to the ~/static directory to run `python -m http.server` to start the webpage service
5. Open `http://localhost:8000/index.html` in the browser to view the panel
6. Open another terminal and go back to the root directory then run `python main.py` to start the program
   - the default mode is the autonomous mode, so the robot will start locating the ball as soon as your computer is connected to the robot
   - an Opencv frame will be pulled up on your computer, this frame should have better video quality than the frame shown on the webpage
   - to switch to manual command selection mode, go to `~/threads/control_thread.py` then comment out the line `command_planner.update(update_signal)` at line 46, then you will be able to control the robot fully through the buttons on the webpage

## 🌟 Possible Future Updates
1. Implement a new Ball-Goal-Robot aligning algorithm to replace the current goal-locking method.
2. Augment the dataset to address misdetection and no-detection issues in bright, overexposed environments.
3. Frontend webpage updates
4. And more...
