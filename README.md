# OS Reliability in AI-Assisted Lean Visual Inspection

## Project Title

OS Reliability in AI-Assisted Lean Visual Inspection:  
Race Conditions and Real-Time Scheduling in a Smart Manufacturing Cell

## Premise

This project studies how operating-system level concurrency errors can affect an AI-assisted visual inspection workflow in lean manufacturing.

The system abstracts a smart manufacturing inspection cell:

Sensor -> Camera -> AI Inspection -> Rule Inspection -> Decision Fusion -> Actuator -> Logger

The project demonstrates:

1. A race condition caused by unsafe shared state.
2. A synchronized producer-consumer pipeline that fixes the issue.
3. Earliest Deadline First scheduling for real-time task execution.
4. FCFS scheduling as a baseline comparison.
5. JSON event export for Unreal Engine digital-twin replay.
6. Browser preview for quick visualization.

## Case Study

The case study is inspired by AI-assisted industrial visual inspection systems such as MELSOFT VIXIO-style workflows.

The project does not clone or integrate MELSOFT VIXIO directly.  
Instead, it abstracts the operating-system reliability layer underneath an AI-assisted inspection cell.

## Why This Is an OS Problem

Automated inspection systems involve multiple concurrent tasks:

- Sensor detection
- Camera frame capture
- AI inference
- Rule-based inspection
- Decision fusion
- Actuator control
- Logging
- Operator monitoring

These tasks share product IDs, frame IDs, inspection results, buffers, and actuator decisions.

If shared state is accessed without synchronization, the result may depend on timing rather than program logic. This creates a race condition.

## Race Condition Model

Unsafe mode uses a global shared variable:

current_product_id

When the sensor updates this variable while the AI inspection task is still processing a previous product, the AI result may be mapped to the wrong product.

Example failure:

Product P017 is inspected.  
Before the AI result is saved, the sensor updates current_product_id to P030.  
The AI result for P017 is written under P030.  
The actuator may reject or pass the wrong product.

## Synchronization Model

Safe mode uses product packets and queue discipline.

Each product receives an immutable packet:

- product_id
- frame_id
- ai_result
- rule_result
- final_decision
- rejected_product_id

The packet moves through the pipeline, so product identity is preserved.

## Scheduling Model

The project uses Earliest Deadline First scheduling.

Each product creates jobs such as:

- sensor
- camera
- ai_inspection
- rule_inspection
- decision_fusion
- actuator
- logger

Each job has:

- arrival time
- burst time
- absolute deadline

EDF schedules the job with the nearest deadline first.

FCFS is used as a comparison baseline.

## Folder Structure

backend/
- unsafe_race_model.py
- synchronized_pipeline.py
- edf_scheduler.py
- fcfs_scheduler.py
- metrics.py
- summary_charts.py
- event_exporter.py
- validate_events.py
- replay_events.py
- run_all.py

simulation_events/
- unsafe_mode_events.json
- safe_mode_events.json
- edf_schedule.json
- fcfs_schedule.json

visual_outputs/
- edf_gantt_chart.png
- deadline_miss_comparison.png
- race_condition_comparison.png
- quality_decision_summary.png

preview/
- index.html

docs/
- UNREAL_EVENT_SCHEMA.md

## Setup

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run

./run_project.sh

## Terminal Replay

python -m backend.replay_events

Choose:

1. Unsafe race-condition mode
2. Safe synchronized mode
3. EDF scheduling mode
4. FCFS scheduling mode

## Browser Preview

python3 -m http.server 8000

Open:

http://localhost:8000/preview/

## Unreal Engine Integration

Python exports JSON event timelines.

Unreal Engine can read these timelines and animate:

- product movement
- sensor detection
- camera flash
- AI inspection station
- actuator rejection
- race-condition warning
- deadline miss warning

The event schema is documented in:

docs/UNREAL_EVENT_SCHEMA.md

## Future Scope

1. Replace synthetic product defects with real visual defect datasets.
2. Add a lightweight anomaly-detection model.
3. Connect the simulation to an Unreal Engine digital twin.
4. Use a MELSOFT VIXIO-style AI inspection node in a real industrial workflow.
5. Add PLC/SCADA-style communication using MQTT or OPC-UA.
6. Compare EDF, FCFS, Round Robin, Priority Scheduling, and RMS.
7. Extend the model to include deadlock, starvation, and fault recovery.
8. Build a technician-facing training simulator for visual-inspection cells.
