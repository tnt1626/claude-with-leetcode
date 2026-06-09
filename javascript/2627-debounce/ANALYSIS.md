# Debounce

## Video Solution

For more details about **Debounce**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=1sxSpnxNx5w).

## Concept

Debouncing limits how often a function can be invoked. When a debounced function is called, it postpones its execution by a fixed delay `t`. If the function is called again before that delay expires, the pending execution is cancelled and a new delay starts from the most recent call. Only after a period of inactivity lasting at least `t` milliseconds does the function finally run with the arguments from the latest call.

A real‑world analogy is an elevator door: the doors stay open for a few seconds after someone steps in, but if another person rushes in before the doors close, the timer resets and the doors stay open longer. The doors finally close only when no one has entered for the full waiting period.

## When to Use It

Use debouncing when you see:
- Rapid, repeated events (e.g., `resize`, `scroll`, `keydown`) that should trigger a heavy operation only after the user pauses.
- API autosave or search‑as‑you‑type features where you want to wait until the user stops typing before sending a request.
- Any scenario where you need to **rate‑limit** successive function calls to the most recent one.

## Template

```python
import threading
from typing import Callable, List, Any

def debounce(fn: Callable, t: int) -> Callable[[Any], None]:
    """
    Returns a debounced version of `fn`.
    `t` is the delay in milliseconds.
    """
    # Holds the ID of the pending timer so we can cancel it.
    timer: threading.Timer | None = None

    def debounced(*args: Any) -> None:
        nonlocal timer
        # Cancel any previous pending execution.
        if timer is not None:
            timer.cancel()
        # Schedule a new execution after `t` milliseconds.
        timer = threading.Timer(t / 1000.0, fn, args)
        timer.start()

    return debounced
```

## LeetCode Problem Walkthrough

### Problem: 2627. Debounce

https://leetcode.com/problems/debounce/

---

### Approach 1: Brute Force (Look‑Ahead)

**Intuition**  
If we knew the entire list of calls in advance, we could decide for each call whether it will survive by checking whether any later call arrives before its scheduled execution time (`call.time + t`). A later call that arrives early cancels the current one. This leads to a simple O(n²) scan: for each call, look ahead to see if a cancelling call exists.

**Algorithm**
1. Initialise an empty list `result` to store the executions that actually happen.
2. For each call `i` with time `ti` and arguments `argsi`:
   - Assume the call will execute at `execute_at = ti + t`.
   - Scan all later calls `j > i`. If any call `j` has time `tj < execute_at`, then call `i` is cancelled → break and do not add anything.
   - If no later call cancels it, append a record `{"t": execute_at, "inputs": argsi}` to `result`.
3. Return `result`.

**Implementation**

```python
from typing import List, Dict, Any

def debounce_bruteforce(t: int, calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Brute‑force debounce that works with a known list of calls.
    Returns the list of executions that would actually occur.
    """
    n = len(calls)
    result: List[Dict[str, Any]] = []

    for i in range(n):
        ti = calls[i]["t"]
        argsi = calls[i]["inputs"]
        execute_at = ti + t

        # Check whether any later call cancels this one.
        cancelled = False
        for j in range(i + 1, n):
            if calls[j]["t"] < execute_at:
                cancelled = True
                break

        if not cancelled:
            result.append({"t": execute_at, "inputs": argsi})

    return result
```

**Complexity Analysis**

- Time complexity: O(n²) — for each of the `n` calls we may scan all later calls.
- Space complexity: O(n) — the output list stores at most `n` executions.

---

### Approach 2: Optimized (Timer‑Based)

**Intuition**  
Instead of looking ahead, we can handle calls as they arrive in real time. Each new call should cancel any previously scheduled execution and start a fresh delay. This is exactly what a timer (e.g., `setTimeout` in JavaScript or `threading.Timer` in Python) provides: we keep a reference to the pending timer, clear it on every new call, and schedule a new one. When the timer finally fires, we know no further call arrived during the waiting interval, so we safely invoke the original function.

**Algorithm**
1. Keep a mutable reference `timer` (initially `None`) that stores the currently pending `threading.Timer`.
2. Return a wrapper function that accepts arbitrary arguments:
   - If `timer` is not `None`, cancel it (`timer.cancel()`).
   - Create a new `threading.Timer` set to fire after `t/1000` seconds, calling `fn` with the captured arguments.
   - Start the timer and store its reference in `timer`.
3. When the timer’s callback runs, it invokes `fn(*args)` – this is the actual debounced execution.

**Implementation**

```python
import threading
from typing import Callable, Any

def debounce(fn: Callable, t: int) -> Callable[[Any], None]:
    """
    Returns a debounced version of `fn` using a timer.
    """
    timer: threading.Timer | None = None

    def debounced(*args: Any) -> None:
        nonlocal timer
        # Cancel any previous pending execution.
        if timer is not None:
            timer.cancel()
        # Schedule a new execution after `t` milliseconds.
        timer = threading.Timer(t / 1000.0, fn, args)
        timer.start()

    return debounced
```

**Complexity Analysis**

- Time complexity: O(1) per call — each call does only constant‑time work (cancel/start a timer).
- Space complexity: O(1) extra space (aside from the timer object itself). The output list that LeetCode checks is built by the test harness, not by our algorithm.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We dry‑run the optimized debounce on Example 2 (`t = 20`, calls at 50 ms and 100 ms).

#### Dry Run

| Step | Call time (ms) | Action                              | Pending timer (executes at) |
|------|----------------|-------------------------------------|-----------------------------|
| 1    | 50             | Cancel none → start timer for 50+20 = 70 ms | 70 |
| 2    | 100            | Cancel timer (70) → start new timer for 100+20 = 120 ms | 120 |
| End  | –              | No further calls → timer fires at 120 ms, executes second call. First call never executed because its timer was cancelled. | – |

Resulting executions: `[{t: 70, inputs: [1]}, {t: 120, inputs: [2]}]`, matching the expected output.

---

**Summary**  
- The brute‑force version shows the underlying logic but is inefficient (`O(n²)`).  
- The timer‑based version gives the optimal `O(1)` per‑call solution, which is what the LeetCode judge expects.  
Both approaches illustrate the core idea: **cancel the previous pending execution and restart the delay on every new call**.