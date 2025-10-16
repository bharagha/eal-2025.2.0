/*******************************************************************************
 * Copyright (C) 2025 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

#pragma once

#include "inference_backend/image.h"
#include "d3d11_images.h"
#include <d3d11.h>
#include <wrl/client.h>

namespace InferenceBackend {


class D3D11ImageMap_SystemMemory : public ImageMap {
  public:
    D3D11ImageMap_SystemMemory();
    ~D3D11ImageMap_SystemMemory();

    Image Map(const Image &image) override;
    void Unmap() override;

    void SetContext(D3D11Context* context) { d3d11_context = context; }

  protected:
    D3D11Context* d3d11_context = nullptr;
    Microsoft::WRL::ComPtr<ID3D11DeviceContext> d3d11_device_context;
    Microsoft::WRL::ComPtr<ID3D11Texture2D> d3d11_texture;  // Original render target texture
    Microsoft::WRL::ComPtr<ID3D11Texture2D> staging_texture;  // Staging texture for CPU readback
    int num_planes;
};

class D3D11ImageMap_D3D11Texture : public ImageMap {
  public:
    D3D11ImageMap_D3D11Texture();
    ~D3D11ImageMap_D3D11Texture();

    Image Map(const Image &image) override;
    void Unmap() override;
};

} // namespace InferenceBackend
