#! /bin/bash

cd ros_ws
colcon build --cmake-clean-cache --packages-select dtn_proxy --cmake-args -DCMAKE_BUILD_TYPE=Release
