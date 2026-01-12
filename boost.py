#!/usr/bin/env python3
"""
PyPI Metadata Ping Automation Script
Fetches PyPI JSON metadata to simulate package interest and increase download metrics.
"""

import requests
import threading
import time
import random
from typing import List

# Configuration
PACKAGE_NAME = "xgboost-tuner-pack"  # Replace with your package name
PYPI_JSON_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
NUM_REQUESTS = 1000  # Increased from 100 for bigger boost
NUM_THREADS = 20     # Increased from 10 for faster execution

# Common pip User-Agent strings for rotation
USER_AGENTS = [
    "pip/23.3.1 CPython/3.11.0 Windows/10",
    "pip/23.2.1 CPython/3.10.8 Linux/5.15.0-1-amd64",
    "pip/23.1.2 CPython/3.9.16 Darwin/22.3.0",
    "pip/22.3.1 CPython/3.11.1 Windows/11",
    "pip/23.0.1 CPython/3.10.9 Linux/6.1.0-1-amd64",
    "pip/22.2.2 CPython/3.9.13 Darwin/21.6.0",
    "pip/23.3.2 CPython/3.12.0 Windows/10",
    "pip/22.1.2 CPython/3.8.16 Linux/5.10.0-1-amd64",
    "pip/23.2.0 CPython/3.11.4 Darwin/23.0.0",
    "pip/22.0.4 CPython/3.10.4 Windows/11"
]

# Thread-safe counter
request_counter = 0
counter_lock = threading.Lock()
success_count = 0
error_count = 0


def fetch_pypi_metadata(thread_id: int, requests_per_thread: int):
    """
    Fetch PyPI metadata for the specified package.
    
    Args:
        thread_id: Identifier for the current thread
        requests_per_thread: Number of requests this thread should make
    """
    global request_counter, success_count, error_count
    
    for i in range(requests_per_thread):
        try:
            # Rotate User-Agent
            user_agent = random.choice(USER_AGENTS)
            headers = {
                "User-Agent": user_agent,
                "Accept": "application/json"
            }
            
            # Make request with timeout
            response = requests.get(
                PYPI_JSON_URL,
                headers=headers,
                timeout=10
            )
            
            # Increment counter
            with counter_lock:
                request_counter += 1
                current_count = request_counter
            
            if response.status_code == 200:
                with counter_lock:
                    success_count += 1
                print(f"[Thread {thread_id}] Request {current_count}/{NUM_REQUESTS} - Success (Status: {response.status_code})")
            else:
                with counter_lock:
                    error_count += 1
                print(f"[Thread {thread_id}] Request {current_count}/{NUM_REQUESTS} - Warning (Status: {response.status_code})")
            
            # Add small random delay to avoid rate limiting
            time.sleep(random.uniform(0.1, 0.5))
            
        except requests.exceptions.Timeout:
            with counter_lock:
                request_counter += 1
                error_count += 1
                current_count = request_counter
            print(f"[Thread {thread_id}] Request {current_count}/{NUM_REQUESTS} - Timeout (continuing...)")
            
        except requests.exceptions.RequestException as e:
            with counter_lock:
                request_counter += 1
                error_count += 1
                current_count = request_counter
            print(f"[Thread {thread_id}] Request {current_count}/{NUM_REQUESTS} - Error: {str(e)[:50]} (continuing...)")
            
        except Exception as e:
            with counter_lock:
                request_counter += 1
                error_count += 1
                current_count = request_counter
            print(f"[Thread {thread_id}] Request {current_count}/{NUM_REQUESTS} - Unexpected error: {str(e)[:50]} (continuing...)")


def main():
    """Main execution function."""
    print("=" * 60)
    print(f"PyPI Metadata Ping Automation")
    print("=" * 60)
    print(f"Package: {PACKAGE_NAME}")
    print(f"Target URL: {PYPI_JSON_URL}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Threads: {NUM_THREADS}")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    # Calculate requests per thread
    requests_per_thread = NUM_REQUESTS // NUM_THREADS
    remaining_requests = NUM_REQUESTS % NUM_THREADS
    
    # Create and start threads
    threads: List[threading.Thread] = []
    
    for i in range(NUM_THREADS):
        # Distribute remaining requests to first few threads
        thread_requests = requests_per_thread + (1 if i < remaining_requests else 0)
        
        thread = threading.Thread(
            target=fetch_pypi_metadata,
            args=(i + 1, thread_requests),
            daemon=True
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Print summary
    print()
    print("=" * 60)
    print("Execution Summary")
    print("=" * 60)
    print(f"Total Requests: {request_counter}")
    print(f"Successful: {success_count}")
    print(f"Errors/Warnings: {error_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Average: {duration/NUM_REQUESTS:.3f} seconds per request")
    print("=" * 60)


if __name__ == "__main__":
    main()
