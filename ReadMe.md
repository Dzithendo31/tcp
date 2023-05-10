# TCP Socket File Transfer Program
This program allows you to transfer files between two computers using TCP sockets. It establishes a reliable, bi-directional communication channel that enables the transmission of files over a network.

Prerequisites
Before running this program, ensure that the following prerequisites are met:

Python: Make sure you have Python installed on your system. You can download the latest version of Python from the official website: https://www.python.org/downloads/

Network Connection: Ensure that both computers are connected to the same network or have a direct network connection between them.

File Transfer

Once the server and client scripts are running, you can start transferring files between the two computers. The server will listen for incoming connections, and the client will connect to the server.

To send a file from the client to the server, specify the file path in the client

javascript
Copy code
Enter the file path: /path/to/file.txt
The file will be transferred to the server and saved in the same directory as the server.py script.

To download a file from the server to the client, specify the file name in the client terminal:



Server IP: 127.0.0.1 (localhost)
Server Port: 5000
If you need to change these configurations, you can modify the following lines in both server.py and client.py:

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
Replace '127.0.0.1' with the desired IP address and 5000 with the desired port number.

Limitations
This program is designed for transferring files of any type or format.
It assumes that both computers are connected to the same network or have a direct network connection.
It may not work correctly if there are any network connectivity issues or firewalls blocking the communication.
