# DTN7 Lab

This repo contains a containerized environment to test the [ROS2DTN Proxy](https://github.com/Wollwolke/dnt_ros_proxy).

Based on [coreemu-lab](https://github.com/gh0st42/coreemu-lab).

## Building the container

```sh
cd docker
./build.sh
```

## Running the environment:

```sh
./clab.sh ./shared/
```

>ℹ In case of weird connection problems within CORE, please make sure that `ebtables` and `sch_netem` kernel modules are loaded!

## Generating Mobility Scripts using BonnMotion

Generating a screnario:  
`bm -f <name> -I <paramsFile> <modelName>`

Convert it to ns-2 format:  
`bm NSFile -f <name>`

>ℹ Resolving the Error *Error reading file*:  
Delete the last empty line in the `paramsFile`

---

## core-helpers

Helper scripts for core network emulator

- `cbash <nodename>` - open bash
- `cexec <node_name> '<commands>'`- execute a command on a specific node
- `ccc` - core crash checker, greps for any FATALs
- `cda <cmd>` - core daemonize all
- `cea <cmd>` - core execute all
- `cpa <cmd>` - core parallel all
- `gf <size> <filename>` - generate file, e.g. `gf 10M /tmp/10m.file`
