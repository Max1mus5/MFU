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
        
        for i, resource in enumerate(resources):
            if resource.counter > max_counter:
                max_counter = resource.counter
                max_index = i
        
        return max_index