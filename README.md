# ConferenceSandTable

The Conference Sand Table consists of an arm that spans the diameter of the table, with two permanent magnets attached to pieces that span the radii. The arm's rotation is controlled by an ODrive motor, and each magnetic piece is controlled by ODrive motors. While the arms rotates, the radii motors move the magnets in and out, depending on the polar equation being drawn. These magnets are attracted to metal balls that sit in the table's sand.

The exhibit is controlled with two Raspberry Pis. One Pi is stationary at the bottom of the exhibit (ServerPi), while the other rotates with the arm near the top of the table (ClientPi). Here is a more detailed overview of what they specifically do.
1. ServerPi: Responsible for running a deployed Flask application on Apache, which can easily be connected to by typing in its IP address (it is currently 10.107.200.19, but that could change. SSH into the Pi and type "ifconfig" in the terminal to find its IP address), as long as you're connected to the same local network (LAN) (connect to the DPEA wifi). This Pi is also responsible for rotating the theta motor when the user draws an equation and, about 25 times/second, sending its position relative to the total number of rotations the user specifies for the equation. When the Flask application starts up, it immediately attempts to connect to the ClientPi to begin sending data over.
2. ClientPi: Responsible for constantly receiving and decoding packets, and processing their meaning by appropriately moving the radius motors. On the Pi's startup procedure, a launcher file is immediately run, which runs a Python script that connects to the ServerPi and indefinitely receives packets from it.

The two Raspberry Pis are connected to each other via ethernet, which nicely takes care of packet transfer and loss through TCP/IP. Learn more about TCP/IP here: https://www.techtarget.com/searchnetworking/definition/TCP-IP

This Server/Client model has proved to work extremely well. Before two Pis were on the project, there was only the Pi responsible for running Apache, which was connected to the radius motor controller via USB, in addition to the theta motor controller. However, we found that the USB cable connected to the radius motor controller, which passed through the slip ring, consistently gave us "ODrive Disappeared" errors when the theta motor was rotating. When it wasn't rotating, it behaved perfectly fine. This gave us reason to believe that the slip ring was not well-built for USB cables, but we aren't completely sure about that, as we don't see any reason why the slip ring isn't designed for USB packet transfer.

The order that Apache, the Flask application, the Server, and the Client all start is very important for the project to immediately be ready to connect to and control via its IP address in the browser. Since Apache automatically runs when the Pi turns on, here is the order for everything else.
1. Flask application
2. Server
3. Client

Interestingly, when the ClientPi boots up, it runs "wget" in the terminal, on a thread, to start code execution in the Flask application. Immediately after this, the ClientPi sleeps for a few seconds to give Flask the chance to import required modules, connect to and calibrate the theta motor, start up the Server, and attempt to connect to a client. When the ClientPi finishes its sleep, it establishes a connection to the Server as a Client.

Notes for future maintainers:
1. When testing the Flask app before deploying it for Apache to run, follow all the commented and non-commented instructions in startup.bash to run Flask. They will allow you to connect to the Flask app via the Pi's IP address on port 5000 (type 10.107.200.19:5000 in the browser), as long as you're connected to the same LAN.
2. In order to deploy code to the Webserver and Client Pis, copy and paste the commands in copy_Webserver_commands.sh and copy_ClientPi_commands, respectively, in the terminal.
   1. For the ClientPi, make sure that the main file you want it to run on startup is called main.py and is in /home/pi/projects/ConferenceSandTable/ClientPi/
   2. For the ServerPi, take note that the command in copy_Webserver_commands.sh copies files to /home/pi/projects/. In order for Apache to recognize the new development code and run it on reboot, ssh into pi@conference-sand-table-v2-pi.local and follow these commands...
      1. cd /var/www/FLASKAPPS/
      2. sudo rm -r ConferenceSandTable
      3. sudo cp -r /home/pi/projects/ConferenceSandTable ConferenceSandTable
      4. cd ConferenceSandTable/Webserver/
      5. sudo chown www-data:pi database.db
      6. cd ..
      7. cd ..
      8. sudo chmod -R ugo+rw ConferenceSandTable/
      9. cd ConferenceSandTable/Webserver/
      10. sudo chmod ugo+x database.db
   3. Once you've finished typing all these commands in the terminal, ssh into pi@conference-sand-table-v2-radius-pi.local
3. The code for the table itself is pretty much done... The web aspect could be improved.

