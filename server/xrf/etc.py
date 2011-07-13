
from struct import Struct as _LibStruct

# Add support for variable length strings to struct
# by moving them to the end and appending "\0" to them
# NOTE: DOES NOT support counts (i.e. 10i). Only a string
# of single letters is permitted

# for example, if a struct is made with a format "#i#i#"
# (where # is the new variable length string), then it wil
# be encoded / decoded as "ii#\0#\0#\0"

# note that the size attribute only includes non-variable-length
# elements

class ExtendedStruct(object):
	def __init__(self, format):
		self.format_str = ""
		self.string_map = []
		self.total_elements = len(format)
		for i in xrange(len(format)):
			if format[i] == "#": self.string_map.append(i)
			else:                self.format_str += format[i]
		self.struct = _LibStruct(self.format_str)
		self.size   = self.struct.size
		
	def pack(self, *passedargs):
		if (len(passedargs)) != self.total_elements:
			raise Exception("incorrect number of args passed to pack")
		args = list(passedargs)
		strings = []
		for x in self.string_map:
			strings.append(args.pop(x - len(strings)))
		return self.struct.pack(*args) + "\0".join(strings) + "\0"
		
	def unpack(self, string):
		size = self.struct.size
		struct_ret = list(self.struct.unpack(string[:size]))
		strings = string[size:].split("\0")[:-1]
		if len(strings) != len(self.string_map):
			raise Exception("Invalid string passed to unpack")
		for i in xrange(len(strings)):
			struct_ret.insert(self.string_map[i], strings[i])
		return struct_ret
