# Linked List

## Video Solution

For more details about **Merge Two Sorted Lists**, watch the walkthrough at [https://www.youtube.com/watch?v=XIdigk956u0](https://www.youtube.com/watch?v=XIdigk956u0)

## Concept

Merging two sorted linked lists is like merging two already‑sorted queues of people. You repeatedly compare the front person of each queue, take the shorter (or earlier) one, and place them at the back of a new line. Because each input list is already sorted, you never need to look back—you always know the next smallest element lives at the head of one of the two lists.

## When to Use It

Use the merge‑two‑sorted‑lists pattern when you see:
- Two (or more) **sorted** linked lists (or arrays) that need to be combined into a single sorted structure.
- The problem explicitly mentions “splice together the nodes” or “return the head of the merged list.”
- Constraints guarantee each input is individually sorted in non‑decreasing order.

## Template

```python
# Dummy head technique for merging two sorted linked lists
dummy = ListNode()          # placeholder to simplify edge cases
tail = dummy                # tail always points to the last node in the merged list

while list1 and list2:      # while both lists still have nodes
    if list1.val < list2.val:
        tail.next = list1   # attach the smaller node
        list1 = list1.next  # advance in list1
    else:
        tail.next = list2   # attach the smaller node
        list2 = list2.next  # advance in list2
    tail = tail.next        # move tail forward

# Attach the remainder of whichever list is not empty
tail.next = list1 if list1 else list2

return dummy.next           # skip the dummy and return the real head
```

---

## LeetCode Problem Walkthrough

### Problem: 21. Merge Two Sorted Lists

https://leetcode.com/problems/merge-two-sorted-lists/

### Approach 1: Brute Force – Collect & Sort

**Algorithm**
1. Traverse both input lists and copy every node’s value into a Python list.
2. Sort the collected values.
3. Create a new linked list from the sorted values and return its head.

**Implementation**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Step 1: gather all values
        values = []
        cur = list1
        while cur:
            values.append(cur.val)
            cur = cur.next
        cur = list2
        while cur:
            values.append(cur.val)
            cur = cur.next

        # Step 2: sort them
        values.sort()

        # Step 3: rebuild linked list
        dummy = ListNode()
        tail = dummy
        for v in values:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
```

**Complexity Analysis**
- Time complexity: O((n+m) log (n+m)) — we spend O(n+m) to traverse and O((n+m) log (n+m)) to sort.
- Space complexity: O(n+m) — we store all values in an auxiliary list and create new nodes.

---

### Approach 2: Iterative Merge (Dummy Head)

**Intuition**
Because each list is already sorted, the smallest unseen element must be at the head of one of the two lists. By repeatedly picking the smaller head and advancing that list, we build the merged list in order without any extra sorting.

**Algorithm**
1. Create a dummy node to act as a placeholder for the merged list’s head.
2. Use a `tail` pointer that always points to the last node of the merged list.
3. While both `list1` and `list2` are non‑null:
   - Compare `list1.val` and `list2.val`.
   - Append the smaller node to `tail.next` and advance that list’s pointer.
   - Move `tail` to the newly appended node.
4. After the loop, exactly one list may still have nodes; attach its remainder to `tail.next`.
5. Return `dummy.next` (the real head).

**Implementation**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()          # placeholder head
        tail = dummy                # tracks the end of merged list

        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # One list is exhausted; attach the other
        tail.next = list1 if list1 else list2

        return dummy.next
```

**Complexity Analysis**
- Time complexity: O(n + m) — each node is visited exactly once.
- Space complexity: O(1) — only a few pointers are used; we rearrange existing nodes.

---

### Approach 3: Recursive Merge

**Intuition**
The merge operation has a natural recursive definition: the merged list’s head is the smaller of the two current heads, and its `next` pointer should point to the merge of the remaining tails. This mirrors the iterative logic but expresses it via function calls.

**Algorithm**
1. Base case: if either list is empty, return the other list (nothing to merge).
2. Recursively decide which head is smaller:
   - If `list1.val < list2.val`, set `list1.next` to the result of merging `list1.next` with `list2`, then return `list1`.
   - Otherwise, set `list2.next` to the result of merging `list1` with `list2.next`, then return `list2`.
3. The recursion unwinds, linking nodes in sorted order.

**Implementation**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: one list is empty
        if not list1:
            return list2
        if not list2:
            return list1

        # Choose the smaller head and recurse on the remainder
        if list1.val < list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

**Complexity Analysis**
- Time complexity: O(n + m) — each node is processed once in a recursive call.
- Space complexity: O(n + m) — due to the recursion stack (worst‑case depth equals total nodes).  
  (If tail‑call optimization were available it could be O(1), but Python does not provide it.)

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

#### Dry Run

Input:  
`list1 = [1 → 2 → 4]`  
`list2 = [1 → 3 → 4]`

We trace the iterative dummy‑head approach (Approach 2).

| Step | list1.val | list2.val | Chosen node | tail.next after action | list1 after | list2 after | tail after |
|------|-----------|-----------|-------------|------------------------|-------------|-------------|------------|
| Init | –         | –         | –           | dummy → None           | 1→2→4       | 1→3→4       | dummy      |
| 1    | 1         | 1         | list1 (1)   | dummy → 1              | 2→4         | 1→3→4       | node(1) from list1 |
| 2    | 2         | 1         | list2 (1)   | dummy → 1 → 1          | 2→4         | 3→4         | node(1) from list2 |
| 3    | 2         | 3         | list1 (2)   | dummy → 1 → 1 → 2      | 4           | 3→4         | node(2) |
| 4    | 4         | 3         | list2 (3)   | dummy → 1 → 1 → 2 → 3  | 4           | 4           | node(3) |
| 5    | 4         | 4         | list1 (4)   | dummy → 1 → 1 → 2 → 3 → 4 | None      | 4           | node(4) from list1 |
| 6    | –         | 4         | list2 (4)   | dummy → 1 → 1 → 2 → 3 → 4 → 4 | None   | None        | node(4) from list2 |

After the loop, both lists are exhausted, so `tail.next` remains `None`.  
Return `dummy.next` → `[1,1,2,3,4,4]`, which matches the expected output.

---