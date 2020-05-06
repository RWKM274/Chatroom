from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            GUI.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    msg = messageSend.get()
    messageSend.set("Delete this and enter your username")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    messageSend.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

messageSend_frame = tkinter.Frame(top)
messageSend = tkinter.StringVar()
messageSend.set(" ")
scrollbar = tkinter.Scrollbar(messageSend_frame)
GUI = tkinter.Listbox(messageSend_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
GUI.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
GUI.pack()
messageSend_frame.pack()

entry_field = tkinter.Entry(top, textvariable=messageSend)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.withdraw()

top.protocol("WM_DELETE_WINDOW", on_closing)




window = tkinter.Tk()
window.title("Host and port")
window.geometry('350x200')
lbl = tkinter.Label(window, text="host")
lbl.grid(column=0, row=0)
hostNumber = tkinter.Entry(window,width=10)
hostNumber.grid(column=1, row=10)
lbl = tkinter.Label(window, text="port")
lbl.grid(column=0, row=10)
portNumber = tkinter.Entry(window,width=10)
portNumber.grid(column=1, row=0)

def clicked():
    window.destroy()
    top.deiconify()

btn = tkinter.Button(window, text="Connect", command=clicked)

btn.grid(column=175, row=200)


HOST = hostNumber.get()
PORT = portNumber.get()

if not PORT:
    PORT = 4
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()