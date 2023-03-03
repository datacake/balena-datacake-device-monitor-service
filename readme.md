# Balena Device Monitoring Service

This is a simple server which uses Python `psutil` library to collect information about the system, including:

- CPU usage
- Free memory
- swap
- Disk accesses

The collected information is passed to an HTTPS webhook URL. 

## Why not using Supervisor API?

- The Supervisor API is available locally on the Balena Device. This provides us with information about the accessibility of the system.
- On the Balena Cloud side, the Supervisor API also has endpoints for device metrics, such as CPU, memory. 
- However, this API is seemingly not available locally on the Device.

## Required Configuration

The following environment variables must be present for use. If they are not, the service cannot start.

### WEBHOOK_DESTINATION_URL

Here you must specify the URL to which the data will be forwarded. The data comes in JSON format, a sample payload can be found below.

### DEVICE_ID

In order to use the data on Datacake IoT platform, identification of the device must be performed. The Datacake UUID can be used here. Enter this into the `DEVICE_ID` environment variable.

## Optional Configuration

You can use the following environment variable to modify the behaviour of the service.

### REGULAR_TRANSMISSION_INTERVAL
- Default: 60 seconds
- Recommended: 300 seconds or more, in order to save bandwidth and datapoints on Datacake

### EMERGENCY_TRANSMISSION_INTERVAL
- Default: 10 seconds

### CPU_PERCENTAGE_MAX
- Threshold for maximum cpu load.
- If exceeded, emergency-mode will be enabled and transmission will start at `EMERGENCY_TRANSMISSION_INTERVAL`
- If back below, regular-mode will continue and transmission will be at `REGULAR_TRANSMISSION_INTERVAL`
- Default: 70 percent

### CPU_PERCENTAGE_AVERAGE_TIME
- Smoothing of CPU load
- Default: 10 secodns

## Sample Payload

```
{
   "device_id":"7d25b11d-396a-46d9-b32d-9c2f4e7e875b",
   "emergency":false,
   "cpu_percentage":4.9,
   "virtual_memory":{
      "total":34359738368,
      "available":13635780608,
      "percent":60.3,
      "used":15407939584,
      "free":1661714432,
      "active":11948310528,
      "inactive":11937169408,
      "wired":3459629056
   },
   "disk_io":{
      "read_count":48472390,
      "write_count":117373406,
      "read_bytes":1220511014912,
      "write_bytes":2082562387968,
      "read_time":9291837,
      "write_time":8408687
   },
   "swap":{
      "total":2147483648,
      "used":1222574080,
      "free":924909568,
      "percent":56.9,
      "sin":681228550144,
      "sout":2840313856
   },
   "percentage_all_memory":39.68544006347656
}
```