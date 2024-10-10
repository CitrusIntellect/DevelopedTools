#!/bin/bash

CONFIG_DIR="/home/elias/.config/waybar"

while true; do
    inotifywait -r -e modify,create,delete "$CONFIG_DIR" &&
    {
        echo "Change detected. Restarting waybar..."
        pkill waybar
        waybar &
    }
done