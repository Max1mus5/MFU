"""
Resource module - Defines resource entities
"""

class Resource:
    """Resource entity that can be collected and used in crafting"""
    
    # Class constants
    COUNTER_INCREMENT = 8  # How much counter increases when used
    TOXIC_THRESHOLD = 64   # Counter value above which removal is toxic
    
    def __init__(self, resource_type):
        """
        Initialize a resource
        
        Args:
            resource_type (str): Type of resource ("nut", "circuit", "cell", "core")
        """
        self.type = resource_type
        self.counter = 0  # Usage counter (0-255)
    
    def use(self):
        """
        Use the resource, increasing its counter
        
        Returns:
            bool: Whether the counter was successfully increased
        """
        if self.counter < 255:  # 8-bit counter max
            self.counter += self.COUNTER_INCREMENT
            return True
        return False
    
    def apply_aging(self):
        """
        Apply aging to the resource (divide counter by 2)
        Simulates oxidation/degradation over time
        """
        self.counter //= 2