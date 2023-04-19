#!/usr/bin/env python3

import random
import os
from collections import defaultdict

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException

from sensor_msgs.msg import Image
from sensor_msgs.msg import Temperature

class MsgGenerator(Node):
    def __init__(self):
        super().__init__("msg_generator")
        random.seed("specialSeed")
       
        self.tempPub = self.create_publisher(Temperature, "/temperature", 10)
        self.imgPub = self.create_publisher(Image, "/detectedImages", 10)
        self.count = defaultdict(lambda: 0)
        self.timerInterval = 1.0
        self.timer = self.create_timer(self.timerInterval, self.timerCallback)

        self.tempMsg = Temperature()
        self.tempMsg.header.frame_id = "test"

        self.imgMsg = Image()
        self.imgMsg.header.frame_id = "test"
        self.imgMsg.encoding = "rgb8"
        self.imgMsg.is_bigendian = 0
        self.imgMsg.step = 1920
        self.imgMsg.width = 640
        self.imgMsg.height = 480

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "image.bin")
        with open(file_path, "rb") as file:
            data = file.read()
            self.imgMsg.data = list(data)

    def timerCallback(self):
        self.tempMsg.header.stamp = self.get_clock().now().to_msg()
        self.tempMsg.temperature = random.uniform(0,1)
        self.tempMsg.variance = random.uniform(0,1)

        self.imgMsg.header.stamp = self.get_clock().now().to_msg()

        self.tempPub.publish(self.tempMsg)
        self.imgPub.publish(self.imgMsg)

        self.count["/temperature"] += 1
        self.count["/detectedImages"] += 1

    def __del__(self):
        print(f"msg_generator interval: {self.timerInterval}")
        for topic in ["/temperature", "/detectedImages"]:
            print(f"{topic}: {self.count[topic]}")


def main():
    rclpy.init(args=None)
    player = MsgGenerator()

    try:
        rclpy.spin(player)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
