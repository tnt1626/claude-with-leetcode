# Fast & Slow Pointers

## Video Solution

For more details about **Remove Nth Node From End of List**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=7eQI3xlAGLg).

## Concept

The fast & slow pointer technique uses two pointers that move through a sequence at different speeds. By maintaining a fixed gap between them, we can solve problems that require accessing elements relative to the end (or middle) of a list in a single pass. A dummy node placed before the head simplifies edge cases such as removing the first node.

## When to Use It

Use fast & slow pointers when you see:
- Linked list problems that ask to remove, find, or modify a node relative to the end (e.g., “nth node from the end”).
- Need to detect cycles or find the middle of a list.
- Constraints that require O(1) extra space and a single traversal.

## Template

```python
# Dummy node to handle head removal uniformly
dummy = ListNode(0, head)

# Initialize two pointers with a gap of `n` nodes
fast = dummy
slow = dummy

# Move `fast` ahead by n+1 steps so that the gap between slow and fast is n+1
for _ in range(n + 1):
    fast = fast.next

# Move both pointers until fast reaches the end.
# At that point, slow will be right before the node to delete.
while fast:
    fast = fast.next
    slow = slow.next

# Skip the target node
slow.next = slow.next.next

return dummy.next
```

## LeetCode Problem Walkthrough

### Problem: 19. Remove Nth Node From End of List

https://leetcode.com/problems/remove-nth-node-from-end-of-list/

### Approach 1: Brute Force (Two Passes)

**Algorithm**
1. First pass: compute the length `L` of the linked list.
2. Calculate the index to remove from the start: `target = L - n`.
3. Second pass: traverse again to the node just before the target and bypass it.
4. Handle the case where the head itself is removed.

**Implementation**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # ---- Pass 1: find length ----
        length = 0
        cur = head
        while cur:
            length += 1
            cur = cur.next

        # If we need to remove the head
        if length == n:
            return head.next

        # ---- Pass 2: reach node before target ----
        steps_to_target = length - n - 1   # zero‑based steps from head
        cur = head
        for _ in range(steps_to_target):
            cur = cur.next
        # cur now points to the node before the one to delete
        cur.next = cur.next.next
        return head
```

**Complexity Analysis**
- Time complexity: O(L) + O(L) = O(L) — two linear scans of the list.
- Space complexity: O(1) — only a few pointers are used.

### Approach 2: One Pass with Fast & Slow Pointers

**Intuition**
By creating a gap of exactly `n` nodes between two pointers, when the leading pointer reaches the end, the trailing pointer will be positioned just before the node we need to delete. This lets us find the target in a single traversal.

**Algorithm**
1. Create a dummy node pointing to the head to uniformly handle removal of the first node.
2. Initialize `fast` and `slow` at the dummy.
3. Advance `fast` by `n + 1` steps so the gap between `slow` and `fast` is `n + 1`.
4. Move both pointers together until `fast` hits the end; `slow` will now point to the node preceding the target.
5. Bypass the target node (`slow.next = slow.next.next`).
6. Return `dummy.next`.

**Implementation**

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)   # sentinel simplifies edge cases
        fast = slow = dummy

        # Move fast ahead so that the gap is n+1 nodes
        for _ in range(n + 1):
            fast = fast.next

        # Advance both until fast reaches the end
        while fast:
            fast = fast.next
            slow = slow.next

        # Skip the nth node from the end
        slow.next = slow.next.next
        return dummy.next
```

**Complexity Analysis**
- Time complexity: O(L) — each node is visited at most twice (once by fast, once by slow).
- Space complexity: O(1) — only a few pointers and the dummy node.

### Approach 3: One Pass with Fast & Slow Pointers (Explicit Edge‑Case Handling)

**Intuition**
The core idea is identical to Approach 2, but we make the handling of the head‑removal case explicit by checking whether the node to delete is the head after the first pass of the fast pointer. This can be easier to follow for beginners while preserving the same complexity.

**Algorithm**
1. Move `fast` `n` steps ahead from the head.
2. If `fast` becomes `None`, the node to remove is the head; return `head.next`.
3. Otherwise, move both `fast` and `slow` (starting at head) together until `fast.next` is `None`. At that point, `slow` points to the node before the target.
4. Bypass the target node and return the original head.

**Implementation**

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        fast = head
        # Step 1: create the gap
        for _ in range(n):
            fast = fast.next

        # Step 2: if fast reached the end, we need to remove the head
        if not fast:
            return head.next

        # Step 3: move both pointers until fast hits the last node
        slow = head
        while fast.next:
            fast = fast.next
            slow = slow.next

        # Step 4: delete the target node
        slow.next = slow.next.next
        return head
```

**Complexity Analysis**
- Time complexity: O(L) — one pass with two pointers.
- Space complexity: O(1) — constant extra space.

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

#### Dry Run

We trace Approach 2 (dummy head) on the example `head = [1,2,3,4,5]`, `n = 2`.

| Step | fast position | slow position | Action |
|------|---------------|---------------|--------|
| Init | dummy (0)     | dummy (0)     | start |
| Advance fast n+1=3 steps | node 3 (value 3) | dummy (0) | fast moved 3 ahead |
| Move both until fast at end | fast: node 4 → node 5 → None<br>slow: dummy → node 1 → node 2 |  |
| After loop | fast = None | slow = node 2 (value 2) | slow is before target |
| Delete | slow.next = slow.next.next (skip node 3) |  |
| Result | list becomes `[1,2,3,5]` |  |

The table shows how the gap of `n+1` nodes ensures that when `fast` reaches the end (`None`), `slow` sits right before the node to remove. Removing `slow.next` yields the correct list.