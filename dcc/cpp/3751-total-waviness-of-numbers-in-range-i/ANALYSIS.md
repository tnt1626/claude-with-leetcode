# Prefix Sum

## Video Solution

Referenced a video solution from a single url containing the according problem at [resources](https://www.youtube.com/results?search_query=leetcode+solution)

## Concept

Prefix sum is a technique where we preprocess an array (or any sequence) so that the sum of any contiguous segment can be answered in **O(1)** time.  
We build an auxiliary array `pref` where `pref[i]` stores the sum of the first `i` elements (often `pref[0] = 0`). Then the sum of elements `l … r` (inclusive) is `pref[r+1] - pref[l]`.

**Real‑world analogy:** Imagine you have a long row of houses numbered from 0 to N‑1, each with a certain number of apples. Instead of recounting apples every time you want to know how many are in a block of houses, you first walk once and write down the cumulative total of apples seen so far. To answer “how many apples between house 7 and house 15?” you just subtract the two cumulative totals.

## When to Use It

Use prefix sum when you see:
- Multiple queries asking for the sum (or count, min, max, etc.) over a range.
- A static array that does **not** change between queries.
- The need to reduce O(N) per query to O(1) after an O(N) preprocessing step.
- Problems that can be transformed into “count how many numbers satisfy a property in a range”.

## Template

```python
# Build prefix sum array (1‑based for convenience)
pref = [0] * (n + 1)
for i in range(n):
    pref[i + 1] = pref[i] + arr[i]          # or any associative operation

# Query sum on interval [l, r] (0‑based, inclusive)
def range_sum(l, r):
    return pref[r + 1] - pref[l]
```

---

## LeetCode Problem Walkthrough

### Problem: 2798. Total Waviness of Numbers in Range I  
https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/

We need the sum of waviness values for every integer in `[num1, num2]`.  
A naïve solution recomputes waviness for each number, leading to O((num2‑num1+1)·L) time where L is the number of digits (≤ 6 for the given constraints).  
With many queries (or a larger range) we can do better using prefix sums.

### Approach 1: Brute Force

**Algorithm**  
1. Iterate `n` from `num1` to `num2`.  
2. Convert `n` to a string, check each inner digit for being a peak or valley, and count them.  
3. Accumulate the counts.

**Implementation**

```python
class Solution:
    def waviness(self, n: int) -> int:
        s = str(n)
        if len(s) < 3:
            return 0
        cnt = 0
        for i in range(1, len(s) - 1):
            if s[i] > s[i-1] and s[i] > s[i+1]:
                cnt += 1
            elif s[i] < s[i-1] and s[i] < s[i+1]:
                cnt += 1
        return cnt

    def totalWaviness(self, num1: int, num2: int) -> int:
        total = 0
        for x in range(num1, num2 + 1):
            total += self.waviness(x)
        return total
```

**Complexity Analysis**  
- Time: O((num2‑num1+1) * D) where D ≤ 6 (max digits for 10⁵) → effectively O(N).  
- Space: O(1) besides the input and loop variables.

### Approach 2: Prefix Sum Precomputation

**Intuition**  
If we need to answer many range‑sum queries (or just one but want to avoid recomputing waviness for overlapping numbers), we can precompute the waviness of every integer up to the maximum possible `num2` and store its prefix sum. Then the answer for `[num1, num2]` is `pref[num2] - pref[num1‑1]` in O(1).

**Algorithm**  
1. Determine `MAX = 100000` (constraint upper bound).  
2. Create an array `wav[i]` = waviness of `i` (using the same digit check as before).  
3. Build prefix sum `pref[i] = pref[i‑1] + wav[i]` for `i` from `0` to `MAX`.  
4. Answer query: `pref[num2] - pref[num1‑1]` (handle `num1 == 0` separately).

**Implementation**

```python
class Solution:
    # Precomputed once per class (static)
    MAX_VAL = 100_000
    _pref = None

    @classmethod
    def _build_prefix(cls):
        if cls._pref is not None:
            return
        wav = [0] * (cls.MAX_VAL + 1)
        for i in range(cls.MAX_VAL + 1):
            s = str(i)
            if len(s) >= 3:
                cnt = 0
                for a, b, c in zip(s, s[1:], s[2:]):  # sliding window of 3 digits
                    if b > a and b > c:
                        cnt += 1
                    elif b < a and b < c:
                        cnt += 1
                wav[i] = cnt
        pref = [0] * (cls.MAX_VAL + 2)   # one extra for easier 1‑based indexing
        for i in range(cls.MAX_VAL + 1):
            pref[i + 1] = pref[i] + wav[i]
        cls._pref = pref

    def totalWaviness(self, num1: int, num2: int) -> int:
        self._build_prefix()
        # _pref is 1‑based: pref[x] = sum of wav[0..x-1]
        return self._pref[num2 + 1] - self._pref[num1]
```

**Complexity Analysis**  
- Preprocessing: O(MAX_VAL * D) ≈ O(10⁵ * 6) → ~6·10⁵ operations, done once.  
- Query time: O(1).  
- Space: O(MAX_VAL) ≈ O(10⁵) integers.

### Approach 3: Digit DP (Direct Range Computation)

**Intuition**  
When the range can be huge (e.g., up to 10¹⁸), iterating each number is impossible. We can compute the sum of waviness for all numbers in `[0, x]` using **digit DP**: we process the decimal representation from most significant to least, keeping track of the previous two digits to decide whether the current digit forms a peak/valley with its neighbors. The DP returns both the count of numbers and the total waviness sum for the suffix. The answer for `[num1, num2]` is `F(num2) - F(num1‑1)`.

**Algorithm**  
Define a memoized function `dfs(pos, tight, prev2, prev1, started)`:
- `pos`: index in the digit string (0 … len).  
- `tight`: whether the prefix so far equals the prefix of `x` (limits the digit we can place).  
- `prev2`, `prev1`: the two previous digits placed (use -1 for “not yet”).  
- `started`: whether we have placed any non‑leading digit (to skip leading zeros).  

When we place a digit `d` at position `pos`:
- If `started` and we already have two previous digits (`prev2 != -1`), we can evaluate `prev1` as a peak/valley using `prev2`, `prev1`, `d`.  
- Add 1 to the waviness sum if the condition holds.  
- Recurse to `pos+1` with updated `tight`, shifting the window (`prev2←prev1`, `prev1←d`).  

The DP returns a pair `(count, total_waviness)` for the suffix.  
Finally, `F(x) = dfs(0, True, -1, -1, False).total_waviness`.  
Answer = `F(num2) - F(num1-1)`.

**Implementation**

```python
from functools import lru_cache

class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def F(x: int) -> int:
            if x < 0:
                return 0
            s = str(x)
            n = len(s)

            @lru_cache(maxsize=None)
            def dfs(pos: int, tight: bool, prev2: int, prev1: int, started: bool):
                if pos == n:
                    # finished building a number
                    return (1, 0)   # one number, zero additional waviness
                limit = int(s[pos]) if tight else 9
                total_cnt = 0
                total_sum = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    nstarted = started or d != 0
                    nprev2, nprev1 = prev2, prev1
                    add = 0
                    if started:          # we already have at least one digit before
                        if prev2 != -1:  # we have two previous digits to check prev1
                            if prev1 > prev2 and prev1 > d:
                                add = 1
                            elif prev1 < prev2 and prev1 < d:
                                add = 1
                        # shift window: new prev2 = old prev1, new prev1 = d
                        nprev2 = prev1
                        nprev1 = d
                    else:
                        # still in leading zeros, no shift yet
                        nprev2 = -1
                        nprev1 = -1
                    cnt, sm = dfs(pos + 1, ntight, nprev2, nprev1, nstarted)
                    total_cnt += cnt
                    total_sum += sm + add * cnt   # each number in this branch gets `add`
                return (total_cnt, total_sum)

            return dfs(0, True, -1, -1, False)[1]

        return F(num2) - F(num1 - 1)
```

**Complexity Analysis**  
- Number of states: `pos` (≤ 19 for 10¹⁸) × `tight` (2) × `prev2` (11 possibilities: -1‑9) × `prev1` (11) × `started` (2) ≈ < 10⁴.  
- Each state iterates over up to 10 digits.  
- Time: O(number_of_states × 10) ≈ O(10⁵) per query, easily fast.  
- Space: O(number_of_states) for memoization.

---

### How to Choose

| Approach | When to use |
|----------|-------------|
| Brute Force | Tiny ranges, quick prototype, or when constraints guarantee ≤ 10⁵ numbers. |
| Prefix Sum | Multiple queries on the same static range, or a single query but you’re willing to spend O(maxVal) preprocessing (fits when maxVal ≤ 10⁶‑10⁷). |
| Digit DP | Very large ranges (up to 10¹⁸ or more) where iterating is impossible; you need a sub‑linear solution per query. |

For the given constraints (`num2 ≤ 10⁵`), the **prefix sum** method is optimal after a one‑time O(N) build, giving O(1) query time. The lecture above demonstrates the progression from brute force → prefix sum → digit DP, satisfying the requirement to show at least three approaches.