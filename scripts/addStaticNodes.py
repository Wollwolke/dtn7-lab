#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET

FIRST_ID = 6
FIRST_IP4 = 24
FIRST_IP6 = 18
FIRST_MAC = 4


def updateFile(args):
    staticNodes = []
    with open(args.static, "r") as file:
        data = file.readlines()
    for line in data:
        _, _, x, y = line.split()
        staticNodes.append((float(x), float(y)))

    tree = ET.parse(args.scenario)
    root = tree.getroot()

    devices = root.find("devices")
    links = root.find("links")

    cnt = 0
    for node in staticNodes:
        new_device = ET.SubElement(
            devices,
            "device",
            attrib={
                "id": f"{FIRST_ID + cnt}",
                "name": f"static{cnt}",
                "icon": "",
                "canvas": "0",
                "type": "DTN",
                "class": "",
                "image": "",
            },
        )
        ET.SubElement(
            new_device,
            "position",
            attrib={"x": f"{node[0]:.2f}", "y": f"{node[1]:.2f}"},
        )
        services = ET.SubElement(new_device, "services")
        ET.SubElement(services, "service", attrib={"name": "DefaultMulticastRoute"})

        new_link = ET.SubElement(
            links, "link", attrib={"node1": "1", "node2": f"{FIRST_ID + cnt}"}
        )
        ET.SubElement(
            new_link,
            "iface2",
            attrib={
                "id": "0",
                "name": "eth0",
                "mac": f"00:00:00:aa:00:{(FIRST_MAC + cnt):02x}",
                "ip4": f"10.0.0.{FIRST_IP4 + cnt}",
                "ip4_mask": "24",
                "ip6": f"2001::{FIRST_IP6 + cnt}",
                "ip6_mask": "128",
            },
        )

        cnt += 1

    tree.write(
        args.output,
        encoding="UTF-8",
        xml_declaration="True",
    )
    print(root)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--scenario",
        help="file path to the core scenario",
        default="/home/lars/Documents/mt/dtn7-lab/shared/scenarios/industrial/template.xml",
    )
    parser.add_argument(
        "--static",
        help="file path to the csv file containing the static nodes",
        default="/home/lars/Documents/mt/dtn7-lab/shared/data/bm/static.csv",
    )
    parser.add_argument(
        "--output",
        help="file path store the new scenario",
        default="/home/lars/Documents/mt/dtn7-lab/scripts/test.xml",
    )
    args = parser.parse_args()

    updateFile(args)


if __name__ == "__main__":
    main()
