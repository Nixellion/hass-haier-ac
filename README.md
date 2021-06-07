# hass-haier-ac

Home Assistant Haier AC Custom integration

This repository is a heavy work in progress and is not in a working state yet.

The code is based on this Homebridge plugin: https://github.com/bstuff/haier-ac-remote

# Goals 

First step is to convert haier-ac-remote code to Python to a state where we can succesfully send proper commands to Haier AC and it will properly respond to them and perform proper actions.

Second step is converting the response parsing part so we can get AC state.

And the final step will be to write it into a proper Home Assistant integration. After that it can be added to HACS.

# Current state

Currently most of the bytecode functions and commands have been translated to the best of my and my friend's knowledge. Code sends commands to AC and it seems to do **something**, because after running this code AC will no longer reply to other commands from original HomeBridge plugin until it's turned OFF and then back ON from it's original IR remote.

I suspect there may be some mistake in bytecode conversion or maybe some important step is missing.