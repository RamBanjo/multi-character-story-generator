def remove_exceeding_elements_in_place(lst, x):
    """
    Removes all elements from the list that exceed the value x in place.
    
    Parameters:
    lst (list): The list from which elements are to be removed.
    x (int or float): The threshold value.
    
    Returns:
    None
    """
    lst[:] = [element for element in lst if element <= x]

# Example usage
original_list = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
ref = original_list
threshold = 5
remove_exceeding_elements_in_place(ref, threshold)
print(original_list)  # Output: [1, 3, 5, 2, 4]