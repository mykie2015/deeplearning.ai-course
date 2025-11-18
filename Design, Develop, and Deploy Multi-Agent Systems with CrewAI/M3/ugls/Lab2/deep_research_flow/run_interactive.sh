#!/bin/bash
# Interactive runner for the Deep Research Flow
# This script activates the virtual environment and runs the flow

cd "$(dirname "$0")"
source venv/bin/activate
crewai run

