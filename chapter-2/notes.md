# 📘 **Chapter 2 — Basic Networking Tools (Notes + Algorithms)**
## ⭐ Overview
Chapter 2 introduces **networking fundamentals for hackers** using Python.
You learn how computers talk to each other over TCP and UDP, and how to write your own networking tools.
This chapter is the foundation for all future Black Hat Python projects.
---
## 🟦 **1. Networking Basics (Super Simple)**
### ✔ Host
A device on the network (like a house).
### ✔ IP Address
The _address_ of the device.
Example: `192.168.1.99`
### ✔ Port
A door inside the house.
Example:
*   `80` → websites
*   `22` → SSH
*   `4000` → your chat app
### ✔ Protocol
The rules of talking.
*   **TCP** → like a phone call (reliable)
*   **UDP** → like throwing paper planes (fast, unreliable)
### ✔ Socket
A plug used by Python to talk on the network.
Created with:
`socket(AF\_INET, SOCK\_STREAM) \# TCP`
---
## 🟩 **2. TCP vs UDP (Kid-Friendly)**
### 🔹 TCP (SOCK_STREAM)
*   Reliable
*   Ordered
*   Delivers everything
*   Perfect for messages, chat, web
### 🔹 UDP (SOCK_DGRAM)
*   Fast
*   May drop messages
*   Not ordered
*   Good for games, voice, streaming
Your programs use **TCP**.
---
## 🟧 **3. Important Socket Functions**
|Function|Purpose|
|---|---|
|`socket()`|Creates a communication plug|
|`connect()`|Client connects to server|
|`bind()`|Server chooses IP + port|
|`listen()`|Server waits for connections|
|`accept()`|Server accepts the client|
|`send()`|Send data|
|`recv()`|Receive data|
These are the building blocks for all hacking tools.
---
## 🟨 **4. Chapter 2 Projects**
### ✔ 1. TCP Client
Connect to a server and send/receive messages.
### ✔ 2. TCP Server
Accept connections and talk to the client.
### ✔ 3. Netcat Clone (Major Chapter 2 Project)
Python replacement for `nc` tool.
### ✔ 4. TCP Proxy
Forwards data between two devices.
### ✔ 5. UDP Echo Server/Client
Learn how UDP works.
### ✔ 6. Raw Sockets (Preview for Chapter 3)
---
## 🟪 **5. Algorithms for TCP Client & Server**
---
### ⭐ **TCP Client Algorithm**
```
start client
ask user for server ip
ask user for port
ask user for message
create socket
connect to (ip, port)
while message is not exit:
    send message
    wait for reply
    print reply
    ask for next message
close socket
end

```
---
### ⭐ **TCP Server Algorithm**
```
start server
create socket
bind to server ip and port
listen for connections
accept first client
while true:
    receive message from client
    if message is empty or exit:
         break
    print client message
    ask user (server admin) for reply
    send reply to client
close sockets
end

```
---
## 🟥 **6. Attacker Awareness (Defensive Only)**
Attackers use networking scripts to:
*   scan devices
*   test ports
*   automate connections
Defenders use this knowledge to:
✔ detect abnormal network traffic
✔ recognize unauthorized tools
✔ secure open ports
---
## 🟦 **7. Key Takeaways**
```
• IP = device address
• Port = door used for communication
• TCP = reliable communication (use for chat)
• UDP = fast, unreliable communication
• socket() creates a communication plug
• connect() for clients
• bind(), listen(), accept() for servers
• send() and recv() move data
• You can now build chat apps, scanners, proxies

```

