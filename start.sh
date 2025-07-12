#!/bin/sh

echo "=== Environment Variables Check ==="
env | grep -E "GOOGLE|OAUTH|SPRING|KAKAO|DEBUG" || echo "No matching environment variables found"
echo "=== End Environment Variables Check ==="

echo "Starting Spring Boot application..."
java -jar ./app.jar 