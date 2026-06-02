# Scheduling Comparative Analysis

## Algorithms Compared

- Earliest Deadline First
- First Come First Serve
- Round Robin
- Priority Scheduling
- Rate Monotonic Scheduling

## Metrics Table

| algorithm   |   total_jobs |   missed_deadlines |   average_waiting_time |   average_turnaround_time |
|:------------|-------------:|-------------------:|-----------------------:|--------------------------:|
| EDF         |           56 |                 38 |                 101.11 |                    106.25 |
| RMS         |           56 |                 32 |                 104    |                    109.14 |
| FCFS        |           56 |                 40 |                 113    |                    118.14 |
| Round Robin |           56 |                 43 |                 126.11 |                    131.25 |
| Priority    |           56 |                 37 |                 102.71 |                    107.86 |

## Interpretation

- Best algorithm by missed deadlines: **RMS** with **32** missed deadlines.
- Best algorithm by average waiting time: **EDF** with **101.11** time units.
- Best algorithm by average turnaround time: **EDF** with **106.25** time units.

## Case Study Interpretation

In an AI-assisted visual inspection cell, deadline misses represent products reaching the actuator before the required sensing, inspection, decision, or logging tasks finish. Therefore, the most suitable algorithm is not merely the one with the lowest waiting time, but the one that protects time-critical inspection and rejection operations.

EDF is the most thematically suitable algorithm because the conveyor-based inspection cell is deadline-driven. RMS is also relevant because industrial control tasks often repeat periodically, and RMS gives higher priority to tasks with shorter periods. FCFS is simple but ignores urgency. Round Robin improves fairness but may fragment urgent work. Priority Scheduling can protect critical tasks such as sensor and actuator operations, but its effectiveness depends heavily on correct priority assignment.
