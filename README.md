# Apache-log-manager
Apache-log-manager is a Django app for Apache log processing and analysis with the Django admin web interface.    


<img src="/extra/screenshot.png" alt="Django admin"/>

Get Started
===========

The easiest way is to use the supplied Dockerfile.

1. To build the Docker image, run:
```
make -f docker/Makefile build
```

2. Then, to initialize the database structure and set up the default user, run:
```
make -f docker/Makefile init
```

3. To load Apache logs from the link use:
```
# The Apache log file must be written in the following format:
# %h %l %u %{[%d/%b/%Y:%H:%M:%S %z]}t "%r" %>s %b "%{Referer}i" "%{User-agent}i"

make -f docker/Makefile link=[LINK] load

# For example:
# make -f docker/Makefile link=http://www.almhuette-raith.at/apache-log/access.log load
```

4. Finally to run the Django webserver, issue:
```
make -f docker/Makefile app
```

5. Go to [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) and use `user: admin, pass: 123456`.

6. Enjoy!
