#!/usr/bin/env python3

"""Player for step files generated with calcCoreStepFiles.py. Moves nodes in CORE using 'core-pos'."""

from collections import defaultdict
import argparse
import time
import subprocess


def parseStepFile(filePath):
    stepsDir = defaultdict(lambda: {})
    nodes = set()
    with open(filePath, "r") as file:
        lines = file.readlines()

    for line in lines:
        if not line or line.startswith("#"):
            continue
        if line.startswith("%"):
            time_ = int(line[1::].strip())
        else:
            node, x, y = line.split()
            nodes.add(node)
            stepsDir[time_][node] = (float(x), float(y))

    return stepsDir, nodes


def getNodeIds(nodeList):
    nodeMap = {}
    for node in nodeList:
        initial_pos = subprocess.run(["core-pos", node], stdout=subprocess.PIPE)
        try:
            id = initial_pos.stdout.decode("utf-8").split("\n")[0].split()[0]
        except IndexError as err:
            raise ValueError(f"Node {node} doesn't exist in current simulation.")
        nodeMap[node] = int(id)
    return nodeMap

def sendInitPos(stepFile, nodeIds):
    if list(stepFile.keys())[0] != 0:
        raise ValueError("Can't set initial Positions, Timestep 0 not available.")
    for node, point in list(stepFile.values())[0].items():
        cmd = ["core-pos", str(nodeIds[node]), str(point[0]), str(point[1]), "0"]
        subprocess.call(cmd)
        print(f"Set inital position: {node} - ({point[0]},{point[1]})")

def playStepFile(stepFile, nodeIds, start):
    # lastRun = start #time.time() * 1000
    times = list(stepFile.keys())
    nodes = list(stepFile.values())
    index = 0
    cmds = []

    def sendIfReady():
        nonlocal index
        diff = times[index] + start - time.time() * 1000 - 1
        if diff > 0:
            time.sleep((diff) / 1000)
        if time.time() * 1000 >= times[index] + start:
            for cmd in cmds:
                subprocess.call(cmd)
            cmds.clear()
            index += 1

    while index < len(times):
        if len(cmds) == 0:
            # fill cmd queue
            for node, point in nodes[index].items():
                cmd = ["core-pos", str(nodeIds[node]), str(point[0]), str(point[1]), "0"]
                cmds.append(cmd)
            # check time and send
            sendIfReady()
        else:
            # check time and send
            sendIfReady()


def main():
    start = time.time() * 1000
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", help="StepFile to play")
    parser.add_argument(
        "--init",
        help="Sends the positions of Timestep 0",
        dest="init",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    stepFile, nodeList = parseStepFile(args.input)
    nodeIds = getNodeIds(nodeList)
    if args.init:
        sendInitPos(stepFile, nodeIds)
    else:
        playStepFile(stepFile, nodeIds, start)


if __name__ == "__main__":
    main()
