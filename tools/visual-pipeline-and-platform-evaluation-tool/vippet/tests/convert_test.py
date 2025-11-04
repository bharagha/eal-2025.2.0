import re
import unittest
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from convert import config_to_string, string_to_config, _tokenize


@dataclass
class ParseTestCase:
    launch_string: str
    launch_dict: dict


parse_test_cases = [
    ParseTestCase(
        # old simplevs
        r"filesrc location=/tmp/license-plate-detection.mp4 ! decodebin3 ! vapostproc ! "
        r"video/x-raw(memory:VAMemory) ! gvafpscounter starting-frame=500 ! "
        r"gvadetect model=/yolov8_license_plate_detector.xml model-instance-id=detect0 device=GPU "
        r"pre-process-backend=va-surface-sharing batch-size=0 inference-interval=3 nireq=0 ! queue ! "
        r"gvatrack tracking-type=short-term-imageless ! queue ! "
        r"gvaclassify model=/ch_PP-OCRv4_rec_infer/ch_PP-OCRv4_rec_infer.xml "
        r"model-instance-id=classify0 device=GPU pre-process-backend=va-surface-sharing batch-size=0 "
        r"inference-interval=3 nireq=0 reclassify-interval=1 ! queue ! gvawatermark ! "
        r"gvametaconvert format=json json-indent=4 source=/tmp/license-plate-detection.mp4 ! "
        r"gvametapublish method=file file-path=/dev/null ! vah264enc ! h264parse ! mp4mux ! "
        r"filesink location=/tmp/license-plate-detection-output.mp4",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "/tmp/license-plate-detection.mp4"},
                },
                {"id": "1", "type": "decodebin3", "data": {}},
                {"id": "2", "type": "vapostproc", "data": {}},
                {"id": "3", "type": "video/x-raw(memory:VAMemory)", "data": {}},
                {
                    "id": "4",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {
                    "id": "5",
                    "type": "gvadetect",
                    "data": {
                        "model": "/yolov8_license_plate_detector.xml",
                        "model-instance-id": "detect0",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                    },
                },
                {"id": "6", "type": "queue", "data": {}},
                {
                    "id": "7",
                    "type": "gvatrack",
                    "data": {"tracking-type": "short-term-imageless"},
                },
                {"id": "8", "type": "queue", "data": {}},
                {
                    "id": "9",
                    "type": "gvaclassify",
                    "data": {
                        "model": "/ch_PP-OCRv4_rec_infer/ch_PP-OCRv4_rec_infer.xml",
                        "model-instance-id": "classify0",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                        "reclassify-interval": "1",
                    },
                },
                {"id": "10", "type": "queue", "data": {}},
                {"id": "11", "type": "gvawatermark", "data": {}},
                {
                    "id": "12",
                    "type": "gvametaconvert",
                    "data": {
                        "format": "json",
                        "json-indent": "4",
                        "source": "/tmp/license-plate-detection.mp4",
                    },
                },
                {
                    "id": "13",
                    "type": "gvametapublish",
                    "data": {"method": "file", "file-path": "/dev/null"},
                },
                {"id": "14", "type": "vah264enc", "data": {}},
                {"id": "15", "type": "h264parse", "data": {}},
                {"id": "16", "type": "mp4mux", "data": {}},
                {
                    "id": "17",
                    "type": "filesink",
                    "data": {"location": "/tmp/license-plate-detection-output.mp4"},
                },
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "14", "source": "14", "target": "15"},
                {"id": "15", "source": "15", "target": "16"},
                {"id": "16", "source": "16", "target": "17"},
            ],
        },
    ),
    ParseTestCase(
        # gst docs tee example
        r"filesrc location=song.ogg ! decodebin ! tee name=t ! queue ! audioconvert ! audioresample "
        r"! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "song.ogg"},
                },
                {"id": "1", "type": "decodebin", "data": {}},
                {"id": "2", "type": "tee", "data": {"name": "t"}},
                {"id": "3", "type": "queue", "data": {}},
                {"id": "4", "type": "audioconvert", "data": {}},
                {"id": "5", "type": "audioresample", "data": {}},
                {"id": "6", "type": "autoaudiosink", "data": {}},
                {"id": "7", "type": "queue", "data": {}},
                {"id": "8", "type": "audioconvert", "data": {}},
                {"id": "9", "type": "goom", "data": {}},
                {"id": "10", "type": "videoconvert", "data": {}},
                {"id": "11", "type": "autovideosink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "2", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
            ],
        },
    ),
    ParseTestCase(
        # 2 nested tees
        r"filesrc location=song.ogg ! decodebin ! tee name=t ! queue ! audioconvert ! tee name=x ! "
        r"queue ! audiorate ! autoaudiosink x. ! queue ! audioresample ! autoaudiosink t. ! queue "
        r"! audioconvert ! goom ! videoconvert ! autovideosink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "song.ogg"},
                },
                {"id": "1", "type": "decodebin", "data": {}},
                {"id": "2", "type": "tee", "data": {"name": "t"}},
                {"id": "3", "type": "queue", "data": {}},
                {"id": "4", "type": "audioconvert", "data": {}},
                {"id": "5", "type": "tee", "data": {"name": "x"}},
                {"id": "6", "type": "queue", "data": {}},
                {"id": "7", "type": "audiorate", "data": {}},
                {"id": "8", "type": "autoaudiosink", "data": {}},
                {"id": "9", "type": "queue", "data": {}},
                {"id": "10", "type": "audioresample", "data": {}},
                {"id": "11", "type": "autoaudiosink", "data": {}},
                {"id": "12", "type": "queue", "data": {}},
                {"id": "13", "type": "audioconvert", "data": {}},
                {"id": "14", "type": "goom", "data": {}},
                {"id": "15", "type": "videoconvert", "data": {}},
                {"id": "16", "type": "autovideosink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "5", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "2", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "14", "source": "14", "target": "15"},
                {"id": "15", "source": "15", "target": "16"},
            ],
        },
    ),
    ParseTestCase(
        # template
        r"filesrc location=XXX ! demux ! tee name=t ! queue ! splitmuxsink location=output_%02d.mp4 "
        r"t. ! queue ! h264parse ! vah264dec ! "
        r"gvadetect ! queue ! gvatrack ! gvaclassify ! queue ! "
        r"gvawatermark ! gvafpscounter ! gvametaconvert ! gvametapublish ! "
        r"vah264enc ! h264parse ! mp4mux ! filesink location=YYY",
        {
            "nodes": [
                {"id": "0", "type": "filesrc", "data": {"location": "XXX"}},
                {"id": "1", "type": "demux", "data": {}},
                {"id": "2", "type": "tee", "data": {"name": "t"}},
                {"id": "3", "type": "queue", "data": {}},
                {
                    "id": "4",
                    "type": "splitmuxsink",
                    "data": {"location": "output_%02d.mp4"},
                },
                {"id": "5", "type": "queue", "data": {}},
                {"id": "6", "type": "h264parse", "data": {}},
                {"id": "7", "type": "vah264dec", "data": {}},
                {"id": "8", "type": "gvadetect", "data": {}},
                {"id": "9", "type": "queue", "data": {}},
                {"id": "10", "type": "gvatrack", "data": {}},
                {"id": "11", "type": "gvaclassify", "data": {}},
                {"id": "12", "type": "queue", "data": {}},
                {"id": "13", "type": "gvawatermark", "data": {}},
                {"id": "14", "type": "gvafpscounter", "data": {}},
                {"id": "15", "type": "gvametaconvert", "data": {}},
                {"id": "16", "type": "gvametapublish", "data": {}},
                {"id": "17", "type": "vah264enc", "data": {}},
                {"id": "18", "type": "h264parse", "data": {}},
                {"id": "19", "type": "mp4mux", "data": {}},
                {"id": "20", "type": "filesink", "data": {"location": "YYY"}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "2", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "14", "source": "14", "target": "15"},
                {"id": "15", "source": "15", "target": "16"},
                {"id": "16", "source": "16", "target": "17"},
                {"id": "17", "source": "17", "target": "18"},
                {"id": "18", "source": "18", "target": "19"},
                {"id": "19", "source": "19", "target": "20"},
            ],
        },
    ),
    ParseTestCase(
        # SmartNVR Analytics Branch
        r"filesrc location=${VIDEO} ! qtdemux ! h264parse ! "
        r"tee name=t0 ! queue2 ! splitmuxsink location=/tmp/$(uuid).mp4 "
        r"t0. ! queue2 ! vah264dec ! video/x-raw\(memory:VAMemory\) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"gvadetect   model=${MODEL_YOLOv5s_416} model-proc=${MODEL_PROC_YOLOv5s_416} "
        r"model-instance-id=detect0   pre-process-backend=va-surface-sharing device=GPU "
        r"batch-size=0 inference-interval=3 nireq=0 ! queue2 ! "
        r"gvatrack tracking-type=short-term-imageless ! queue2 ! "
        r"gvaclassify   model=${MODEL_RESNET} model-proc=${MODEL_PROC_RESNET} "
        r"model-instance-id=classify0 pre-process-backend=va-surface-sharing device=GPU "
        r"batch-size=0 inference-interval=3 nireq=0 reclassify-interval=1 ! queue2 ! "
        r"gvawatermark ! "
        r"gvametaconvert format=json json-indent=4 ! "
        r"gvametapublish method=file file-path=/dev/null ! "
        r"vapostproc ! video/x-raw\(memory:VAMemory\),width=320,height=240 ! fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "tee", "data": {"name": "t0"}},
                {"id": "4", "type": "queue2", "data": {}},
                {
                    "id": "5",
                    "type": "splitmuxsink",
                    "data": {"location": "/tmp/$(uuid).mp4"},
                },
                {"id": "6", "type": "queue2", "data": {}},
                {"id": "7", "type": "vah264dec", "data": {}},
                {
                    "id": "8",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {},
                },
                {
                    "id": "9",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {
                    "id": "10",
                    "type": "gvadetect",
                    "data": {
                        "model": "${MODEL_YOLOv5s_416}",
                        "model-proc": "${MODEL_PROC_YOLOv5s_416}",
                        "model-instance-id": "detect0",
                        "pre-process-backend": "va-surface-sharing",
                        "device": "GPU",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                    },
                },
                {"id": "11", "type": "queue2", "data": {}},
                {
                    "id": "12",
                    "type": "gvatrack",
                    "data": {"tracking-type": "short-term-imageless"},
                },
                {"id": "13", "type": "queue2", "data": {}},
                {
                    "id": "14",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_RESNET}",
                        "model-proc": "${MODEL_PROC_RESNET}",
                        "model-instance-id": "classify0",
                        "pre-process-backend": "va-surface-sharing",
                        "device": "GPU",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                        "reclassify-interval": "1",
                    },
                },
                {"id": "15", "type": "queue2", "data": {}},
                {"id": "16", "type": "gvawatermark", "data": {}},
                {
                    "id": "17",
                    "type": "gvametaconvert",
                    "data": {"format": "json", "json-indent": "4"},
                },
                {
                    "id": "18",
                    "type": "gvametapublish",
                    "data": {"method": "file", "file-path": "/dev/null"},
                },
                {"id": "19", "type": "vapostproc", "data": {}},
                {
                    "id": "20",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {"width": "320", "height": "240"},
                },
                {"id": "21", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "3", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "14", "source": "14", "target": "15"},
                {"id": "15", "source": "15", "target": "16"},
                {"id": "16", "source": "16", "target": "17"},
                {"id": "17", "source": "17", "target": "18"},
                {"id": "18", "source": "18", "target": "19"},
                {"id": "19", "source": "19", "target": "20"},
                {"id": "20", "source": "20", "target": "21"},
            ],
        },
    ),
    ParseTestCase(
        # SmartNVR Media-only Branch
        r"filesrc location=${VIDEO} ! qtdemux ! h264parse ! "
        r"tee name=t0 ! queue2 ! splitmuxsink location=/tmp/$(uuid).mp4 "
        r"t0. ! queue2 ! vah264dec ! video/x-raw\(memory:VAMemory\) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"vapostproc ! video/x-raw\(memory:VAMemory\),width=320,height=240 ! fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "tee", "data": {"name": "t0"}},
                {"id": "4", "type": "queue2", "data": {}},
                {
                    "id": "5",
                    "type": "splitmuxsink",
                    "data": {"location": "/tmp/$(uuid).mp4"},
                },
                {"id": "6", "type": "queue2", "data": {}},
                {"id": "7", "type": "vah264dec", "data": {}},
                {
                    "id": "8",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {},
                },
                {
                    "id": "9",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {"id": "10", "type": "vapostproc", "data": {}},
                {
                    "id": "11",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {"width": "320", "height": "240"},
                },
                {"id": "12", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "3", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
            ],
        },
    ),
    ParseTestCase(
        # Magic 9 Light
        r"filesrc location=${VIDEO} ! h265parse ! vah265dec ! "
        r"capsfilter caps=\"video/x-raw(memory:VAMemory)\" ! queue ! "
        r"gvadetect model=${MODEL_YOLOv11n} model-proc=${MODEL_PROC_YOLOv11n} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 threshold=0.5 model-instance-id=yolov11n ! "
        r"queue ! "
        r"gvatrack tracking-type=1 config=tracking_per_class=false ! queue ! "
        r"gvaclassify model=${MODEL_RESNET} model-proc=${MODEL_PROC_RESNET} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 inference-region=1 "
        r"model-instance-id=resnet50 ! queue ! "
        r"gvafpscounter starting-frame=2000 ! fakesink sync=false async=false",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "h265parse", "data": {}},
                {"id": "2", "type": "vah265dec", "data": {}},
                {
                    "id": "3",
                    "type": "capsfilter",
                    "data": {"caps": '\\"video/x-raw(memory:VAMemory)\\"'},
                },
                {"id": "4", "type": "queue", "data": {}},
                {
                    "id": "5",
                    "type": "gvadetect",
                    "data": {
                        "model": "${MODEL_YOLOv11n}",
                        "model-proc": "${MODEL_PROC_YOLOv11n}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "threshold": "0.5",
                        "model-instance-id": "yolov11n",
                    },
                },
                {"id": "6", "type": "queue", "data": {}},
                {
                    "id": "7",
                    "type": "gvatrack",
                    "data": {
                        "tracking-type": "1",
                        "config": "tracking_per_class=false",
                    },
                },
                {"id": "8", "type": "queue", "data": {}},
                {
                    "id": "9",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_RESNET}",
                        "model-proc": "${MODEL_PROC_RESNET}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "inference-region": "1",
                        "model-instance-id": "resnet50",
                    },
                },
                {"id": "10", "type": "queue", "data": {}},
                {
                    "id": "11",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "2000"},
                },
                {
                    "id": "12",
                    "type": "fakesink",
                    "data": {"sync": "false", "async": "false"},
                },
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
            ],
        },
    ),
    ParseTestCase(
        # Magic 9 Medium
        r"filesrc location=${VIDEO} ! h265parse ! vah265dec ! "
        r"capsfilter caps=\"video/x-raw(memory:VAMemory)\" ! queue ! "
        r"gvadetect model=${MODEL_YOLOv5m} model-proc=${MODEL_PROC_YOLOv5m} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 threshold=0.5 model-instance-id=yolov5m ! "
        r"queue ! "
        r"gvatrack tracking-type=1 config=tracking_per_class=false ! queue ! "
        r"gvaclassify model=${MODEL_RESNET} model-proc=${MODEL_PROC_RESNET} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 inference-region=1 "
        r"model-instance-id=resnet50 ! queue ! "
        r"gvaclassify model=${MODEL_MOBILENET} model-proc=${MODEL_PROC_MOBILENET} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 inference-region=1 "
        r"model-instance-id=mobilenetv2 ! queue ! "
        r"gvafpscounter starting-frame=2000 ! fakesink sync=false async=false",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "h265parse", "data": {}},
                {"id": "2", "type": "vah265dec", "data": {}},
                {
                    "id": "3",
                    "type": "capsfilter",
                    "data": {"caps": '\\"video/x-raw(memory:VAMemory)\\"'},
                },
                {"id": "4", "type": "queue", "data": {}},
                {
                    "id": "5",
                    "type": "gvadetect",
                    "data": {
                        "model": "${MODEL_YOLOv5m}",
                        "model-proc": "${MODEL_PROC_YOLOv5m}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "threshold": "0.5",
                        "model-instance-id": "yolov5m",
                    },
                },
                {"id": "6", "type": "queue", "data": {}},
                {
                    "id": "7",
                    "type": "gvatrack",
                    "data": {
                        "tracking-type": "1",
                        "config": "tracking_per_class=false",
                    },
                },
                {"id": "8", "type": "queue", "data": {}},
                {
                    "id": "9",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_RESNET}",
                        "model-proc": "${MODEL_PROC_RESNET}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "inference-region": "1",
                        "model-instance-id": "resnet50",
                    },
                },
                {"id": "10", "type": "queue", "data": {}},
                {
                    "id": "11",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_MOBILENET}",
                        "model-proc": "${MODEL_PROC_MOBILENET}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "inference-region": "1",
                        "model-instance-id": "mobilenetv2",
                    },
                },
                {"id": "12", "type": "queue", "data": {}},
                {
                    "id": "13",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "2000"},
                },
                {
                    "id": "14",
                    "type": "fakesink",
                    "data": {"sync": "false", "async": "false"},
                },
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
            ],
        },
    ),
    ParseTestCase(
        # Magic 9 Heavy
        r"filesrc location=${VIDEO}! h265parse ! vah265dec ! "
        r"capsfilter caps=\"video/x-raw(memory:VAMemory)\" ! queue ! "
        r"gvadetect model=${MODEL_YOLOv11n} model-proc=${MODEL_PROC_YOLOv11n} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 threshold=0.5 model-instance-id=yolov11m ! "
        r"queue ! "
        r"gvatrack tracking-type=1 config=tracking_per_class=false ! queue ! "
        r"gvaclassify model=${MODEL_RESNET} model-proc=${MODEL_PROC_RESNET} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 inference-region=1 "
        r"model-instance-id=resnet50 ! queue ! "
        r"gvaclassify model=${MODEL_MOBILENET} model-proc=${MODEL_PROC_MOBILENET} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"nireq=2 ie-config=NUM_STREAMS=2 batch-size=8 inference-interval=3 inference-region=1 "
        r"model-instance-id=mobilenetv2 ! queue ! "
        r"gvafpscounter starting-frame=2000 ! fakesink sync=false async=false",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "h265parse", "data": {}},
                {"id": "2", "type": "vah265dec", "data": {}},
                {
                    "id": "3",
                    "type": "capsfilter",
                    "data": {"caps": '\\"video/x-raw(memory:VAMemory)\\"'},
                },
                {"id": "4", "type": "queue", "data": {}},
                {
                    "id": "5",
                    "type": "gvadetect",
                    "data": {
                        "model": "${MODEL_YOLOv11n}",
                        "model-proc": "${MODEL_PROC_YOLOv11n}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "threshold": "0.5",
                        "model-instance-id": "yolov11m",
                    },
                },
                {"id": "6", "type": "queue", "data": {}},
                {
                    "id": "7",
                    "type": "gvatrack",
                    "data": {
                        "tracking-type": "1",
                        "config": "tracking_per_class=false",
                    },
                },
                {"id": "8", "type": "queue", "data": {}},
                {
                    "id": "9",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_RESNET}",
                        "model-proc": "${MODEL_PROC_RESNET}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "inference-region": "1",
                        "model-instance-id": "resnet50",
                    },
                },
                {"id": "10", "type": "queue", "data": {}},
                {
                    "id": "11",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${MODEL_MOBILENET}",
                        "model-proc": "${MODEL_PROC_MOBILENET}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "nireq": "2",
                        "ie-config": "NUM_STREAMS=2",
                        "batch-size": "8",
                        "inference-interval": "3",
                        "inference-region": "1",
                        "model-instance-id": "mobilenetv2",
                    },
                },
                {"id": "12", "type": "queue", "data": {}},
                {
                    "id": "13",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "2000"},
                },
                {
                    "id": "14",
                    "type": "fakesink",
                    "data": {"sync": "false", "async": "false"},
                },
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
            ],
        },
    ),
    ParseTestCase(
        # Simple Video Structuration
        r"filesrc location=${VIDEO} ! qtdemux ! h264parse ! vaapidecodebin ! "
        r"vapostproc ! video/x-raw\(memory:VAMemory\) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"gvadetect   model=${LPR_MODEL} model-instance-id=detect0 "
        r"pre-process-backend=va-surface-sharing   device=GPU   batch-size=0   inference-interval=3  nireq=0 ! "
        r"queue2 ! gvatrack   tracking-type=short-term-imageless ! queue2 ! "
        r"gvaclassify   model=${OCR_MODEL} model-instance-id=classify0 "
        r"pre-process-backend=va-surface-sharing   device=GPU   batch-size=0   inference-interval=3   nireq=0 "
        r"reclassify-interval=1 ! queue2 ! gvawatermark ! gvametaconvert   format=json   json-indent=4 ! "
        r"gvametapublish   method=file file-path=/dev/null ! "
        r"fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "vaapidecodebin", "data": {}},
                {"id": "4", "type": "vapostproc", "data": {}},
                {
                    "id": "5",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {},
                },
                {
                    "id": "6",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {
                    "id": "7",
                    "type": "gvadetect",
                    "data": {
                        "model": "${LPR_MODEL}",
                        "model-instance-id": "detect0",
                        "pre-process-backend": "va-surface-sharing",
                        "device": "GPU",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                    },
                },
                {"id": "8", "type": "queue2", "data": {}},
                {
                    "id": "9",
                    "type": "gvatrack",
                    "data": {"tracking-type": "short-term-imageless"},
                },
                {"id": "10", "type": "queue2", "data": {}},
                {
                    "id": "11",
                    "type": "gvaclassify",
                    "data": {
                        "model": "${OCR_MODEL}",
                        "model-instance-id": "classify0",
                        "pre-process-backend": "va-surface-sharing",
                        "device": "GPU",
                        "batch-size": "0",
                        "inference-interval": "3",
                        "nireq": "0",
                        "reclassify-interval": "1",
                    },
                },
                {"id": "12", "type": "queue2", "data": {}},
                {"id": "13", "type": "gvawatermark", "data": {}},
                {
                    "id": "14",
                    "type": "gvametaconvert",
                    "data": {"format": "json", "json-indent": "4"},
                },
                {
                    "id": "15",
                    "type": "gvametapublish",
                    "data": {"method": "file", "file-path": "/dev/null"},
                },
                {"id": "16", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "14", "source": "14", "target": "15"},
                {"id": "15", "source": "15", "target": "16"},
            ],
        },
    ),
    ParseTestCase(
        # Human Pose Pipeline
        r"filesrc location=${VIDEO}! qtdemux ! h264parse ! vah264dec ! "
        r"video/x-raw(memory:VAMemory) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"gvadetect model=${YOLO11n_POST_MODEL} "
        r"device=GPU pre-process-backend=va-surface-sharing "
        r"model-instance-id=yolo11-pose ! queue2 ! "
        r"gvatrack tracking-type=short-term-imageless ! "
        r"gvawatermark ! gvametaconvert   format=json   json-indent=4 ! "
        r"gvametapublish   method=file file-path=/dev/null ! "
        r"fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "vah264dec", "data": {}},
                {"id": "4", "type": "video/x-raw(memory:VAMemory)", "data": {}},
                {
                    "id": "5",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {
                    "id": "6",
                    "type": "gvadetect",
                    "data": {
                        "model": "${YOLO11n_POST_MODEL}",
                        "device": "GPU",
                        "pre-process-backend": "va-surface-sharing",
                        "model-instance-id": "yolo11-pose",
                    },
                },
                {"id": "7", "type": "queue2", "data": {}},
                {
                    "id": "8",
                    "type": "gvatrack",
                    "data": {"tracking-type": "short-term-imageless"},
                },
                {"id": "9", "type": "gvawatermark", "data": {}},
                {
                    "id": "10",
                    "type": "gvametaconvert",
                    "data": {"format": "json", "json-indent": "4"},
                },
                {
                    "id": "11",
                    "type": "gvametapublish",
                    "data": {"method": "file", "file-path": "/dev/null"},
                },
                {"id": "12", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "11", "source": "11", "target": "12"},
            ],
        },
    ),
    ParseTestCase(
        # Video Decode Pipeline
        r"filesrc location=${VIDEO} ! qtdemux ! h264parse ! vah264dec ! "
        r"video/x-raw\(memory:VAMemory\) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "vah264dec", "data": {}},
                {
                    "id": "4",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {},
                },
                {
                    "id": "5",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {"id": "6", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
            ],
        },
    ),
    ParseTestCase(
        # Video Decode Scale Pipeline
        r"filesrc location=${VIDEO} ! qtdemux ! h264parse ! vah264dec ! "
        r"video/x-raw\(memory:VAMemory\) ! "
        r"gvafpscounter starting-frame=500 ! "
        r"vapostproc ! video/x-raw\(memory:VAMemory\),width=320,height=240 ! fakesink",
        {
            "nodes": [
                {
                    "id": "0",
                    "type": "filesrc",
                    "data": {"location": "${VIDEO}"},
                },
                {"id": "1", "type": "qtdemux", "data": {}},
                {"id": "2", "type": "h264parse", "data": {}},
                {"id": "3", "type": "vah264dec", "data": {}},
                {
                    "id": "4",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {},
                },
                {
                    "id": "5",
                    "type": "gvafpscounter",
                    "data": {"starting-frame": "500"},
                },
                {"id": "6", "type": "vapostproc", "data": {}},
                {
                    "id": "7",
                    "type": "video/x-raw\\(memory:VAMemory\\)",
                    "data": {"width": "320", "height": "240"},
                },
                {"id": "8", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
            ],
        },
    ),
]


