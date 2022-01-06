import requests
from socket import socket

RUNNING = False


class Client:
	def __init__(self):
		self.ip = "127.0.0.1"
		self.port = 43210
		self.server_ip = "192.168.1.72"
		self.server_port = 5000
		self.data = ""
		self.__is_running = False
		if RUNNING:
			self.run()
		else:
			print("WARNING: Client is not running")

	def data_exchange(self):
		"""
		:return:
		"""
		if not self.__is_running or not self.data:
			return
		sock = socket()
		sock.connect((self.server_ip, self.server_port))
		sock.send(self.data.encode())
		data = sock.recv(1024)
		print(data.decode())
		self.data = ""
		sock.close()

	def write_data(self, *data):
		for e in data:
			self.data += str(e) + "\n"

	def run(self):
		print("Client is running")
		self.__is_running = True


client = Client()
