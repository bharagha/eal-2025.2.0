import contextlib
import logging
import mmap
import os
import random
import re
import select
import string
import struct
import subprocess
import threading
import time
from itertools import product
from subprocess import Popen, PIPE
from typing import List, Dict, Any

import cv2
import numpy as np
import psutil as ps

from gstpipeline import GstPipeline

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject
Gst.init(None)

cancelled = False
logger = logging.getLogger("utils")

UINT8_DTYPE_SIZE = 1
DEFAULT_FRAME_RATE = 30.0
VIDEO_STREAM_META_PATH = "/tmp/shared_memory/video_stream.meta"


def prepare_video_and_constants(
    **kwargs: dict[str, Any],
):
    """
    Prepares the video output path, constants, and parameter grid for the pipeline.

    Args:
        input_video_player (str): Path to the input video.
        object_detection_model (str): Selected object detection model.
        object_detection_device (str): Selected object detection device.

    Returns:
        tuple: A tuple containing video_output_path, constants, and param_grid.
    """

    # Collect parameters from kwargs
    input_video_player = str(kwargs.get("input_video_player", ""))
    object_detection_model = kwargs.get("object_detection_model", "")
    object_detection_device = str(kwargs.get("object_detection_device", ""))
    object_detection_batch_size = kwargs.get("object_detection_batch_size", 1)
    object_detection_inference_interval = kwargs.get(
        "object_detection_inference_interval", 0.0
    )
    object_detection_nireq = kwargs.get("object_detection_nireq", 1)
    object_classification_model = kwargs.get("object_classification_model", "")
    object_classification_device = str(kwargs.get("object_classification_device", ""))
    object_classification_batch_size = kwargs.get("object_classification_batch_size", 1)
    object_classification_inference_interval = kwargs.get(
        "object_classification_inference_interval", 0.0
    )
    object_classification_reclassify_interval = kwargs.get(
        "object_classification_reclassify_interval", 0.0
    )
    object_classification_nireq = kwargs.get("object_classification_nireq", 1)
    tracking_type = kwargs.get("tracking_type", "short-term-imageless")
    pipeline_watermark_enabled = kwargs.get("pipeline_watermark_enabled", True)
    pipeline_video_enabled = kwargs.get("pipeline_video_enabled", True)
    live_preview_enabled = kwargs.get("live_preview_enabled", False)

    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    video_output_path = input_video_player.replace(
        ".mp4", f"-output-{random_string}.mp4"
    )
    # Delete the video in the output folder before producing a new one
    # Otherwise, gstreamer will just save a few seconds of the video
    # and stop.
    if os.path.exists(video_output_path):
        os.remove(video_output_path)

    # Reset the FPS file
    with open("/home/dlstreamer/vippet/.collector-signals/fps.txt", "w") as f:
        f.write("0.0\n")

    param_grid = {
        "object_detection_device": object_detection_device.split(", "),
        "object_detection_batch_size": [object_detection_batch_size],
        "object_detection_inference_interval": [object_detection_inference_interval],
        "object_detection_nireq": [object_detection_nireq],
        "object_classification_device": object_classification_device.split(", "),
        "object_classification_batch_size": [object_classification_batch_size],
        "object_classification_inference_interval": [
            object_classification_inference_interval
        ],
        "object_classification_reclassify_interval": [
            object_classification_reclassify_interval
        ],
        "object_classification_nireq": [object_classification_nireq],
        "tracking_type": [tracking_type],
        "pipeline_watermark_enabled": [pipeline_watermark_enabled],
        "pipeline_video_enabled": [pipeline_video_enabled],
        "live_preview_enabled": [live_preview_enabled],
    }

    constants = {
        "VIDEO_PATH": input_video_player,
        "VIDEO_OUTPUT_PATH": video_output_path,
    }

    MODELS_PATH = "/home/dlstreamer/vippet/models"

    match object_detection_model:
        case "SSDLite MobileNet V2 (INT8)":
            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/ssdlite_mobilenet_v2_INT8/FP16-INT8/ssdlite_mobilenet_v2.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/ssdlite_mobilenet_v2_INT8/ssdlite_mobilenet_v2.json"
            )
        case "YOLO v5m 416x416 (INT8)":
            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5m-416_INT8/FP16-INT8/yolov5m-416_INT8.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5m-416_INT8/yolo-v5.json"
            )
        case "YOLO v5m 640x640 (INT8)":
            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5m-640_INT8/FP16-INT8/yolov5m-640_INT8.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5m-640_INT8/yolo-v5.json"
            )
        case "YOLO v5s 416x416 (INT8)":
            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5s-416_INT8/FP16-INT8/yolov5s.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/yolov5s-416_INT8/yolo-v5.json"
            )
        case "YOLO v10s 640x640 (FP16)":
            if object_detection_device == "NPU":
                raise ValueError(
                    "YOLO v10s model is not supported on NPU device. Please select another model."
                )

            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/public/yolov10s/FP16/yolov10s.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = ""
        case "YOLO v10m 640x640 (FP16)":
            if object_detection_device == "NPU":
                raise ValueError(
                    "YOLO v10m model is not supported on NPU device. Please select another model."
                )

            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/public/yolov10m/FP16/yolov10m.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = ""
        case "YOLO v8 License Plate Detector (FP32)":
            if object_detection_device == "NPU":
                raise ValueError(
                    "YOLO v8 License Plate Detector model is not supported on NPU device. Please select another model."
                )

            constants["OBJECT_DETECTION_MODEL_PATH"] = (
                f"{MODELS_PATH}/public/yolov8_license_plate_detector/FP32/yolov8_license_plate_detector.xml"
            )
            constants["OBJECT_DETECTION_MODEL_PROC"] = ""
        case _:
            raise ValueError("Unrecognized Object Detection Model")

    match object_classification_model:
        case "Disabled":
            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = "Disabled"
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = "Disabled"
        case "ResNet-50 TF (INT8)":
            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/resnet-50-tf_INT8/resnet-50-tf_i8.xml"
            )
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/resnet-50-tf_INT8/resnet-50-tf_i8.json"
            )
        case "EfficientNet B0 (INT8)":
            if object_classification_device == "NPU":
                raise ValueError(
                    "EfficientNet B0 model is not supported on NPU device. Please select another model."
                )

            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/efficientnet-b0_INT8/FP16-INT8/efficientnet-b0.xml"
            )
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = (
                f"{MODELS_PATH}/pipeline-zoo-models/efficientnet-b0_INT8/efficientnet-b0.json"
            )
        case "MobileNet V2 PyTorch (FP16)":
            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = (
                f"{MODELS_PATH}/public/mobilenet-v2-pytorch/FP16/mobilenet-v2-pytorch.xml"
            )
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = (
                f"{MODELS_PATH}/public/mobilenet-v2-pytorch/mobilenet-v2.json"
            )
        case "PaddleOCR (FP32)":
            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = (
                f"{MODELS_PATH}/public/ch_PP-OCRv4_rec_infer/FP32/ch_PP-OCRv4_rec_infer.xml"
            )
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = ""
        case "Vehicle Attributes Recognition Barrier 0039 (FP16)":
            constants["OBJECT_CLASSIFICATION_MODEL_PATH"] = (
                f"{MODELS_PATH}/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml"
            )
            constants["OBJECT_CLASSIFICATION_MODEL_PROC"] = (
                f"{MODELS_PATH}/intel/vehicle-attributes-recognition-barrier-0039/vehicle-attributes-recognition-barrier-0039.json"
            )
        case _:
            raise ValueError("Unrecognized Object Classification Model")

    return video_output_path, constants, param_grid


