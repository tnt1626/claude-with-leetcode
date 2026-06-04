**Git Commit:** `main`  
**Lecture File:** `/lectures/arrays-hashing/2025-09-26-arrays-hashing.md`  

---  

# Arrays & Hashing  

## Video Solution  

For more details about **Determine if Two Strings Are Close**, watch the walkthrough at  
[https://www.youtube.com/watch?v=Y5v3cJ6kZ8U](https://www.youtube.com/watch?v=Y5v3cJ6kZ8U)  

---  

## Concept  

*Operation 1* lets you **reorder** the characters arbitrarily (any permutation).  
*Operation 2* lets you **swap the frequencies** of two characters that both already appear in the string.  

Therefore two strings are *close* iff  

1. they have the **same length** (otherwise you can never match counts),  
2. they contain **exactly the same set of distinct characters** (otherwise a character would have to appear/disappear, which neither operation allows), and  
3. the **multiset of frequencies** of those characters is the same (you can redistribute frequencies among the existing characters via operation 2).  

If the three conditions hold, you can first reorder to line up characters, then swap frequencies to match the target counts.  

---  

## When to Use It  

Use this pattern when a problem talks about:  

* Transforming one string into another by **rearranging** characters.  
* **Swapping counts** of characters while preserving the alphabet that appears.  
* Checking equality of **character frequency multisets** (order of characters irrelevant).  

Typical clues: “swap any two characters”, “transform every occurrence of X into Y”, “only lowercase letters”, “same length required”.  

---  

## Template  

```python
from collections import Counter

def close_strings(word1: str, word2: str) -> bool:
    # 1️⃣ length check
    if len(word1) != len(word2):
        return False

    # 2️⃣ frequency maps (size 26 because only lowercase letters)
    freq1 = [0] * 26
    freq2 = [0] * 26
    for ch in word1:
        freq1[ord(ch) - ord('a')] += 1
    for ch in word2:
        freq2[ord(ch) - ord('a')] += 1

    # 3️⃣ same set of characters ?
    for i in range(26):
        if (freq1[i] == 0) != (freq2[i] == 0):
            return False

    # 4️⃣ same multiset of frequencies ?
    freq1.sort()
    freq2.sort()
    return freq1 == freq2
```

*Explanation of each step is given in the algorithm sections below.*  

---  

## LeetCode Problem Walkthrough  

### Problem: 1657. Determine if Two Strings Are Close  

https://leetcode.com/problems/determine-if-two-strings-are-close/  

---  

### Approach 1: Brute Force (Backtracking over possible frequency assignments)  

**Algorithm**  
1. Verify the strings have equal length – if not, return `False`.  
2. Build the frequency arrays `f1` and `f2`.  
3. The only freedom we have is to **reassign** frequencies to characters via operation 2.  
   * We try every possible bijection between the set of characters that appear in `word1` and the set that appear in `word2`.  
   * For each bijection we check whether we can match the frequencies by swapping them (i.e., whether the multiset of frequencies is identical).  
   * This is essentially checking all permutations of the frequency list – exponential in the number of distinct characters (≤ 26).  

**Implementation**  

```python
from itertools import permutations

def closeStrings_brute(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    freq1 = [0] * 26
    freq2 = [0] * 26
    for c in word1:
        freq1[ord(c) - 97] += 1
    for c in word2:
        freq2[ord(c) - 97] += 1

    # indices of characters that actually appear
    present1 = [i for i, v in enumerate(freq1) if v > 0]
    present2 = [i for i, v in enumerate(freq2) if v > 0]

    # if the sets of present characters differ, impossible
    if set(present1) != set(present2):
        return False

    # brute‑force: try every permutation of freq1 and see if it can match freq2
    for perm in permutations(freq1):
        # Build a temporary frequency list according to this permutation
        tmp = [0] * 26
        for idx, char_idx in enumerate(present1):
            tmp[char_idx] = perm[idx]
        if tmp == freq2:
            return True
    return False
```

**Complexity Analysis**  

- Time complexity: **O(k! · k)** where *k* ≤ 26 is the number of distinct letters (worst‑case factorial).  
- Space complexity: **O(1)** – only a few fixed‑size arrays of length 26.  

*Why we avoid this:* Even with only 26 letters the factorial blow‑up makes the solution infeasible for the given constraints (|word| up to 10⁵).  

---  

### Approach 2: Optimized – Frequency Set Equality  

**Intuition**  
Operation 1 lets us permute characters arbitrarily, so the *order* of letters does not matter.  
Operation 2 lets us **exchange** the frequencies of any two letters that both exist. Consequently, the exact pairing of a specific letter to a specific count is irrelevant; only the **multiset** of frequencies matters, provided the *set* of letters is identical.  

Thus the problem reduces to three simple checks: equal length, identical character sets, and identical frequency multisets.  

**Algorithm**  

1. If lengths differ → `False`.  
2. Count frequencies of each letter in both words (arrays of size 26).  
3. Verify that for every index `i`, either both counts are zero or both are non‑zero → same character set.  
4. Sort the two frequency arrays; if they are equal → same multiset of frequencies.  
5. Return the result of step 4.  

**Implementation**  

```python
def closeStrings(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    freq1 = [0] * 26
    freq2 = [0] * 26
    for ch in word1:
        freq1[ord(ch) - 97] += 1
    for ch in word2:
        freq2[ord(ch) - 97] += 1

    # same set of characters ?
    for i in range(26):
        if (freq1[i] == 0) != (freq2[i] == 0):
            return False

    # same multiset of frequencies ?
    freq1.sort()
    freq2.sort()
    return freq1 == freq2
```

**Complexity Analysis**  

- Time complexity: **O(n + 26 log 26)** → **O(n)** (single pass to count, then constant‑size sort).  
- Space complexity: **O(1)** – two arrays of length 26.  

---  

### Approach 3: Most Optimal – Same as Approach 2 (no further asymptotic gain)  

The optimized solution already runs in linear time with constant extra memory, which is optimal for this problem because we must read every character at least once. No further improvement in big‑O is possible.  

---  

## Provide a Visual Demonstration  

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example  

We dry‑run the optimized algorithm on Example 3:  

```
word1 = "cabbba"
word2 = "abbccc"
```

| Step | i | ch (word1) | freq1[ch]++ | ch (word2) | freq2[ch]++ |
|------|---|------------|-------------|------------|-------------|
| 0    | 0 | c          | freq1[2]=1  | a          | freq2[0]=1  |
| 1    | 1 | a          | freq1[0]=1  | b          | freq2[1]=1  |
| 2    | 2 | b          | freq1[1]=1  | b          | freq2[1]=2  |
| 3    | 3 | b          | freq1[1]=2  | c          | freq2[2]=1  |
| 4    | 4 | b          | freq1[1]=3  | c          | freq2[2]=2  |
| 5    | 5 | a          | freq1[0]=2  | c          | freq2[2]=3  |

Resulting frequency arrays (only non‑zero entries shown):  

- `freq1`: a→2, b→3, c→1 → `[2,3,1,0,…]`  
- `freq2`: a→1, b→2, c→3 → `[1,2,3,0,…]`  

**Same‑set check:** indices with non‑zero counts are `{0,1,2}` in both arrays → passes.  

**Sort frequencies:**  

- Sorted `freq1` → `[1,2,3]`  
- Sorted `freq2` → `[1,2,3]`  

Arrays equal → return `True`.  

---  

### Summary  

- **Operation 1** gives us free reordering → character order irrelevant.  
- **Operation 2** lets us swap frequencies among existing letters → only the *multiset* of frequencies matters, provided the *set* of letters is identical.  
- The final solution is therefore:  

  1. Equal length.  
  2. Same set of distinct characters.  
  3. Same sorted frequency list.  

All steps run in **O(n)** time and **O(1)** extra space, satisfying the constraints (`|word| ≤ 10⁵`).  

---  

*End of lecture.*