import simpy
import random
import numpy as np

class OS:
    def __init__(self, env, num_processes):
        self.env = env
        self.cpu = simpy.Resource(env, capacity=1)
        self.ram = simpy.Container(env, init=100, capacity=100)  # Memoria RAM inicial de 100
        self.num_processes = num_processes
        self.processes = []
        self.process_times = []

    def run(self):
        for i in range(self.num_processes):
            self.env.process(self.new_process(i))
        self.env.run()
        self.calculate_stats()

    def new_process(self, process_id):
        memory_required = random.randint(1, 10)  # Cantidad de memoria requerida para el proceso
        instructions_to_execute = random.randint(1, 10)  # Instrucciones totales a ejecutar
        process = {'id': process_id, 'memory_required': memory_required, 'instructions_left': instructions_to_execute}
        self.processes.append(process)
        print(f"Process {process_id} created. Memory required: {memory_required}, Instructions left: {instructions_to_execute}")
        return self.ready_process(process)  # Devolver el generador para procesar el proceso

    def ready_process(self, process):
        start_time = self.env.now
        while True:
            try:
                yield self.ram.get(process['memory_required'])
                break
            except simpy.ContainerPutError:  # Si no hay suficiente memoria, el proceso espera en cola
                yield self.env.timeout(1)  # Esperar un ciclo de tiempo

        with self.cpu.request() as req:
            yield req  # Esperar a que el CPU esté disponible
            while process['instructions_left'] > 0:
                yield self.env.timeout(1)  # Tiempo de ejecución de instrucción
                process['instructions_left'] -= 3  # Restar las instrucciones ejecutadas

            # Proceso finalizado
            yield self.ram.put(process['memory_required'])  # Devolver memoria utilizada
            self.process_times.append(self.env.now - start_time)

    def calculate_stats(self):
        process_times_array = np.array(self.process_times)
        mean_time = np.mean(process_times_array)
        std_deviation = np.std(process_times_array)
        print(f"Mean Time: {mean_time}, Standard Deviation: {std_deviation}")

# Configuración de la simulación
random.seed(15)
env = simpy.Environment()
os = OS(env, num_processes=200)  
os.run()
