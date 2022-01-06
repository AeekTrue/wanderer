import select
from socket import socket


class Server:
	def __init__(self):
		self.ip = "192.168.1.72"
		self.port = 5000
		self.sock = socket()
		self.sock.bind((self.ip, self.port))
		self.to_monitor = [self.sock]

	def accept_connection(self, sock):
		client, addr = sock.accept()
		self.to_monitor.append(client)
		print('Connection from addr:', addr)

	def send_message(self, client):
		try:
			request = client.recv(2048)
			print(request.decode('utf-8'))

			response = self.generate_response(request)
			client.sendall(response)
		except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
			print(e)
		finally:
			client.close()
			self.to_monitor.remove(client)

	def generate_response(self, request):
		method, url = 'GET', '/'  # parse_request(request)
		headers, code = self.generate_headers(method, url)
		body = '<h1>Hello, World!!!</h1>\n\n'

		return (headers + body).encode()

	def generate_headers(self, method, url):
		return 'OK\n\n', 200

	def run(self):
		self.sock.listen()
		print(f'Listen on http://{self.ip}:{self.port}')
		while True:
			ready_to_read, _, _ = select.select(self.to_monitor, [], [])
			for s in ready_to_read:
				if s is self.sock:
					self.accept_connection(s)
				else:
					self.send_message(s)