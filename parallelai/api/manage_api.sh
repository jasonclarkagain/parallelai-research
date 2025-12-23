#!/bin/bash

case "$1" in
    start)
        echo "🚀 Starting ParallelAI API server..."
        cd ~/parallelai/api
        source venv/bin/activate
        python parallelai_api.py &
        echo $! > ~/parallelai/api_server.pid
        echo "✅ Server started (PID: $(cat ~/parallelai/api_server.pid))"
        ;;
    stop)
        echo "🛑 Stopping ParallelAI API server..."
        if [ -f ~/parallelai/api_server.pid ]; then
            kill $(cat ~/parallelai/api_server.pid) 2>/dev/null
            rm ~/parallelai/api_server.pid
            echo "✅ Server stopped"
        else
            echo "⚠️  No PID file found, killing any parallelai processes..."
            pkill -f "parallelai_api.py" 2>/dev/null && echo "✅ Killed" || echo "❌ No processes found"
        fi
        ;;
    status)
        echo "📊 ParallelAI API Server Status:"
        if curl -s http://localhost:8000/health >/dev/null; then
            echo "✅ RUNNING - http://localhost:8000"
            echo "📡 Health: $(curl -s http://localhost:8000/health | python3 -c "import sys,json;print(json.load(sys.stdin)['status'])")"
        else
            echo "❌ STOPPED"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