def _iterate_param_grid(param_grid: Dict[str, List[str]]):
    keys, values = zip(*param_grid.items())
    for combination in product(*values):
        yield dict(zip(keys, combination))


def find_shm_file():
    """
    Finds the most recent shared memory file for live preview.

    Returns:
        str or None: Full path of the most recent shared memory file, or None if not found.
    """
    try:
        shm_dir = "/dev/shm"
        files = os.listdir(shm_dir)
        shm_files = [f for f in files if f.startswith("shmpipe.")]
        if not shm_files:
            return None
        shm_files.sort(
            key=lambda x: os.path.getctime(os.path.join(shm_dir, x)), reverse=True
        )
        return os.path.join(shm_dir, shm_files[0])
    except OSError:
        logger.error("Error accessing /dev/shm directory.")
        return None


def read_latest_meta(meta_path):
    """
    Reads the metadata file for shared memory frame dimensions and dtype size.

    Args:
        meta_path (str): Path to the metadata file.

    Returns:
        tuple or None: (height, width, dtype_size) if successful, None otherwise.
    """
    try:
        with open(meta_path, "rb") as f:
            meta = f.read(12)
            if len(meta) != 12:
                logger.error("Metadata file does not contain expected 12 bytes.")
                return None
            height, width, dtype_size = struct.unpack("III", meta)
            return height, width, dtype_size
    except (OSError, struct.error) as e:
        logger.error(f"Error reading metadata file {meta_path}: {e}")
        return None


