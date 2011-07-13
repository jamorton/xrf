
XRF Project
===========

XRF (a recursive acronym for "XRF is Realtime Flash") is a realtime flash game engine,
which is different from most other server software in a couple of ways:

 * All game logic is implemented server side. This is primarily for security
   reasons; the clients are only responsible for implementing UI code and
   sending controls updates, making games hard to hack.
 * The framework is built specifically for real time applications, using an
   entity and server architecture very similar to valve's source engine. A single
   server instance only hosts one game at a time, and works in ticks sending
   delta updates every so often. Servers implement all game logic by creating,
   modifying, and simulating entities in the world. The client only needs to
   keep track of these changes and display them on the screen.
 * The core of xrf is implemented using gevent, allowing for very efficient
   networking that will scale to many users (the core code does not have
   any game specific logic, it can be used to implement master servers,
   chat servers, etc. that host thousands of users at once)
   
The software is implemented in layers, from the bottom up:

core - the core module contains the basic tcp server tools for easily
building scalable network programs. It also includes a simple, efficient,
and small binary command protocol. It allows for the sending of commands
that are defined as python classes that specify arguments packed into a
struct-like format. Each command only needs a 3-byte header.

... rest to come ...