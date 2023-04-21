#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from tf2_msgs.msg import TFMessage


class TfSubscriber(Node):
    def __init__(self):
        super().__init__("tf_subscriber")
        self.subscription = self.create_subscription(
            TFMessage, "/tf", self.listener_callback, 10
        )
        self.msgCount = 0

    def listener_callback(self, msg):
        if (
            msg.transforms[0].child_frame_id == "map"
            and msg.transforms[0].header.frame_id == "base_link"
        ):
            self.msgCount += 1

    def __del__(self):
        print(f"tf_log - Message Count: {self.msgCount}")


def main():
    rclpy.init(args=None)

    tfSubscriber = TfSubscriber()
    try:
        rclpy.spin(tfSubscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