def read_shared_memory_frame(meta_path, shm_fd):
    """
    Reads a frame from shared memory using metadata for shape and dtype.

    Args:
        meta_path (str): Path to the metadata file.
        shm_fd (file object): File descriptor for shared memory.

    Returns:
        np.ndarray or None: RGB frame if successful, None otherwise.
    """
    if shm_fd is None:
        logger.error("Shared memory file descriptor is invalid.")
        return None

    meta = read_latest_meta(meta_path)
    if not meta:
        logger.error("Metadata is invalid.")
        return None
    height, width, dtype_size = meta
    try:
        frame_size = height * width * 3 * dtype_size
        mm = mmap.mmap(shm_fd.fileno(), 0, access=mmap.ACCESS_READ)
        buf = mm[:frame_size]
        mm.close()
        if len(buf) != frame_size:
            logger.error(
                f"Frame buffer size does not match expected frame size. Expected: {frame_size}, Actual: {len(buf)}"
            )
            return None
        frame_bgr = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3))
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return frame_rgb
    except (ValueError, OSError, cv2.error) as e:
        logger.error(f"Error reading shared memory frame: {e}")
        return None


def get_video_resolution(video_path):
    """
    Returns (width, height) of a video file or default (1280, 720) if any error occurs.
    """
    default_width = 1280
    default_height = 720

    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error(f"Cannot open video file: {video_path}")
            return default_width, default_height
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        # If width or height is zero, return defaults and log warning
        if width == 0 or height == 0:
            logging.warning(f"Could not read video resolution for file: {video_path}")
            return default_width, default_height
        return width, height
    except Exception:
        logging.error(
            f"Exception occurred while reading video resolution for file: {video_path}"
        )
        return default_width, default_height


def glib_mainloop(mainloop):
    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass

def bus_call(bus, message, pipeline, mainloop):
    t = message.type
    if t == Gst.MessageType.EOS:
        logger.info("pipeline ended")
        pipeline.set_state(Gst.State.NULL)
        mainloop.quit()
        # sys.exit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        logger.info("Error:\n{}\nAdditional debug info:\n{}\n".format(err, debug))
        pipeline.set_state(Gst.State.NULL)
        mainloop.quit()
        # sys.exit()
    else:
        pass
    return True

def set_callbacks(pipeline, mainloop):
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call, pipeline, mainloop)

def run_pipeline_and_extract_metrics(
    pipeline_cmd: GstPipeline,
    constants: Dict[str, str],
    parameters: Dict[str, List[str]],
    channels: int | tuple[int, int] = 1,
    elements: List[tuple[str, str, str]] = [],
    poll_interval: int = 1,
):
    global cancelled
    """

    Runs a GStreamer pipeline and extracts FPS metrics.

    Args:
        pipeline_cmd (str): The GStreamer pipeline command to execute.
        poll_interval (int): Interval to poll the process for metrics.
        channels (int): Number of channels to match in the FPS metrics.

    Returns:
        List[Dict[str, any]]: A list of dictionaries containing the parameters and FPS metrics for each pipeline run.
    """

    results = []

    # Set the number of regular channels
    # If no tuple is provided, the number of regular channels is 0
    regular_channels = 0 if isinstance(channels, int) else channels[0]

    # Set the number of inference channels
    # If no tuple is provided, the number of inference channels is equal to the number of channels
    inference_channels = channels if isinstance(channels, int) else channels[1]

    for params in _iterate_param_grid(parameters):
        # Get live_preview_enabled from params
        live_preview_enabled = params.get("live_preview_enabled", False)

        # Evaluate the pipeline with the given parameters, constants, and channels
        _pipeline = pipeline_cmd.evaluate(
            constants, params, regular_channels, inference_channels, elements
        )

        # Log the command
        logger.info(f"Pipeline Command: {_pipeline}")

        os.environ["GST_VA_ALL_DRIVERS"] = "1"
        mainloop = GLib.MainLoop()
        pipeline = Gst.parse_launch(_pipeline)

        set_callbacks(pipeline, mainloop)

        pipeline.set_state(Gst.State.PLAYING)
        glib_mainloop(mainloop)

    return results


def is_yolov10_model(model_path: str) -> bool:
    """
    Checks if the given model path corresponds to a YOLO v10 model.

    Args:
        model_path (str): Path to the model file.

    Returns:
        bool: True if the model is a YOLO v10 model, False otherwise.
    """
    return "yolov10" in model_path.lower()
