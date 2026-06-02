#!/usr/bin/env bash
set -e

source .venv/bin/activate

echo "Running OS simulation backend..."
python -m backend.run_all

echo
echo "Validating Unreal JSON event files..."
python -m backend.validate_events

echo
echo "Generating additional summary charts..."
python -m backend.summary_charts

echo
echo "Generating scheduling comparative analysis..."
python -m backend.comparative_analysis

echo
echo "Exporting Unreal-friendly CSV event tables..."
python -m backend.export_csv_for_unreal

echo
echo "Project run complete."
echo
echo "Generated:"
echo "  simulation_events/"
echo "  visual_outputs/"
echo "  unreal_project/event_tables/"
echo "  docs/SCHEDULING_COMPARATIVE_ANALYSIS.md"
echo
echo "Preview command:"
echo "  python3 -m http.server 8000"
echo
echo "Then open:"
echo "  http://localhost:8000/preview/"
