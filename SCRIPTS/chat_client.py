#!/usr/bin/env python3

import threading
import sys
import socket
import tkinter
import time

#The constants needed
HEADER = 10
IP = ""
PORT = 0
USERNAME = ""

##########################################
#set up the tkinter GUI window

root = tkinter.Tk()
root.title("Ludde_Chat")
#root.geometry("700x500")



def raise_frame(frame):
    frame.tkraise()


def connect(event=None):
    IP = ip_msg.get()
    print (IP)

    PORT = int(port_entry.get())
    print (PORT)
    USERNAME = usr_entry.get()

    client_socket.connect((IP, PORT))
    #client_socket.setblocking(False)

    usr_name = USERNAME.encode('utf-8')
    usr_header = f"{len(usr_name):<{HEADER}}".encode('utf-8')
    client_socket.send(usr_header + usr_name)

    receive_thread.start()
    raise_frame(chat_frame)
    messages.grid()



def send(my_msg):

    new_message = my_msg.get()

    if new_message:
        message_header = f"{len(new_message):<{HEADER}}".encode('utf-8')
        ready_message = new_message.encode('utf-8')

        client_socket.send(message_header + ready_message)

        messages.insert(tkinter.END, new_message)
        msg.set("")



def receive():

    while True:

        try:
            usr_header = client_socket.recv(HEADER)


            usrname_length = int(usr_header.decode('utf-8').strip())


            if usrname_length == 0:
                message_box.insert(tkinter.END, "Disconnected from server")
                sys.exit()

            print(usrname_length)
            usrname = client_socket.recv(usrname_length).decode('utf-8')

            msg_header = client_socket.recv(HEADER)
            msg_length = int(msg_header.decode('utf-8').strip())

            msg = client_socket.recv(msg_length).decode('utf-8')

            complete_msg = f"{usrname} >> {msg}"

            messages.insert(tkinter.END, complete_msg)
        except:
            break


def closing(event=None):

    client_socket.close()
    root.destroy()
    sys.exit()




#####Functions

root.protocol("WM_DELETE_WINDOW", closing)

chat_frame = tkinter.Frame(master=root)
start_frame = tkinter.Frame(master=root)

####START####
start_frame.grid(row=0, column=0)
#start_frame.place(relx=0.5, rely=0.5, anchor="center")

ip_msg = tkinter.StringVar()
port_msg = tkinter.StringVar()
usr_msg = tkinter.StringVar()

ip_entry = tkinter.Entry(master=start_frame, textvariable=ip_msg)
port_entry = tkinter.Entry(master=start_frame, textvariable=port_msg)
usr_entry = tkinter.Entry(master=start_frame, textvariable=usr_msg)

ip_label = tkinter.Label(master=start_frame, text="IP ADDRESS")
port_label = tkinter.Label(master=start_frame, text="PORT NUMBER")
usr_label = tkinter.Label(master=start_frame, text="USERNAME")

ip_label.grid(row=0, column=0)
port_label.grid(row=1, column=0)
usr_label.grid(row=2, column=0)

ip_entry.grid(row=0, column=1)
port_entry.grid(row=1, column=1)
usr_entry.grid(row=2, column=1)

connect_button = tkinter.Button(master=start_frame, text="Connect", command=connect)

connect_button.grid(row=2, column=2)

####CHAT####

chat_frame.grid(row=0, column=0)
#chat_frame.place(relx=0.5, rely=0.5, anchor="center")

scrollbar = tkinter.Scrollbar(master=chat_frame)
messages = tkinter.Listbox(master=chat_frame, height=30, width=100, font=("Helvetica", 15), yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="nse")
messages.grid(row=0, column=0)
messages.grid_remove()

msg = tkinter.StringVar()
message_box = tkinter.Entry(master=chat_frame, textvariable=msg)
message_box.grid(row=1, column=0, sticky="swe")
message_box.bind("<Return>", lambda event: send(msg))




#########################################Networking side'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True



tkinter.mainloop()
