try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    
import subprocess
import time
import logging
import os

log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)

def get_cpu_temperature():
    """Get CPU temperature using vcgencmd"""
    try:
        # Try vcgencmd first (Raspberry Pi specific)
        result = subprocess.run(
            ['vcgencmd', 'measure_temp'],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        if result.returncode == 0:
            # Parse output like "temp=45.2'C"
            temp_str = result.stdout.strip()
            if '=' in temp_str:
                temp_value = temp_str.split('=')[1].replace("'C", "").replace("°C", "")
                return float(temp_value)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError, ValueError, IndexError) as e:
        logger.debug(f"vcgencmd failed: {e}")
        # Fallback to thermal zone if vcgencmd is not available
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read().strip()) / 1000.0
                return temp
        except (IOError, OSError, ValueError) as e:
            logger.warning(f"Could not get CPU temperature: {e}")
            return None
    return None

def get_uptime():
    """Get system uptime in hours"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds / 3600  # Convert to hours
    except (IOError, OSError, ValueError, IndexError) as e:
        logger.warning(f"Could not get system uptime: {e}")
        return None

def get_network_status():
    """Get basic network status"""
    if not PSUTIL_AVAILABLE:
        return {}
    
    try:
        # Get network interfaces
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        }
    except (AttributeError, OSError) as e:
        logger.warning(f"Could not get network status: {e}")
        return {}

def get_system_stats():
    """Get all system statistics"""
    try:
        if not PSUTIL_AVAILABLE:
            # Fallback implementation when psutil is not available
            return {
                'cpu_usage': get_fallback_cpu_usage(),
                'memory_usage': get_fallback_memory_usage(),
                'temperature': get_cpu_temperature(),
                'uptime': get_uptime(),
                'network': get_network_status()
            }
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Temperature
        temperature = get_cpu_temperature()
        
        # Uptime
        uptime = get_uptime()
        
        # Network
        network = get_network_status()
        
        return {
            'cpu_usage': cpu_percent,
            'memory_usage': memory_percent,
            'temperature': temperature,
            'uptime': uptime,
            'network': network
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise

def get_fallback_cpu_usage():
    """Fallback method to get CPU usage"""
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        cpu_times = [int(x) for x in line.split()[1:]]
        idle_time = cpu_times[3]
        total_time = sum(cpu_times)
        if total_time == 0:
            return 0.0
        return round((1.0 - idle_time / total_time) * 100, 1)
    except (IOError, OSError, ValueError, IndexError, ZeroDivisionError) as e:
        logger.warning(f"Could not get CPU usage: {e}")
        return 0.0

def get_fallback_memory_usage():
    """Fallback method to get memory usage"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        mem_total = int(lines[0].split()[1])
        mem_free = int(lines[1].split()[1])
        if mem_total == 0:
            return 0.0
        mem_used = mem_total - mem_free
        return round((mem_used / mem_total) * 100, 1)
    except (IOError, OSError, ValueError, IndexError, ZeroDivisionError) as e:
        logger.warning(f"Could not get memory usage: {e}")
        return 0.0

if __name__ == "__main__":
    # Test the function
    stats = get_system_stats()
    print(stats)