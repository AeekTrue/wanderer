import socket

while True:
	sock = socket.socket()
	IP = input('Enter IP-address:')
	PORT = int(input('Enter port:'))
	try:
		sock.connect((IP, PORT))
	except ConnectionRefusedError:
		print('[Error] Connection refused')
		continue
	except TimeoutError:
		print('[Error] Time out')
		continue
	while True:
		message = input()
		try:
			sock.send(message.encode())
			data = sock.recv(1024)
		except ConnectionResetError:
			print('[Error] Disconnect')
			sock.close()
			break
		except BrokenPipeError:
			print('[Error] Disconnect')
			break			
		print(data.decode('utf-8'))