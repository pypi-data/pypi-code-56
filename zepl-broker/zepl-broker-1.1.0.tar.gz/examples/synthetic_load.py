# spawn dummy devices and start them in a seperate process
import zmq
from multiprocessing import Process
from zepl_broker import DummyClient
from time import sleep

broker_ip = '192.168.0.5' # raspberrypi
dummy_machine_ip = '192.168.0.10' # desktop
dummy_count = 30
task_num = 2

# dummy devices
dummy_cfg = {}
port = 5000
d_template = {
    'dev_ip': dummy_machine_ip,
    'dev_port': port,
    'proto': 'dummy-example',
    'dev_pw': 'asdf'
}
for d in range(dummy_count):
    port += 1
    d_template['dev_port'] = port
    dummy_cfg[f'dummy{d}'] = {}
    dummy_cfg[f'dummy{d}'].update(d_template)


def dd_proc(broker, cfg):
    import zmq.asyncio, asyncio
    from zepl_device.devices.dummy import DummyDevice
    print(cfg)
    ctx = zmq.asyncio.Context()
    for dev_id in cfg.keys():
        d = DummyDevice(ctx, cfg[dev_id])
        d.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()

dev_proc = Process(target=dd_proc, args=(broker_ip, dummy_cfg))
dev_proc.start()

## client stuff
ctx = zmq.Context()
client = DummyClient(ctx, broker_ip)
for dev_id in dummy_cfg.keys():
    client.add_device(dev_id, dummy_cfg[dev_id])

# start sender tasks
for dev_id in dummy_cfg.keys():
    for x in range(task_num):
        sleep(0.05)
        client.start_task(dev_id, 'device', f'task{x}', 'a', arg={'device': f'task{x}'})
        sleep(0.05)
        client.start_task(dev_id, 'device', f'task{x}', 'b', arg={'device': f'task{x}'})
        sleep(0.05)
        client.start_task(dev_id, 'runner', f'task{x}', 'a', arg={'runner': f'task{x}'})
        sleep(0.05)
        client.start_task(dev_id, 'runner', f'task{x}', 'b', arg={'runner': f'task{x}'})

# msg counter
print('>>> Starting message counter...')
print(f'Number of sender tasks is: {dummy_count*task_num*4} (1/2 devices and runners each.')
from time import perf_counter
client.log_sub('')
avg = 3
s_counter, msg_counter, avg_counter = [0 ,0 ,0]
tic = perf_counter()
while True:
    client.cnt_log()
    msg_counter += 1
    toc = perf_counter()
    if (toc-tic) > 1:
        tic = perf_counter()
        s_counter += 1
        avg_counter += msg_counter
        if s_counter > avg:
            print(f'({avg}s): {int(avg_counter/avg)} msg/s',  end='\r', flush=True)
            avg_counter = 0
            s_counter = 0
        msg_counter = 0
