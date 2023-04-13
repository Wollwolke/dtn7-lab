#! /bin/bash

rm -rf /shared/ros_ws/
cp -a /tmp/shared/ros_ws/ /shared/
rm -rf /shared/ros_ws/build /shared/ros_ws/install /shared/ros_ws/log

cd /shared/ros_ws

colcon build --cmake-clean-cache --packages-up-to dtn_proxy --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
