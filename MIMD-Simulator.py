import multiprocessing
import time
import csv
import os

def compute_square_chunk(process_id, number_chunk, shared_total, cache, cache_lock, global_lock):
    local_sum = sum(num * num for num in number_chunk)  # Compute local sum (Private Memory)

    # Update local cache (simulating private memory for each CPU)
    cache[process_id] = local_sum
    
    # Simulate cache coherence: Invalidate other caches (write-invalidate)
    with cache_lock:
        # Broadcast that the cache has been updated (simple write-invalidate)
        cache_invalid = {pid: False for pid in range(len(cache))}  # Mark all caches invalid
        cache_invalid[process_id] = True  # This process' cache is valid
    
    # Synchronize access to shared total (global memory)
    with global_lock:
        # Update shared total safely, simulating M.I.M.D. communication via shared memory
        shared_total.value += local_sum

def run_simulation(num_processes, numbers):
    # Total workload
    chunk_size = len(numbers) // num_processes  # Determine chunk size

    # Divide workload into chunks, ensuring no numbers are skipped
    chunks = [numbers[i * chunk_size:(i + 1) * chunk_size] for i in range(num_processes - 1)]
    chunks.append(numbers[(num_processes - 1) * chunk_size:])  # Handle the last chunk

    # Shared data and synchronization
    shared_total = multiprocessing.Value('d', 0.0)  # Shared memory (global memory)
    cache = multiprocessing.Manager().dict()  # Each process' cache (private memory)
    cache_lock = multiprocessing.Lock()  # Lock for cache coherence
    global_lock = multiprocessing.Lock()  # Lock for shared memory access

    # Performance benchmarking: start time
    start_time = time.time()

    # Create and start processes (CPUs)
    processes = []
    for i, chunk in enumerate(chunks):
        p = multiprocessing.Process(target=compute_square_chunk, args=(i, chunk, shared_total, cache, cache_lock, global_lock))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Performance benchmarking: end time
    end_time = time.time()
    elapsed_time = end_time - start_time

    return shared_total.value, elapsed_time

def log_data(cpu_count, workload_size, final_sum, elapsed_time, filename="performance_log.csv"):
    # Ensure the file is written in the current working directory or specify an absolute path
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    
    # Write data to the file in append mode to avoid overwriting
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        # If it's the first run, add header to the file
        if os.path.getsize(file_path) == 0:  # Check if the file is empty
            writer.writerow(['CPU Count', 'Workload Size', 'Final Sum', 'Elapsed Time (seconds)'])
        
        writer.writerow([cpu_count, workload_size, final_sum, elapsed_time])

    print(f"Data logged in: {file_path}")  # Print the file path for confirmation

    # Print the current results to the CMD
    print(f"Current results:")
    print(f"CPU Count: {cpu_count}")
    print(f"Workload Size: {workload_size}")
    print(f"Final Sum: {final_sum}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")

def main():
    # Total workload
    numbers = list(range(1, 1001))  # Increase size for more workload

    # Run the simulation for a specific CPU count, for example, 4 CPUs
    num_processes = 8  # Change this as needed
    final_sum, elapsed_time = run_simulation(num_processes, numbers)
    
    # Log the result to the file
    log_data(num_processes, len(numbers), final_sum, elapsed_time)  # Log the result for this run

if __name__ == "__main__":
    main()
