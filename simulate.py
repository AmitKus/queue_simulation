import simpy
import random

def request_generator(env, arrival_rate, server):
    """Generates requests according to a Poisson process."""
    while True:
        yield env.timeout(random.expovariate(arrival_rate))  # Time between arrivals
        env.process(handle_request(env, server))

def handle_request(env, server):
    """Handles a single request."""
    with server.request() as request:
        yield request  # Wait for an available server
        processing_time = random.uniform(1, 5)  # Random processing time between 1 and 5 seconds
        yield env.timeout(processing_time)  # Process the request
        print(f"Request handled at {env.now:.2f} seconds (processing time: {processing_time:.2f}s)")

def main():
    # Parameters
    N = 5  # Number of nodes (servers)
    arrival_rate = 2  # Average number of requests per second

    # Environment and resources
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=N)

    # Start the request generator
    env.process(request_generator(env, arrival_rate, server))

    # Run the simulation for a specified time (e.g., 30 seconds)
    simulation_time = 30
    env.run(until=simulation_time)

if __name__ == "__main__":
    main()
