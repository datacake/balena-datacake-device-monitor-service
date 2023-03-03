import requests
import os
import psutil
import time

class BalenaDeviceUptimeMetricsService:

    def __init__(self) -> None:
        
        try: self.request_url = os.environ["WEBHOOK_DESTINATION_URL"]
        except Exception as e: 
            print("No Webhook URL specified. Please set WEBHOOK_DESTINATION_URL environment variable.")
            time.sleep(10)
            quit()
        
        try: self.device_id = os.environ["DEVICE_ID"]
        except Exception as e: 
            print("No Device ID specified. Please set DEVICE_ID environment variable.")
            time.sleep(10)
            quit()
        
        self.is_emergency_transmission = False
        self.regular_transmission_interval = os.environ.get("REGULAR_TRANSMISSION_INTERVAL", 60)
        self.emergency_transmission_interval = os.environ.get("EMERGENCY_TRANSMISSION_INTERVAL", 10)
        self.cpu_percentage_max = os.environ.get("CPU_PERCENTAGE_MAX", 70)
        self.cpu_percentage_average_time = os.environ.get("CPU_PERCENTAGE_AVERAGE_TIME", 10)

    def start(self):
        print("Starting device uptime and metrics reporter...")
        self.loop()

    def loop(self):
        while True:
            cpu_percentage = psutil.cpu_percent(self.cpu_percentage_average_time)   
            if cpu_percentage >= self.cpu_percentage_max: self.is_emergency_transmission = True
            else: self.is_emergency_transmission = False
            data = {
                'device_id' : self.device_id,
                'emergency' : self.is_emergency_transmission,
                'cpu_percentage' : cpu_percentage,
                'virtual_memory' : psutil.virtual_memory()._asdict(),
                'disk_io' : psutil.disk_io_counters()._asdict(),
                'swap' : psutil.swap_memory()._asdict(),
                'percentage_all_memory' : psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
            }
            try:                    
                r = requests.post(url=self.request_url, json=data)
                print("Successfully send metrics")
            except Exception as e:
                print(f"Caught Exception when trying to send metrics: {e}")
            if self.is_emergency_transmission: time.sleep(self.emergency_transmission_interval - self.cpu_percentage_average_time)
            else: time.sleep(self.regular_transmission_interval - self.cpu_percentage_average_time)

if __name__ == '__main__':
    service = BalenaDeviceUptimeMetricsService()
    service.start()