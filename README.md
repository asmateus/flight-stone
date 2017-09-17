# FlightStone

[![Build Status](https://travis-ci.org/asmateus/flight-stone.svg?branch=master)](https://travis-ci.org/asmateus/flight-stone)
[![Documentation Status](https://readthedocs.org/projects/flight-stone/badge/?version=latest)](http://flight-stone.readthedocs.io/en/latest/?badge=latest)



FlightStone is a complete platform for drone navigation in bounded environments (it is tested indoor). The system comprises an onboard controller for obstacle avoidance and path finding (using information obtained from proximity sensors and a cheap camera), a wireless sensor network for accurate positioning of the drone via adaptive triangulation and a base server were information is stored/retreived from and the hard computation is performed, if needed (this can be toggled).

## Content
This repository contains the firmware of the wireless sensor network (WSN) and onboard controller (OC), and the source code for the base server. As you can see it is a large solution so be sure to read through the documentation before building. Pre-compiled code is offered for the WSN and OC, as this is base code were you are expected to have the correct hardware. A guide to build the solution is offered, from code documentation to electrical characteristics, such as device selection, bill of materials, gerber schematics of the circuits, performance and limitations, etc.

## Impact
Write here the possible uses of what we are doing

## Usage
Usage information is rather large so, go to the source directly. However, to give a taste here are the following commands:
* To test serial communications execute `python -m test.general_testbed -t serial`
* To test keyboard communication to PIC execute `python -m test.general_testbed -t keytocontroller`
* To test tracking execute `python -m test.general_testbed -t tracking`
* To test patch selection execute `python -m test.general_testbed -t patchselector`
There you go, play with that.

## Versioning
*Current version: **1.0624***

Versioning is done through milestones and through issue completion. The number after the decimal point indicates the milestone we are in, the number before it is composed by the date the last feature change was made. Different branches may have different versions, but the official one is always in the master branch. Each time a major version change occurs you will see a new release with a fancy name.

## References

[1] Hagström, K. (2013). Tutorial - nRF24L01 and AVR. [online] Gizmosnack.blogspot.com.co. Available at: http://gizmosnack.blogspot.com.co/2013/04/tutorial-nrf24l01-and-avr.html [Accessed 11 Jun. 2017].

[2] http://www.atmel.com/images/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf
