import simpy


class Process:
    def __init__(self, env, pid, neighbors):
        self.env = env
        self.pid = pid
        self.neighbors = neighbors
        self.seen_message = False
        self.inbox = simpy.Store(env)
        env.process(self.run())

    def send(self, message):
        for neighbor in self.neighbors:
            neighbor.inbox.put((self.pid, message))

    def run(self):
        while True:
            sender, message = yield self.inbox.get()
            if not self.seen_message:
                self.seen_message = True
                print(f"Time {self.env.now}: Process {self.pid} received message from {sender}")
                self.send(message)


# Simulation setup
def simulate_broadcast(num_processes, edges, source):
    env = simpy.Environment()
    processes = {}

    # Create processes
    for i in range(num_processes):
        processes[i] = Process(env, i, [])

    # Establish neighbors
    for a, b in edges:
        processes[a].neighbors.append(processes[b])
        processes[b].neighbors.append(processes[a])

    # Start broadcast from source
    env.process(initial_broadcast(env, processes[source]))
    env.run()


# Initial broadcast trigger
def initial_broadcast(env, source_process):
    yield env.timeout(0)
    source_process.seen_message = True
    print(f"Time {env.now}: Process {source_process.pid} initiates broadcast")
    source_process.send("Message")


# Example usage
graph_edges = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 4), (0, 6), (1, 5), (6, 7), (7, 4)]
simulate_broadcast(8, graph_edges, source=7)
