#!/usr/bin/env bash
set -e

source .venv/bin/activate

echo "Refreshing simulation outputs..."
./run_project.sh

echo
echo "Opening project files..."
open visual_outputs
open simulation_events
open unreal_project/event_tables
zed report/OS_AAT_Report_Draft.md
zed presentation/OS_AAT_Presentation_Outline.md
zed docs/FACULTY_DEMO_SCRIPT.md
zed docs/SCHEDULING_COMPARATIVE_ANALYSIS.md

echo
echo "Starting browser preview server..."
echo "Open: http://localhost:8000/preview/"
python3 -m http.server 8000
