#!/bin/bash
# Workout Tracker Launcher
# Makes it easy to start the workout tracker server from anywhere (including Spotlight)

cd "$(dirname "$0")"
python3 server.py
