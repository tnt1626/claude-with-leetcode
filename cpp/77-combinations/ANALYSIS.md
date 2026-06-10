# Backtracking

## Video Solution

For more details about **Combinations**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=q0s6m7AiM7o).

## Concept

Backtracking is a systematic way to iterate through all possible configurations of a search space. We build candidates incrementally and abandon a candidate ("backtrack") as soon as we determine it cannot possibly lead to a valid solution. For generating combinations, we recursively pick numbers, ensuring we never reuse a number and that the picked numbers are in increasing order to avoid duplicates.

## When to Use It

Use backtracking when you see:
- “All possible …” (combinations, permutations, subsets)
- Need to explore a tree/graph of choices where each choice leads to further sub‑choices
- Constraints are small enough that exponential exploration is feasible (here n ≤ 20)

## Template

```python
def backtrack(state, start):
    # state: current partial solution (list)
    if is_complete(state):
        record_solution(state)
        return

    for i in range(start, n_candidates + 1):
        # choose i
        state.append(i)
        # explore further with next start = i + 1 (to keep order)
        backtrack(state, i + 1)
        # undo choice
        state.pop()
```

The loop bound can be tightened with pruning when we know how many more elements are still needed.

## LeetCode Problem Walkthrough

### Problem: 77. Combinations

https://leetcode.com/problems/combinations/

### Approach 1: Brute Force Backtracking

**Algorithm**
1. Start with an empty temporary list `path`.
2. From a given `start` value (initially 1), try every number `i` from `start` to `n`.
3. Append `i` to `path` and recursively call the function with `start = i + 1`.
4. When `path` reaches length `k`, add a copy of `path` to the result.
5. Backtrack by removing the last element and try the next candidate.

**Implementation**

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        path = []

        def backtrack(start: int):
            # If we have k numbers, record the combination
            if len(path) == k:
                res.append(path.copy())
                return
            # Try every possible next number
            for i in range(start, n + 1):
                path.append(i)          # choose i
                backtrack(i + 1)        # explore further
                path.pop()              # undo choice

        backtrack(1)
        return res
```

**Complexity Analysis**
- Time complexity: O(k * C(n, k)) — each valid combination of length k is built once, and copying it costs O(k).
- Space complexity: O(k) — recursion depth plus the temporary `path` (output not counted).

### Approach 2: Pruned Backtracking (Optimized Loop Bound)

**Intuition**
When we still need `remaining = k - len(path)` numbers, picking a number `i` that leaves fewer than `remaining` numbers afterwards can never succeed. We can stop the loop early: the largest viable start is `n - remaining + 1`. This cuts useless branches without affecting correctness.

**Algorithm**
Same as brute force, but the for‑loop runs from `start` to `n - (k - len(path)) + 1` inclusive.

**Implementation**

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        path = []

        def backtrack(start: int):
            if len(path) == k:
                res.append(path.copy())
                return
            # Numbers left to pick
            remaining = k - len(path)
            # The last possible value we can start from
            for i in range(start, n - remaining + 2):
                path.append(i)
                backtrack(i + 1)
                path.pop()

        backtrack(1)
        return res
```

**Complexity Analysis**
- Time complexity: O(k * C(n, k)) — we still generate every valid combination, but we avoid exploring dead branches.
- Space complexity: O(k) — recursion stack and temporary list.

### Approach 3: Bitmask Iteration

**Intuition**
Each combination of size `k` from `[1..n]` can be represented by an `n`‑bit mask where exactly `k` bits are set. Enumerating all masks from `0` to `2^n‑1` and selecting those with popcount == k yields all combinations. This approach avoids recursion and uses simple bit operations.

**Algorithm**
1. Iterate `mask` from `0` to `(1 << n) - 1`.
2. If `mask` has exactly `k` set bits, build the combination by checking which positions are set.
3. Append the built list to the result.

**Implementation**

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        limit = 1 << n          # 2^n

        for mask in range(limit):
            # fast popcount check
            if bin(mask).count('1') != k:
                continue
            comb = []
            for i in range(n):
                if mask & (1 << i):
                    comb.append(i + 1)   # numbers are 1‑based
            res.append(comb)
        return res
```

**Complexity Analysis**
- Time complexity: O(2^n * n) — we examine every mask and, for each, scan up to n bits.
- Space complexity: O(k) for each temporary combination (output not counted).  
  (When n is 20, 2^n ≈ 1 M, still acceptable.)

## Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

### Dry Run

Input: n = 4, k = 2  

We trace the pruned backtracking (Approach 2).

```
| Step | start | path before loop | i (chosen) | path after push | remaining needed | next start |
|------|-------|------------------|------------|-----------------|------------------|------------|
| 1    | 1     | []               | 1          | [1]             | 1                | 2          |
| 2    | 2     | [1]              | 2          | [1,2]           | 0 (k reached)    | -> record  |
| 3    | 2     | [1]              | 3          | [1,3]           | 0                | -> record  |
| 4    | 2     | [1]              | 4          | [1,4]           | 0                | -> record  |
| 5    | 1     | []               | 2          | [2]             | 1                | 3          |
| 6    | 3     | [2]              | 3          | [2,3]           | 0                | -> record  |
| 7    | 3     | [2]              | 4          | [2,4]           | 0                | -> record  |
| 8    | 1     | []               | 3          | [3]             | 1                | 4          |
| 9    | 4     | [3]              | 4          | [3,4]           | 0                | -> record  |
|10    | 1     | []               | 4          | [4]             | 1                | 5 (loop ends) |
```

The recorded combinations, in order, are:
`[1,2] [1,3] [1,4] [2,3] [2,4] [3,4]`, matching the expected output.  

Each leaf where `len(path) == k` corresponds to a valid combination. The pruning condition `i ≤ n - remaining + 1` prevents exploring paths like starting with `4` when we still need two numbers (since only `4` remains).