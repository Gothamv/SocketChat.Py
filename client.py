print('Enter   1 - Text Message\n\t2 - Image\n\t3 - Video Calling')
op = int(input())

if(op == 1):

    """Script for client. GUI using Tkinter."""
    from socket import AF_INET, socket, SOCK_STREAM
    from threading import Thread
    import tkinter

    def receive():
        """Handles incoming messages"""
        while True:
            try:
                msg = client_socket.recv(BUFSIZE).decode("utf8")
                msg_list.insert(tkinter.END, msg)
            except OSError: # Incase the user has left the chat
                break

    def send(event=None): # Event is passed by binders
        msg = my_msg.get()
        my_msg.set("") # Clears the input field
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            top.quit()

    def onClosingWindow(event=None):
        """This function is to called when the window is closed"""
        my_msg.set("{quit}")
        send()

    top = tkinter.Tk()
    top.title("SocketChat")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar() # for messages to be sent
    my_msg.set("Type your message here...")
    scrollbar = tkinter.Scrollbar(messages_frame) # to navigate through the messages

    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    top.protocol("WM_DELETE_WINDOW", onClosingWindow)

    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000  # Default value.
    else:
        PORT = int(PORT)
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution.

if(op == 2):

    import random
    import socket, select
    from time import gmtime, strftime
    from random import randint

    image = raw_input('Enter the Image name: ')
    image = image + ".jpg"

    HOST = '127.0.0.1'
    PORT = 6666

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)

    try:

        # open image
        myfile = open(image, 'rb')
        bytes = myfile.read()
        size = len(bytes)

        # send image size to server
        sock.sendall("SIZE %s" % size)
        answer = sock.recv(4096)

        print('answer = %s' % answer)

        # send image to server
        if answer == 'GOT SIZE':
            sock.sendall(bytes)

            # check what server send
            answer = sock.recv(4096)
            print('answer = %s' % answer)

            if answer == 'GOT IMAGE' :
                sock.sendall("BYE BYE ")
                print('Image successfully send to server')

        myfile.close()

    finally:
        sock.close()

if(op == 3):

    import socket, videosocket
    import StringIO
    from videofeed import VideoFeed
    import sys

    class Client:
        def __init__(self, ip_addr = "127.0.0.1"):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_addr, 6000))
            self.vsock = videosocket.videosocket (self.client_socket)
            self.videofeed = VideoFeed(1,"client",1)
            self.data = StringIO.StringIO()

        def connect(self):
            while True:
                frame=self.videofeed.get_frame()
                self.vsock.vsend(frame)
                frame = self.vsock.vreceive()
                self.videofeed.set_frame(frame)

    if __name__ == "__main__":
        ip_addr = "127.0.0.1"
        if len(sys.argv) == 2:
            ip_addr = sys.argv[1]

        print("Connecting to " + ip_addr + "....")
        client = Client(ip_addr)
        client.connect()