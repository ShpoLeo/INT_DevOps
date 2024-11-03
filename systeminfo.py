import platform
import socket
import os
import psutil
import argparse
import json
import time
from logs import logger

# Custom exception for no arguments
class NoArgumentsException(Exception):
    pass

"""The script collects system information. including the following:

    1.  Operating System Information:
        Retrieves the hostname, username, and type of operating system currently in use.
    2.  CPU Information: 
        Gathers details about the CPU, including the number of logical processors and the current CPU usage percentage.
    3.  Memory Information: 
        Provides insights into the system's memory usage, detailing total, used, and free memory in gigabytes.
    4.  Disk Information: 
        Displays information about disk partitions, including the device name, mount point, file system type, and disk usage statistics.
    5.  Time Information: 
        Collects and displays the current local time and the system boot time.
    """

# Initialize argument parser
parser = argparse.ArgumentParser(description="Get system information")
parser.add_argument("-os", "--os-info", action='store_true', help="Display operating system info")
parser.add_argument("-c", "--cpu", action='store_true', help="Display CPU info")
parser.add_argument("-m", "--mem", action='store_true', help="Display memory info")
parser.add_argument("-d", "--disk", action='store_true', help="Display HD info")
parser.add_argument("-t", "--time", action='store_true', help="Display all info")
parser.add_argument("-a", "--all", action='store_true', help="Display all info")
parser.add_argument("-f", "--file", choices=["text", "json"], default="text", help="Output format: text or json")
args = parser.parse_args()

# Prepare arguments to display
args_list = vars(args)

# Check for no arguments
if not (args.os_info or args.cpu or args.mem or args.disk or args.time or args.all):
    error_message = "No arguments provided. Please specify at least one option: " \
                    "-os, -c, -m, -d, -t, or -a."
    logger.error(error_message)
    print(error_message)  # Print to console
    raise NoArgumentsException(error_message)

class SystemInfo:
    def __init__(self):
        self.result = {
            "os_info": {},
            "cpu": {},
            "mem": {},
            "disk": {},
            "time": {}
        }
        logger.debug(f'SystemInfo object created')

        """Collect operating system information."""
    def get_os_info(self):
        logger.debug(f'Getting OS info') 
        try:
            self.result['os_info'] = {
                "Operating System": platform.system(),
                "Hostname": socket.gethostname(),
                "User": os.getlogin()
            }
        except Exception as e:
            logger.error(f"Could not retrieve Os info: {str(e)}")
            self.result(['os_info']) == {"Error": f"Could not retrieve OS info: {str(e)}"}

            """Collect CPU usage information."""
    def get_cpu_info (self):
        logger.debug(f'Getting CPU info')
        try:
            self.result['cpu'] = {
                "Count": psutil.cpu_count(logical=True),
                "Usage": f"{psutil.cpu_percent(interval=1)}%"
            }
        except Exception as e:
            logger.error(f"Could not retrieve CPU info: {str(e)}")
            self.result['cpu'] = {"Error": f"Could not retrieve CPU info: {str(e)}"}

        """Collect memory usage information."""
    def get_memory_info(self):
        logger.debug(f'Getting memory info')
        try:
            mem = psutil.virtual_memory()
            self.result['mem'] = {
                "Total Memory (GB)": round(mem.total / (1024 ** 3), 2),
                "Used Memory (GB)": round(mem.used / (1024 ** 3), 2),
                "Free Memory (GB)": round(mem.free / (1024 ** 3), 2)
            }
        except Exception as e:
            logger.error(f"Could not retrieve memory info: {str(e)}")
            self.result['mem'] = {"Error": f"Could not retrieve memory info: {str(e)}"}
        

        """Collect hard drive information."""
    def get_hd_info(self):
        logger.debug('Getting hard drive info')
        try:
            partitions = psutil.disk_partitions()
            hd_info = []
            for part in partitions:
                  usage = psutil.disk_usage(part.mountpoint)
                  hd_info.append({
                        'Device': part.device,
                        'Mountpoint': part.mountpoint,
                        'File System Type': part.fstype,
                        'Total Space (GB)': round(usage.total / (1024 ** 3), 2),
                        'Used Space (GB)': round(usage.used / (1024 ** 3), 2),
                        'Free Space (GB)': round(usage.free / (1024 ** 3), 2),
                        'Usage Percentage': usage.percent
                })
            self.result['disk'] = hd_info
        except Exception as e:
            logger.error(f"Could not retrieve hard drive info: {str(e)}")
            self.result['disk'] = {"Error": f"Could not retrieve hard drive info: {str(e)}"}


        """Collect Time information."""
    def get_time_info(self):
        logger.debug(f'Getting OS info')
        try:
            self.result['time'] = {
                "Local_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "Boot_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
            }
        except Exception as e:
            logger.error(f"Could not retrieve Time info: {str(e)}")
            self.result['time'] = {"Error": f"Could not retrieve Time info: {str(e)}"}

    def collect_info(self):
        self.get_os_info()
        self.get_cpu_info()
        self.get_memory_info()
        self.get_hd_info()
        self.get_time_info()

        """Display collected information in the specified format."""
    def display_result(self, metrics, file="text"):
        logger.debug(f'Displaying result')
        response = {}
        if 'all' in metrics:
            response = self.result
        else:
            for metric in metrics:
                response[f"{metric} information"] = self.result[metric]
       
        if file == "json":
            logger.debug(f'Output format: JSON')
            print(json.dumps(response, indent=4))
        else:
            logger.debug(f'Output format: text')
            for key in response:
                print(f'{key}:')
                print(str(response[key]).strip('{}').replace(',', '\n'))

try:
    # Initialize SystemInfo instance
    system_info = SystemInfo()

    # Collect specified information
    system_info.collect_info()

    args_to_display = []
    if args_list['all']:
        args_to_display.append("all")
    else:
        for arg in args_list:
            if args_list[arg] == True:
                args_to_display.append(arg)

    system_info.display_result(args_to_display, args.file)

except NoArgumentsException as e:
    logger.error(e)