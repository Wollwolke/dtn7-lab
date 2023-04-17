#!/usr/bin/env python3

import random
from collections import defaultdict

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException

from sensor_msgs.msg import RelativeHumidity
from sensor_msgs.msg import Temperature

noConnectionCounter = 10

class MsgGenerator(Node):
    def __init__(self):
        super().__init__("msg_generator")
        random.seed("specialSeed")
       
        self.tempPub = self.create_publisher(Temperature, "/temperature", 10)
        self.count = defaultdict(lambda: 0)
        self.timerInterval = 2.0
        self.timer = self.create_timer(self.timerInterval, self.timerCallback)

        self.tempMsg = Temperature()
        self.tempMsg.header.frame_id = "test"

    def timerCallback(self):
        global noConnectionCounter
        self.tempMsg.header.stamp = self.get_clock().now().to_msg()
        self.tempMsg.temperature = random.uniform(0,1)
        self.tempMsg.variance = random.uniform(0,1)

        self.tempPub.publish(self.tempMsg)
        if noConnectionCounter == 0:
            self.count["/temperature"] = 1
        else:
            self.count["/temperature"] += 1
        noConnectionCounter -= 1

    def __del__(self):
        print(f"msg_generator interval: {self.timerInterval}")
        for topic in ["/temperature"]:
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
