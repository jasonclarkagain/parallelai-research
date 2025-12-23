#!/bin/bash
echo "🔧 ParallelAI API Management"
echo "==========================="

case "$1" in
    start)
        echo "🚀 Starting ParallelAI API Server..."
        if [ -f "api/parallelai_api.py" ]; then
            # Check if in virtual environment
            if [ -z "$VIRTUAL_ENV" ] && [ -f "venv/bin/activate" ]; then
                echo "⚠️  Activating virtual environment..."
                source venv/bin/activate
            fi
            
            # Start in background
            cd api
            nohup python3 parallelai_api.py > ../api_server.log 2>&1 &
            API_PID=$!
            cd ..
            echo $API_PID > api_server.pid
            sleep 2
            
            if ps -p $API_PID > /dev/null; then
                echo "✅ API server started (PID: $API_PID)"
                echo "📝 Logs: api_server.log"
                echo "🌐 Access: http://localhost:8000"
                echo "📚 Docs: http://localhost:8000/docs"
            else
                echo "❌ Server failed to start. Check logs."
                rm -f api_server.pid
            fi
        else
            echo "❌ api/parallelai_api.py not found"
            echo "Current directory: $(pwd)"
            ls api/ 2>/dev/null || echo "api/ directory doesn't exist"
        fi
        ;;
    
    stop)
        echo "🛑 Stopping ParallelAI API Server..."
        if [ -f api_server.pid ]; then
            API_PID=$(cat api_server.pid)
            kill $API_PID 2>/dev/null && echo "✅ Stopped API server (PID: $API_PID)" || echo "⚠️  No process found"
            rm -f api_server.pid
            sleep 1
        else
            echo "⚠️  No API server PID file found"
        fi
        pkill -f "parallelai_api.py" 2>/dev/null && echo "✅ Cleaned up stray processes" || true
        ;;
    
    status)
        echo "📊 API Server Status:"
        if [ -f api_server.pid ]; then
            API_PID=$(cat api_server.pid)
            if ps -p $API_PID > /dev/null; then
                echo "✅ Running (PID: $API_PID)"
                echo "🌐 Endpoint: http://localhost:8000"
                if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
                    echo "🩺 Health: Healthy"
                else
                    echo "🩺 Health: Not responding"
                fi
            else
                echo "❌ Not running (stale PID file)"
                rm -f api_server.pid
            fi
        else
            if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
                echo "⚠️  Server running but no PID file"
            else
                echo "❌ Not running"
            fi
        fi
        ;;
    
    generate-key)
        echo "🔑 Generating new API key..."
        if [ -z "$2" ]; then
            echo "Usage: $0 generate-key 'Key Name'"
            exit 1
        fi
        KEY_NAME="$2"
        curl -X POST "http://localhost:8000/keys/generate?name=$KEY_NAME" 2>/dev/null || \
            echo "❌ API server may not be running. Start it with: $0 start"
        ;;
    
    list-keys)
        echo "📋 Listing API keys..."
        curl -s "http://localhost:8000/keys/list" 2>/dev/null | python3 -m json.tool 2>/dev/null || \
            echo "❌ API server may not be running"
        ;;
    
    logs)
        echo "📝 API Server Logs:"
        if [ -f api_server.log ]; then
            tail -30 api_server.log
        else
            echo "No log file found"
        fi
        ;;
    
    test)
        echo "🧪 Testing API connection..."
        if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
            echo "✅ API is healthy"
            echo ""
            echo "📡 Testing endpoints:"
            echo -n "Root: " && curl -s http://localhost:8000/ | grep -q "ParallelAI" && echo "✅" || echo "❌"
            echo -n "Providers: " && curl -s http://localhost:8000/providers | grep -q "providers" && echo "✅" || echo "❌"
            echo ""
            echo "🚀 Server is ready!"
        else
            echo "❌ API is not responding"
        fi
        ;;
    
    restart)
        echo "🔄 Restarting API server..."
        $0 stop
        sleep 2
        $0 start
        ;;
    
    *)
        echo "Usage: $0 {start|stop|status|restart|generate-key|list-keys|logs|test}"
        echo ""
        echo "Commands:"
        echo "  start         - Start the API server"
        echo "  stop          - Stop the API server"
        echo "  status        - Check server status"
        echo "  restart       - Restart the API server"
        echo "  generate-key  - Generate a new API key"
        echo "  list-keys     - List all API keys"
        echo "  logs          - View server logs"
        echo "  test          - Test API connection"
        exit 1
        ;;
esac
