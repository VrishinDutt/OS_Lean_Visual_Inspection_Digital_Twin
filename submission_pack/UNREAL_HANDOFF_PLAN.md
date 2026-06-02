# Unreal Engine Handoff Plan

## Project Role of Unreal Engine

Unreal Engine acts as the digital-twin simulation layer.

The Python backend handles:

- Race-condition modelling
- Safe synchronization modelling
- EDF scheduling
- FCFS scheduling
- Metrics generation
- JSON event export

Unreal Engine handles:

- 3D conveyor scene
- Product movement
- Sensor zone visualization
- Camera station visualization
- AI inspection station visualization
- Actuator rejection animation
- Race-condition warning effects
- Deadline-miss warning effects

## Scene Concept

A lean visual-inspection cell with the following flow:

Conveyor Entry -> Sensor Gate -> Camera Zone -> AI Inspection Station -> Rule Check Station -> Decision Fusion -> Actuator -> Pass/Reject Exit

## Required Unreal Actors

### 1. BP_Product

Represents one manufactured part on the conveyor.

Suggested properties:

- ProductID: String
- CurrentStation: String
- IsDefective: Boolean
- HasRaceCondition: Boolean
- DeadlineMissed: Boolean
- FinalDecision: String

Suggested visual states:

- Normal: grey/blue material
- Under inspection: yellow glow
- Pass: green material
- Reject: purple material
- Race condition: red pulse
- Deadline miss: amber pulse

---

### 2. BP_Conveyor

Represents the conveyor belt.

Responsibilities:

- Define movement path
- Hold station transforms
- Move products between station points

Suggested station points:

- EntryPoint
- SensorPoint
- CameraPoint
- AIInspectionPoint
- RuleCheckPoint
- DecisionPoint
- ActuatorPoint
- PassExitPoint
- RejectExitPoint

---

### 3. BP_Station

Generic station actor.

Suggested properties:

- StationName: String
- IdleMaterial
- ActiveMaterial
- ErrorMaterial
- DeadlineMissMaterial

Used for:

- Sensor
- Camera
- AI Inspection
- Rule Check
- Decision Fusion
- Actuator
- Logger

---

### 4. BP_EventManager

Main event playback controller.

Responsibilities:

- Load event data
- Sort by time
- Spawn products
- Route event types to visual actions
- Trigger station highlights
- Trigger product movement
- Trigger warning effects

---

### 5. BP_StatusBoard

A 3D or UI status display.

Shows:

- Current mode
- Events played
- Race events
- Deadline misses
- Current product ID
- Current active station

---

## JSON Event Format

Example event:

{
  "time": 12.5,
  "product_id": "P005",
  "event": "inspection_complete",
  "mode": "safe",
  "status": "normal"
}

Fields:

- time: simulation timestamp
- product_id: product identifier
- event: event name
- mode: unsafe, safe, edf, fcfs
- status: normal, race, scheduled, deadline_missed

## Event-to-Visual Mapping

sensor_detected:
- Spawn product if not already present
- Move/highlight product at SensorPoint
- Activate Sensor station

camera_frame_attached:
- Move product to CameraPoint
- Flash Camera station

inspection_complete:
- Move product to AIInspectionPoint
- Activate AI station

decision_fused:
- Move product to DecisionPoint
- Activate Decision station

actuator_pass:
- Move product to PassExitPoint
- Set product material to green

actuator_reject:
- Move product to RejectExitPoint
- Set product material to purple

race_condition_result_mapped_to_*:
- Move product to AIInspectionPoint
- Trigger red warning pulse
- Increment race count

*_started:
- Highlight corresponding station
- Move product to corresponding station

*_completed:
- Turn off station highlight
- Keep product at station unless next event moves it

deadline_missed:
- Trigger amber warning pulse
- Increment deadline miss count

## Recommended Implementation Order

1. Create static conveyor scene.
2. Place station actors along the conveyor.
3. Create BP_Product with basic movement between points.
4. Create a manually defined event list inside Blueprint first.
5. Verify products move correctly.
6. Add JSON loading.
7. Parse event fields.
8. Connect JSON events to product movement.
9. Add race-condition visual effects.
10. Add deadline-miss visual effects.
11. Add status board.
12. Record unsafe vs safe demo footage.

## Minimum Successful Unreal Demo

The minimum acceptable Unreal scene should show:

1. Products moving on a conveyor.
2. Unsafe mode showing a race-condition warning.
3. Safe mode showing clean product flow.
4. Actuator pass/reject behavior.
5. EDF or FCFS mode showing deadline-miss warning.

## Polished Demo Sequence

### Scene 1: Unsafe Mode

- Product enters conveyor.
- Sensor detects multiple products.
- AI result gets mapped to wrong product.
- Red warning appears.
- Wrong product decision is shown.

### Scene 2: Safe Mode

- Product packet remains consistent.
- Inspection result follows correct product.
- Correct reject/pass behavior.
- No red warning.

### Scene 3: Scheduling Mode

- Stations activate based on EDF event order.
- Deadline misses appear in amber.
- Status board shows deadline count.

## Recommended Unreal File Import Strategy

Simplest approach:

- Copy JSON files from simulation_events/ into Unreal Content or Saved folder.
- Use VaRest, Json Blueprint Utilities, or a small C++ helper to load JSON.
- For a student demo, hardcoded event arrays are acceptable if JSON loading becomes a bottleneck.

Most stable fallback:

- Export a simplified CSV from Python.
- Import CSV as a DataTable in Unreal.
- Replay rows in order.

## Suggested Visual Style

Use a clean industrial lab look:

- Matte dark floor
- Metal conveyor
- Minimal station boxes
- Colored status lights
- Red warning pulse for race condition
- Amber warning pulse for deadline miss
- Green pass lane
- Purple reject lane

Avoid overbuilding the environment. The focus is OS reliability, not cinematic realism.

## Final Deliverable from Unreal

Expected output:

- Unreal project folder
- Demo video
- Screenshots
- Optional packaged build

The report should explain that Unreal is the digital-twin visualization layer and Python is the OS simulation backend.
