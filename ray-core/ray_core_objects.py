import ray
import time

# Get the value of one object ref.
obj_ref = ray.put(1)
assert(ray.get(obj_ref)) == 1

# Get the values of multiple object refs in parallel.
assert ray.get([ray.put(i) for i in range(3)]) == [0, 1, 2]

# You can also set a timeout to return early from a ``get``
# that's blocking for too long.
from ray.exceptions import GetTimeoutError
# ``GetTimeoutError`` is a subclass of ``TimeoutError``.

@ray.remote
def long_running_function():
    time.sleep(8)

obj_ref = long_running_function.remote()
try:
    ray.get(obj_ref, timeout=4)
except GetTimeoutError:  # You can capture the standard "TimeoutError" instead
    print("`get` timed out.")
    

# passing object arguments

@ray.remote
def echo(a: int, b: int, c: int):
    """This function prints its input values to stdout."""
    print(a, b, c)


# Passing the literal values (1, 2, 3) to `echo`.
echo.remote(1, 2, 3)
# -> prints "1 2 3"

# Put the values (1, 2, 3) into Ray's object store.
a, b, c = ray.put(1), ray.put(2), ray.put(3)

# Passing an object as a top-level argument to `echo`. Ray will de-reference top-level
# arguments, so `echo` will see the literal values (1, 2, 3) in this case as well.
echo.remote(a, b, c)
# -> prints "1 2 3"

try:
    input("Press enter to continue")
except SyntaxError:
    pass

