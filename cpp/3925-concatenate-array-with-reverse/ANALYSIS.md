# Arrays & Hashing

## Video Solution

For more details about **Concatenate Array With Reverse**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=K8ZD6UwIO84).

## Concept

The task is to create a new array that first contains the original elements in order, followed by the same elements in reverse order. Think of it like taking a deck of cards, laying them out face‑up from left to right, then laying the same deck again face‑up but from right to left. The result is a sequence that reads forward then backward.

## When to Use It

Use this pattern when you need to:
- Duplicate a sequence and append its reverse (palindrome‑like constructions).
- Build an array that is symmetric around its center.
- Problems that explicitly ask for “original + reversed” or “concat with reverse”.

## Template

```python
def concat_with_reverse(nums):
    """
    Returns a new list: original nums followed by reversed nums.
    """
    n = len(nums)
    ans = [0] * (2 * n)          # allocate output array
    for i in range(n):
        ans[i] = nums[i]         # copy forward part
        ans[2 * n - 1 - i] = nums[i]   # copy reversed part
    return ans
```

---

## LeetCode Problem Walkthrough

### Problem: 3925. Concatenate Array With Reverse

https://leetcode.com/problems/concatenate-array-with-reverse/

### Approach 1: Brute Force (Two‑Pass)

**Algorithm**
1. Create an empty list `ans`.
2. Iterate through `nums` and append each element to `ans` (forward copy).
3. Iterate through `nums` in reverse order and append each element to `ans`.
4. Return `ans`.

**Implementation**

```python
class Solution:
    def concatenateArrayWithReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        ans = []
        # forward copy
        for x in nums:
            ans.append(x)
        # reverse copy
        for x in reversed(nums):
            ans.append(x)
        return ans
```

**Complexity Analysis**
- Time complexity: O(n) — we traverse the list twice (still linear).
- Space complexity: O(n) — the output array of size 2n (ignoring output, auxiliary space is O(1)).

### Approach 2: Single‑Pass with Pre‑allocated Array

**Intuition**
Instead of two separate loops, we can fill the output array in one pass by placing the forward element at index `i` and the mirrored element at index `2n‑1‑i`. This reduces loop overhead and avoids calling `reversed`.

**Algorithm**
1. Let `n = len(nums)`. Allocate `ans` of size `2n`.
2. For each index `i` from `0` to `n‑1`:
   - Set `ans[i] = nums[i]` (forward copy).
   - Set `ans[2*n - 1 - i] = nums[i]` (reverse copy).
3. Return `ans`.

**Implementation**

```python
class Solution:
    def concatenateArrayWithReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        n = len(nums)
        ans = [0] * (2 * n)
        for i in range(n):
            ans[i] = nums[i]
            ans[2 * n - 1 - i] = nums[i]
        return ans
```

**Complexity Analysis**
- Time complexity: O(n) — single loop over `n` elements.
- Space complexity: O(n) — output array; auxiliary space O(1).

### Approach 3: Pythonic One‑Liner (Using List Concatenation)

**Intuition**
Python lets us concatenate lists directly. The reversed list can be obtained with slicing `nums[::-1]`. This approach is concise and leverages built‑in optimizations.

**Algorithm**
1. Return `nums + nums[::-1]`.

**Implementation**

```python
class Solution:
    def concatenateArrayWithReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        return nums + nums[::-1]
```

**Complexity Analysis**
- Time complexity: O(n) — slicing creates a reversed copy (O(n)) and concatenation copies both lists (O(n)).
- Space complexity: O(n) — output array; the temporary reversed slice also uses O(n) auxiliary space.

---

## Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

### Dry Run

Input: `nums = [1, 2, 3]`, `n = 3`

We'll trace Approach 2 (single‑pass pre‑allocated).

```
| Step | i | nums[i] | ans before assignment          | ans after ans[i] = nums[i] | ans after ans[2n-1-i] = nums[i] |
|------|---|---------|--------------------------------|----------------------------|---------------------------------|
| Init |   |         | [0, 0, 0, 0, 0, 0]             |                            |                                 |
| 1    | 0 | 1       | [0, 0, 0, 0, 0, 0]             | [1, 0, 0, 0, 0, 0]         | [1, 0, 0, 0, 0, 1]              |
| 2    | 1 | 2       | [1, 0, 0, 0, 0, 1]             | [1, 2, 0, 0, 0, 1]         | [1, 2, 0, 0, 2, 1]              |
| 3    | 2 | 3       | [1, 2, 0, 0, 2, 1]             | [1, 2, 3, 0, 2, 1]         | [1, 2, 3, 3, 2, 1]              |
Final ans = [1, 2, 3, 3, 2, 1]
```

The table shows how each iteration fills both the forward and symmetric positions, producing the required concatenated‑plus‑reversed array.