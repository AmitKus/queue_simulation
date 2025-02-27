import simpy
import random
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Global data structures to store metrics
queue_sizes = []
request_timeline = []

def request_generator(env, arrival_rate, server):
    """Generates requests according to a Poisson process."""
    request_id = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))  # Time between arrivals
        request_id += 1
        env.process(handle_request(env, server, request_id))
        queue_sizes.append((env.now, len(server.queue)))

def handle_request(env, server, request_id):
    """Handles a single request."""
    arrival_time = env.now
    with server.request() as request:
        yield request  # Wait for an available server
        start_time = env.now
        processing_time = random.uniform(1, 5)
        yield env.timeout(processing_time)
        end_time = env.now
        
        request_timeline.append({
            'Request': request_id,
            'Start': start_time,
            'End': end_time,
            'Wait': start_time - arrival_time,
            'Processing': processing_time
        })

def plot_metrics():
    # Plot queue size over time
    queue_df = pd.DataFrame(queue_sizes, columns=['Time', 'Queue Size'])
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=queue_df, x='Time', y='Queue Size')
    plt.title('Queue Size Over Time')
    plt.show()

    # Plot Gantt chart
    timeline_df = pd.DataFrame(request_timeline)
    plt.figure(figsize=(12, 6))
    
    # Plot waiting time bars (red)
    for _, row in timeline_df.iterrows():
        plt.barh(y=row['Request'], 
                width=row['Wait'],
                left=row['Start']-row['Wait'],
                color='red')
    
    # Plot processing time bars (green)        
    for _, row in timeline_df.iterrows():
        plt.barh(y=row['Request'],
                width=row['Processing'], 
                left=row['Start'],
                color='green')
    
    plt.title('Request Timeline (Gantt Chart)')
    plt.xlabel('Time')
    plt.ylabel('Request ID')
    plt.show()

def main():
    # Parameters
    N = 5  # Number of nodes (servers)
    arrival_rate = 2  # Average number of requests per second

    # Clear previous data
    queue_sizes.clear()
    request_timeline.clear()

    # Environment and resources
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=N)

    # Start the request generator
    env.process(request_generator(env, arrival_rate, server))

    # Run the simulation for a specified time (e.g., 30 seconds)
    simulation_time = 30
    env.run(until=simulation_time)

    # Plot the results
    plot_metrics()

if __name__ == "__main__":
    main()
