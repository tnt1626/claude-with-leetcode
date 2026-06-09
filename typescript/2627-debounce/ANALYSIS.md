# Debounce

## Video Solution

For more details about **Debounce**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=1sxSpnxNx5w).

## Concept

Debouncing is a technique used to limit how often a function can be executed.  
When a debounced function is called, it waits for a specified delay `t`. If another call arrives before that delay expires, the previous pending call is cancelled and the timer restarts. Only after `t` milliseconds of *inactivity* does the original function finally run with the arguments from the most recent call.

A real‑world analogy: think of a waiter who only brings your order to the kitchen after you’ve stopped adding items for a full minute. If you keep shouting new items, the waiter resets the timer and waits again.

## When to Use It

- Handling rapid UI events such as `window.resize`, `keydown`, or `input` where you only want to act after the user has paused.
- Throttling API calls (e.g., autocomplete search) to avoid sending a request on every keystroke.
- Any scenario where you need to collapse multiple closely‑spaced triggers into a single action.

## Template

A generic debounce wrapper in Python (conceptually identical to the JavaScript version) looks like this:

```python
import threading
from typing import Callable, Any, List

def debounce(fn: Callable[..., Any], t: float) -> Callable[..., None]:
    """
    Returns a debounced version of `fn`.
    t: delay in seconds (the LeetCode problem uses milliseconds).
    """
    timer: threading.Timer | None = None

    def debounced(*args: Any) -> None:
        nonlocal timer
        # Cancel any pending execution
        if timer is not None:
            timer.cancel()
        # Schedule a new execution after `t` seconds
        timer = threading.Timer(t, fn, args=args)
        timer.start()

    return debounced
```

*Note:* In JavaScript we would use `setTimeout`/`clearTimeout`; in Python we can achieve the same behavior with `threading.Timer`.

---

## LeetCode Problem Walkthrough

### Problem: 2627. Debounce  
https://leetcode.com/problems/debounce/

---

### Approach 1: Brute Force – Time‑Driven Simulation

**Algorithm**  
Because the constraints are tiny (`calls.length ≤ 10`, times ≤ 1000), we can simulate every millisecond from `0` to the latest possible execution time.

1. Determine the maximum time we need to consider:  
   `max_time = max(call.t for call in calls) + t`  
   (the latest call could be delayed by `t`).
2. Create an array `pending` that stores the most recent call’s arguments for each millisecond.
3. Iterate `curr_time` from `0` to `max_time`:
   - If there is a call scheduled exactly at `curr_time`, store its arguments as the current pending call.
   - If `curr_time` equals `call.t + t` for the *currently stored* pending call **and** no newer call has arrived in the interval `(call.t, curr_time)`, then execute the function with those arguments and record the result.
4. Return all recorded executions in order.

**Implementation**

```python
from typing import List, Dict, Any

def debounce_brute(fn: Callable[..., Any], t: int, calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not calls:
        return []

    max_time = max(call["t"] for call in calls) + t
    # pending holds the most recent call that has not yet been cancelled/executed
    pending: Dict[str, Any] = {"time": None, "inputs": None}
    output: List[Dict[str, Any]] = []

    for curr in range(max_time + 1):
        # 1️⃣ Register any new calls that happen exactly at this millisecond
        for call in calls:
            if call["t"] == curr:
                pending = {"time": call["t"], "inputs": call["inputs"]}

        # 2️⃣ Check whether the pending call should now fire
        if pending["time"] is not None:
            # The call would fire at pending["time"] + t if not interrupted
            fire_at = pending["time"] + t
            if curr == fire_at:
                # Verify that no newer call arrived after pending["time"] up to now
                interrupted = any(
                    pending["time"] < call["t"] <= curr for call in calls
                )
                if not interrupted:
                    output.append({"t": curr, "inputs": pending["inputs"]})
                    # Clear pending – it has been executed
                    pending = {"time": None, "inputs": None}

    return output
```

**Complexity Analysis**

- Time complexity: O(`max_time` * `calls.length`) → at most O(1000 * 10) = O(10⁴), which is fine for the tiny constraints.  
- Space complexity: O(`calls.length`) for storing the input + O(1) extra → O(1) auxiliary.

---

### Approach 2: Optimized – Cancel‑and‑Reset Timer (Closure + setTimeout)

**Intuition**  
Instead of scanning every millisecond, we can keep track of only the *most recent* call. When a new call arrives, we cancel any previously scheduled execution (if it exists) and schedule a fresh one `t` milliseconds later. This mirrors the real‑world behavior of a debounce: the timer is always reset on fresh input.

**Algorithm**

1. Maintain a variable `timer_id` that holds the identifier of the currently pending `setTimeout`.
2. When the debounced function is invoked:
   - If `timer_id` is not `None`, clear it with `clearTimeout`.
   - Call `setTimeout` to schedule `fn` with the current arguments after `t` ms; store the returned ID in `timer_id`.
3. The scheduled callback will run only if no further call cleared it beforehand.

**Implementation (JavaScript – matches LeetCode expectations)**

```javascript
/**
 * @param {Function} fn
 * @param {number} t   // delay in milliseconds
 * @return {Function}
 */
function debounce(fn, t) {
    let timerId = null;               // holds the active timeout, if any

    return function (...args) {
        // Cancel any previous pending execution
        if (timerId !== null) {
            clearTimeout(timerId);
        }
        // Schedule a new execution after t ms
        timerId = setTimeout(() => {
            fn(...args);
            timerId = null;          // optional: clean up after execution
        }, t);
    };
}
```

**Complexity Analysis**

- Time complexity: O(1) per call – only constant‑time work (`clearTimeout` + `setTimeout`).  
- Space complexity: O(1) – we store a single timer identifier and the closure’s environment.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We trace the execution for Example 1 (`t = 50`, calls at 50 ms and 75 ms).

| Step | Time (ms) | Action                                           | Pending Call (time, inputs) | Timer ID |
|------|-----------|--------------------------------------------------|-----------------------------|----------|
| 0    | 0         | –                                                | None                        | null     |
| 1    | 50        | Call `dlog(1)` → clear none, schedule at 100 ms | (50, [1])                   | id₁      |
| 2    | 75        | Call `dlog(2)` → clear id₁, schedule at 125 ms   | (75, [2])                   | id₂      |
| 3    | 100       | (would have fired id₁, but cleared)             | –                           | –        |
| 4    | 125       | Timer id₂ fires → `fn(2)` executed               | None                        | null     |
| 5    | >125      | No further calls                                 | None                        | null     |

Result: a single execution at **125 ms** with inputs `[2]`, matching the expected output.

---

**Summary**  
- The brute‑force simulation works but is unnecessary overhead.  
- The optimal solution uses a closure to hold a single timer, clearing it on every new call and setting a fresh one.  
- This yields O(1) time per invocation and O(1) extra space, which is the standard implementation for debounce in JavaScript (and easily portable to other languages).