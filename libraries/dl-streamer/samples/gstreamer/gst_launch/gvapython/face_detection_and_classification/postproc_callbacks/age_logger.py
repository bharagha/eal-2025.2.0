# ==============================================================================
# Copyright (C) 2018-2025 Intel Corporation
#
# SPDX-License-Identifier: MIT
# ==============================================================================

# pylint: disable=missing-module-docstring

from gstgva import VideoFrame

class AgeLogger:
    # pylint: disable=missing-class-docstring
    def __init__(self, log_file_path):
        # pylint: disable=consider-using-with
        self.log_file = open(log_file_path, "a", encoding="utf-8")

    def log_age(self, frame: VideoFrame) -> bool:
        # pylint: disable=missing-function-docstring
        for roi in frame.regions():
            for tensor in roi.tensors():
                if tensor.name() == "detection":
                    continue
                layer_name = tensor.layer_name()
                if "age_conv3" == layer_name:
                    self.log_file.write(tensor.label() + "\n")
                    continue
        return True

    def __del__(self):
        self.log_file.close()
