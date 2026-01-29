#!/bin/bash
# InstaReelTranscriber - Unix Launcher
# Starts both backend and frontend servers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "     InstaReelTranscriber - Starting Application"
echo "============================================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run ./setup.sh first."
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "[WARNING] Frontend dependencies not installed!"
    echo "Running: cd frontend && npm install"
    cd frontend && npm install && cd ..
fi

# Cleanup function
cleanup() {
    echo
    echo "[INFO] Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "[INFO] Starting Backend API server..."
source venv/bin/activate
uvicorn src.api:app --reload --port 8000 &
BACKEND_PID=$!

echo "[INFO] Waiting for backend to start..."
sleep 3

echo "[INFO] Starting Frontend development server..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "============================================================"
echo "  Servers are running!"
echo
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo
echo "  Press Ctrl+C to stop all servers"
echo "============================================================"
echo

# Try to open browser (works on most systems)
if command -v xdg-open &> /dev/null; then
    sleep 3 && xdg-open "http://localhost:3000" &
elif command -v open &> /dev/null; then
    sleep 3 && open "http://localhost:3000" &
fi

# Wait for both processes
wait
