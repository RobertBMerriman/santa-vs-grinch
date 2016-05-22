import socket

l_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

def listen(port):
	l_socket.bind(('', port))
	l_socket.listen( 4 )

def receive():
	lis, addr = l_socket.accept()
	s = lis.recv(1024).decode("UTF-8")
	lis.close()
	return s

def send(dest, port, data_to_send):
	s_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s_socket.connect( (dest, port) )
	s_socket.send( bytes( data_to_send, "UTF-8") )
	s_socket.close()