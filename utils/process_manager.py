import logging
import queue as queue_lib
import signal
import sys
from multiprocessing import Process, Queue

import GPUtil
from tornado.ioloop import IOLoop


class ProcessManager():
    """A ProcessManager class is used for controlling the multi-processing features of this application.

    """

    def __init__(self):
        """Initialization method.

        """

        # Creates a queue object
        self.queue = Queue()

        # Creates an process object with a specific target
        self.current_process = Process(target=self.handle_process, args=(self.queue,), daemon=False)

        # Starts the process
        self.current_process.start()

    def handle_process(self, queue):
        """It handles a new process by calling a specific IOLoop and starting it with a callback.

        Args:
            queue (Queue): A queue object.

        """

        # Creates an IOLoop object
        loop = IOLoop()

        # Spawns the callback function
        loop.spawn_callback(self.work_vili, queue)

        # Starts the loop
        loop.start()

    def add_process(self, process):
        """Adds a new process to the queue.

        Args:
            process (Process): A new process to be added to the queue.

        """

        # Puts a new process in the queue
        self.queue.put(process)

    def gpu_settings(self):
        """
        """

        load_per_process = float(10)
        mem_per_process = float(100)
        return load_per_process, mem_per_process

    def get_device_config(self):
        """
        """

        # check if there exists any gpu available

        try:

            gpus = GPUtil.getGPUs()
            for g in gpus:
                logging.info(g.name)

            load_per_process, mem_per_process = self.gpu_settings()

            gpu_max_load = 1 - load_per_process
            gpu_mem_fraction = 1 - mem_per_process

            device_id = GPUtil.getFirstAvailable(order='first',
                                                 maxLoad=gpu_max_load,
                                                 maxMemory=gpu_mem_fraction,
                                                 attempts=3,
                                                 interval=3,
                                                 verbose=False)[0]

            if device_id is not None:
                config = {
                    "gpu": {
                        "DEVICE_ID": device_id,
                        "MEMORY_FRACTION": mem_per_process
                    }
                }
                return config
        except Exception as e:
            print(e)
            print("No gpus found. Falling back")
            config = {
                "cpu": {
                }
            }
            return config

    def drain_pool(self, pool_name, pool):
        """
        """

        new_pool = []
        for idx, p in enumerate(pool):
            if not p.is_alive():
                p.terminate()
            else:
                new_pool.append(p)
        return new_pool

    async def work_vili(self, queue):
        """
        """
        
        def empty_process_pool(pool):
            for idx, p in enumerate(pool):
                p.terminate()
        def sig_handler(*args):
            """Intercepts CTRL+C and exits gracefully."""
            empty_process_pool(cpu_pool)
            empty_process_pool(gpu_pool)
            logging.warning('Terminating Test PROCESSOR')
            sys.exit()
        job = False
        cpu_pool = []
        gpu_pool = []
        signal.signal(signal.SIGINT, sig_handler)
        while True:
            try:
                cpu_pool = self.drain_pool("CPU Pool", cpu_pool)
                gpu_pool = self.drain_pool("gpu Pool", cpu_pool)

                job = queue.get()
                if job:
                    processor = job["target"]()
                    device_config = self.get_device_config()
                    job["data"]["device_config"] = device_config
                    if device_config.get("gpu"):
                        p = Process(target=processor.consume,
                                    name="mimir-training_gpu-" + str(len(gpu_pool) + 1),
                                    args=(job["data"],),
                                    daemon=False)
                        p.start()
                        gpu_pool.append(p)
                        print("Added process to gpu pool")
                    else:
                        p = Process(target=processor.consume,
                                    name="mimir-training_cpu-" + str(len(gpu_pool) + 1),
                                    args=(job["data"],),
                                    daemon=False)
                        p.start()
                        cpu_pool.append(p)
                        print("Added process to CPU pool")
            except queue_lib.Empty as e:
                print(e)
