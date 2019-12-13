# import socket programming library 
import socket 

# import thread module 
from _thread import *
import threading 
from time import sleep

print_lock = threading.Lock() 

# thread function 
def threaded(c): 
	while True: 

		# data received from client 
		data = c.recv(1024) 
		if not data: 
			print('Bye') 
			
			# lock released on exit 
			print_lock.release() 
			break

		# reverse the given string from client 
		data = data[::-1] 

		# send back reversed string to client 
		c.send(data) 

	# connection closed 
	c.close() 


def Main(): 
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 6797
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind(('localhost', port)) 
	print("socket binded to port", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("socket is listening") 
	# s.setblocking(False)
	# s.settimeout(1)
	c, addr = s.accept() 
	# a forever loop until client wants to exit 
	count = 0
	while True: 

		# establish connection with client 
		# lock acquired by client 
		# print_lock.acquire() 

		# Start a new thread and return its identifier 
		# start_new_thread(threaded, (c,))
		sleep(3)
		try: 
			# c.settimeout(0.001)
			# print('Connected to :', addr[0], ':', addr[1]) 
			# data = c.recv(1024)
			# print('data: ', data)
			print("enviando data...")
			# c.send("data[::-1]")
			c.sendall("deu certoooooooooooooooooooooooOOOOOOOOOOOOOOOOOOOOOOO".encode())
			count += 1
			if count == 10: break
		except socket.timeout:
			print("Nada ainda")
		# data = data[::-1] 
		# c.close()
	
	s.close() 


if __name__ == '__main__': 
	Main() 