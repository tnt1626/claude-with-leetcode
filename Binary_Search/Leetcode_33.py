"""
Docstring for Leetcode 33

Search in Rotated Sorted Array

You are given an array of length n which was originally sorted in ascending order. 
It has now been rotated between 1 and n times. For example, the array nums = [1,2,3,4,5,6] might become:

[3,4,5,6,1,2] if it was rotated 4 times.
[1,2,3,4,5,6] if it was rotated 6 times.
Given the rotated sorted array nums and an integer target, return the index of target within nums, or -1 if it is not present.

You may assume all elements in the sorted rotated array nums are unique,

A solution that runs in O(n) time is trivial, can you write an algorithm that runs in O(log n) time?

Example 1:

Input: nums = [3,4,5,6,1,2], target = 1

Output: 4
Example 2:

Input: nums = [3,5,6,0,1,2], target = 4

Output: -1
Constraints:

1 <= nums.length <= 1000
-1000 <= nums[i] <= 1000
-1000 <= target <= 1000
All values of nums are unique.
nums is an ascending array that is possibly rotated.

"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        
        """
        Intuition:
        A rotated sorted array consists of two sorted subarrays split at a pivot. 
        At any index, at least one half of the array (left or right of mid) is guaranteed to be sorted. 
        By identifying which half is sorted, we can determine whether the target lies within that half 
        and safely discard the other half—just like binary search.
        
        Approach:
        We apply a modified binary search. At each iteration:
        
        Compute the middle index.
        
        If the middle element equals the target, return its index.
        
        Determine which half of the array is sorted:
        
        If the left half is sorted, check whether the target lies within its bounds.
        
        Otherwise, the right half must be sorted, and we check its bounds.
        
        Narrow the search space to the half that may contain the target.
        
        This process continues until the target is found or the search space is exhausted.
        
        Time Complexity:
        
        O(log n) — the search space is halved at every step, just like standard binary search.
        
        Space Complexity:
        
        O(1) — only constant extra space is used.
        """
        n = len(nums)
        left, right = 0, n - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            
            # Identify which half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1