unsorted_nodes_edges = [
    ParseTestCase(
        # gst docs tee example
        r"filesrc location=song.ogg ! decodebin ! tee name=t ! queue ! audioconvert ! audioresample "
        r"! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink",
        {
            "nodes": [
                {"id": "1", "type": "decodebin", "data": {}},
                {"id": "0", "type": "filesrc", "data": {"location": "song.ogg"}},
                {"id": "3", "type": "queue", "data": {}},
                {"id": "6", "type": "autoaudiosink", "data": {}},
                {"id": "4", "type": "audioconvert", "data": {}},
                {"id": "8", "type": "audioconvert", "data": {}},
                {"id": "5", "type": "audioresample", "data": {}},
                {"id": "7", "type": "queue", "data": {}},
                {"id": "11", "type": "autovideosink", "data": {}},
                {"id": "9", "type": "goom", "data": {}},
                {"id": "2", "type": "tee", "data": {"name": "t"}},
                {"id": "10", "type": "videoconvert", "data": {}},
            ],
            "edges": [
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "0", "source": "0", "target": "1"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "6", "source": "2", "target": "7"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "8", "source": "8", "target": "9"},
            ],
        },
    ),
    ParseTestCase(
        # gst docs tee example, ids start from 1
        r"filesrc location=song.ogg ! decodebin ! tee name=t ! queue ! audioconvert ! audioresample "
        r"! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink",
        {
            "nodes": [
                {"id": "2", "type": "decodebin", "data": {}},
                {"id": "1", "type": "filesrc", "data": {"location": "song.ogg"}},
                {"id": "4", "type": "queue", "data": {}},
                {"id": "7", "type": "autoaudiosink", "data": {}},
                {"id": "5", "type": "audioconvert", "data": {}},
                {"id": "9", "type": "audioconvert", "data": {}},
                {"id": "6", "type": "audioresample", "data": {}},
                {"id": "8", "type": "queue", "data": {}},
                {"id": "12", "type": "autovideosink", "data": {}},
                {"id": "10", "type": "goom", "data": {}},
                {"id": "3", "type": "tee", "data": {"name": "t"}},
                {"id": "11", "type": "videoconvert", "data": {}},
            ],
            "edges": [
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "8", "source": "8", "target": "9"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "11", "source": "11", "target": "12"},
                {"id": "7", "source": "3", "target": "8"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "9", "source": "9", "target": "10"},
            ],
        },
    ),
    ParseTestCase(
        # 2 nested tees
        r"filesrc location=song.ogg ! decodebin ! tee name=t ! queue ! audioconvert ! tee name=x ! "
        r"queue ! audiorate ! autoaudiosink x. ! queue ! audioresample ! autoaudiosink t. ! queue "
        r"! audioconvert ! goom ! videoconvert ! autovideosink",
        {
            "nodes": [
                {"id": "1", "type": "decodebin", "data": {}},
                {"id": "3", "type": "queue", "data": {}},
                {"id": "2", "type": "tee", "data": {"name": "t"}},
                {"id": "0", "type": "filesrc", "data": {"location": "song.ogg"}},
                {"id": "4", "type": "audioconvert", "data": {}},
                {"id": "6", "type": "queue", "data": {}},
                {"id": "7", "type": "audiorate", "data": {}},
                {"id": "5", "type": "tee", "data": {"name": "x"}},
                {"id": "9", "type": "queue", "data": {}},
                {"id": "10", "type": "audioresample", "data": {}},
                {"id": "14", "type": "goom", "data": {}},
                {"id": "16", "type": "autovideosink", "data": {}},
                {"id": "8", "type": "autoaudiosink", "data": {}},
                {"id": "11", "type": "autoaudiosink", "data": {}},
                {"id": "12", "type": "queue", "data": {}},
                {"id": "13", "type": "audioconvert", "data": {}},
                {"id": "15", "type": "videoconvert", "data": {}},
            ],
            "edges": [
                {"id": "15", "source": "15", "target": "16"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "0", "source": "0", "target": "1"},
                {"id": "2", "source": "2", "target": "3"},
                {"id": "3", "source": "3", "target": "4"},
                {"id": "4", "source": "4", "target": "5"},
                {"id": "5", "source": "5", "target": "6"},
                {"id": "6", "source": "6", "target": "7"},
                {"id": "7", "source": "7", "target": "8"},
                {"id": "13", "source": "13", "target": "14"},
                {"id": "8", "source": "5", "target": "9"},
                {"id": "9", "source": "9", "target": "10"},
                {"id": "10", "source": "10", "target": "11"},
                {"id": "12", "source": "12", "target": "13"},
                {"id": "11", "source": "2", "target": "12"},
                {"id": "14", "source": "14", "target": "15"},
            ],
        },
    ),
]


