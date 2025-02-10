#!/bin/bash
set -e

echo "[start.sh] Starting Tor in the background (logging errors only)..."
tor -f /etc/tor/torrc &

# Wait until the hostname file appears (which means Tor has generated the onion service)
while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
  echo "[start.sh] Waiting for .onion hostname to be generated..."
  sleep 1
done

# Display the generated .onion address
ONION_ADDRESS=$(cat /var/lib/tor/hidden_service/hostname)
echo "[start.sh] *** Your Onion Address: $ONION_ADDRESS ***"

echo "[start.sh] Starting Python HTTP server (debug mode) on 127.0.0.1:80..."
exec python3 /app/server.py
