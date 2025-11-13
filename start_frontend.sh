#!/bin/bash
cd "$(dirname "$0")/frontend"
echo "Starting FitMentor Frontend Server..."
echo "Visit http://localhost:8000 in your browser"
python3 -m http.server 8000
