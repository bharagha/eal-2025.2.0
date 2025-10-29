#!/usr/bin/env python3

import json
import logging
import os
import re
import sys
import time

# === Constants ===
FIFO_FILE = "/app/qmassa.fifo"
DEBUG_LOG = "/app/qmassa_reader_trace.log"
HOSTNAME = os.uname()[1]

# Configure logger
logging.basicConfig(
    filename=DEBUG_LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s (line %(lineno)d)",
)


def emit_engine_usage(eng_usage, gpu_id, ts):
    for eng, vals in eng_usage.items():
        if vals:
            print(
                f"gpu_engine_usage,engine={eng},type={eng},host={HOSTNAME},gpu_id={gpu_id} usage={vals[-1]} {ts}"
            )


def emit_frequency(freqs, gpu_id, ts):
    if freqs and isinstance(freqs[-1], list):
        freq_entry = freqs[-1][0]
        if isinstance(freq_entry, dict) and "cur_freq" in freq_entry:
            print(
                f"gpu_frequency,type=cur_freq,host={HOSTNAME},gpu_id={gpu_id} value={freq_entry['cur_freq']} {ts}"
            )


def emit_power(power, gpu_id, ts):
    if power:
        for key, val in power[-1].items():
            print(
                f"gpu_power,type={key},host={HOSTNAME},gpu_id={gpu_id} value={val} {ts}"
            )


def process_device_metrics(dev, gpu_id, current_ts_ns):
    dev_stats = dev.get("dev_stats", {})
    eng_usage = dev_stats.get("eng_usage", {})
    freqs = dev_stats.get("freqs", [])
    power = dev_stats.get("power", [])

    emit_engine_usage(eng_usage, gpu_id, current_ts_ns)
    emit_frequency(freqs, gpu_id, current_ts_ns)
    emit_power(power, gpu_id, current_ts_ns)


def process_state_line(state_line):
    try:
        state = json.loads(state_line)
        current_ts_ns = int(time.time() * 1e9)
        devs_state = state.get("devs_state", [])
        if not devs_state:
            logging.warning("No devs_state found in state line")
            return

        # Process all devices in devs_state
        for dev in devs_state:
            dev_nodes = dev.get("dev_nodes", "")
            match = re.search(r"renderD(\d+)", dev_nodes)
            if not match:
                continue  # no renderD<number> found, skip this device

            number = int(match.group(1))
            if number < 128:
                logging.warning(
                    f"renderD{number} in dev_nodes '{dev_nodes}' is less than 128, skipping device"
                )
                continue

            gpu_id = number - 128
            process_device_metrics(dev, gpu_id, current_ts_ns)
    except Exception as e:
        logging.error(f"Error processing state line: {e}")


def main():
    while True:
        try:
            # Open the FIFO for reading (blocks until a writer is available)
            with open(FIFO_FILE, "r") as fifo:
                # Read lines from the FIFO, blocking until data is available
                for state_line in fifo:
                    state_line = state_line.strip()
                    if not state_line:
                        continue
                    # Only process lines that contain the "timestamps" field
                    if '"timestamps"' not in state_line:
                        continue
                    process_state_line(state_line)
            # If we reach here, the writer closed the FIFO. Loop to reopen and wait for new writers.
        except Exception as e:
            logging.error(f"Error reading from FIFO: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
