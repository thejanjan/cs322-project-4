# UOCIS322 - Project 4 #

- Author: Micah Nichols
- Contact: micahanichols27@gmail.com

This application provides a calculator for determining the opening and closing times of defined controle checkpoints for a RUSA ACP Brevet.

## Algorithm

The open and close times are based on the individual control distance, the complete distance of the brevet, and the start time of the brevet.
To align with rider endurance, different kilometer spans have defined speed ranges (hovering around 15 km/hr min, 30 km/hr max).

The open times are based on the total time it would take to reach the control distance based on the maximum speed of each defined span.
The closed times are calculated similarly, but instead use the minimum speed of each defined span.
In addition, each brevet has a time limit for the close time of the final control, and the close time of the initial control is always one hour after opening.

## Startup

Navigate to the `brevets` directory and run:

`docker build -t <name> .`

Then, run:

`docker run -d -p 5001:5000 <name>`

The application will then be available at `localhost:5001`.

## Application

On the webpage, you can configure the brevet distance and its start time at the top.
From there, you can specify either miles or kilometers to obtain their open and close times. (One may also specify an optional location parameter.)
