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
   3. Once you've finished typing all these commands in the terminal, reboot both RaspberryPis with "sudo reboot", starting with the ServerPi. Be sure to not leave a very long delay between reboots. You could also just shut them down with "sudo shutdown now", and power cycle the project.
3. If you'd like to learn more about how Apache is running on the ServerPi, open /etc/apache2/sites-available/conferencesandtable.com.conf with you favorite editor. For example, type in "sudo nano /etc/apache2/sites-available/conferencesandtable.com.conf". This is the file where I tell Apache where the Flask application I want to run is. I also specify the virtual environment I'm using with the python-home flag, and associate a few domain names with the Pi's IP address. NOTE: these domain names only work if you open a browser on the Raspberry Pi itself. If you want to set them up such that they are accessible from the LAN, you need to set up a local DNS server. If you'd like to do that, follow the instructions here: https://serverfault.com/questions/101822/how-to-make-local-domain-name-available-to-people-on-lan#:~:text=I-,strongly%20recommend,-to%20use%20DNS
4. Here are some helpful web server commands to use that help deploy a Flask app to Apache. https://docs.google.com/document/d/1TVO4eFgKt67rHBJfX1SHweImXI8MTxCv4Zn9oLcH6D0/edit?pli=1
5. If you'd like to familiarize yourself with Flask, follow Codemy tutorials on YouTube by building your own personl Flask app: https://www.youtube.com/playlist?list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz
6. If you'd like to run code without the web server, disable Apache and run test code in the Table directory.
7. If, for any reason, you decide to change the directory structure of the project, please proceed with caution. If you do so, you'll also have to modify the Apache configuration files.


If you have any questions whatsoever, please reach out to me through email at zschweyk@gmail.com. I'd be more than happy to help! (:

