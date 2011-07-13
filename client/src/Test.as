package
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.system.Security;
	
	/**
	 * ...
	 * @author Jonanin
	 */
	public class Test extends Sprite 
	{
		
		private var test:SimpleSocketTest;
		
		public function Test():void 
		{
			Security.allowDomain("71.90.76.10");
			trace("hi");
			test = new SimpleSocketTest();
		}
		
	}
	
}