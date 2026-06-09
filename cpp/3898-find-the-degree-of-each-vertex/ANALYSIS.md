# Find the Degree of Each Vertex

## Video Solution
For more details about **Find the Degree of Each Vertex**, watch the walkthrough at [https://www.youtube.com/watch?v=7ArORJS6eDs](https://www.youtube.com/watch?v=7ArORJS6eDs)

## Concept
The degree of a vertex in an undirected graph is simply the number of edges incident to that vertex. When the graph is given as an adjacency matrix `matrix`, each row `i` contains a `1` for every vertex `j` that is connected to `i`. Therefore, the degree of vertex `i` equals the sum of the entries in row `i`.

## When to Use It
Use this technique when:
- The graph is provided as an adjacency matrix.
- You need to compute the degree (or valency) of each vertex.
- The matrix is square (`n x n`) and symmetric (`matrix[i][j] == matrix[j][i]`).

## Template
```python
def find_degrees(matrix):
    """
    Returns a list where the i-th element is the degree of vertex i.
    """
    n = len(matrix)
    degrees = [0] * n
    for i in range(n):
        # Sum of row i gives the degree of vertex i
        degrees[i] = sum(matrix[i])
    return degrees
```

## LeetCode Problem Walkthrough

### Problem: 3898. Find the Degree of Each Vertex
https://leetcode.com/problems/find-the-degree-of-each-vertex/

### Approach 1: Brute Force (Nested Loops)

**Algorithm**
1. Initialise an answer array `ans` of size `n` with zeros.
2. For each vertex `i` (row), iterate over all columns `j`.
3. Whenever `matrix[i][j] == 1`, increment a counter for the current row.
4. After scanning the whole row, store the counter in `ans[i]` and reset the counter.
5. Return `ans`.

**Implementation**
```python
class Solution:
    def findDegrees(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        ans = [0] * m
        
        for i in range(m):
            count = 0
            for j in range(n):
                if matrix[i][j] == 1:
                    count += 1
            ans[i] = count
        
        return ans
```

**Complexity Analysis**
- Time complexity: O(n²) — we examine every entry of the n×n matrix once.
- Space complexity: O(n) — the output array of size n.

### Approach 2: Row Sum (Using Built‑in Sum)

**Intuition**
Since each row already contains the adjacency information for a vertex, we can avoid an explicit inner loop by summing the row directly. This reduces constant factors and makes the code more concise while retaining the same asymptotic complexity.

**Algorithm**
1. Initialise an answer array `ans` of size `n` with zeros.
2. For each row `i` in the matrix, set `ans[i]` to `sum(matrix[i])`.
3. Return `ans`.

**Implementation**
```python
class Solution:
    def findDegrees(self, matrix: List[List[int]]) -> List[int]:
        return [sum(row) for row in matrix]
```

**Complexity Analysis**
- Time complexity: O(n²) — summing each row still touches every element once.
- Space complexity: O(n) — only the result list is allocated.

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

## Dry Run

Input: `matrix = [[0,1,0],[1,0,0],[0,0,0]]`

| Step | i (row) | row contents | sum(row) | ans after step |
|------|---------|--------------|----------|----------------|
| 1    | 0       | [0, 1, 0]    | 1        | [1, 0, 0]      |
| 2    | 1       | [1, 0, 0]    | 1        | [1, 1, 0]      |
| 3    | 2       | [0, 0, 0]    | 0        | [1, 1, 0]      |

Final answer: `[1, 1, 0]` which matches the expected output.

--- 

*This lecture follows the standard format: concept → when to use → template → multiple approaches (brute force → optimized) with full complexity analysis and a dry‑run demonstration.*