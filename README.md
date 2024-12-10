# Socket-Chat Application

A minimalistic chat application built in Python that allows multiple clients to communicate via a centralized server. The project demonstrates socket programming and multithreading with simplicity in mind.

---

## Features

- **Real-time messaging:** Clients can send and receive messages instantly.
- **Broadcast messaging:** Messages from one client are relayed to all connected clients.
- **Graceful disconnection:** Handles client and server disconnections cleanly without crashes.
- **Simple and lightweight:** Designed for clarity and ease of understanding.

---

## Requirements

- Python 3.6 or newer.

---

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/cesarverapy/socket-chat.git
cd socket-chat
```

### 2. Run the server

Run the server script to start the chat server:

```bash
python chat_server.py
```

The server will start on `127.0.0.1` and port `12345`.

### 3. Run the client(s)

Run the client script for each user who wants to connect:

```bash
python chat_client.py
```

Each client can now send and receive messages in the chat.

### 4. Exit the chat

To exit the chat, type `exit` in the client terminal or press `Ctrl+C`.

---

## How It Works

1. **Server:**
   - Listens for incoming connections on `127.0.0.1:12345`.
   - Accepts multiple clients and maintains a list of active connections.
   - Relays messages from one client to all other connected clients using a broadcast mechanism.

2. **Client:**
   - Connects to the server at the specified host and port.
   - Allows the user to input messages, which are sent to the server.
   - Displays messages broadcasted by the server.

---

## Project Structure

- **`chat_server.py`:** The server-side script manages client connections and relays messages between them.
- **`chat_client.py`:** The client-side script allows users to connect to the server, send messages, and receive broadcasts.

---

## Example Usage

### Server Output:
```
Chat server started on 127.0.0.1:12345
Client ('127.0.0.1', 54321) connected.
Client ('127.0.0.1', 54322) connected.
```

### Client Interaction:
Client 1:
```
Hello, this is Client 1!
```

Client 2:
```
Client 1: Hello, this is Client 1!
```

---

## Future Improvements

- Add **dynamic configuration** for host and port through command-line arguments or a configuration file.
- Integrate **SSL/TLS encryption** for secure communication.
- Develop a **graphical user interface (GUI)** using frameworks like Tkinter or PyQt.
- Implement **logging** on the server to track connections, disconnections, and message activity.
- Add **usernames/nicknames** for better chat organization.
- Introduce **chat rooms** or private messaging functionality.
