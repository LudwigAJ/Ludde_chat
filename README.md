A simple chat room app that uses built-in sockets in the OS and Python to communicate with a server over TCP, like an Ununtu server (which I tested this on) or localhost.

In the 'MAC' and 'WINDOWS' folders I will in a future update include executables. They will be located in the /dist/ folder.

Just run the script in terminal otherwise and enter an IP, PORT, and Username. Press 'Connect'. Then the app will take you to the main screen. It does this by calling Connect(Address) on its socket which was initialized at the start of execution with ipv4 and 'stream' indicating TCP. This will then tell the server to respond by using Accept() (Since it has since being executed been using Listen() on its own socket) The server socket uses some sock options to enable reconnection etc.


The chat_server.py is the server side of the app, and chat_client.py the client side.
Uses tkinter as GUI.
There will be a writable spot at the lower part of the window, to send text press 'Enter' or 'Return'.
The listbox will automatically move down when the texts exceed the vertical space.
