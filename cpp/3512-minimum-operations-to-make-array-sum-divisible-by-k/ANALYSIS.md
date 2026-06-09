# Arrays & Hashing

## Video Solution

For more details about **Minimum Operations to Make Array Sum Divisible by K**, watch the walkthrough at [https://www.youtube.com/watch?v=BzgZ777a6MU](https://www.youtube.com/watch?v=BzgZ777a6MU)

## Concept

The only allowed operation is decreasing an element by 1. Each operation reduces the total sum of the array by exactly 1. Therefore, to make the sum divisible by k we only need to know how far the current sum is from the nearest multiple of k that is **not greater** than the sum. That distance is simply `sum % k`. If the remainder is 0, no operations are needed; otherwise we must subtract that remainder from the sum, which requires exactly that many decrement operations.

## When to Use It

Use this simple remainder‑based reasoning when you see:
- A problem that asks for the **minimum number of ±1‑style operations** to achieve a divisibility condition.
- The operation changes a global quantity (like sum) by a fixed amount each time.
- Constraints are small enough that a direct formula exists (no need for DP or complex data structures).

## Template

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        # 1. Compute the total sum of the array.
        total = sum(nums)
        # 2. The answer is how much we need to subtract to reach the previous multiple of k.
        return total % k
```

## LeetCode Problem Walkthrough

### Problem: 3512. Minimum Operations to Make Array Sum Divisible by K

https://leetcode.com/problems/minimum-operations-to-make-array-sum-divisible-by-k/

### Approach 1: Brute‑Force Simulation (Conceptual)

**Algorithm**
- Repeatedly pick any index and decrement its value by 1.
- After each decrement, check if the current sum is divisible by k.
- Stop when the condition is met and count the number of performed decrements.

This approach is only for illustration; it would be far too slow for the given limits because the sum can be as large as 10⁶.

**Implementation**

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        total = sum(nums)
        ops = 0
        while total % k != 0:          # keep going until divisible
            # Decrement any element (e.g., the first one) – the choice does not matter.
            nums[0] -= 1
            total -= 1
            ops += 1
        return ops
```

**Complexity Analysis**
- Time complexity: O(total sum) – each iteration reduces the sum by 1, worst‑case up to 10⁶ steps.
- Space complexity: O(1) – only a few integer variables are used.

### Approach 2: Direct Remainder Calculation (Optimal)

**Intuition**
Each operation reduces the sum by exactly 1. To reach the nearest multiple of k that is ≤ sum we need to subtract exactly `sum % k`. No smarter selection of indices can do better because every operation contributes the same −1 to the sum.

**Algorithm**
1. Compute `total = sum(nums)`.
2. Return `total % k` as the minimal number of required decrements.

**Implementation**

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        total = sum(nums)          # Step 1: aggregate the array
        return total % k           # Step 2: distance to previous multiple of k
```

**Complexity Analysis**
- Time complexity: O(n) – one pass to compute the sum, where n = len(nums) ≤ 1000.
- Space complexity: O(1) – only the accumulator variable is used.

### Approach 3: Alternative View – Modular Arithmetic

**Intuition**
The problem asks for the smallest non‑negative integer x such that `(sum - x) % k == 0`. Solving the congruence gives `x ≡ sum (mod k)`, and the minimal x in `[0, k-1]` is exactly `sum % k`. This reinforces why the direct remainder works.

**Algorithm**
Identical to Approach 2; presented here to emphasize the modular‑equivalence perspective.

**Implementation**

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(nums) % k
```

**Complexity Analysis**
- Time complexity: O(n)
- Space complexity: O(1)

--- 

**Key Takeaway:** When each operation changes a global metric by a fixed amount, the answer often reduces to a simple modular arithmetic computation—no need for elaborate data structures or dynamic programming.