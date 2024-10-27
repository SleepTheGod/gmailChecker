import random
import time
import threading
from queue import Queue

# Number of worker threads
NUM_THREADS = 10

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def simulate_username_check(username):
    # Simulate a random chance of being taken (this is for demonstration only)
    taken = random.choice([True, False])
    return taken

def worker(username_queue, available_usernames):
    while not username_queue.empty():
        username = username_queue.get()
        is_taken = simulate_username_check(username)

        if not is_taken:
            available_usernames.append(username)
            print(f"Username available: {username}")
        else:
            print(f"Username taken: {username}")

        username_queue.task_done()

def main():
    words = load_words('words.txt')
    username_queue = Queue()
    available_usernames = []

    # Fill the queue with usernames
    for word in words:
        username = f"{word.lower()}@gmail.com"
        username_queue.put(username)

    # Create threads
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(username_queue, available_usernames))
        thread.start()
        threads.append(thread)

    # Wait for the queue to be empty
    username_queue.join()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save available usernames to a file
    if available_usernames:
        with open('available_usernames.txt', 'w') as file:
            for username in available_usernames:
                file.write(f"{username}\n")
        print("Available usernames saved to available_usernames.txt")

if __name__ == "__main__":
    main()
