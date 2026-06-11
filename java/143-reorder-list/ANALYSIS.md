# Fast & Slow Pointers

## Video Solution

For more details about **Reorder List**, watch the walkthrough at [https://www.youtube.com/watch?v=Pno7rUOZM-o](https://www.youtube.com/watch?v=Pno7rUOZM-o)

## Concept

The fast‑and‑slow pointer technique uses two pointers that traverse a linked list at different speeds.  
- The **slow** pointer moves one node at a time.  
- The **fast** pointer moves two nodes at a time.  

When the fast pointer reaches the end, the slow pointer will be at the middle (or the first middle in an even‑length list).  
This lets us split the list, reverse a half, or detect cycles without extra memory.

**Analogy:** Two runners on a track — one runs twice as fast as the other. When the faster runner laps the track, the slower runner is exactly halfway around.

## When to Use It

Use fast/slow pointers when you see:
- Need to find the middle of a linked list.
- Check for a palindrome in a linked list.
- Reorder a list (as in this problem).
- Find the k‑th node from the end.
- Detect a cycle in a linked list.

## Template

```python
# Fast & Slow Pointers template (Python)
def fast_slow_pointer(head):
    slow = fast = head
    while fast and fast.next:          # fast moves two steps
        slow = slow.next               # slow moves one step
        fast = fast.next.next
    # At this point, `slow` is the middle (or first middle)
    return slow
```

---

## LeetCode Problem Walkthrough

### Problem: 143. Reorder List
https://leetcode.com/problems/reorder-list/

> You are given the head of a singly linked list. Reorder it to  
> `L0 → Ln → L1 → Ln‑1 → L2 → Ln‑2 …` without changing node values.

### Approach 1: Brute Force (Extra Array)

**Algorithm**  
1. Traverse the list and store each node’s value in a Python list.  
2. Use two pointers (`i` from start, `j` from end) to build the reordered sequence of values.  
3. Overwrite the original list’s node values with this new order.

**Implementation**

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return

        # 1️⃣ Collect values
        vals = []
        cur = head
        while cur:
            vals.append(cur.val)
            cur = cur.next

        # 2️⃣ Build reordered values
        reordered = []
        i, j = 0, len(vals) - 1
        while i <= j:
            reordered.append(vals[i])
            if i != j:
                reordered.append(vals[j])
            i += 1
            j -= 1

        # 3️⃣ Write back
        cur = head
        for v in reordered:
            cur.val = v
            cur = cur.next
```

**Complexity Analysis**

- Time complexity: O(n) — one pass to collect values, one pass to write them back.  
- Space complexity: O(n) — the auxiliary list `vals`.

---

### Approach 2: Fast & Slow + In‑Place Reverse + Merge (Optimal)

**Intuition**  
If we can split the list into two halves, reverse the second half, then merge them alternately, we achieve the desired order using only pointer changes — no extra storage for node values.

**Algorithm**  
1. Use fast/slow pointers to locate the middle; break the list there.  
2. Reverse the second half in place.  
3. Merge the two halves by alternating nodes: first from the front half, then from the reversed back half.

**Implementation**

```python
class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return

        # ---------- 1️⃣ Find middle ----------
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # `slow` is the end of the first half
        second = slow.next
        slow.next = None          # terminate first half

        # ---------- 2️⃣ Reverse second half ----------
        prev = None
        curr = second
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # `prev` is the head of the reversed second half
        second = prev

        # ---------- 3️⃣ Merge two halves ----------
        first = head
        while second:
            # Save next pointers
            tmp1 = first.next
            tmp2 = second.next

            # Link
            first.next = second
            second.next = tmp1

            # Advance
            first = tmp1
            second = tmp2
```

**Complexity Analysis**

- Time complexity: O(n) — each step (find middle, reverse, merge) scans the list once.  
- Space complexity: O(1) — only a few pointer variables are used.

---

### Approach 3: Using a Stack (Alternative O(n) Space)

**Intuition**  
A stack naturally gives us nodes in reverse order. By pushing the first half onto a stack, we can pop nodes to interleave them with the second half, achieving the reorder without reversing pointers.

**Algorithm**  
1. Use fast/slow to find the middle and split the list.  
2. Push all nodes of the first half onto a stack.  
3. Pop from the stack and insert each node after the current node of the second half.

**Implementation**

```python
class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return

        # ---------- 1️⃣ Find middle ----------
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None          # break list

        # ---------- 2️⃣ Push first half onto stack ----------
        stack = []
        cur = head
        while cur:
            stack.append(cur)
            cur = cur.next

        # ---------- 3️⃣ Interleave using stack ----------
        cur = second
        while stack:
            node = stack.pop()    # gets nodes from end of first half
            nxt = cur.next
            cur.next = node
            node.next = nxt
            cur = nxt
```

**Complexity Analysis**

- Time complexity: O(n) — each node is visited a constant number of times.  
- Space complexity: O(n) — the stack stores up to ⌈n/2⌉ nodes.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We trace Algorithm 2 (fast/slow + reverse + merge) on the input `[1,2,3,4,5]`.

#### Dry Run

```
Initial list: 1 → 2 → 3 → 4 → 5
```

| Step | Action                                 | List state (first half | reversed second half) |
|------|----------------------------------------|------------------------|------------------------|
| 1    | Find middle (slow stops at 3)          | 1 → 2 → 3              | 4 → 5                  |
| 2    | Break after slow                       | 1 → 2 → 3  (null)      | 4 → 5                  |
| 3    | Reverse second half                    | 1 → 2 → 3              | 5 → 4                  |
| 4    | Merge: take 1, then 5                  | 1 → 5 → 2 → 3          | 4                      |
| 5    | Merge: take 2, then 4                  | 1 → 5 → 2 → 4 → 3      | (empty)                |
| 6    | Done                                   | **1 → 5 → 2 → 4 → 3**  |                        |

Final order matches the expected output. The same logic works for even‑length lists (e.g., `[1,2,3,4]` → `[1,4,2,3]`).