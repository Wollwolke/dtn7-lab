#!/usr/bin/env python3

"""Inject random DTN Messages into node's dtnd service."""

import argparse
import random
import string
import threading
import time
import os

NODES = [f"static{i}" for i in range(10)]
RECEIVER = NODES + ["robot0", "robot1", "robot2", "base"]
SEED = "specialSeed"

shutdownRequested = False


def sendRandomDtnMessage(node, min_length, max_length, rng):
    length = rng.randint(min_length, max_length)
    result = "".join(
        rng.choice(string.ascii_letters + string.digits) for _ in range(length)
    )
    rec = RECEIVER[rng.randint(0, len(RECEIVER) - 1)]
    os.system(f"cexec {node} \"echo '{result}' | dtnsend -r dtn://{rec}/rand\"")


def startThread(node, args):
    global shutdownRequested

    rng = random.Random(SEED + node)
    while not shutdownRequested:
        time.sleep(rng.randint(5, 60))
        sendRandomDtnMessage(node, args.minLen, args.maxLen, rng)


def main():
    global shutdownRequested

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--minLen",
        help="Minimal length of the DTN Message",
        default=10,
    )
    parser.add_argument(
        "--maxLen",
        help="Minimal length of the DTN Message",
        default=40,
    )
    args = parser.parse_args()

    threads = []
    for node in NODES:
        thread = threading.Thread(target=startThread, args=(node, args))
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        shutdownRequested = True
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    main()
