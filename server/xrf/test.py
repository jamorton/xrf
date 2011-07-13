#!/usr/bin/env python


import core

class HelloCommand(core.FormattedCommand):
	id_byte = 12
	name = "hello"
	format = [("msg", "string")]

commands = [HelloCommand]
server = core.create_server(9001, commands)
server.start()
