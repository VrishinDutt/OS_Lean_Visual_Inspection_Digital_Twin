# OS Reliability in AI-Assisted Lean Visual Inspection

## Race Conditions and Real-Time Scheduling in a Smart Manufacturing Cell

---

## Abstract

This project investigates the role of operating-system reliability in an AI-assisted lean visual-inspection cell. The case study models a conveyor-based inspection system where products are detected by sensors, captured by cameras, processed by AI and rule-based inspection modules, and finally passed or rejected by an actuator. The project demonstrates how race conditions can corrupt product-inspection mapping when shared state is accessed without synchronization. A safe producer-consumer pipeline is then implemented to preserve product identity. Finally, Earliest Deadline First scheduling is simulated and compared with FCFS scheduling to demonstrate the importance of deadline-aware execution in real-time inspection workflows.

---

## 1. Introduction

Modern manufacturing systems increasingly depend on automation, machine vision, and AI-assisted inspection. In lean manufacturing, the objective is to reduce waste, waiting time, rework, and unnecessary human inspection burden.

However, automation shifts reliability concerns from manual inspection to software coordination. Multiple tasks may execute concurrently: sensing, image capture, AI inference, rule-based checking, decision fusion, actuator control, and logging.

If these concurrent tasks access shared data without synchronization, the result may depend on timing. This is known as a race condition.

---

## 2. Case Study Background

The project uses a smart visual-inspection cell as its case study.

The cell consists of:

- Conveyor
- Presence sensor
- Camera
- AI visual inspection module
- Rule-based inspection module
- Decision fusion module
- Reject actuator
- Logger
- Operator display

This is inspired by industrial AI visual-inspection workflows, including MELSOFT VIXIO-style systems, where camera input, AI inspection, and existing rule-based inspection can work together in an industrial quality-control pipeline.

---

## 3. Operating System Concepts Used

The project demonstrates the following OS concepts:

- Process
- Thread
- Race condition
- Critical section
- Mutual exclusion
- Lock
- Queue
- Producer-consumer problem
- Shared buffer
- Real-time scheduling
- Earliest Deadline First scheduling
- FCFS scheduling
- Deadline miss

---

## 4. Race Condition in the Inspection Cell

The unsafe system uses a global shared variable called current_product_id.

When a product enters the camera zone, the sensor task updates current_product_id. At the same time, the AI inspection task may still be processing the previous product.

This can cause the result of one product to be mapped onto another product.

Example:

Product P017 enters the inspection station.  
The AI module starts processing P017.  
Before the AI result is written, the sensor detects P030 and updates current_product_id.  
The AI result of P017 is incorrectly stored under P030.  

This is a product-inspection mapping failure.

---

## 5. Unsafe Model

The unsafe model uses concurrent threads:

- sensor_task
- ai_inspection_task
- actuator_task

The sensor updates shared state.  
The AI task reads the shared state.  
The actuator uses the inspection result.

Because there is no synchronization, the output can become inconsistent.

---

## 6. Safe Synchronized Model

The safe model removes dependence on global shared product identity.

Instead, each product receives a ProductPacket containing:

- product_id
- frame_id
- ai_result
- rule_result
- final_decision
- rejected_product_id

The packet moves through queues from sensor to camera to inspection to decision to actuator.

This preserves the product-result relationship.

---

## 7. Scheduling Algorithm

The project uses Earliest Deadline First scheduling.

Each job has:

- arrival time
- burst time
- absolute deadline

At each scheduling decision, the job with the nearest deadline is selected first.

This is relevant because a moving product must be inspected and rejected before it passes the actuator gate.

FCFS is also simulated as a baseline comparison.

---

## 8. Simulation Output

The backend produces:

- unsafe_mode_events.json
- safe_mode_events.json
- edf_schedule.json
- fcfs_schedule.json

It also generates visual outputs:

- EDF Gantt chart
- Deadline miss comparison
- Race condition comparison
- Quality decision summary

These outputs are used for browser preview and Unreal Engine digital-twin playback.

---

## 9. Results

The unsafe model produces race-condition events where inspection results are mapped to incorrect product IDs.

The safe model eliminates these race conditions by using product packets and queue-based synchronization.

The scheduling simulation demonstrates how EDF is more suitable than FCFS for real-time inspection because it considers deadlines explicitly.

---

## 10. Future Scope

The project can be extended by:

1. Adding a real defect-detection model.
2. Integrating an Unreal Engine digital twin.
3. Using real camera or image-dataset inputs.
4. Adding PLC/SCADA-style communication.
5. Comparing additional scheduling algorithms such as RMS, Round Robin, and Priority Scheduling.
6. Adding fault recovery and missed-actuation simulation.
7. Creating a technician-training simulator for lean visual-inspection cells.

---

## 11. Conclusion

This project demonstrates that race conditions are not merely theoretical programming errors. In an AI-assisted visual-inspection system, race conditions can become quality-control failures. The project shows how synchronization preserves product identity and how real-time scheduling supports deadline-sensitive inspection workflows.

---

## Additional Scheduling Algorithm: Rate Monotonic Scheduling

Rate Monotonic Scheduling is a fixed-priority real-time scheduling algorithm.

In RMS, tasks with shorter periods receive higher priority. This is relevant to the inspection-cell case study because many industrial control tasks are periodic. For example, the sensor task may run very frequently, camera capture may run at a fixed interval, AI inspection may run at a slower interval, and logging may run least frequently.

In this project, RMS is compared with EDF, FCFS, Round Robin, and Priority Scheduling. RMS provides a useful bridge between operating-system scheduling theory and embedded industrial control systems.
