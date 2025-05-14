"""
MFU Algorithm module - Implements the Most Frequently Used replacement algorithm
"""

class MFUAlgorithm:
    """
    Most Frequently Used (MFU) replacement algorithm
    Tracks usage frequency of resources and replaces the most frequently used
    """
    
    def __init__(self):
        """Initialize the MFU algorithm"""
        pass
    
    def get_replacement_index(self, resources):
        """
        Determine which resource to replace based on MFU algorithm
        
        Args:
            resources (list): List of Resource objects
            
        Returns:
            int: Index of resource to replace
        """
        if not resources:
            return -1
        
        # Find resource with highest counter (most frequently used)
        max_counter = -1
        max_index = -1
        print("MFUAlgorithm: get_replacement_index called")
        
        # Print resources with useful information
        print("Resources:")
        for i, resource in enumerate(resources):
            print(f"  [{i}] Type: {resource.type}, Counter: {resource.counter}")
        
        for i, resource in enumerate(resources):
            if resource.counter > max_counter:
                max_counter = resource.counter
                max_index = i
                print(f"New max counter found: {max_counter} at index {max_index} (Type: {resource.type})")
        
        if max_index >= 0:
            print(f"Selected resource for replacement: [{max_index}] Type: {resources[max_index].type}, Counter: {resources[max_index].counter}")
        else:
            print("No resource selected for replacement")
            
        return max_index