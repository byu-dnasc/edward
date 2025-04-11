# Running the app in different environments

This document explains how to run the app in different environments.

There are several objects that should be configured differently depending on the environment in which the app is running, including system parameters, service client credentials.

### Configuring service clients for testing

By default, if a client cannot be initialized (e.g. service is not available, credentials are invalid), the object will still be available, however its value will be assigned `None`.

A testing environment usually doesn't provide live Globus and/or SMRT Link services.

If services are unavailable, their clients are assigned `None`.
This way, the variable exists and thus can be targeted by `unittest.mock` features.
These `unittest.mock` features are used stand in for these service clients, mimicking their behavior.


### Nominal execution (fully operational state)

In scenarios where service clients are expected to be functional, a check must be performed to see whether their initialization succeeded.
If the client variable's value is `None`, then the initialization failed.
Otherwise, assume that the client is good to go.
A script `app.__main__.py` has been prepared to start the app and verify that it is fully functional.
If any of these checks fail, the script exits and prints an error message.

## Load environment variables

Most configurable parameters that affect the app's execution are drawn from a file `.env`.
These variables are loaded once upon startup of the app.
For the duration of the app, these variables can be imported by other modules by importing `app`.
The app looks for a file called `.env` in the working directory, unless `pytest` is loaded, in which case it looks for the file at `tests/.env`.

## Initialize the SMRT Link client

The `smrtlink` module has a variable `CLIENT` that gets initialized on startup.
If no SMRT Link service is available, then an exception will rise.
This exception is handled by setting `CLIENT` to `None`.

## Initialize an instance of FastAPI

Loading the `app/endpoints.py` module creates an instance of FastAPI called `FASTAPI`.
