#!/bin/sh

echo "=== START.SH EXECUTED ==="
echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

echo "=== Environment Variables Check ==="
env | grep -E "GOOGLE|OAUTH|SPRING|KAKAO|DEBUG" || echo "No matching environment variables found"
echo "=== End Environment Variables Check ==="

echo "Starting Spring Boot application at $(date '+%Y-%m-%d %H:%M:%S')..."
exec java -jar ./app.jar 