def normalize(s: str) -> str:
    s = re.sub(r",", " ", s)
    s = re.sub(r" {2,}", " ", s)
    s = re.sub(r"(?<!\s)!", " !", s)
    s = re.sub(r"!(?!\s)", "! ", s)
    return s


class TestDictToString(unittest.TestCase):
    def test_dict_to_string(self):
        self.maxDiff = None

        for tc in parse_test_cases:
            actual = config_to_string(tc.launch_dict)
            self.assertEqual(actual, normalize(tc.launch_string))

        for tc in unsorted_nodes_edges:
            actual = config_to_string(tc.launch_dict)
            self.assertEqual(actual, normalize(tc.launch_string))


class TestParseLaunchString(unittest.TestCase):
    def test_parsing(self):
        self.maxDiff = None

        for tc in parse_test_cases:
            actual = string_to_config(tc.launch_string)
            self.assertDictEqual(actual, tc.launch_dict)

    def test_empty_pipeline(self):
        pipeline = ""
        result = string_to_config(pipeline)

        self.assertIn("nodes", result)
        self.assertIn("edges", result)

    def test_single_element(self):
        pipeline = "filesrc"
        result = string_to_config(pipeline)

        self.assertEqual(len(result["nodes"]), 1)
        self.assertEqual(result["nodes"][0]["type"], "filesrc")
        self.assertEqual(len(result["edges"]), 0)

    def test_caps_filter(self):
        # Caps filters like "video/x-raw(memory:VAMemory)" should be parsed
        pipeline = "filesrc ! video/x-raw(memory:VAMemory) ! filesink"
        result = string_to_config(pipeline)

        # The caps filter should be treated as an element type
        self.assertEqual(len(result["nodes"]), 3)
        self.assertIn(
            "video/x-raw(memory:VAMemory)", [n["type"] for n in result["nodes"]]
        )

    def test_node_ids_are_sequential(self):
        pipeline = "filesrc ! queue ! filesink"
        result = string_to_config(pipeline)

        self.assertEqual(result["nodes"][0]["id"], "0")
        self.assertEqual(result["nodes"][1]["id"], "1")
        self.assertEqual(result["nodes"][2]["id"], "2")

    def test_edge_ids_are_sequential(self):
        pipeline = "filesrc ! queue ! filesink"
        result = string_to_config(pipeline)

        self.assertEqual(result["edges"][0]["id"], "0")
        self.assertEqual(result["edges"][1]["id"], "1")


