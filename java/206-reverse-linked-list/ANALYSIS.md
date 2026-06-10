# Reverse Linked List

## Video Solution

For more details about **Reverse Linked List**, watch the walkthrough at [https://www.youtube.com/watch?v=G0_I-ZF0S38](https://www.youtube.com/watch?v=G0_I-ZF0S38)

## Concept

Reversing a singly linked list means changing the direction of each node’s `next` pointer so that the last node becomes the new head. Instead of moving data around, we rewire the links in‑place using a few pointer variables.

**Real‑world analogy:** Think of a line of people holding hands. To reverse the line, each person lets go of the hand on their right and grabs the hand on their left. After everyone has done this, the person who was at the back is now at the front.

## When to Use It

Use linked‑list reversal when you see:
- A problem that explicitly asks to reverse a list.
- Sub‑problems like checking if a list is a palindrome (reverse the second half).
- Reordering nodes (e.g., reorder list, rotate list).
- Situations where you need to process the list from tail to head without using extra space.

## Template

```python
# Iterative in‑place reversal of a singly linked list
def reverseList(head):
    prev = None          # New head of the reversed part
    cur = head           # Node we are currently processing
    while cur:
        nxt = cur.next   # Save next node before we overwrite cur.next
        cur.next = prev  # Reverse the link
        prev = cur       # Move prev forward
        cur = nxt        # Move cur forward
    return prev          # prev is the new head
```

## LeetCode Problem Walkthrough

### Problem: 206. Reverse Linked List  
https://leetcode.com/problems/reverse-linked-list/

---

### Approach 1: Brute Force (Using a Stack)

**Algorithm**
1. Traverse the list and push each node’s value onto a stack.
2. Traverse the list again, popping values from the stack and overwriting each node’s value.
3. Return the original head (now holding reversed values).

**Implementation**

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Step 1: collect values
        stack = []
        cur = head
        while cur:
            stack.append(cur.val)
            cur = cur.next

        # Step 2: write back in reverse order
        cur = head
        while cur:
            cur.val = stack.pop()
            cur = cur.next

        return head
```

**Complexity Analysis**
- Time complexity: O(N) — we traverse the list twice.
- Space complexity: O(N) — the stack stores all node values.

---

### Approach 2: Iterative In‑Place (Optimal)

**Intuition**
By reversing the direction of each `next` pointer as we walk through the list, we avoid any extra storage. We only need three pointers: `prev` (the reversed portion), `cur` (the node we are processing), and `nxt` (to remember the original next node).

**Algorithm**
1. Initialize `prev = None`, `cur = head`.
2. While `cur` is not `None`:
   - Store `cur.next` in `nxt`.
   - Set `cur.next = prev` to reverse the link.
   - Advance `prev` to `cur`.
   - Advance `cur` to `nxt`.
3. When the loop ends, `prev` points to the new head; return it.

**Implementation**

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        cur = head
        while cur:
            nxt = cur.next      # 1️⃣ save next node
            cur.next = prev     # 2️⃣ reverse link
            prev = cur          # 3️⃣ move prev forward
            cur = nxt           # 4️⃣ move cur forward
        return prev
```

**Complexity Analysis**
- Time complexity: O(N) — single pass through the list.
- Space complexity: O(1) — only a few pointer variables.

---

### Approach 3: Recursive

**Intuition**
The recursive solution mirrors the iterative idea: we first reverse the rest of the list, then adjust the links of the current node. The base case is an empty list or a single node, which is already reversed.

**Algorithm**
1. Base case: if `head` is `None` or `head.next` is `None`, return `head`.
2. Recursively reverse the sublist starting at `head.next`; let the new head be `new_head`.
3. The node after `head` (i.e., `head.next`) is now the tail of the reversed sublist. Set its `next` pointer to `head`.
4. Set `head.next` to `None` to break the original link.
5. Return `new_head`.

**Implementation**

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case
        if not head or not head.next:
            return head
        
        # Reverse the rest of the list
        new_head = self.reverseList(head.next)
        
        # Adjust pointers: head's next node becomes its predecessor
        head.next.next = head
        head.next = None
        
        return new_head
```

**Complexity Analysis**
- Time complexity: O(N) — each node is visited once.
- Space complexity: O(N) — call stack depth equals the list size (due to recursion).

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We dry‑run the iterative approach on the example `head = [1,2,3,4,5]`.

#### Dry Run

Input: `head = [1,2,3,4,5]`

| Step | cur.val | prev.val (before) | nxt.val (saved) | Action                              | prev after | cur after |
|------|---------|-------------------|-----------------|-------------------------------------|------------|-----------|
| 0    | –       | None              | –               | Initialise                          | None       | 1         |
| 1    | 1       | None              | 2               | 1.next = None; prev=1; cur=2        | 1          | 2         |
| 2    | 2       | 1                 | 3               | 2.next = 1; prev=2; cur=3           | 2          | 3         |
| 3    | 3       | 2                 | 4               | 3.next = 2; prev=3; cur=4           | 3          | 4         |
| 4    | 4       | 3                 | 5               | 4.next = 3; prev=4; cur=5           | 4          | 5         |
| 5    | 5       | 4                 | None            | 5.next = 4; prev=5; cur=None        | 5          | None      |

When `cur` becomes `None`, `prev` holds the node with value `5`, which is the new head. The list is now `[5,4,3,2,1]`.

---