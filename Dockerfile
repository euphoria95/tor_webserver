# Dockerfile

FROM debian:stable-slim

# Install Tor and Python
RUN apt-get update && apt-get install -y \
    tor \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy configuration and scripts
COPY torrc /etc/tor/torrc
COPY start.sh /app/start.sh
COPY server.py /app/server.py

# Make the start script executable
RUN chmod +x /app/start.sh

# Create Hidden Service directory with proper permissions
RUN mkdir -p /var/lib/tor/hidden_service \
    && chown debian-tor:debian-tor /var/lib/tor/hidden_service \
    && chmod 700 /var/lib/tor/hidden_service

# Expose port 80 (the server listens on 127.0.0.1:80 inside the container)
EXPOSE 80

USER debian-tor

# Default command to run the start script
CMD ["/app/start.sh"]
