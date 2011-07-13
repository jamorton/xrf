
import gevent.server
from etc import ExtendedStruct as Struct

_header_struct = Struct("!BH") # id, length
_struct_types = {
	"int": "i",
	"float": "f",
	"string": "#",
	"char": "c",
	"bool": "?"
}

class Command(object):
	id_byte = None
	name = "RFGS Command"
		
	def serialize(self):
		return ""
	
	@classmethod
	def from_bytes(cls, bytes):
		raise Exception("Unserialize not implemented")
	
	def __str__(self):  return "<%s>" % self.name
	def __repr__(self): return self.__str__()
	
class FormattedCommand(Command):
	name = "Formatted Command"
	format = None
	def __init__(self, *args, **kwargs):
		if type(self.format) != list:
			raise Exception("Invalid format, class format must be a list.")
		self.vars = {i[0] : None for i in self.format}
		self.struct = FormattedCommand.create_struct(self.format)
		self.set_vars(*args)
		self.vars.update(kwargs)
		
	def set_var(self, var, val):
		self.vars[var] = val
		
	def set_vars(self, *args):
		if len(args) > len(self.format):
			raise Exception("Invalid set_vars call")
		for i in range(len(args)):
			self.vars[self.format[i][0]] = args[i]
		
	def serialize(self):
		args = []
		for i in self.format:
			if self.vars[i[0]] is None:
				raise Exception("Not all vars for FormattedCommand are set")
			args.append(self.vars[i[0]])
		return self.struct.pack(*args)
		
	@classmethod
	def from_bytes(cls, bytes):
		struct = FormattedCommand.create_struct(cls.format)
		vars = struct.unpack(bytes)
		return cls(*vars)
		
	@staticmethod
	def create_struct(format):
		str = "!"
		for var in format:
			str += _struct_types[var[1]]
		return Struct(str)
		
	def __str__(self):
		return "<%s %s>" % (self.name, "".join(["%s='%s'" % (k, self.vars[k]) for k  in self.vars]))

class Server(object):
	def __init__(self, port):
		self._gstream  = gevent.server.StreamServer(("", port), self._new_conn)
		self.commands = {}
		self.clients = []
		
	def _new_conn(self, sock, addr):
		cid = len(self.clients)
		c = Client(cid, self, sock, addr)
		self.clients.append(c)
		c.recv_loop()
		
	def start(self):
		self._gstream.serve_forever()
		
	def add_command(self, cmd):
		self.commands[cmd.id_byte] = cmd
		
	def get_command(self, id):
		return self.commands.get(id, None)
		
	def broadcast(self, cmd):
		for c in self.clients:
			c.send_cmd(cmd)
			
class Client(object):
	def __init__(self, cid, server, sock, addr):
		self.cid          = cid
		self.server       = server
		self.sock         = sock
		self.addr         = addr
		self.next_cmd_id  = None
		self.next_cmd_len = 0
		self.buffer       = ""
		
	def recv_loop(self):
		while True:
			self.new_data(self.sock.recv(4096))
		
	def send_cmd(self, cmd):
		self.transport.write(self._get_bytes(cmd))
		
	def new_cmd(self, cmd):
		print "Command Received: " + str(cmd)

	def new_data(self, data):
		self.buffer += data
		hsize = _header_struct.size
		while len(self.buffer):
			buflen = len(self.buffer)
			if self.next_cmd_id == None:
				if buflen < hsize:
					break
				self.next_cmd_id, self.next_cmd_len = _header_struct.unpack(
					self._eat(hsize))
			else:
				if buflen < self.next_cmd_len:
					break
				self.new_cmd(
					self.server.get_command(self.next_cmd_id).from_bytes(
						self._eat(self.next_cmd_len)))
				
	def _get_bytes(self, cmd):
		if cmd.id_byte is None:
			raise Exception("Invalid command number for command '%s'" % cmd)
		bytes = cmd.serialize()
		return _header_struct.pack(cmd.id_byte, len(bytes)) + bytes
		
	def _eat(self, amt):
		data = self.buffer[:amt]
		self.buffer = self.buffer[amt:]
		return data
	
def create_server(port, commands):
	s = Server(port)
	for c in commands:
		s.add_command(c)
	return s
