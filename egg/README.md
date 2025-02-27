# EGG

Welcome to egg, weary traveller. This directory contains all of the code for the egg's brain, which is really just a single Python file.

## Running the code

### Prereqs
This is meant to run on an adafruit RP2040 SCORPIO board, which is unique in that it has 8 dedicated channels for running peripherals, each with a data and ground pin. 

https://www.adafruit.com/product/5650


### Board Setup & CircuitPython
If you have a board, and you have the ability to hook it up to a dev machine, follow the instructions here on how to get setup with CircuitPython:

https://learn.adafruit.com/introducing-feather-rp2040-scorpio

Use the provided uf2 file to flash the board


### Deploying
Once you see the board show up as a directory on your dev machine, deploying should be as simple as copying main.py over and changing its name to code.py on the board's storage.

Make sure to also include the mpy files in the lib directory.


## Pinouts

The SCORPIO has 8 separate output pins, and several input ones (of which we only use 4). 

### Inputs

Inputs to the code are treated as instructions to switch to a certain mode, or mood. Each pin will transition the egg to that corresponding mood. These are pulled down, so a HIGH signal will turn that mood on.

<pre>A0 = stasis - flash slow blue light every 30 seconds, no smoke</pre>
<pre>A1 = idle - green blinks every 6 seconds, soft smoke</pre>
<pre>A2 = angry - furious red heartbeat, angry alternating smoke</pre>
<pre>A3 = happy - rainbow color chase, soft smoke</pre>

### Outputs

NeoPixel output on the first SCORPIO pin.

Vape outputs on SCORPIO pins 2-8


## Configuration

### Lights
Lights config is defined as heartbeats, which essentially is two pulses, one after the other.

Each mood has a config defined as:
<pre>{
    'color': (0.01, 0.01, 0.9), # what color should we flash for this mood?
    'counter_start': 300, # when to do the first beat after changing to this mood, in "frames"
    'second_beat_start': 100, # how long after the first pulse should the second pulse start
    'second_beat_end': 105,
    'drop_rate': 1.2, # how quickly does each pulse fade?
    'beat_interval': 30, # seconds
    'last_heartbeat': 0 # seconds (as float)
}</pre>

Note, the "happy" mood ignores this configuration, since it just uses a looping rainbow chase animation.

### Vapes
Each vape is controlled separately, and can only be turned on or off.

Each mood has a config defined as:
<pre>{
    'total_time': 10000, # How long this entire cycle lasts, in "frames"
    'rate': 1, # How many frames in a cycle
    'vape_1_start': 50, # At what point in the cycle do we turn on the first vape?
    'vape_1_end': 150, # Same, but when to turn it off
    'vape_2_start': 2000,
    'vape_2_end': 2100,
    'vape_3_start': 7050,
    'vape_3_end': 7150
}</pre>
