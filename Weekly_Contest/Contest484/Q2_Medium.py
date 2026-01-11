"""
Docstring for Q2. Number of Centered Subarrays

You are given an integer array nums.

A subarray of nums is called centered if the sum of its elements is equal to at least one element within that same subarray.

Return the number of centered subarrays of nums.

 

Example 1:

Input: nums = [-1,1,0]

Output: 5

Explanation:

All single-element subarrays ([-1], [1], [0]) are centered.
The subarray [1, 0] has a sum of 1, which is present in the subarray.
The subarray [-1, 1, 0] has a sum of 0, which is present in the subarray.
Thus, the answer is 5.
Example 2:

Input: nums = [2,-3]

Output: 2

Explanation:

Only single-element subarrays ([2], [-3]) are centered.

 

Constraints:

1 <= nums.length <= 500
-105 <= nums[i] <= 105

Note: Please do not copy the description during the contest to maintain the integrity of your submissions.

"""

# Coding Section

from typing import List

class Solution:
    def centeredSubarrays(self, nums: List[int]) -> int:
        """
        Count the number of centered subarrays in an integer array.

        Intuition:
        A subarray is centered if its sum equals at least one of its elements.
        We can check all subarrays efficiently by tracking the running sum and
        the elements seen so far within the subarray.

        Approach:
        - Iterate through all possible subarray starting indices.
        - For each start index, expand the subarray to the right.
        - Keep a running sum of elements and a set/dictionary of elements seen.
        - If the running sum matches any element in the current subarray, increment count.

        Complexity:
        - Time: O(N^2), where N is the length of nums, due to checking all subarrays.
        - Space: O(N) for the dictionary storing elements in the current subarray.

        Returns:
            int: Total number of centered subarrays.
        """
        n = len(nums)
        count = 0

        for l in range(n):
            current_sum = 0
            seen = {}  # dictionary to store elements 

            for r in range(l, n):
                val = nums[r]
                current_sum += val
                seen[val] = 1  # mark element as seen

                if current_sum in seen:
                    count += 1

        return count
