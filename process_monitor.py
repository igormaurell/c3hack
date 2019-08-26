import psutil
import time, datetime

PC = 'pc'

monitor_dict = {PC:{}}

monitor_dict[PC]['stamp'] = time.time()

#CPU
monitor_dict[PC]['cpu'] = {}
cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
monitor_dict[PC]['cpu']['percent'] = cpu_percent

monitor_dict[PC]['cpu']['cpu_freq'] = []
cpu_freqs =  psutil.cpu_freq(percpu=True)
for cpu_freq in cpu_freqs:
    monitor_dict[PC]['cpu']['cpu_freq'].append({'current':cpu_freq.current, 'min':cpu_freq.min, 'max':cpu_freq.max})

load_avg = psutil.getloadavg()
monitor_dict[PC]['cpu']['load_avg'] = list(load_avg)

#Memory
monitor_dict[PC]['memory'] = {}
monitor_dict[PC]['memory']['ram'] = {}
virtual_memory =  psutil.virtual_memory()
monitor_dict[PC]['memory']['ram']['total'] = virtual_memory.total
monitor_dict[PC]['memory']['ram']['percent'] = virtual_memory.percent
monitor_dict[PC]['memory']['ram']['active'] = virtual_memory.active
monitor_dict[PC]['memory']['ram']['inactive'] = virtual_memory.inactive
monitor_dict[PC]['memory']['ram']['cached'] = virtual_memory.cached
monitor_dict[PC]['memory']['ram']['shared'] = virtual_memory.shared

monitor_dict[PC]['memory']['swap'] = {}
swap_memory = psutil.swap_memory()
monitor_dict[PC]['memory']['swap']['total'] = swap_memory.total
monitor_dict[PC]['memory']['swap']['percent'] = swap_memory.percent


#Disks
monitor_dict[PC]['disks'] = {}
monitor_dict[PC]['disks']['partitions'] = []
disk_partitions = psutil.disk_partitions(all=False)
for disk_partition in disk_partitions:
    monitor_dict[PC]['disks']['partitions'].append({'device':disk_partition.device, 'mount_point':disk_partition.mountpoint, 'fstype':disk_partition.fstype, 'opts':disk_partition.opts})

monitor_dict[PC]['disks']['usage'] = {}
disk_usage = psutil.disk_usage('/')
monitor_dict[PC]['disks']['usage']['total'] = disk_usage.total
monitor_dict[PC]['disks']['usage']['percent'] = disk_usage.percent

monitor_dict[PC]['disks']['io_counters'] = {}
disk_io = psutil.disk_io_counters(perdisk=True, nowrap=True)
for key in disk_io.keys():
    monitor_dict[PC]['disks']['io_counters'][key] = {}
    monitor_dict[PC]['disks']['io_counters'][key]['read_count'] = disk_io[key].read_count
    monitor_dict[PC]['disks']['io_counters'][key]['write_count'] = disk_io[key].write_count
    monitor_dict[PC]['disks']['io_counters'][key]['read_bytes'] = disk_io[key].read_bytes
    monitor_dict[PC]['disks']['io_counters'][key]['write_bytes'] = disk_io[key].write_bytes
    monitor_dict[PC]['disks']['io_counters'][key]['read_time'] = disk_io[key].read_time
    monitor_dict[PC]['disks']['io_counters'][key]['write_time'] = disk_io[key].write_time
    monitor_dict[PC]['disks']['io_counters'][key]['busy_time'] = disk_io[key].busy_time

