# Intel Paho MQTT C Package

This package provides the Eclipse Paho MQTT C client library optimized for Intel DL Streamer.

## Package Information

- **Name**: intel-paho-mqtt-c
- **Version**: 1.3.4
- **Installation Path**: `/opt/intel/paho-mqtt-c/`
- **License**: EPL-2.0 OR BSD-3-Clause

## Features

- SSL/TLS support with OpenSSL
- High performance optimizations
- Synchronous and asynchronous APIs
- Both C and C++ bindings

## Build Dependencies

- cmake
- gcc gcc-c++
- make
- openssl-devel

## Runtime Dependencies

- openssl

## Libraries Provided

- `libpaho-mqtt3c.so` - C synchronous client
- `libpaho-mqtt3cs.so` - C synchronous client with SSL
- `libpaho-mqtt3a.so` - C asynchronous client  
- `libpaho-mqtt3as.so` - C asynchronous client with SSL

## Usage in Applications

```c
#include "MQTTClient.h"

// Basic MQTT client setup
MQTTClient client;
MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
int rc;

MQTTClient_create(&client, "tcp://localhost:1883", "ExampleClientPub",
    MQTTCLIENT_PERSISTENCE_NONE, NULL);

conn_opts.keepAliveInterval = 20;
conn_opts.cleansession = 1;

if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) {
    printf("Failed to connect, return code %d\n", rc);
}
```

## Building

This package is built as part of the Intel DL Streamer modular build system:

```bash
cd SPECS/intel-paho-mqtt-c
rpmbuild -ba intel-paho-mqtt-c.spec
```

## Installation

```bash
sudo rpm -ivh intel-paho-mqtt-c-*.rpm
```

## Files Installed

```
/opt/intel/paho-mqtt-c/
├── include/
│   ├── MQTTClient.h
│   ├── MQTTClientPersistence.h
│   └── MQTTAsync.h
├── lib64/
│   ├── libpaho-mqtt3c.so*
│   ├── libpaho-mqtt3cs.so*
│   ├── libpaho-mqtt3a.so*
│   ├── libpaho-mqtt3as.so*
│   └── pkgconfig/
│       └── paho-mqtt-c.pc
```

## Development Package

The `-devel` subpackage includes:
- Header files
- Static libraries  
- pkg-config files

Install with:
```bash
sudo rpm -ivh intel-paho-mqtt-c-devel-*.rpm
```
