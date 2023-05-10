import socket 
import csv
import hashlib

import os

IP = socket.gethostbyname(socket.gethostname())
Port = 1133
add = (IP, Port)
FORMAT = "utf-8"
SIZE = 1024
buffer = 4096

#an Array to act as a Database :: 1. Name of File, 2. boolean Open or Locked 3. passCode ::default to 0000
class File:
    def __init__(self,name,open,pinCode):
         self.name = name
         self.open = open
         self.pinCode = pinCode
    
def main():
    my_files = []
    send_to_array(my_files)
    #this is the array for storing our File objects
    print("[STARTING] Sever is starting.")
    sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sever.bind(add)
    sever.listen()
    print("[LISTENING] Sever is listening.")

    while True:
        conn, addr = sever.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        #connection has been Established here
        while True:

            #in command the server expert like 
            #upload/file_name.txt/c@0001
            #download/file_name.txt/O

            #now lets handle this request message
            command =conn.recv(SIZE).decode(FORMAT)
            if len(command.split("/"))< 3:
                conn.close()
                print(f"[Disconnected] {addr} disconnected, Incorrect input on Client" )
                break
            comnd,filename,state = command.split("/")

            #now to handle the locked part

            if comnd == "upload":
                if state[0] == "C":
                    #then the file should be closed with passCode
                    c,code = state.split("@")
                    my_files.append(File(filename,"locked",code))
                    save_file("data/saved.csv",filename,"locked",code)
                else:
                    #this will be when the file is open
                    my_files.append(File(filename,"open",0))
                    save_file("data/saved.csv",filename,"open",0)
                #then call the uploading stuff
                #filename = conn.recv(SIZE).decode(FORMAT)
                upload(filename,conn)
            elif comnd == "query":
                if len(my_files) == 0:
                    #if the array is empty there are no files in the server
                    conn.send("No files in server".encode(FORMAT))
                else:
                    #print them all to the client server
                    String = ""
                    String = query(my_files, String)
                    conn.send(String.encode(FORMAT))
                    #the string is sent to user
                    print("There are Files")
            elif comnd == "download":
                #this where it gonna check even the passwords and stuff
                code = state
                #method to search for file name in protocol

                #search for array 
                ans = search_array(my_files, filename)
                if ans == None:
                    #sends a message to server that file was not found
                    conn.send("NONE".encode(FORMAT))
                else:
                    #look into password now
                    if ans.pinCode == code:
                        #sends a message to server that file was found
                        conn.send("FOUND".encode(FORMAT))
                        siZe = os.path.getsize(f"data/{filename}")
                        download(filename,conn,addr,siZe)
                    else:
                        #sends message that file was found but incorrect password
                        #for security reason this is the same code as when the file was not found
                        conn.send("NONE".encode(FORMAT))


            else:
                conn.close()
                print(f"[Disconnected] {addr} disconnected." )


        #print(filename)



def upload(file_name,conn):
        print("[RECV] Filename received")
        #file = open(f"data/{file_name}", "wb")
        conn.send("Filename received".encode(FORMAT))
        try:
            SizeX = int(conn.recv(SIZE).decode(FORMAT))
        except:
            print("no ways")
            return
        #data = bytes(data, encoding='utf-8')
        sent = 0
        with open(f"data/{file_name}", 'wb') as f:
            
            while sent<SizeX:
                data = conn.recv(1096)#.decode(FORMAT)
                computed_file_hash = hashlib.sha256(data).hexdigest()
                #print(computed_file_hash)
                #so the alogorithm 
                #check each byte's hash if it does it match, stop and delete what is written
                hash = conn.recv(64).decode(FORMAT)
                if hash == computed_file_hash:
                    sent += 1096
                    f.write(data)
                    conn.send("Continue".encode(FORMAT))
                else:
                    #delete file
                    os.remove(f"data/{file_name}")
                    conn.send("Corrupt".encode(FORMAT))
                    break

            f.close()
        
        print("[RECV] Filename Data received")
        conn.send("File data received".encode(FORMAT))


        #Receive hash 
        #received_file_hash = conn.recv(64).decode()
        #Create Hash
        #computed_file_hash = hashlib.sha256(data).hexdigest()
        
        #Compare two hashes
        #if received_file_hash == computed_file_hash:
            #print('File has been transmitted successfully')
            #conn.send("File received Unchanged!".encode(FORMAT))
        #else:
            #print('File has been corrupted during transmission')

        
def download(file_name,client,addr,size):
    #this is the method to download files from this server
    #two parameterfile name and the socket connection
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[Client]: {msg}")

    #get file size
    file_size = size
    client.send(str(file_size).encode(FORMAT))
    print(file_size)
    sent = 0 #bytes


    with open(f"data/{file_name}", 'rb') as f:

        while sent<file_size:
            bytes_read = f.read(1096)
            client.sendall(bytes_read)
            sent += 1096
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[Client]: {msg}")

def query(my_files, String):
    #will take an array parameter of the files
    String = ""
    #this will be the string sent on to the client
    for obj in my_files:
        String = String + obj.name + "  " + str(obj.open) + "\n"
    return String
def save_file(CSV,file_name,ope,pin):
        with open(CSV, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([file_name,ope,pin])

def send_to_array(array):
    with open("data/saved.csv", newline = '') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')

        for row in reader:
            ins_File = File(row[0],row[1],row[2])
            array.append(ins_File)

def search_array(arr, file_name):
    for obj in arr:
        if obj.name == file_name:
            return obj
    return None
        
if __name__ == '__main__':
    main()
