# nvtop exporter

[![check](https://img.shields.io/github/actions/workflow/status/spotdemo4/nvtop-exporter/check.yaml?branch=main&logo=github&logoColor=%23bac2de&label=check&labelColor=%23313244)](https://github.com/spotdemo4/nvtop-exporter/actions/workflows/check.yaml/)
[![vulnerable](https://img.shields.io/github/actions/workflow/status/spotdemo4/nvtop-exporter/vulnerable.yaml?branch=main&logo=github&logoColor=%23bac2de&label=vulnerable&labelColor=%23313244)](https://github.com/spotdemo4/nvtop-exporter/actions/workflows/vulnerable.yaml)
[![nix](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fspotdemo4%2Fnvtop-exporter%2Frefs%2Fheads%2Fmain%2Fflake.lock&query=%24.nodes.nixpkgs.original.ref&logo=nixos&logoColor=%23bac2de&label=channel&labelColor=%23313244&color=%234d6fb7)](https://nixos.org/)
[![python](<https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fspotdemo4%2Fnvtop-exporter%2Frefs%2Fheads%2Fmain%2F.python-version&search=(.*)&logo=python&logoColor=%23bac2de&label=version&labelColor=%23313244&color=%23306998>)](https://www.python.org/downloads/)

prometheus exporter for [`Syllo/nvtop`](https://github.com/Syllo/nvtop)

## use

```elm
nvtop-exporter
```

### environment

| Variable  | Description                           | Default |
| --------- | ------------------------------------- | ------- |
| PORT      | Port for the HTTP server to listen on | 8080    |
| LOG_LEVEL | How verbose the logs should be        | INFO    |

## install

### docker

```elm
docker run ghcr.io/spotdemo4/nvtop-exporter:0.0.2
```

#### nvidia

```yaml
services:
  nvtop:
    image: ghcr.io/spotdemo4/nvtop-exporter:0.0.2
    pid: host
    ports:
      - "8080:8080"

    # Expose the GPU
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities:
                - gpu
```

#### intel

```yaml
services:
  nvtop-exporter:
    image: ghcr.io/spotdemo4/nvtop-exporter:0.0.2
    pid: host
    ports:
      - "8080:8080"

    # Expose the GPU
    devices:
      - /dev/dri:/dev/dri
    cap_add:
      - CAP_PERFMON
```

### nix

```elm
nix run github:spotdemo4/nvtop-exporter
```

### uv

```elm
uvx git+https://github.com/spotdemo4/nvtop-exporter
```
