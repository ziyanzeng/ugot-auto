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
- ps: this front end webpage might look terrible, as I am not a frontend person, it is just usable, lol

### Computer Vision
- **YOLOv8 Model**
  - Trained with a customized dataset of ping-pong balls and goals used in the UGOT soccer game.
- **Monocam Distance and Angle Measure Algorithm**
  - No depth camera or depth prediction model involved.
  - Algorithm located in `utils.get_relative_position.py`.

## 🎥 Video Demo
*Coming soon...*

## 🌟 Possible Future Updates
1. Implement a new Ball-Goal-Robot aligning algorithm to replace the current goal locking method.
2. Augment the dataset to address misdetection and no detection issues in bright, overexposed environments.
3. Frontend webpage updates
4. And more...
