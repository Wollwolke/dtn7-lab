#! /bin/bash

rm -rf /shared/ros_ws/
cp -a /tmp/shared/ros_ws/ /shared/

cd /shared/ros_ws
colcon build --cmake-clean-cache --packages-select dtn_proxy --cmake-args -DCMAKE_BUILD_TYPE=Release
