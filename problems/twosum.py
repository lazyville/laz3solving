from z3 import *

# Z3 solves well when a search space is huge and writing the
# algorithm is non-trivial. Here, we use Z3 to solve a simple
# two-sum problem to solve it but it's not the best tool for this job.


# Problem: Given a list of numbers and a target, find two numbers that add up to the target.
# Example: nums = [1, 3, 9, 11, 16, 15, 20], target = 25
# Output: (9, 16) because 9 + 16 = 25

def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


def two_sum_z3(nums, target):
    # Declare vars -> Add Constraints -> Solve
    # Z3 Variables
    i, j = Ints('i j')
    s = Solver()
    A = Array('A', IntSort(), IntSort())

    for idx, val in enumerate(nums):
        s.add(Select(A, idx) == val)

    # Add constraints
    s.add(i >= 0, i < len(nums))
    s.add(j >= 0, j < len(nums))
    s.add(i < j)
    s.add(Select(A, i) + Select(A, j) == target)

    # Solve the constraints
    if s.check() == sat:
        m = s.model()
        return (m[i].as_long(), m[j].as_long())
    else:
        print("No solution found")
        return None


# Example usage
nums = [1, 3, 9, 11, 14, 15, 20]
target = 25

print('Solving Two Sum Problem using Z3:')
result = two_sum_z3(nums, target)
if result:
    i, j = result
    print(f"Indices: {i}, {j}")
    print(
        f"Numbers: {nums[i]}, {nums[j]}, because {nums[i]} + {nums[j]} = {target}")
else:
    print("No solution found")
