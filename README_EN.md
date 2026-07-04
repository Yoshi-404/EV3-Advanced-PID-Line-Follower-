# EV3 Advanced PID Line Follower 

An autonomous navigation system for line-follower robots using the LEGO Mindstorms EV3 brick and the Pybricks (MicroPython) library. This project implements an optimized Proportional-Integral-Derivative (PID) controller featuring real-time calculation ($dt$), dynamic curve braking, and anti-windup architecture.

## Features

* **Time-Domain PID Control:** The derivative term is calculated using the real elapsed time of each processing loop (`StopWatch`), preventing physical micro-jitters caused by CPU lag.
* **Dynamic Velocity (Adaptive Braking):** The robot adjusts its base speed relative to the current error margin. It accelerates on straights and automatically decelerates on sharp turns to maintain traction and stay on track.
* **Interactive Calibration:** An onboard guided setup sequence via the EV3 screen reads the exact environmental light reflection values (white and black) to autonomously calculate the precise `offset` (setpoint).
* **Anti-Windup Protection:** Hard limits applied to the integral accumulator to prevent aggressive overcorrection or loss of control after prolonged periods off the line.
* **Object-Oriented Architecture:** Clean, class-based code structure designed for easy maintenance, scalability, and rapid parameter tuning.

## Hardware Requirements

* 1x LEGO Mindstorms EV3 Brick
* 2x EV3 Large Motors (Drive)
* 1x EV3 Color Sensor
* Connection cables

**Port Mapping:**
* **Port A:** Right Motor
* **Port D:** Left Motor
* **Port S1:** Color Sensor (facing the floor)

## Software Requirements

* [Pybricks MicroPython](https://pybricks.com/) flashed onto the EV3 (via MicroSD card).
* Visual Studio Code with the EV3 MicroPython extension (or the Pybricks web IDE).

## How to Run

1. Build the robot and connect the motors and color sensor to the specified ports.
2. Deploy the `main.py` script to the EV3 brick.
3. Upon starting the program, follow the on-screen instructions:
   * Place the sensor over the **WHITE** area of the track and press any brick button.
   * Place the sensor directly over the **BLACK** line and press any brick button.
4. The system will calculate the optimal setpoint, sound a double beep, and immediately begin autonomous navigation using the PID algorithm.

## Tuning Parameters
To adapt the robot to different track geometries or physical builds, adjust the following variables in the `__init__` method of the `SeguidorDeLinha` class:
* `self.kp`, `self.ki`, `self.kd`: The core tuning constants for the PID controller.
* `self.tp_maximo`: Target base speed for straightaways (e.g., 300).
* `self.fator_frenagem`: The multiplier that dictates how sharply speed decreases relative to the tracking error.