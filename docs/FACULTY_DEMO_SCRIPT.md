# Faculty Demo Script

## Opening

This project studies race conditions and scheduling in the context of an AI-assisted lean visual-inspection cell.

Instead of using a generic bank account or ticket booking race-condition example, the case study uses a product inspection line. This makes the OS concepts easier to connect to real automation and manufacturing systems.

## System Explanation

The simulated inspection cell has seven stages:

Sensor, Camera, AI Inspection, Rule Inspection, Decision Fusion, Actuator, and Logger.

Each stage is treated as an operating-system task or thread.

The shared resources are product ID, frame ID, inspection result, decision result, and actuator command.

## Race Condition Explanation

In the unsafe model, the sensor task keeps updating a global variable called current_product_id.

The AI inspection task also reads this variable.

If the sensor updates the product ID before the AI task finishes writing the previous product's result, the result can be mapped to the wrong product.

This creates a race condition.

In a real inspection system, this could mean that a defective product passes or a good product is rejected.

## Unsafe Demo

Now I am running the unsafe mode.

The race-condition count is non-zero.

In the replay, red events indicate product-result mapping corruption.

The system is logically correct in terms of individual functions, but unreliable because concurrent access is not synchronized.

## Safe Demo

Now I am running the safe synchronized mode.

Instead of relying on global shared product identity, every product gets a ProductPacket.

The ProductPacket moves through the pipeline using queues.

This preserves the relationship between product ID, camera frame, inspection result, and actuator decision.

The race-condition count becomes zero.

## Scheduling Demo

The second part of the project simulates scheduling.

In this case study, scheduling matters because a product is physically moving on a conveyor. Inspection and actuator tasks must finish before the product reaches the reject gate.

I used Earliest Deadline First scheduling because it chooses the task with the nearest deadline first.

I also implemented FCFS as a baseline comparison.

The generated charts compare deadline misses and show the EDF Gantt chart.

## Unreal / Digital Twin Explanation

The browser preview is a lightweight visualization.

The project is also structured for Unreal Engine.

Python generates JSON and CSV event timelines.

Unreal can consume those timelines and animate a 3D inspection cell with a conveyor, sensor, camera, AI inspection node, actuator, and status board.

## MELSOFT VIXIO Angle

The project is inspired by industrial AI visual-inspection workflows such as MELSOFT VIXIO.

The goal is not to clone that software.

The goal is to model the OS reliability layer underneath such systems: synchronization, race prevention, and real-time scheduling.

## Conclusion

The conclusion is that race conditions are not only theoretical programming errors.

In an automated inspection line, they can become quality-control failures.

The project shows how synchronization preserves product identity and how deadline-aware scheduling supports reliable inspection.
