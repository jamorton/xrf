
from twisted.application import internet, service
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

POLICY_RESPONSE = """<?xml version="1.0"?>
<cross-domain-policy>
   <site-control permitted-cross-domain-policies="master-only"/>
   <allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>"""

class PolicyProtocol(LineReceiver):
	delimiter = "\0"
	def lineReceived(self, line):
		if line == "<policy-file-request/>":
			print "New request, sending policy file"
			self.transport.write(POLICY_RESPONSE + "\0")
		else:
			self.transport.loseConnection()

class PolicyFactory(Factory):
	protocol = PolicyProtocol
	
	def buildProtocol(self, addr):
		print "new protocol"
		p = self.protocol()
		p.factory = self
		return p

if __name__ == "__main__":
	from twisted.internet import reactor
	reactor.listenTCP(843, PolicyFactory())
	reactor.run()
else:
	application = service.Application("rfgs_flash_policy")
	pservice    = internet.TCPServer(843, PolicyFactory())
	pservice.setServiceParent(service.IServiceCollection(application))
