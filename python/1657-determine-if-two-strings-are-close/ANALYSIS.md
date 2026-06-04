# Arrays & Hashing

## Video Solution

For more details about **Determine if Two Strings Are Close**, watch the walkthrough at [https://www.youtube.com/watch?v=K8X6bG6Uj2M](https://www.youtube.com/watch?v=K8X6bG6Uj2M).

## Concept

Operation 1 lets us swap any two existing characters. Because we can apply it arbitrarily many times, we can **reorder the characters in any way** we like – the strings become *anagrams* of each other if only this operation were allowed.

Operation 2 lets us pick two distinct characters that both appear in the string and **exchange all of their occurrences**. In other words, we can swap the *frequencies* of any two characters that are present.

Combining both operations, two strings are close **iff**:

1. They contain **exactly the same set of characters** (otherwise we could never create a missing character).
2. The **multiset of their character frequencies** is the same (we can reorder characters freely, and we can swap frequencies between any pair of characters that exist).

Thus the problem reduces to checking:
- `set(word1) == set(word2)`
- `sorted(Counter(word1).values()) == sorted(Counter(word2).values())`

## When to Use It

Use this pattern when a problem describes:
- Unlimited swaps of characters (implies any permutation is possible).
- Operations that exchange whole blocks of identical characters (frequency swapping).
- You need to decide if two strings can be made equal under such flexible transformations.

Typical clues: “swap any two characters”, “transform every occurrence of X into Y”, “only lowercase letters”, length up to 10⁵.

## Template

```python
from collections import Counter

def close_strings(word1: str, word2: str) -> bool:
    # 1️⃣ length check (optional but cheap)
    if len(word1) != len(word2):
        return False

    # 2️⃣ same set of characters?
    if set(word1) != set(word2):
        return False

    # 3️⃣ same multiset of frequencies?
    return sorted(Counter(word1).values()) == sorted(Counter(word2).values())
```

## LeetCode Problem Walkthrough

### Problem: 1657. Determine if Two Strings Are Close

https://leetcode.com/problems/determine-if-two-strings-are-close/

### Approach 1: Brute Force (Conceptual)

**Algorithm**
- Enumerate every possible bijection (one‑to‑one mapping) between the distinct characters of `word1` and those of `word2`.
- For each mapping, apply it to `word1` (renaming characters) and then check if the resulting string can be rearranged to `word2` using only swaps (i.e., compare sorted strings).
- If any mapping works, return `True`; otherwise `False`.

**Why it’s brute force**
- The number of distinct characters can be up to 26, so the number of bijections is `k!` where `k = |set(word1)|`. In the worst case this is factorial time – infeasible for large inputs, but it correctly captures the definition of “close”.

**Implementation** (illustrative, not meant for production)

```python
from itertools import permutations
from collections import Counter

def closeStrings_bruteforce(word1, word2):
    if len(word1) != len(word2):
        return False
    chars1 = list(set(word1))
    chars2 = list(set(word2))
    if set(chars1) != set(chars2):
        return False
    # try every permutation of chars2 as a mapping from chars1
    for perm in permutations(chars2):
        mapping = {c1: c2 for c1, c2 in zip(chars1, perm)}
        transformed = ''.join(mapping[ch] for ch in word1)
        if sorted(transformed) == sorted(word2):
            return True
    return False
```

**Complexity Analysis**
- Time: `O(k! * n log n)` where `k` = number of distinct letters (≤26) and `n` = length of strings. Factorial dominates.
- Space: `O(n)` for the transformed string and counters.

### Approach 2: Optimized with Character Set & Frequency Multiset

**Intuition**
- Because swaps let us reorder arbitrarily, the exact order of characters does not matter – only their counts.
- Because we can swap frequencies of any two existing characters, the *identity* of which character has which count does not matter; only the **multiset** of counts matters.
- Therefore we only need to verify that the two strings share the same character set and the same list of frequencies (order‑independent).

**Algorithm**
1. If lengths differ → return `False`.
2. Compute `Counter` for each string.
3. Ensure the key sets are identical.
4. Compare the sorted lists of frequency values.

**Implementation**

```python
from collections import Counter

class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False

        c1, c2 = Counter(word1), Counter(word2)

        # same set of characters?
        if set(c1.keys()) != set(c2.keys()):
            return False

        # same multiset of frequencies?
        return sorted(c1.values()) == sorted(c2.values())
```

**Complexity Analysis**
- Time: `O(n + C log C)` where `n` is the string length and `C ≤ 26` is the number of distinct characters (sorting a tiny list). Effectively `O(n)`.
- Space: `O(C)` for the counters (constant w.r.t. input size).

### Approach 3: Alternative Using Frequency Buckets

**Intuition**
- Instead of sorting the frequency lists, we can count how many times each frequency occurs (a “frequency of frequencies”) and compare those histograms. This avoids the `O(C log C)` sort and works in linear time relative to the alphabet size.

**Algorithm**
1. Length check.
2. Build two `Counter`s for characters.
3. Verify key sets match.
4. Build a second‑level counter: `freq_cnt1[f] = how many letters appear f times`.
5. Compare the two frequency‑level counters.

**Implementation**

```python
from collections import Counter

class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False

        c1, c2 = Counter(word1), Counter(word2)

        if set(c1.keys()) != set(c2.keys()):
            return False

        freq1 = Counter(c1.values())
        freq2 = Counter(c2.values())
        return freq1 == freq2
```

**Complexity Analysis**
- Time: `O(n)` – one pass to build each counter, plus `O(C)` to build the frequency‑of‑frequency counters.
- Space: `O(C)` – still constant (≤26).

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

#### Dry Run

Take `word1 = "cabbba"`, `word2 = "abbccc"` (example from the statement).

| Step | word1 | word2 | c1 (word1)          | c2 (word2)          | set(c1) == set(c2)? | sorted(c1.values()) | sorted(c2.values()) | equal? |
|------|-------|-------|---------------------|---------------------|---------------------|---------------------|---------------------|--------|
| Init | cabbba| abbccc| {c:1, a:2, b:3}     | {a:1, b:2, c:3}     | True ({a,b,c})      | [1,2,3]             | [1,2,3]             | ✅     |

Since both checks pass, the function returns `True`.

---

**Summary**

- The problem collapses to checking equality of character sets and equality of frequency multisets.
- The optimal solution runs in linear time and constant extra space using Python’s `Counter`.
- Always start with the brute‑force reasoning to appreciate why the optimized conditions are sufficient, then implement the fast version.