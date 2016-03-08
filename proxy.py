#!/usr/bin/python

#works on python 2.7

import sys,socket,threading

def server_loop(lhost,lport,rhost,rport,rece):
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		server.bind((lhost, lport))
	except:
		print "[!] Failed to listen on %s:%d" % (lhost,lport)
		print "[!] Check for other listening sockets or correct permissions."
		sys.exit(0)
	print "[*] Listening on %s:%d" % (lhost, lport)
	server.listen(5)
	while True:
		client_socket, addr = server.accept()
		#print the local connection information
		print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])
		#start a thread to talk to the remote host
		proxy_thread = threading.Thread(target = proxy_handler, args = (client_socket, rhost, rport, rece))
		proxy_thread.start()

def proxy_handler(client_socket, rhost, rport, rece):
	#connect to the remote host
	remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	remote_socket.connect((rhost, rport))

	#receive data from the remote host
	if rece:
		remote_buffer = receive_from(remote_socket)
		#hexdump(remote_buffer)        #disable comment to show the content of the buffer

		#send it to our response handler
		remote_buffer = response_handler(remote_buffer)

		#if data needs to be sent to local client, send it
		if len(remote_buffer):
			print "[<==] Sending %d byte to localhost." % len(remote_buffer)
			client_socket.send(remote_buffer)

	#loop and read from local, send to remote, send to local
	while True:
		#read from local host
		local_buffer = receive_from(client_socket)

		if len(local_buffer):
			print "[==>] Received %d byte from localhost." % len(local_buffer)
			#hexdump(local_buffer)       #disable the comment to show the content of the buffer

			#send it to our request handler
			local_buffer = request_handler(local_buffer)

			#send the data to the remote host
			remote_socket.send(local_buffer)
			print "[<==] Sent to remote."

			#Receive back the response
			remote_buffer = receive_from(remote_socket)
			
			if len(remote_buffer):
				print "[==>] Received %d bytes from remote." % len(remote_buffer)

				#send to our response handler
				remote_buffer = response_handler(remote_buffer)

				#send the response to the local socket
				client_socket.send(remote_buffer)
				print "[<==] Sent to localhost."

			if not len(local_buffer) or not len(remote_buffer):
				client_socket.close()
				remote_socket.close()
				print "[*] No more data. CLosing connections."

				break

def hexdump(src, length = 16):
	result = []
	digits = 4 if isinstance(src, str) else 2
	for i in range (0, len(src), length):
		s = src[i:i+length]
		hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
		text = b' '.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
		result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))

		print b'\n'.join(result)

def receive_from(connection):
	buffer = ""

	connection.settimeout(2)
	try:
		while True:
			data = connection.recv(4096)

			if not data:
				break
			buffer += data
	except:
		pass
	return buffer

def request_handler(buffer):
	#perform packet modifications
	return buffer

def response_handler(buffer):
	#perform packet modifications
	return buffer

def main():
	if sys.version_info > (2,8):
		print "Please run in Python 2.7"
		sys.exit(0)

	if len(sys.argv[1:]) < 4:
		print "Usage: ./" + sys.argv[0] + " [lhost] [lport] [rhost] [rport] [receivefirst]"
		print "Example: 127.0.0.1 9000 10.12.13221 9000 True"
		sys.exit(0)

	#setup local listening parameters
	lhost = sys.argv[1]
	lport = int(sys.argv[2])

	#setup remote target
	rhost = sys.argv[3]
	rport = int(sys.argv[4])

	#the following tells the proxy to connect and receive data before sending to the remote host
	try:
		rece = sys.argv[5]
	except IndexError:
		rece = "True"

	if "True" in rece:
		rece = True
	else:
		rece = False

	server_loop(lhost, lport, rhost, rport, rece)
main()
