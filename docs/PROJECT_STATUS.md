# Project Status

## Current Status

The project is functional as a software artifact.

## Implemented

### Race Condition Simulation

- Unsafe shared-state model
- Race-condition event generation
- Product-result mapping corruption
- Safe synchronized queue-based pipeline
- ProductPacket identity preservation

### Scheduling Simulation

Implemented algorithms:

- Earliest Deadline First
- First Come First Serve
- Round Robin
- Priority Scheduling

Metrics generated:

- Missed deadlines
- Average waiting time
- Average turnaround time

### Visualization

Implemented:

- Terminal replay
- Browser simulation preview
- Race-condition comparison chart
- Quality decision summary chart
- EDF Gantt chart
- All-scheduler comparative charts

### Unreal Handoff

Generated:

- JSON event files
- CSV event tables
- Unreal handoff document
- Unreal README
- Event schema documentation

## Main Academic Claim

Race conditions in automated visual-inspection systems can become quality-control failures because inspection results may be mapped to the wrong product.

Synchronization preserves product identity.

Deadline-aware scheduling is important because products move physically through a conveyor cell and actuator decisions must complete before the product passes the rejection point.

## Best Algorithmic Interpretation

EDF is the most suitable scheduling algorithm for the case study because the system is deadline-driven.

Priority Scheduling is industrially intuitive because sensor and actuator tasks may be treated as critical.

Round Robin improves fairness but can fragment urgent work.

FCFS is simple but weak for real-time inspection because it ignores deadlines and task criticality.

## Recommended Demo Flow

1. Run ./run_project.sh
2. Show unsafe terminal replay.
3. Show safe terminal replay.
4. Open browser preview.
5. Show unsafe mode.
6. Show safe mode.
7. Show EDF, FCFS, Round Robin, and Priority modes.
8. Open visual_outputs.
9. Explain charts.
10. Explain Unreal handoff and future scope.

## Remaining Optional Enhancements

- Add RMS scheduling.
- Add actual image-defect model.
- Add Unreal Engine scene.
- Add real camera or dataset input.
- Convert report draft to PDF.
- Convert presentation outline to PPTX.

## RMS Added

Rate Monotonic Scheduling has been added as an additional real-time scheduling comparison.

RMS is relevant because the inspection cell can be modelled as a set of periodic control tasks:

- Sensor polling
- Camera capture
- Rule inspection
- AI inspection
- Actuator control
- Logging

In RMS, shorter-period tasks receive higher priority.
This makes it useful for embedded and real-time control-style systems.

