import socket
print(socket.gethostname())
# from .base import *
if(socket.gethostname() == 'anny-X541UJ'):
    from .local import *
else:
    from .production import *

