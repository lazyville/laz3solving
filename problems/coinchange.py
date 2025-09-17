# Coin change problem
from z3 import *
from functools import wraps
import timeit
from func_timeout import func_timeout, FunctionTimedOut
# Problem: Given a list of coin denominations and a target amount, find the minimum number of coins needed to make that amount.
# Example: coins = [1, 2, 5], amount = 11
# Output: 3 because 11 = 5 + 5 + 1
# Complex Example: coins = [1, 3, 4], amount = 6 ([X, Y, Z] => K; aX+bY+cZ = K)
# Output: 2 because 6 = 3 + 3
# Large Example: coins = [1, 5, 10, 25], amount = 63


def coin_change_decorator(title="Coin Change Solver", timeout=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Running {title}...")
            start_time = timeit.default_timer()
            try:
                result = func_timeout(timeout, func, args=args, kwargs=kwargs)
            except FunctionTimedOut:
                print(
                    f"-> Function {func.__name__} timed out after {timeout} seconds")
                return None
            end_time = timeit.default_timer()
            elapsed_time = end_time - start_time
            if result == -1 or result is None:
                print("No solution found")
            else:
                print(
                    f"-> Result for {func.__name__}, args: {args}, result: {result}. Time taken: {elapsed_time:.6f} seconds")
            return result
        return wrapper
    return decorator


@coin_change_decorator("Backtracking Coin Change Solver")
def coin_change(coins, amount):
    # A simple backtracking approach to find the minimum number of coins
    def backtrack(remaining, count):
        if remaining == 0:
            return count
        if remaining < 0:
            return float('inf')
        min_coins = float('inf')
        for coin in coins:
            res = backtrack(remaining - coin, count + 1)
            min_coins = min(min_coins, res)
        return min_coins
    result = backtrack(amount, 0)
    return result if result != float('inf') else -1


@coin_change_decorator("Dynamic Programming Coin Change Solver")
def coin_change_optimal(coins, amount):
    # A simple dynamic programming approach to find the minimum number of coins
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1


@coin_change_decorator("Z3 SMT Solver Coin Change")
def coin_change_z3(coins, amount):
    # Using Z3 to solve the coin change problem
    n = len(coins)
    # Create a list of integer variables to represent the number of each coin used
    count = [Int(f'x_{i}') for i in range(n)]

    # Create an Optimize instance so we can minimize an objective
    s = Solver()
    o = Optimize()

    # Add constraints: each count[i] must be non-negative
    for i in range(n):
        o.add(count[i] >= 0)

    # Add the constraint that the total amount must equal the target amount
    o.add(Sum([count[i] * coins[i] for i in range(n)]) == amount)

    # Objective: Minimize the total number of coins used
    total_coins = Sum(count)
    h = o.minimize(total_coins)

    # Check if the constraints are satisfiable
    if o.check() == sat:
        m = o.model()
        result = [m.evaluate(count[i]).as_long() for i in range(n)]
        total = sum(result)
        return total
    else:
        return None, -1


def run_coin_solvers(coins, amount):
    print(f"Solving Coin Change Problem for coins={coins} and amount={amount}")
    coin_change(coins, amount)
    coin_change_optimal(coins, amount)
    coin_change_z3(coins, amount)
    print("\n")


# Example usage
run_coin_solvers([1, 2, 5], 11)
run_coin_solvers([1, 3, 4], 6)
run_coin_solvers([1, 5, 10, 25], 63)

"""
Output:
Solving Coin Change Problem for coins=[1, 2, 5] and amount=11
Running Backtracking Coin Change Solver...
-> Result for coin_change, args: ([1, 2, 5], 11), result: 3. Time taken: 0.000794 seconds
Running Dynamic Programming Coin Change Solver...
-> Result for coin_change_optimal, args: ([1, 2, 5], 11), result: 3. Time taken: 0.000171 seconds
Running Z3 SMT Solver Coin Change...
-> Result for coin_change_z3, args: ([1, 2, 5], 11), result: 3. Time taken: 0.071743 seconds


Solving Coin Change Problem for coins=[1, 3, 4] and amount=6
Running Backtracking Coin Change Solver...
-> Result for coin_change, args: ([1, 3, 4], 6), result: 2. Time taken: 0.000366 seconds
Running Dynamic Programming Coin Change Solver...
-> Result for coin_change_optimal, args: ([1, 3, 4], 6), result: 2. Time taken: 0.000355 seconds
Running Z3 SMT Solver Coin Change...
-> Result for coin_change_z3, args: ([1, 3, 4], 6), result: 2. Time taken: 0.005493 seconds


Solving Coin Change Problem for coins=[1, 5, 10, 25] and amount=63
Running Backtracking Coin Change Solver...
-> Function coin_change timed out after 10 seconds
Running Dynamic Programming Coin Change Solver...
-> Result for coin_change_optimal, args: ([1, 5, 10, 25], 63), result: 6. Time taken: 0.000291 seconds
Running Z3 SMT Solver Coin Change...
-> Result for coin_change_z3, args: ([1, 5, 10, 25], 63), result: 6. Time taken: 0.009956 seconds
"""
