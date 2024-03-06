import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
NUM_PROCESSES = [25, 50, 100, 150, 200]
CPU_SPEED = 3  # Instrucciones por unidad de tiempo
MEMORY_CAPACITY_1 = 200  # Memoria inicial: 200
MEMORY_CAPACITY_2 = 100  # Memoria reducida: 100
CPU_SPEED_2 = 6  # Velocidad del procesador aumentada: 6
NUM_CPUS = 2  # Número de procesadores aumentado: 2

class Process:
    def __init__(self, env, name, ram, cpu):
        self.env = env
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.instructions = random.randint(1, 10)  # Cantidad de instrucciones aleatoria

    def run(self):
        interval = random.choice([1, 5, 10])  # Intervalo de llegada aleatorio
        with self.ram.get(random.randint(1, 10)) as req:
            yield req

            while self.instructions > 0:
                with self.cpu.request() as req:
                    yield req
                    execution_time = min(self.instructions, self.cpu.speed)
                    yield self.env.timeout(execution_time / self.cpu.speed)
                    self.instructions -= execution_time

                    if self.instructions <= 0:
                        print(f"Process {self.name} terminated.")
                    else:
                        io_waiting = random.randint(1, 21)
                        if io_waiting == 1:
                            print(f"Process {self.name} doing I/O.")
                            yield self.env.timeout(random.randint(1, 2))
                            print(f"Process {self.name} finished I/O.")
                        else:
                            print(f"Process {self.name} ready for next CPU burst.")
            self.ram.put(random.randint(1, 10))

def setup(env, num_processes, ram, cpu):
    for i in range(num_processes):
        p = Process(env, f"Process {i+1}", ram, cpu)
        env.process(p.run())
        yield env.timeout(0)  # No hay un intervalo fijo entre los procesos

def run_simulation(num_processes, ram_capacity, cpu_speed, num_cpus=1):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Recursos (RAM y CPU)
    ram = simpy.Container(env, capacity=ram_capacity, init=ram_capacity)
    cpu = simpy.Resource(env, capacity=num_cpus)
    cpu.speed = cpu_speed  # Asignar velocidad de CPU

    # Configurar simulación
    env.process(setup(env, num_processes, ram, cpu))

    # Ejecutar simulación
    env.run(until=100)  # Duración de la simulación

    # Calcular y retornar estadísticas
    return [env.now / num_processes for _ in range(num_processes)]

def main():
    # Escenario i: Incrementar la memoria a 200
    print("Escenario i: Incrementar la memoria a 200")
    avg_times_i = []
    for num_processes in NUM_PROCESSES:
        times = run_simulation(num_processes, MEMORY_CAPACITY_1, CPU_SPEED)
        avg_time = statistics.mean(times)
        avg_times_i.append(avg_time)

    # Calcular desviación estándar y mostrar resultados del Escenario i
    std_dev_i = statistics.stdev(avg_times_i)
    print("Promedio de tiempos:", avg_times_i)
    print("Desviación estándar:", std_dev_i)

    # Graficar resultados del Escenario i
    plt.plot(NUM_PROCESSES, avg_times_i, marker='o', label='Memory Capacity: 200')
    plt.xlabel('Number of Processes')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Number of Processes (Memory Capacity: 200)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Escenario ii: Reducir la memoria a 100 y aumentar la velocidad del procesador a 6 instrucciones por unidad de tiempo
    print("\nEscenario ii: Reducir la memoria a 100 y aumentar la velocidad del procesador a 6 instrucciones por unidad de tiempo")
    avg_times_ii = []
    for num_processes in NUM_PROCESSES:
        times = run_simulation(num_processes, MEMORY_CAPACITY_2, CPU_SPEED_2)
        avg_time = statistics.mean(times)
        avg_times_ii.append(avg_time)

    # Calcular desviación estándar y mostrar resultados del Escenario ii
    std_dev_ii = statistics.stdev(avg_times_ii)
    print("Promedio de tiempos:", avg_times_ii)
    print("Desviación estándar:", std_dev_ii)

    # Graficar resultados del Escenario ii
    plt.plot(NUM_PROCESSES, avg_times_ii, marker='o', label='Memory Capacity: 100, CPU Speed: 6')
    plt.xlabel('Number of Processes')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Number of Processes (Memory Capacity: 100, CPU Speed: 6)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Escenario iii: Mantener la memoria en 100 pero emplear 2 procesadores con velocidad normal
    print("\nEscenario iii: Mantener la memoria en 100 pero emplear 2 procesadores con velocidad normal")
    avg_times_iii = []
    for num_processes in NUM_PROCESSES:
        times = run_simulation(num_processes, MEMORY_CAPACITY_2, CPU_SPEED, NUM_CPUS)
        avg_time = statistics.mean(times)
        avg_times_iii.append(avg_time)

    # Calcular desviación estándar y mostrar resultados del Escenario iii
    std_dev_iii = statistics.stdev(avg_times_iii)
    print("Promedio de tiempos:", avg_times_iii)
    print("Desviación estándar:", std_dev_iii)

    # Graficar resultados del Escenario iii
    plt.plot(NUM_PROCESSES, avg_times_iii, marker='o', label='Memory Capacity: 100, CPUs: 2')
    plt.xlabel('Number of Processes')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Number of Processes (Memory Capacity: 100, CPUs: 2)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()