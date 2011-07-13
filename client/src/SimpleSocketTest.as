package  
{
	import flash.events.Event;
	import flash.net.Socket;

	public class SimpleSocketTest
	{

		private var sock:Socket;
		
		public function SimpleSocketTest() 
		{
			trace("going");

			sock = new Socket();
			sock.addEventListener(Event.CONNECT, connected);
			sock.connect("71.90.76.10", 9001);
			
		}
		
		private function connected(e:Event):void 
		{
			trace("connected");
			sock.writeByte(12);
			sock.writeShort(5);
			sock.writeUTFBytes("test");
			sock.writeByte(0);
		}
		
	}

}
