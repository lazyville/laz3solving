from functools import wraps
import timeit
from func_timeout import func_timeout, FunctionTimedOut

_DECORATED_BY_SOLVER = object()


def is_decorated_by_solver(obj) -> bool:
    # for bound methods, get the underlying function
    f = getattr(obj, "__func__", obj)
    # walk through wrapper chain
    while f is not None:
        if getattr(f, "__decorated_by_solver__", None) is _DECORATED_BY_SOLVER:
            return True
        f = getattr(f, "__wrapped__", None)  # added by functools.wraps
    return False


def solver(title="Lazy Problem Solver", timeout=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Running '{title}'...")
            start_time = timeit.default_timer()
            try:
                result = func_timeout(timeout, func, args=args, kwargs=kwargs)
            except FunctionTimedOut:
                print(
                    f"-> Function '{func.__name__}' timed out after {timeout} seconds")
                return None
            end_time = timeit.default_timer()
            elapsed_time = end_time - start_time
            if result == -1 or result is None:
                print("No solution found")
            else:
                print(
                    f"-> Result for '{func.__name__}', args: {args}, result: {result}. Time taken: {elapsed_time:.6f} seconds")
            return result
        wrapper.__decorated_by_solver__ = _DECORATED_BY_SOLVER
        return wrapper
    return decorator


def run_solvers(*args, **kwargs):
    """Run multiple solver functions with the same arguments and print their results."""
    # Find all solver functions that are decorated with @solver from the module where this function is called
    import inspect
    import sys
    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)
    _title = caller_module.__title__ if hasattr(
        caller_module, '__title__') else caller_module.__name__
    title = kwargs.pop('title', _title)

    solvers = []
    for name, obj in inspect.getmembers(caller_module):
        # check if it's decorated with @solver
        if inspect.isfunction(obj) and is_decorated_by_solver(obj):
            solvers.append(obj)

    if not solvers:
        print("No solver functions found.")
        return

    print(f"===== Running Solvers for : {_title} =====")
    for solver in solvers:
        solver(*args, **kwargs)
    print(f"===== End of {title} =====\n")
