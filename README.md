# ConferenceSandTable

A large table with a rotating center (theta) and two radii arms that work together to create smooth, polar equations in sand. Controlled by a Raspberry Pi, users interact with the exhibit through a webserver.

Notes for future maintainers:
1. Sometimes the top radius board loses connection (it does so about 10% of the time). I found that power cycling always fixed the problem, and sometimes unplugging and plugging back in the fuse for the top board also works.
2. The code for the table itself is pretty much done... The web aspect could be improved.
3. Convert Flask web app to an official webserver, by following the directions here: https://singleboardbytes.com/1002/running-flask-nginx-raspberry-pi.htm
4. So far, I setup a test webserver and it worked perfectly well, however, when I tried to set the code for this project up as a webserver, I had a hard time trying to figure out how to specify the python interpreter (in packages/Flask). I kept getting module import errors, and I'm currently not exactly sure how to fix this...


