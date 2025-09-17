# LaZ3 Solving

A different paradigm of solving problems with huge search space where writing the algorithm is not trivial.  
Proof driven to guarantee that no bad case exists. When you may need to generate tricky input automatically.

## Problems
Some problems are too basic to use z3 solvers but good starting point to understand and learn z3. Some problems are complex using standard algos but are best candidates based on search space.

**Wrong problems but to learn better**  
* [Two sum](/laz3solving/problems/twosum.py)

**Right problems but complex algorithmic solution**
* [Subset sum](/laz3solving/problems/subsetsum.py)
* [Coin Change](/laz3solving/problems/coinchange.py)


## Solvers setup and run
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Setup environment `uv sync`
3. Run problems using any of the way below
```bash
# As a module
uv run -m laz3solving.problems.twosum 
uv run laz3 # run all problems
uv run laz3 twosum # run single file twosum.py
```
4. Add a new problem solver with just `@solver` annotation and `run_solvers` with examples

## Resources
[Z3 Solver Paper](https://link.springer.com/content/pdf/10.1007/978-3-540-78800-3_24.pdf)  
[Dumb Intro to Z3](https://asibahi.github.io/thoughts/a-gentle-introduction-to-z3/)

## Change Log

### 2025/09/16 
- Came after this from a hackernews post talking their experience solving complex algo problems without writing complex logic, edge cases and ideas.
- Trying to understand the paradigm using standard software engineering and computer science mindset.
- First set of three problems, 1 - CS simple but not Z3 candidate, 2 - CS complex but perfect Z3 candidate