# Zigzag Conversion

## Video Solution

Referenced a single url containing the according problem at [resources](https://www.youtube.com/results?search_query=leetcode+zigzag+conversion+solution)

## Concept

The Zigzag Conversion problem asks us to rewrite a string in a zig‑zag pattern across a given number of rows and then read the characters row‑by‑row.  
Imagine writing the string on a set of horizontal rails (rows). We start at the top rail, move down one rail at a time until we hit the bottom rail, then reverse direction and move up until we reach the top rail again. This “down‑then‑up” motion repeats until all characters are placed. Finally, concatenating the rails from top to bottom yields the answer.

## When to Use It

Use this pattern when a problem describes:
- Writing characters in a repeating up‑and‑down or back‑and‑forth motion.
- Distributing elements into a fixed number of buckets that are filled in a periodic sequence.
- The output is obtained by reading the buckets in order after a deterministic traversal.

## Template

A common reusable skeleton for this kind of simulation is:

```python
def convert(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s

    # Create a list for each row
    rows = [''] * numRows
    cur_row = 0
    going_down = False   # direction flag

    for ch in s:
        rows[cur_row] += ch
        # Change direction at the top or bottom row
        if cur_row == 0 or cur_row == numRows - 1:
            going_down = not going_down
        # Move to next row according to direction
        cur_row += 1 if going_down else -1

    return ''.join(rows)
```

The same idea can be translated to any language; the core is:
1. An array/list representing each row.
2. A pointer to the current row.
3. A flag that flips when we hit the first or last row.
4. Append the character to the current row, then move the pointer.

---

## LeetCode Problem Walkthrough

### Problem: 6. Zigzag Conversion

https://leetcode.com/problems/zigzag-conversion/

---

### Approach 1: Brute Force – 2‑D Matrix Simulation

**Algorithm**
1. Create a 2‑D character matrix with `numRows` rows and enough columns to hold the worst‑case zig‑zag (length of `s` columns is safe).
2. Walk through the string, filling the matrix following the down‑then‑up movement:
   - Move down column by column, filling one cell per row.
   - When the bottom row is reached, move up diagonally, filling one cell per step until the top row is reached.
3. After filling, concatenate each row left‑to‑right, skipping empty cells.

**Implementation**

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        # Allocate a matrix with enough columns (len(s) is a safe upper bound)
        matrix = [['' for _ in range(len(s))] for _ in range(numRows)]
        row, col = 0, 0
        going_down = False

        for ch in s:
            matrix[row][col] = ch
            if row == 0 or row == numRows - 1:
                going_down = not going_down
            row += 1 if going_down else -1
            # Move to next column only when we are going up (diagonal step)
            if not going_down:
                col += 1

        # Read row‑wise
        result = []
        for r in range(numRows):
            for c in range(len(s)):
                if matrix[r][c]:
                    result.append(matrix[r][c])
        return ''.join(result)
```

**Complexity Analysis**
- Time complexity: O(n · numRows) – we touch each cell of the matrix once; the matrix size is O(numRows × n) in the worst case.
- Space complexity: O(n · numRows) – the auxiliary matrix.

*Note:* This approach is easy to visualize but uses more memory than necessary.

---

### Approach 2: Direction‑Flag Simulation (Row Strings)

**Intuition**
Instead of storing a full 2‑D matrix, we only need the characters that belong to each row. By keeping a separate string builder for each row and updating the current row index with a direction flag, we can place each character directly into its final row.

**Algorithm**
1. If `numRows` is 1 or greater than or equal to the string length, return the original string (no zig‑zag effect).
2. Create a list `rows` of `numRows` empty strings.
3. Initialise `cur_row = 0` and a boolean `going_down = False`.
4. Iterate over each character `c` in `s`:
   - Append `c` to `rows[cur_row]`.
   - If we are at the first or last row, flip the direction (`going_down = not going_down`).
   - Move `cur_row` one step toward the next row: `cur_row += 1 if going_down else -1`.
5. After processing all characters, concatenate all strings in `rows` and return.

**Implementation**

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [''] * numRows
        cur_row = 0
        going_down = False

        for ch in s:
            rows[cur_row] += ch
            if cur_row == 0 or cur_row == numRows - 1:
                going_down = not going_down
            cur_row += 1 if going_down else -1

        return ''.join(rows)
```

**Complexity Analysis**
- Time complexity: O(n) – each character is processed exactly once.
- Space complexity: O(n) – we store the characters once across the `rows` strings.

---

### Approach 3: Mathematical Index Calculation (No Extra Storage)

**Intuition**
The zig‑zag pattern repeats every `cycle = 2 * numRows - 2` characters (a full down‑then‑up sweep). For any position `i` in the original string, we can compute which row it belongs to directly:
- Let `rest = i % cycle`.
- If `rest < numRows`, the character is on the downward leg → row = `rest`.
- Otherwise, it is on the upward leg → row = `cycle - rest`.
By iterating over rows and picking the characters that fall into each row using this formula, we can build the answer without auxiliary per‑row strings (only the output string is needed).

**Algorithm**
1. Handle the trivial case `numRows == 1`.
2. Compute `cycle = 2 * numRows - 2`.
3. For each row `r` from `0` to `numRows-1`:
   - Walk through indices `j = r; j < len(s); j += cycle`:
     - Append `s[j]` to the result (downward leg character).
     - If `r` is not the first or last row, there is a second character in the same cycle on the upward leg:
       - `up_index = j + cycle - 2 * r`
       - If `up_index < len(s)`, append `s[up_index]`.
4. Return the accumulated result.

**Implementation**

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s

        cycle = 2 * numRows - 2
        n = len(s)
        result = []

        for r in range(numRows):
            j = r
            while j < n:
                result.append(s[j])                     # down‑leg character
                # up‑leg character exists only for middle rows
                if 0 < r < numRows - 1:
                    up = j + cycle - 2 * r
                    if up < n:
                        result.append(s[up])
                j += cycle                               # jump to next cycle
        return ''.join(result)
```

**Complexity Analysis**
- Time complexity: O(n) – each character is appended exactly once.
- Space complexity: O(1) extra (aside from the output string).

---

## Summary

| Approach | Idea | Time | Space |
|----------|------|------|-------|
| Brute‑Force Matrix | Fill a 2‑D grid following the zig‑zag path | O(n·numRows) | O(n·numRows) |
| Direction‑Flag (Row Strings) | Keep a string per row, flip direction at extremes | O(n) | O(n) |
| Mathematical Index | Compute row via cycle arithmetic, no per‑row storage | O(n) | O(1) |

The direction‑flag solution is the most common interview answer because it is simple, linear, and uses only O(n) space for the result. The mathematical version shows how to achieve O(1) auxiliary space when the output string itself is allowed. Begin by mastering the intuition of the down‑then‑up motion; then you can choose the implementation that best fits the constraints of your environment.