class TestTokenize(unittest.TestCase):
    def test_simple_element_type(self):
        tokens = list(_tokenize("filesrc"))
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "TYPE")
        self.assertEqual(tokens[0].value, "filesrc")

    def test_property(self):
        tokens = list(_tokenize("location=/tmp/file.mp4"))
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "PROPERTY")
        self.assertEqual(tokens[0].value, "location=/tmp/file.mp4")

    def test_property_with_spaces(self):
        tokens = list(_tokenize("dummy   = value"))
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "PROPERTY")
        self.assertEqual(tokens[0].value, "dummy   = value")

    def test_tee_end(self):
        tokens = list(_tokenize("t."))
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "TEE_END")
        self.assertEqual(tokens[0].value, "t.")

    def test_element_with_property(self):
        tokens = list(_tokenize("filesrc location=/tmp/file.mp4"))
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].kind, "TYPE")
        self.assertEqual(tokens[0].value, "filesrc")
        self.assertEqual(tokens[1].kind, "PROPERTY")
        self.assertEqual(tokens[1].value, "location=/tmp/file.mp4")

    def test_element_with_multiple_properties(self):
        tokens = list(_tokenize("vah264enc bitrate=5000 quality=4"))
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].kind, "TYPE")
        self.assertEqual(tokens[0].value, "vah264enc")
        self.assertEqual(tokens[1].kind, "PROPERTY")
        self.assertEqual(tokens[1].value, "bitrate=5000")
        self.assertEqual(tokens[2].kind, "PROPERTY")
        self.assertEqual(tokens[2].value, "quality=4")

    def test_tee_name(self):
        tokens = list(_tokenize("tee name=t"))
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].kind, "TYPE")
        self.assertEqual(tokens[0].value, "tee")
        self.assertEqual(tokens[1].kind, "PROPERTY")
        self.assertEqual(tokens[1].value, "name=t")


