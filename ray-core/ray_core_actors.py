# An actor is essentially a stateful worker (or a service). When a new actor is instantiated, 
# a new worker is created, and methods of the actor are scheduled on that specific worker

import ray
import time
import asyncio

@ray.remote
class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
        return self.value

    def get_counter(self):
        return self.value

# Create an actor from this class
counter = Counter.remote()

# Specify required resources for an actor.
@ray.remote(num_cpus=2, num_gpus=0.5)
class Actor:
    pass

# Call the actor.
obj_ref = counter.increment.remote()
print(ray.get(obj_ref))

# Create ten Counter actors.
counters = [Counter.remote() for _ in range(10)]

# Increment each Counter once and get the results. These tasks all happen in
# parallel.
results = ray.get([c.increment.remote() for c in counters])
print(results)

# Increment the first Counter five times. These tasks are executed serially
# and share state.
results = ray.get([counters[0].increment.remote() for _ in range(5)])
print(results)

# Passing Around Actor Handles
@ray.remote
def f(counter):
    for _ in range(10):
        time.sleep(0.1)
        counter.increment.remote()

# If we instantiate an actor, we can pass the handle around to various tasks.
counter = Counter.remote()

# Start some tasks that use the actor.
[f.remote(counter) for _ in range(3)]

# Print the counter value.
for _ in range(10):
    time.sleep(0.1)
    print(ray.get(counter.get_counter.remote()))

# Cancelling Actor Tasks
# Cancel Actor Tasks by calling ray.cancel() on the returned ObjectRef.

@ray.remote
class Actor:
    async def f(self):
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            print("Actor task canceled.")


actor = Actor.remote()
ref = actor.f.remote()

# Wait until task is scheduled.
time.sleep(1)
ray.cancel(ref)

try:
    ray.get(ref)
except ray.exceptions.RayTaskError:
    print("Object reference was cancelled.")


# AsyncIO for Actors 
@ray.remote
class AsyncActor:
    # multiple invocation of this method can be running in
    # the event loop at the same time
    async def run_concurrent(self):
        print("started")
        await asyncio.sleep(2) # concurrent workload here
        print("finished")

actor = AsyncActor.remote()

# regular ray.get
ray.get([actor.run_concurrent.remote() for _ in range(4)])

# async ray.get
async def async_get():
    await actor.run_concurrent.remote()
asyncio.run(async_get())


try:
    input("Press enter to continue")
except SyntaxError:
    pass
