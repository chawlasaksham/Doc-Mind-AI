#!/usr/bin/env bash
# Doc-Mind AI Unified Launcher (FastAPI + Modern React)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "⚡ Starting Doc–Mind AI (Modern React + FastAPI Engine)"
echo "   JIIT B.Tech CSE Major Project (Course: 15B19CL791)"
echo "=========================================================="

# 1. Build Frontend if dist doesn't exist or if --rebuild flag is given
if [ "$1" == "--rebuild" ] || [ ! -d "frontend/dist" ]; then
    echo "📦 Building modern React frontend..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run build
    cd "$SCRIPT_DIR"
fi

# 2. Ensure sample benchmark files exist
if [ ! -f "samples/sample_marksheet_education.pdf" ]; then
    python3 samples/generate_samples.py
fi

# 3. Free port 8000 if already in use by a previous session
EXISTING_PID=$(lsof -ti :8000 2>/dev/null)
if [ -n "$EXISTING_PID" ]; then
    echo "🔄 Freeing port 8000 (PID: $EXISTING_PID)..."
    kill -9 $EXISTING_PID 2>/dev/null || true
    sleep 1
fi

echo "🚀 Launching unified high-performance application on http://localhost:8000 ..."

# Open browser after 1.5 seconds on macOS
(sleep 2 && open http://localhost:8000) &

# Run FastAPI backend
python3 backend/server.py
