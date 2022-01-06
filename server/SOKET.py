import socket
from select import select

sock = socket.socket()
PORT = 8080
IP_ADDRESS = input('Enter ip:')  # sock.gethostbyname(sock.gethostname())
sock.bind((IP_ADDRESS, PORT))
sock.listen()
print(f'Listen on http://{IP_ADDRESS}:{PORT}\n')
to_monitor = []


def generate_headers(method, url):
	return ('HTTP/1.1 200 OK\n\n', 200)


def generate_response(request):
	method, url = 'GET', '/'  # parse_request(request)
	headers, code = generate_headers(method, url)
	body = '<h1>Hello, World!!!</h1>\n\n'

	return (headers + body).encode()


def accept_connection(sock):
	client, addr = sock.accept()
	to_monitor.append(client)
	print('Connection from addr:', addr, '\n')


def send_message(client):
	try:
		request = client.recv(2048)
		print(request.decode('utf-8'))

		response = generate_response(request)
		client.sendall(response)
		client.close()
		to_monitor.remove(client)

	except (ConnectionResetError, ConnectionAbortedError):
		client.close()
		to_monitor.remove(client)
		return


def event_loop():
	while True:
		ready_to_read, _, _ = select(to_monitor, [], [])
		for s in ready_to_read:
			if s is sock:
				accept_connection(s)
			else:
				send_message(s)


if __name__ == '__main__':
	to_monitor.append(sock)
	event_loop()
