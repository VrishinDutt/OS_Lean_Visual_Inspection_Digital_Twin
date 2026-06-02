# Presentation Outline

## Slide 1: Title

OS Reliability in AI-Assisted Lean Visual Inspection  
Race Conditions and Real-Time Scheduling in a Smart Manufacturing Cell

## Slide 2: Problem Statement

Automated inspection cells run multiple concurrent tasks.  
If these tasks access shared product state without synchronization, the system can corrupt inspection results.

## Slide 3: Case Study

Lean visual-inspection cell:

Sensor -> Camera -> AI Inspection -> Rule Inspection -> Decision Fusion -> Actuator -> Logger

## Slide 4: Why This Is an OS Problem

The system contains:

- Threads
- Shared memory
- Critical sections
- Buffers
- Scheduling deadlines
- Real-time actuator decisions

## Slide 5: Race Condition

Unsafe shared variable:

current_product_id

Failure:

AI result for one product is mapped to another product.

## Slide 6: Unsafe Simulation

Show terminal replay or browser preview.

Key result:

Race events appear.

## Slide 7: Synchronization Fix

Use:

- ProductPacket
- Queue
- Producer-consumer pipeline
- No global shared product identity

## Slide 8: Safe Simulation

Show browser preview.

Key result:

Race events become zero.

## Slide 9: Scheduling Requirement

A product is moving on a conveyor.  
The inspection and actuator decision must finish before the product crosses the reject gate.

## Slide 10: EDF Scheduling

Earliest Deadline First chooses the job with the nearest deadline.

Show EDF Gantt chart.

## Slide 11: FCFS Comparison

FCFS is simple but not deadline-aware.

Show deadline miss comparison.

## Slide 12: Unreal Engine Digital Twin

Python generates JSON events.  
Unreal Engine can use these events to animate the visual-inspection cell.

## Slide 13: MELSOFT VIXIO-Inspired Workflow

The project abstracts the OS reliability layer underneath an AI-assisted industrial visual-inspection workflow.

## Slide 14: Results

Unsafe mode:
- Race conditions occur
- Product-result mapping fails

Safe mode:
- Product identity preserved
- Race condition count becomes zero

Scheduling:
- EDF aligns better with real-time inspection

## Slide 15: Future Scope

- Actual defect-detection model
- Unreal Engine digital twin
- PLC/SCADA communication
- MELSOFT VIXIO-style integration
- Technician training simulator

## Slide 16: Conclusion

Race conditions in automated inspection systems can become real quality-control failures.  
Synchronization and deadline-aware scheduling are essential for reliable AI-assisted manufacturing cells.

## Additional Slide: RMS Scheduling

Rate Monotonic Scheduling assigns higher priority to tasks with shorter periods.

In the inspection-cell model:

- Sensor task has the shortest period
- Camera task runs frequently
- AI inspection has a longer period
- Logger has the longest period

RMS is useful as a real-time scheduling comparison because manufacturing and embedded-control tasks are often periodic.
