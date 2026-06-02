# Unreal Engine Event Schema

This project exports JSON events from the Python OS simulation backend.

Unreal Engine can consume these event files to animate a lean visual-inspection digital twin.

## Event File Location

simulation_events/
- unsafe_mode_events.json
- safe_mode_events.json
- edf_schedule.json
- fcfs_schedule.json

## Core Event Format

{
  "time": 12.5,
  "product_id": "P005",
  "event": "inspection_complete",
  "mode": "safe",
  "status": "normal"
}

## Fields

time:
Simulation timestamp.

product_id:
Product identifier.

event:
Event name.

mode:
Simulation mode. Possible values: unsafe, safe, edf, fcfs.

status:
Event status. Possible values: normal, race, scheduled, deadline_missed.

## Important Event Types

Product flow events:
- sensor_detected
- camera_frame_attached
- inspection_complete
- decision_fused
- actuator_reject
- actuator_pass

Race condition events:
- race_condition_result_mapped_to_<wrong_product_id>

Scheduling events:
- sensor_started
- sensor_completed
- camera_started
- camera_completed
- ai_inspection_started
- ai_inspection_completed
- rule_inspection_started
- rule_inspection_completed
- decision_fusion_started
- decision_fusion_completed
- actuator_started
- actuator_completed
- logger_started
- logger_completed

## Unreal Mapping

sensor_detected:
Spawn or highlight product at sensor gate.

camera_frame_attached:
Flash camera station.

inspection_complete:
Show AI or rule inspection indicator.

decision_fused:
Show pass or reject decision.

actuator_reject:
Move product to reject bin.

actuator_pass:
Move product to pass lane.

race_condition_*:
Trigger red warning pulse.

*_started:
Highlight corresponding station.

*_completed:
Turn station indicator off.

deadline_missed:
Show missed-deadline warning.

## Recommended Unreal Blueprint Logic

1. Load JSON file.
2. Sort events by time.
3. Spawn products using product_id.
4. Use a timer to replay events.
5. Move each product between conveyor checkpoints.
6. Trigger visual effects based on event type and status.
7. Use unsafe_mode_events.json and safe_mode_events.json as separate demo scenes.
