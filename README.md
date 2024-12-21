# MIMD-Simulator
A simulation of a shared memory multiprocessor system. It models MIMD architecture, using processes to compute workloads in parallel. The project includes cache coherence via write-invalidate, shared memory synchronization, and efficient computation of the sum of squares, showcasing parallel processing principles.

The file used to store values in this project is the performance_log.csv file. It logs the results of each simulation run, including the number of CPUs, workload size, final sum, and elapsed time. The file is stored in the current working directory of the project, ensuring easy access. If the file doesn't already exist, it will be created automatically. The log is appended with new data after each simulation run to keep a record of performance over multiple runs.

The size of the problem and the CPU count are controlled by the following variables:

numbers: This variable defines the total workload, represented as a list of integers. The size of the problem can be adjusted by modifying the range of numbers. For example, numbers = list(range(1, 1001)) processes numbers from 1 to 1000, which can be changed to any range of integers based on the desired problem size.

num_processes: This variable controls the number of CPUs (processes) used in the simulation. It is set to the desired number of parallel processes. For instance, setting num_processes = 8 means the simulation will use 8 parallel processes (CPUs) to compute the workload.