class TestParseLaunchStringWithModels(unittest.TestCase):
    def _setup_mock_models(self, mock_manager):
        """Set up mock models for testing"""
        mock_yolov8 = MagicMock()
        mock_yolov8.display_name = "YOLOv8 Detector"
        mock_yolov8.model_path_full = "/models/output/yolov8_detector.xml"
        mock_yolov8.model_proc_full = "/models/output/yolov8_detector.json"

        mock_detection = MagicMock()
        mock_detection.display_name = "Detection Model"
        mock_detection.model_path_full = "/models/output/detection_model.xml"
        mock_detection.model_proc_full = ""

        mock_classification = MagicMock()
        mock_classification.display_name = "Classification Model"
        mock_classification.model_path_full = "/models/output/classification_model.xml"
        mock_classification.model_proc_full = ""

        def find_by_path(path):
            if "yolov8_detector" in path:
                return mock_yolov8
            if "detection_model" in path:
                return mock_detection
            if "classification_model" in path:
                return mock_classification
            return None

        def find_by_name(name):
            if name == "YOLOv8 Detector":
                return mock_yolov8
            if name == "Detection Model":
                return mock_detection
            if name == "Classification Model":
                return mock_classification
            return None

        mock_manager.find_installed_model_by_model_path_full.side_effect = find_by_path
        mock_manager.find_installed_model_by_display_name.side_effect = find_by_name

    @patch("convert.models_manager")
    def test_string_to_config_converts_model_path_to_display_name(
        self, mock_manager
    ):
        self._setup_mock_models(mock_manager)

        launch_string = (
            "filesrc location=/tmp/input.mp4 ! decodebin3 ! gvadetect "
            "model=/models/output/yolov8_detector.xml model-proc=/models/output/yolov8_detector.json "
            "device=GPU ! fakesink"
        )

        result = string_to_config(launch_string)

        self.assertEqual(len(result["nodes"]), 4)
        gvadetect_node = result["nodes"][2]
        self.assertEqual(gvadetect_node["type"], "gvadetect")
        self.assertEqual(gvadetect_node["data"]["model"], "YOLOv8 Detector")
        self.assertNotIn("model-proc", gvadetect_node["data"])

    @patch("convert.models_manager")
    def test_config_to_string_converts_display_name_to_model_path(
        self, mock_manager
    ):
        self._setup_mock_models(mock_manager)

        config = {
            "nodes": [
                {"id": "0", "type": "filesrc", "data": {"location": "/tmp/input.mp4"}},
                {"id": "1", "type": "decodebin3", "data": {}},
                {
                    "id": "2",
                    "type": "gvadetect",
                    "data": {"model": "YOLOv8 Detector", "device": "GPU"},
                },
                {"id": "3", "type": "fakesink", "data": {}},
            ],
            "edges": [
                {"id": "0", "source": "0", "target": "1"},
                {"id": "1", "source": "1", "target": "2"},
                {"id": "2", "source": "2", "target": "3"},
            ],
        }

        result = config_to_string(config)

        self.assertIn("model=/models/output/yolov8_detector.xml", result)
        self.assertIn("model-proc=/models/output/yolov8_detector.json", result)
        self.assertNotIn("YOLOv8 Detector", result)

    @patch("convert.models_manager")
    def test_multiple_models_conversion(self, mock_manager):
        self._setup_mock_models(mock_manager)

        launch_string = (
            "filesrc location=/tmp/input.mp4 ! decodebin3 ! gvadetect "
            "model=/models/output/detection_model.xml device=GPU ! gvaclassify "
            "model=/models/output/classification_model.xml device=GPU ! fakesink"
        )

        result = string_to_config(launch_string)

        self.assertEqual(len(result["nodes"]), 5)
        gvadetect_node = result["nodes"][2]
        gvaclassify_node = result["nodes"][3]

        self.assertEqual(gvadetect_node["data"]["model"], "Detection Model")
        self.assertEqual(gvaclassify_node["data"]["model"], "Classification Model")

        config_string = config_to_string(result)

        self.assertIn("model=/models/output/detection_model.xml", config_string)
        self.assertIn(
            "model=/models/output/classification_model.xml", config_string
        )


if __name__ == "__main__":
    unittest.main()
