import ray

ray.init()

# Show the ray cluster resources
print(ray.cluster_resources())

# Running a task
@ray.remote
def square(x):
    return x*x

# launch four parallel square tasks
futures = [square.remote(i) for i in range(4)]

# Retrieve results
print(ray.get(futures))

# Calling an Actor
# define the Counter actor
@ray.remote
class Counter:
    def __init__(self):
        self.i = 0
        
    def get(self):
        return self.i

    def incr(self, value):
        self.i += value

# # Create a Counter actor.
c = Counter.remote()

# Submit calls to the actor. These calls run asynchronously but in
# submission order on the remote actor process.
for _ in range(10):
    c.incr.remote(1)

# Retrieve final actor state
print(ray.get(c.get.remote()))
