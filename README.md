# DTN7 Lab

Run Container:

```sh
sudo modprobe ebtables
podman run -it -d --init \
    --privileged \
    --name dtn \
    -p 5901:5901 \
    -v ./shared:/shared \
    dtn7-lab
```
You can then connect with any VNC client to the local *dtn7 showroom* instance with the password `sneakers`.

*NOTE:* In case of weird connection problems within the showroom, please make sure that *ebtables* and *sch_netem* kernel modules are loaded!

## Manually building the container

Just run `docker build -t dtn7-showroom .` and run it with `docker run --rm -it --name showroom -p 5901:5901 --privileged -v /tmp/shared:/shared dtn7-showroom`

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

## Notes

- routing algorithms
    - epidemic (default)
    - flooding
    - sink
    - external
    - sprayandwait

