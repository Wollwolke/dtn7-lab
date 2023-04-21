#!/bin/bash
while true; do
    echo "$(date +%s), $(position_dump)" >> output.txt
    sleep 1
done
