import os
import threading
from queue import Queue

def replace_spaces(input_file, output_file, chunk_queue):
    while True:
        chunk = chunk_queue.get()
        if chunk is None:
            break
        
        content = chunk.replace(' ', '\n')
        with open(output_file, 'a') as f:
            f.write(content)
        
        chunk_queue.task_done()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'put-txt-here.txt')
    output_file = os.path.join(current_dir, 'output-here.txt')
    
    if not os.path.exists(input_file):
        print("Error: put-txt-here.txt not found in the same directory of this python script.")
        return
    
    try:
        with open(output_file, 'x'):
            # File does not exist, create it
            pass
    except FileExistsError:
        # File already exists, do nothing
        pass
    
    # Read the entire content of the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    num_threads = 100
    
    # Divide the work into chunks to be processed by threads
    chunk_size = len(content) // num_threads
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    
    # Create a queue to hold chunks
    chunk_queue = Queue()
    
    # Add chunks to the queue
    for chunk in chunks:
        chunk_queue.put(chunk)
    
    # Add None values to signal the threads to stop
    for _ in range(num_threads):
        chunk_queue.put(None)
    
    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=replace_spaces, args=(input_file, output_file, chunk_queue))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    print("Replacement complete. Check output-here.txt for the result.")

if __name__ == "__main__":
    main()
