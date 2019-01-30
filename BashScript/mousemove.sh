#!/bin/bash

#xdotool mousemove 0 0

for i in {0..10}
do
	xdotool getmouselocation
	sleep 1 
done
