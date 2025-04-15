# Edward proxy server

The proxy server is what ties SMRT Link and the Edward app together.

## Nginx

The proxy server runs on [Nginx](http://nginx.org).
The first step is to make sure that Nginx is installed on the server that SMRT Link is running on.

### Generating the Nginx config file

Once Nginx is installed on the server, you need to generate a config file named `nginx.conf`.
`nginx.conf` defines how the proxy server behaves.
In addition to issuing commands to Nginx, `nginx.sh` also generates `nginx.conf` automatically if it is not found.
`nginx.sh` contains several variables, some of which are found in `template.conf`.
Some of these variables have default values, but others will be specific to your system.
Please insert a value for each of the following variables in `nginx.sh`:
- `CERT`: path to the HTTPS certificate used to secure SMRT Link.
In `nginx.conf`, a value for `CERT` is suggested that is based on the value of `SMRT_ROOT` (see below).
- `CERT_KEY`: path to the HTTPS certificate key file. Should be in the same directory as the certificate.
- `SL_USER`: the username of the user that owns SMRT Link's files.
For Nginx to be able to read the HTTPS certificate, it will need the file permissions required to do so.
So, strictly speaking, an acceptable value of `SL_USER` is the name of any user that has read access to `CERT`.
- `PROXY_HOST`: hostname of the server where Nginx will be running.
This value is used to create a link in `index.html` to the SMRT Link proxy.
`index.html` is generated in like manner to `nginx.conf`, i.e. using a template.
- `SMRT_ROOT` (optional): the value of `SMRT_ROOT` is the path to directory described in the [SMRT Link documentation](https://www.pacb.com/wp-content/uploads/SMRT-Link-software-installation-guide-v25.2.pdf).
The documentation suggests that `SMRT_ROOT` should be `/opt/pacbio/smrtlink`, but this may not be suitable for all systems.
If your system doesn't conform with this suggestion, then ignore `SMRT_ROOT` and just use `CERT` and `CERT_KEY` to locate the certificate directly.

Once you have populated these variables, run `nginx.sh` to generate the config file.
This will substitute the values found in `nginx.sh` for the references found in `template.conf` to make `nginx.conf`.
Note that you need to run `nginx.sh` as `SL_USER` (see above).
This is because Nginx will need read access to `CERT`.

## Running the server

Once Nginx is installed and `nginx.conf` is generated, run the proxy server using the script `nginx.sh`.
Note that you need to run `nginx.sh` as `SL_USER` (see above).
This is because Nginx will need read access to `CERT`.

`./nginx.sh start` starts the proxy server.

`./nginx.sh stop` stops the proxy server.

Point your browser to host:8080 (where host is the url for the server running Nginx) to verify that the proxy server is online.
This should serve up the HTML file found in this directory.
This page provides a link to use to access SMRT Link via the proxy.

## Modifying `nginx.conf`

If something is wrong with `nginx.conf`, you could modify it directly, but if the necessary change is a different value for a variable found in `nginx.sh`, then you could follow this procedure instead:
- Modify the value of the variable in `nginx.sh`.
- Delete `nginx.conf`.
- Run `nginx.sh`.

The idea is that using the parameters defined in `nginx.sh` to generate `nginx.conf` is sometimes a more reproducable approach.