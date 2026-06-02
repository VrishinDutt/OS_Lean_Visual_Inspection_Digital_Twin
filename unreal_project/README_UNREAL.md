# Unreal Engine Digital Twin Layer

## Purpose

This folder is reserved for the Unreal Engine digital-twin simulation layer of the project.

The Python backend generates event files that Unreal can replay visually.

## Event Table Files

CSV event tables are generated in:

event_tables/

Files:

- unsafe_mode_events.csv
- safe_mode_events.csv
- edf_schedule.csv
- fcfs_schedule.csv

These can be imported into Unreal as DataTables or parsed manually.

## Recommended Unreal Scene

Create a simple lean visual-inspection cell:

- Conveyor belt
- Sensor gate
- Camera station
- AI inspection station
- Rule-check station
- Decision-fusion station
- Reject actuator
- Pass lane
- Reject lane
- Status board

## Recommended Blueprints

- BP_Product
- BP_Conveyor
- BP_Station
- BP_EventManager
- BP_StatusBoard

## Minimum Demo

1. Load unsafe_mode_events.csv.
2. Spawn products by product_id.
3. Move products through station points.
4. Flash red when status is race.
5. Load safe_mode_events.csv.
6. Show clean synchronized flow.
7. Load edf_schedule.csv.
8. Show station activation and deadline miss warnings.

## Fallback

If Unreal JSON/CSV parsing takes too much time, manually enter 10-15 events into a Blueprint array and replay them.

The academic value remains intact because the OS backend already generates valid event timelines.
