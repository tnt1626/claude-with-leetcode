# Promises

## Video Solution

For more details about **Add Two Promises**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=p-XtCP74q0U).

## Concept

A **Promise** represents a value that may be available now, later, or never. It is the core building block for asynchronous programming in JavaScript.  
When you have two promises that each resolve to a number, you can wait for both to settle and then combine their resolved values.  
Think of it like ordering two dishes at a restaurant: you don’t eat until both dishes arrive, then you add their portions together.

## When to Use It

Use this pattern when you see:
- Multiple asynchronous operations that are independent.
- You need the **combined result** (sum, merge, etc.) after all operations finish.
- The operations return values (e.g., numbers, objects) that you will process together.

## Template

```python
# Generic template for awaiting multiple promises and combining results
async def combine_promises(promises, combiner):
    # Wait for all promises to resolve
    results = await Promise.all(promises)
    # Apply the combining function (e.g., sum, concat)
    return combiner(results)
```

In JavaScript/TypeScript the same idea looks like:

```typescript
async function combine<T>(promises: Promise<T>[], fn: (vals: T[]) => any): Promise<any> {
    const vals = await Promise.all(promises);
    return fn(vals);
}
```

---

# LeetCode Problem Walkthrough

### Problem: 2723. Add Two Promises
https://leetcode.com/problems/add-two-promises/

Given two promises `promise1` and `promise2` that each resolve to a number, return a new promise that resolves to the sum of the two numbers.

---

## Approach 1: Sequential Await (Brute Force)

**Algorithm**
1. Await `promise1` to get its resolved value `a`.
2. Await `promise2` to get its resolved value `b`.
3. Return `a + b`.

This works but waits for the second promise only after the first has settled, potentially adding unnecessary latency.

**Implementation**

```typescript
type P = Promise<number>;

async function addTwoPromises(seq1: P, seq2: P): P {
    const a = await seq1;   // wait for first
    const b = await seq2;   // then wait for second
    return a + b;           // sum the results
}
```

**Complexity Analysis**
- Time complexity: O(1) – we perform a constant amount of work; the actual waiting time is dictated by the promises themselves, not our code.
- Space complexity: O(1) – only a few scalar variables are used.

---

## Approach 2: Parallel Wait with `Promise.all` (Optimal)

**Intuition**
Since the two promises are independent, we can wait for them **in parallel** rather than sequentially. `Promise.all` creates a new promise that resolves when *all* input promises have resolved, giving us an array of their resolved values in the same order. This minimizes the total waiting time to the slower of the two promises instead of their sum.

**Algorithm**
1. Call `Promise.all([promise1, promise2])` → returns a promise that resolves to `[a, b]`.
2. Await that promise to get the array `[a, b]`.
3. Return `a + b`.

**Implementation**

```typescript
type P = Promise<number>;

async function addTwoPromises(p1: P, p2: P): P {
    const [a, b] = await Promise.all([p1, p2]); // wait for both in parallel
    return a + b;                               // sum the results
}
```

**Complexity Analysis**
- Time complexity: O(1) – constant work aside from the asynchronous waiting.
- Space complexity: O(1) – we store only two numbers and the temporary array of size 2 (constant).

---

## Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

### Dry Run

Assume:
- `promise1` resolves to `2` after 20 ms.
- `promise2` resolves to `5` after 60 ms.

| Step | Action                                 | Value of `promise1` | Value of `promise2` | Notes                              |
|------|----------------------------------------|---------------------|---------------------|------------------------------------|
| 0    | Start both promises                    | pending             | pending             | –                                  |
| 20ms | `promise1` resolves                    | 2                   | pending             | –                                  |
| 60ms | `promise2` resolves                    | 2                   | 5                   | Both now settled                   |
| 60ms | `Promise.all` resolves with `[2,5]`    | –                   | –                   | Array ready                        |
| 60ms | Sum `2 + 5` → `7`                      | –                   | –                   | Final result returned              |

If we used the sequential approach, we would wait for `promise1` (20 ms), then wait for `promise2` (another 60 ms) → total ~80 ms before we could sum. The parallel approach finishes at the slower promise’s time (60 ms).

---