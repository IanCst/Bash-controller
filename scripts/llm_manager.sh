
echo "Checking CPU usage..."
CPU_USAGE=$(top -bn1 | awk '/Cpu\(s\)/ {print 100 - $8}')
echo "CPU Usage: ${CPU_USAGE}%"

echo "Checking Ollama logs..."
if [ -f /home/ubuntu/ollama.log ]; then
  tail -n 40 /home/ubuntu/ollama.log
else
  echo "/home/ubuntu/ollama.log does not exist yet."
fi

if pgrep -f "ollama serve" >/dev/null; then
  echo "Ollama is already running."
else
  echo "Starting Ollama..."
  nohup ollama serve > /home/ubuntu/ollama.log 2>&1 &
  sleep 3
  pgrep -f ollama || echo "Ollama failed to start"
fi
