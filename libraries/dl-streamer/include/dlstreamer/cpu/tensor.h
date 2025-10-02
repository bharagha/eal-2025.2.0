/*******************************************************************************
 * Copyright (C) 2018-2022 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

#pragma once

#include "dlstreamer/base/tensor.h"

namespace dlstreamer {

class CPUTensor : public BaseTensor {
  public:
#if _MSC_VER
    CPUTensor(const TensorInfo &info, void *data) : BaseTensor(MemoryType::D3D11, info, tensor::key::data), _data(data) {
        set_handle(tensor::key::data, reinterpret_cast<handle_t>(data));
    }
#else
    CPUTensor(const TensorInfo &info, void *data) : BaseTensor(MemoryType::CPU, info, tensor::key::data), _data(data) {
        set_handle(tensor::key::data, reinterpret_cast<handle_t>(data));
    }
#endif

    void *data() const override {
        return _data;
    }

  protected:
    void *_data;
};

using CPUTensorPtr = std::shared_ptr<CPUTensor>;

} // namespace dlstreamer
