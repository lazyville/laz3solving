# Z3 Solving

A different paradigm of solving problems with huge search space and writing the algorithm is not trivial.  
Also it fairs well when you want to proof that no bad case exists. When you may need to generate tricky input automatically.

## Wrong problems but to learn better
These problems are too basic to use z3 solvers but 
* [Two sum](/problems/twosum.py)

## Right problems but complex algorithmic solution
* [Subset sum](/problems/subsetsum.py)
* [Coin Change](/problems/coinchange.py)


## Setup and run
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Setup environment `uv sync`
3. Run problems `uv run problems/coinchange.py`

## Change Log

### 2025/09/16 
- Came after this from a hackernews post talking their experience solving complex algo problems without writing complex logic, edge cases and ideas.
- Trying to understand the paradigm using standard software engineering and computer science mindset.
- First set of three problems, 1 - CS simple but not Z3 candidate, 2 - CS complex but perfect Z3 candidate