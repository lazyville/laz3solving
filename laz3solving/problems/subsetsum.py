# Subsetsum
__title__ = "Subset sum"
from z3 import *
from ..laz3 import solver, run_solvers


# Problem: Given a list of numbers and a target, find a subset of numbers that add up to the target.
# Example: nums = [3, 34, 4, 12, 5, 2], target = 9
# Output: [4, 5] because 4 + 5 = 9


@solver(title="Backtracking Subset Sum")
def subset_sum(nums, target):
    # A simple backtracking approach to find a subset that sums to the target
    def backtrack(start, current_sum, subset):
        if current_sum == target:
            return subset
        if current_sum > target or start == len(nums):
            return None
        # Include nums[start]
        result = backtrack(start + 1, current_sum +
                           nums[start], subset + [nums[start]])
        if result is not None:
            return result
        # Exclude nums[start]
        return backtrack(start + 1, current_sum, subset)
    return backtrack(0, 0, [])


@solver(title="Dynamic Programming Subset Sum")
def subset_sum_optimal(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if nums[i - 1] <= j:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i - 1]]
            else:
                dp[i][j] = dp[i - 1][j]
    if not dp[n][target]:
        return None
    subset = []
    w = target
    for i in range(n, 0, -1):
        if not dp[i - 1][w]:
            subset.append(nums[i - 1])
            w -= nums[i - 1]
    return subset[::-1]


@solver(title="Z3 SMT Solver Subset Sum")
def subset_sum_z3(nums, target):
    """Solve the subset sum problem using Z3 SMT solver.
    No Loops, no backtracking, just constraints and solving.
    """
    n = len(nums)
    # Create a list of boolean variables to represent whether each number is included in the subset
    pick = [Bool(f'x_{i}') for i in range(n)]

    # Create a solver instance
    s = Solver()

    # Add the constraint that the sum of the selected numbers must equal the target
    # Explanation: If x[i] is True, include nums[i] in the sum; otherwise, include 0
    s.add(Sum([If(pick[i], nums[i], 0) for i in range(n)]) == target)

    # Check if the constraints are satisfiable
    if s.check() == sat:
        m = s.model()
        subset = [nums[i] for i in range(n) if m.evaluate(pick[i])]
        return subset
    else:
        return None


@solver(title="Optimal Z3 SMT Solver Subset Sum")
def subset_sum_z3_optimal(nums, target):
    """Optimal solution with smallest subset using Z3 SMT solver."""
    n = len(nums)
    pick = [Bool(f'x_{i}') for i in range(n)]
    o = Optimize()

    # Add the constraint that the sum of the selected numbers must equal the target
    total = Sum([If(p, nums[i], 0) for i, p in enumerate(pick)])
    count = Sum([If(p, 1, 0) for p in pick])
    o.add(total == target)
    o.minimize(count)
    if o.check() == sat:
        m = o.model()
        subset = [nums[i] for i, p in enumerate(pick) if m.evaluate(p)]
        return subset
    else:
        return None


run_solvers([3, 34, 4, 12, 5, 2], 9)
run_solvers([3, 34, 4, 12, 5, 2, 7, 8, 10, 15, 20, 25], 30)
