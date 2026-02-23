import os
import signal
import logging
from prometheus_client import (
    GC_COLLECTOR,
    PLATFORM_COLLECTOR,
    PROCESS_COLLECTOR,
    start_http_server,
)
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client.registry import Collector
from .nvtop import get_nvtop

log = logging.getLogger(__name__)


class NvTopCollector(Collector):
    def collect(self):
        log.info("Getting GPU metrics")
        top = get_nvtop()

        # device guages
        gpu_clock = GaugeMetricFamily(
            "gpu_clock_mhz", "gpu clock MHz", labels=["device"]
        )
        mem_clock = GaugeMetricFamily(
            "gpu_mem_clock_mhz", "mem clock MHz", labels=["device"]
        )
        temp = GaugeMetricFamily(
            "gpu_temp_celsius", "gpu temp celsius", labels=["device"]
        )
        fan_speed = GaugeMetricFamily(
            "gpu_fan_speed_rpm", "gpu fan speed rpm", labels=["device"]
        )
        power_draw = GaugeMetricFamily(
            "gpu_power_draw_watts", "gpu power draw watts", labels=["device"]
        )
        gpu_util = GaugeMetricFamily(
            "gpu_util_ratio", "gpu utilization %", labels=["device"]
        )
        encode_decode = GaugeMetricFamily(
            "gpu_encode_decode_ratio", "gpu encode/decode %", labels=["device"]
        )
        mem_util = GaugeMetricFamily(
            "gpu_mem_util_ratio", "gpu memory util %", labels=["device"]
        )
        mem_total = GaugeMetricFamily(
            "gpu_mem_total_bytes", "gpu memory total bytes", labels=["device"]
        )
        mem_used = GaugeMetricFamily(
            "gpu_mem_used_bytes", "gpu memory used bytes", labels=["device"]
        )
        mem_free = GaugeMetricFamily(
            "gpu_mem_free_bytes", "gpu memory free bytes", labels=["device"]
        )

        # process guages
        process_gpu_usage = GaugeMetricFamily(
            "gpu_process_usage_ratio",
            "gpu process usage %",
            labels=["device", "pid", "cmdline", "kind", "user"],
        )
        process_gpu_mem_usage = GaugeMetricFamily(
            "gpu_process_mem_usage_ratio",
            "gpu process memory usage %",
            labels=["device", "pid", "cmdline", "kind", "user"],
        )
        process_encode_decode = GaugeMetricFamily(
            "gpu_process_encode_decode_ratio",
            "gpu process encode/decode %",
            labels=["device", "pid", "cmdline", "kind", "user"],
        )

        for device in top.devices:
            gpu_clock.add_metric([device.device_name], device.gpu_clock)
            mem_clock.add_metric([device.device_name], device.mem_clock)
            temp.add_metric([device.device_name], device.temp)
            fan_speed.add_metric([device.device_name], device.fan_speed)
            power_draw.add_metric([device.device_name], device.power_draw)
            gpu_util.add_metric([device.device_name], device.gpu_util)
            encode_decode.add_metric([device.device_name], device.encode_decode)
            mem_util.add_metric([device.device_name], device.mem_util)
            mem_total.add_metric([device.device_name], device.mem_total)
            mem_used.add_metric([device.device_name], device.mem_used)
            mem_free.add_metric([device.device_name], device.mem_free)

            for process in device.processes:
                process_gpu_usage.add_metric(
                    [
                        device.device_name,
                        str(process.pid),
                        process.cmdline,
                        process.kind,
                        process.user,
                    ],
                    process.gpu_usage,
                )
                process_gpu_mem_usage.add_metric(
                    [
                        device.device_name,
                        str(process.pid),
                        process.cmdline,
                        process.kind,
                        process.user,
                    ],
                    process.gpu_mem_usage,
                )
                process_encode_decode.add_metric(
                    [
                        device.device_name,
                        str(process.pid),
                        process.cmdline,
                        process.kind,
                        process.user,
                    ],
                    process.encode_decode,
                )

        yield gpu_clock
        yield mem_clock
        yield temp
        yield fan_speed
        yield power_draw
        yield gpu_util
        yield encode_decode
        yield mem_util
        yield mem_total
        yield mem_used
        yield mem_free

        yield process_gpu_usage
        yield process_gpu_mem_usage
        yield process_encode_decode


def init() -> None:
    log.debug("Unregistering default collector metrics")
    REGISTRY.unregister(GC_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(PROCESS_COLLECTOR)

    log.debug("Registering NvTop Collector")
    REGISTRY.register(NvTopCollector())


def start() -> None:
    port = os.getenv("PORT", "8080")
    log.info(f"Starting server on :{port}")
    server, t = start_http_server(int(port))

    def shutdown(sig, frame):
        log.info("Shutting down")
        server.shutdown()
        server.server_close()

    signal.signal(signal.SIGINT, shutdown)
    t.join()
