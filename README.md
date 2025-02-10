# tor_webserver
### README.md – Tor Onion Service in Docker  

```markdown
# Tor Onion Service in Docker

This repository provides a **Dockerized Tor Onion Service** with a simple HTTP server.  
The HTTP server runs inside the Docker container and is only accessible via the Tor network.  

It supports the following **HTTP methods**:
- `GET`: Displays a simple HTML landing page.
- `POST`: Logs incoming data and responds with a confirmation.
- `HEAD`: Returns headers only (no content).
- `OPTIONS`: Lists supported HTTP methods.

## Features
- 🛡️ **Fully self-contained**: Runs Tor and an HTTP server in the same container.
- 🔍 **Minimal Tor logging**: Only logs errors to keep logs clean.
- 📡 **Automatic .onion generation**: A new address is generated on each container restart.
- 📝 **Debug logging for HTTP server**: Logs all incoming requests.
- 📂 **Lightweight**: Uses `debian:stable-slim` as the base image.

---

## 🚀 Getting Started

### 1️⃣ Build the Docker Image
Clone this repository and run:

```bash
docker build -t tor-onion-server .
```

### 2️⃣ Run the Container
Start the container with:

```bash
docker run -it --rm --name my-onion-server tor-onion-server
```

The terminal will display:

```
[start.sh] Waiting for .onion hostname to be generated...
[start.sh] *** Your Onion Address: abcdefghijklmnop.onion ***
[start.sh] Starting Python HTTP server (debug mode) on 127.0.0.1:80...
```

📌 **Copy the `.onion` address** and use it in the Tor Browser.

---

## 🔍 Accessing the Service

### Open in Tor Browser
1. Copy the `.onion` address from the logs.
2. Open **Tor Browser**.
3. Paste the address in the address bar.
4. You should see a page like this:

```
Welcome to my .onion service!
Supported HTTP methods: GET, POST, HEAD, OPTIONS.
```

### Testing with `curl`
#### 1️⃣ GET request
```bash
curl --socks5-hostname 127.0.0.1:9050 http://abcdefghijklmnop.onion/
```

#### 2️⃣ POST request
```bash
curl -X POST -d "name=TestUser" http://abcdefghijklmnop.onion --socks5-hostname 127.0.0.1:9050
```
The logs will show:
```
DEBUG: Received POST data: name=TestUser
```

---

## 📌 Persistent Onion Address

By default, the `.onion` address changes every time the container restarts.  
To keep the **same address** between restarts, use a **Docker volume**:

```bash
docker run -it --rm \
  -v my_hidden_service:/var/lib/tor/hidden_service \
  --name my-onion-server tor-onion-server
```

This will persist the generated **private keys** and **hostname**.

---

## 📂 File Structure

```
.
├── Dockerfile   # Docker build instructions
├── torrc        # Tor configuration file
├── start.sh     # Startup script
└── server.py    # Simple HTTP server with logging
```

---

## 🔧 Customizing the Server

Want to modify the server?  
Edit `server.py` to customize responses, logging, or add routes.  

Example: Change the **landing page message** in `LANDING_PAGE`:

```python
LANDING_PAGE = """\
<html>
<head><title>My Hidden Service</title></head>
<body>
  <h1>Welcome to my private .onion site!</h1>
</body>
</html>
"""
```

---

## ❓ FAQ

### 🔹 Why does the .onion address change every time I restart the container?
Because Tor generates new keys each time. Use `-v my_hidden_service:/var/lib/tor/hidden_service` to persist them.

### 🔹 How do I increase Tor logging for debugging?
Modify **torrc** and change:
```ini
Log notice stdout
```
Then rebuild and restart the container.
