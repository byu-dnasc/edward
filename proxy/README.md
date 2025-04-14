# Edward proxy server

The proxy server is what ties SMRT Link and the Edward app together.

## Nginx

The proxy server runs on [Nginx](http://nginx.org).
The first step is to make sure that Nginx is installed on the server that SMRT Link is running on.

## Running the server

Once Nginx is installed, run the proxy server using the script `nginx.sh`.
Before running the script, you need to modify it by inserting the value of `SMRT_ROOT`.
`SMRT_ROOT` is a path that points to the `SMRT_ROOT` directory on your SMRT Link server.
The `SMRT_ROOT` directory is described in the SMRT Link documentation.
Without knowning the path to this directory, Nginx can't find the HTTPS certificates it needs to proxy HTTP requests securely.
In addition to `SMRT_ROOT`, the script also requires that you provide the hostname of the server where SMRT Link is running.

`./nginx.sh start` starts the proxy server.

`./nginx.sh stop` stops the proxy server.

Point your browser to host:8080 (where host is the url for the server running Nginx) to verify that the proxy server is online.
This should serve up the HTML file found in this directory.
This page provides a link to use to access SMRT Link via the proxy.