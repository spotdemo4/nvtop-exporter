# nvtop-exporter

[![check](https://img.shields.io/github/actions/workflow/status/spotdemo4/nvtop-exporter/check.yaml?branch=main&logo=github&logoColor=%23bac2de&label=check&labelColor=%23313244)](https://github.com/spotdemo4/nvtop-exporter/actions/workflows/check.yaml/)
[![vulnerable](https://img.shields.io/github/actions/workflow/status/spotdemo4/nvtop-exporter/vulnerable.yaml?branch=main&logo=github&logoColor=%23bac2de&label=vulnerable&labelColor=%23313244)](https://github.com/spotdemo4/nvtop-exporter/actions/workflows/vulnerable.yaml)
[![nix](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fspotdemo4%2Fnvtop-exporter%2Frefs%2Fheads%2Fmain%2Fflake.lock&query=%24.nodes.nixpkgs.original.ref&logo=nixos&logoColor=%23bac2de&label=channel&labelColor=%23313244&color=%234d6fb7)](https://nixos.org/)
[![python](<https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fspotdemo4%2Fnvtop-exporter%2Frefs%2Fheads%2Fmain%2F.python-version&search=(.*)&logo=python&logoColor=%23bac2de&label=version&labelColor=%23313244&color=%23306998>)](https://www.python.org/downloads/)

![github](https://img.shields.io/github/v/release/spotdemo4/nvtop-exporter?include_prereleases&sort=semver&logo=github&logoColor=%23bac2de&label=GitHub&labelColor=%23313244&color=%234d6fb7)
[![flakehub](https://img.shields.io/endpoint?url=https://flakehub.com/f/spotdemo4/nvtop-exporter/badge)](https://flakehub.com/flake/spotdemo4/nvtop-exporter)
[![pypi](https://img.shields.io/pypi/v/nvtop-exporter?logo=pypi&logoColor=%23bac2de&labelColor=%23313244&color=%23306998&label=PyPI)](https://pypi.org/project/nvtop-exporter/)

Prometheus exporter for [`syllo/nvtop`](https://github.com/Syllo/nvtop)

### Metrics

```bash
# HELP gpu_clock_mhz gpu clock MHz
# TYPE gpu_clock_mhz gauge
gpu_clock_mhz{device="DG2 (Arc A770)",index="0"} 2400.0
# HELP gpu_mem_clock_mhz mem clock MHz
# TYPE gpu_mem_clock_mhz gauge
gpu_mem_clock_mhz{device="DG2 (Arc A770)",index="0"} 0.0
# HELP gpu_temp_celsius gpu temp celsius
# TYPE gpu_temp_celsius gauge
gpu_temp_celsius{device="DG2 (Arc A770)",index="0"} 48.0
# HELP gpu_fan_speed_rpm gpu fan speed rpm
# TYPE gpu_fan_speed_rpm gauge
gpu_fan_speed_rpm{device="DG2 (Arc A770)",index="0"} 302.0
# HELP gpu_power_draw_watts gpu power draw watts
# TYPE gpu_power_draw_watts gauge
gpu_power_draw_watts{device="DG2 (Arc A770)",index="0"} 38.0
# HELP gpu_usage gpu utilization %
# TYPE gpu_usage gauge
gpu_usage{device="DG2 (Arc A770)",index="0"} 0.0
# HELP gpu_mem_usage gpu memory utilization %
# TYPE gpu_mem_usage gauge
gpu_mem_usage{device="DG2 (Arc A770)",index="0"} 0.0
# HELP gpu_encode_decode_usage gpu encode/decode utilization %
# TYPE gpu_encode_decode_usage gauge
gpu_encode_decode_usage{device="DG2 (Arc A770)",index="0"} 0.0
# HELP gpu_mem_total_bytes gpu memory total bytes
# TYPE gpu_mem_total_bytes gauge
gpu_mem_total_bytes{device="DG2 (Arc A770)",index="0"} 1.7079205888e+010
# HELP gpu_mem_used_bytes gpu memory used bytes
# TYPE gpu_mem_used_bytes gauge
gpu_mem_used_bytes{device="DG2 (Arc A770)",index="0"} 7.3265152e+07
# HELP gpu_mem_free_bytes gpu memory free bytes
# TYPE gpu_mem_free_bytes gauge
gpu_mem_free_bytes{device="DG2 (Arc A770)",index="0"} 1.7005940736e+010
# HELP gpu_process_usage gpu process utilization %
# TYPE gpu_process_usage gauge
gpu_process_usage{cmdline="/usr/lib/plexmediaserver/Plex Transcoder ...",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1522258",user="trev"} 0.0
gpu_process_usage{cmdline="nvtop -s",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1550252",user="root"} 0.0
# HELP gpu_process_mem_usage gpu process memory utilization %
# TYPE gpu_process_mem_usage gauge
gpu_process_mem_usage{cmdline="/usr/lib/plexmediaserver/Plex Transcoder ...",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1522258",user="trev"} 0.01
gpu_process_mem_usage{cmdline="nvtop -s",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1550252",user="root"} 0.0
# HELP gpu_process_encode_decode_usage gpu process encode/decode utilization %
# TYPE gpu_process_encode_decode_usage gauge
gpu_process_encode_decode_usage{cmdline="/usr/lib/plexmediaserver/Plex Transcoder ...",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1522258",user="trev"} 0.0
gpu_process_encode_decode_usage{cmdline="nvtop -s",device="DG2 (Arc A770)",index="0",kind="graphic",pid="1550252",user="root"} 0.0
```

## Use

```console
$ ./nvtop-exporter
2026-02-23 11:52:09,536 - INFO - Starting server on :8080
```

### Environment

| Variable  | Default | Description                           |
| --------- | ------- | ------------------------------------- |
| PORT      | 8080    | Port for the HTTP server to listen on |
| LOG_LEVEL | INFO    | How verbose the logs should be        |

### Prometheus

```yaml
scrape_configs:
  - job_name: nvtop
    static_configs:
      - targets:
          - 127.0.0.1:8080"
```

## Install

### AppImage

[`nvtop-exporter_0.0.8_linux_amd64.AppImage`](https://github.com/spotdemo4/nvtop-exporter/releases/tag/v0.0.8)

```console
$ chmod +x nvtop-exporter_0.0.8_linux_amd64.AppImage
$ ./nvtop-exporter_0.0.8_linux_amd64.AppImage
2026-02-23 11:52:09,536 - INFO - Starting server on :8080
```

#### Service

`nvtop_exporter.service`

```ini
[Unit]
Description=nvtop gpu exporter
After=network.target

[Service]
ExecStart=/usr/local/bin/nvtop-exporter_0.0.8_linux_amd64.AppImage
Type=simple
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Docker

```elm
docker run ghcr.io/spotdemo4/nvtop-exporter:0.0.8
```

#### Nvidia

`docker-compose.yaml`

```yaml
services:
  nvtop-exporter:
    image: ghcr.io/spotdemo4/nvtop-exporter:0.0.8
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

#### Intel

`docker-compose.yaml`

```yaml
services:
  nvtop-exporter:
    image: ghcr.io/spotdemo4/nvtop-exporter:0.0.8
    pid: host
    ports:
      - "8080:8080"

    # Expose the GPU
    devices:
      - /dev/dri:/dev/dri
    cap_add:
      - CAP_PERFMON
```

### Python

#### pip

```elm
pip install nvtop-exporter
```

#### uv

```elm
uvx nvtop-exporter
```

### Nix

```elm
nix run github:spotdemo4/nvtop-exporter
```
