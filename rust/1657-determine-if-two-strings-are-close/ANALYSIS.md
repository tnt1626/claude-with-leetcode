```markdown
# Arrays & Hashing

## Video Solution

For more details about **Determine if Two Strings Are Close**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=Y0Znq4i2ZkA).

## Concept

Two strings are *close* if we can make them identical using:
1. **Swap any two existing characters** – this lets us reorder characters arbitrarily, so only the **multiset of characters matters**, not their positions.
2. **Swap all occurrences of two existing characters** – this lets us exchange the frequencies of any two characters that both appear in the string.

Therefore, after any number of operations, a string is characterized by:
- The **set of distinct characters** it contains (which letters appear at least once).
- The **multiset of frequencies** of those characters (how many times each distinct letter occurs), irrespective of which letter has which frequency.

Two strings are close iff:
1. They contain exactly the same set of characters.
2. The sorted list of their character frequencies is identical.

## When to Use It

Use this reasoning when you see problems that:
- Allow arbitrary reordering of characters (swap operation).
- Allow swapping whole character identities (frequency swap).
- Ask whether two strings can be made equal under such operations.
- Involve only lowercase English letters (fixed alphabet size).

## Template

```python
from collections import Counter

def close_strings(word1: str, word2: str) -> bool:
    # 1. Length must match (otherwise frequencies can't match)
    if len(word1) != len(word2):
        return False

    # 2. Count frequencies of each character
    c1 = Counter(word1)
    c2 = Counter(word2)

    # 3. Same set of characters?
    if set(c1.keys()) != set(c2.keys()):
        return False

    # 4. Same multiset of frequencies? (order doesn't matter)
    return sorted(c1.values()) == sorted(c2.values())
```

## LeetCode Problem Walkthrough

### Problem: 1657. Determine if Two Strings Are Close

https://leetcode.com/problems/determine-if-two-strings-are-close/

### Approach 1: Brute Force (by simulating operations)

**Algorithm**
- Repeatedly try to apply the two operations until the strings match or we exhaust possibilities.
- Because the strings can be up to 10⁵ characters, a naive simulation is exponential and infeasible.

**Implementation**

```python
# This is only illustrative; it will time out on large inputs.
from collections import deque

def close_strings_bruteforce(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    visited = set()
    q = deque([word1])
    while q:
        cur = q.popleft()
        if cur == word2:
            return True
        if cur in visited:
            continue
        visited.add(cur)
        # Operation 1: swap any two positions
        lst = list(cur)
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                lst[i], lst[j] = lst[j], lst[i]
                nxt = ''.join(lst)
                if nxt not in visited:
                    q.append(nxt)
                lst[i], lst[j] = lst[j], lst[i]  # revert
        # Operation 2: swap all occurrences of two distinct chars
        chars = list(set(cur))
        for i in range(len(chars)):
            for j in range(i + 1, len(chars)):
                a, b = chars[i], chars[j]
                nxt = cur.replace(a, '_').replace(b, a).replace('_', b)
                if nxt not in visited:
                    q.append(nxt)
    return False
```

**Complexity Analysis**
- Time complexity: O((n²)·states) — each state tries O(n²) swaps and O(α²) character swaps (α ≤ 26); number of states can be huge.
- Space complexity: O(states·n) — to store visited strings and the queue.

### Approach 2: Frequency‑Set Comparison (optimal)

**Intuition**
- Operation 1 lets us reorder arbitrarily → only the multiset of characters matters.
- Operation 2 lets us exchange the frequencies of any two characters that both exist → the *list* of frequencies matters, but not which character owns which frequency.
- Hence we only need to compare (a) the set of distinct characters and (b) the sorted list of their frequencies.

**Algorithm**
1. If lengths differ → return False.
2. Build frequency counters for both strings.
3. Verify the key sets (characters with non‑zero count) are identical.
4. Compare the sorted lists of frequency values.
5. Return True iff both checks pass.

**Implementation**

```python
from collections import Counter

def close_strings(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    cnt1 = Counter(word1)
    cnt2 = Counter(word2)

    # Same set of characters?
    if set(cnt1.keys()) != set(cnt2.keys()):
        return False

    # Same multiset of frequencies?
    return sorted(cnt1.values()) == sorted(cnt2.values())
```

**Complexity Analysis**
- Time complexity: O(n + α log α) → O(n) because counting is linear and sorting at most 26 frequencies is constant.
- Space complexity: O(α) → O(1) extra space (two size‑26 arrays or counters).

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

#### Dry Run

Take the example `word1 = "cabbba"` and `word2 = "abbccc"`.

| Step | word1 frequencies (a,b,c) | word2 frequencies (a,b,c) |
|------|---------------------------|---------------------------|
| Count | a:2, b:3, c:1            | a:1, b:2, c:3            |
| Set of chars | {a,b,c}               | {a,b,c}                 |
| Sorted freqs | [1,2,3]               | [1,2,3]                 |

Since both the character sets and the sorted frequency lists match, the strings are close.

--- 

*End of lecture.*