from typing import List, Tuple, Optional

def binary_search_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return (iterations, upper_bound)

# Test the function
sample_array = [1.1, 2.3, 3.5, 4.7, 5.9, 6.6, 7.8]
target_value = 4
print(binary_search_upper_bound(sample_array, target_value))