#Network
monitor_dict[PC]['network'] = {}
monitor_dict[PC]['network']['io_counters'] = {}
net_io = psutil.net_io_counters(pernic=True, nowrap=True)
for key in net_io.keys():
    monitor_dict[PC]['network']['io_counters'][key] = {}
    monitor_dict[PC]['network']['io_counters'][key]['bytes_sent'] = net_io[key].bytes_sent
    monitor_dict[PC]['network']['io_counters'][key]['bytes_recv'] = net_io[key].bytes_recv
    monitor_dict[PC]['network']['io_counters'][key]['packets_sent'] = net_io[key].packets_sent
    monitor_dict[PC]['network']['io_counters'][key]['packets_recv'] = net_io[key].packets_recv
    monitor_dict[PC]['network']['io_counters'][key]['errin'] = net_io[key].errin
    monitor_dict[PC]['network']['io_counters'][key]['errout'] = net_io[key].errout
    monitor_dict[PC]['network']['io_counters'][key]['dropin'] = net_io[key].dropin
    monitor_dict[PC]['network']['io_counters'][key]['dropout'] = net_io[key].dropout

monitor_dict[PC]['network']['connections'] = []
net_connections = psutil.net_connections(kind='inet')
for net_connection in net_connections:
    monitor_dict[PC]['network']['connections'].append({'fd':net_connection.fd,'family':net_connection.family,'type':net_connection.type,
    'laddr':net_connection.laddr,'raddr':net_connection.raddr,'status':net_connection.status,'pid':net_connection.pid})

monitor_dict[PC]['network']['stats'] = {}
net_stats = psutil.net_if_stats()
for key in net_stats.keys():
    monitor_dict[PC]['network']['stats'][key] = {}
    monitor_dict[PC]['network']['stats'][key]['isup'] = net_stats[key].isup
    monitor_dict[PC]['network']['stats'][key]['duplex'] = net_stats[key].duplex
    monitor_dict[PC]['network']['stats'][key]['speed'] = net_stats[key].speed
    monitor_dict[PC]['network']['stats'][key]['mtu'] = net_stats[key].mtu

print monitor_dict

#Sensors
def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

monitor_dict[PC]['sensors'] = {}
monitor_dict[PC]['sensors']['temperatures'] = {}
sensors_temperatures = psutil.sensors_temperatures(fahrenheit=False)
for key in sensors_temperatures.keys():
    monitor_dict[PC]['sensors']['temperatures'][key] = []
    for sensors_temperature in sensors_temperatures[key]:
        monitor_dict[PC]['sensors']['temperatures'][key].append({'label':sensors_temperature.label,
        'current':sensors_temperature.current, 'high':sensors_temperature.high, 'critical':sensors_temperature.critical})

monitor_dict[PC]['sensors']['fans'] = {}
sensors_fans = psutil.sensors_fans()
for key in sensors_fans.keys():
    monitor_dict[PC]['sensors']['fans'][key] = []
    for sensors_fan in sensors_fans[key]:
        monitor_dict[PC]['sensors']['fans'][key].append({'label':sensors_fan.label,'current':sensors_fan.current})

monitor_dict[PC]['sensors']['battery'] = {}
sensor_battery = psutil.sensors_battery()
if(sensor_battery):
    monitor_dict[PC]['sensors']['battery']['percent'] = sensor_battery.percent
    monitor_dict[PC]['sensors']['battery']['time_left'] = secs2hours(sensor_battery.secsleft)
    monitor_dict[PC]['sensors']['battery']['power_plugged'] = sensor_battery.power_plugged
else: 
    monitor_dict[PC]['sensors']['battery'] = None

#OtherSystemInfo
monitor_dict[PC]['other_system_info'] = {}
boot_time = psutil.boot_time()
monitor_dict[PC]['other_system_info']['boot_time'] = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")

monitor_dict[PC]['other_system_info']['users'] = []
users = psutil.users()
for user in users:
    monitor_dict[PC]['other_system_info']['users'].append({'name':user.name, 'terminal':user.terminal,
    'host':user.host, 'started':user.started, 'pid':user.pid})


#Process
monitor_dict[PC]['process'] = []
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'status', 'nice', 'num_threads'])
    except psutil.NoSuchProcess:
        pass
    else:
        monitor_dict[PC]['process'].append(pinfo)
        #print(pinfo)
print monitor_dict