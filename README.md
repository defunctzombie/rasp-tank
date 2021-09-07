# Build

```shell
make build-image
```

# Development (local)

```shell
make local-shell
```

# Deploy and Launch (raspberry pi)

## On Host

```shell
make build-image
make deploy-image
```

## On Pi

> sudo since we need to run privileged on the raspberry pi to access gpio

```shell
sudo podman load --input rasp-tank.tar.gz
sudo podman run --privileged --rm -p 9090:9090 rasp-tank
```
