"""
Resource Manager module - Handles game resources and inventory
"""

from src.core.mfu_algorithm import MFUAlgorithm
from src.entities.resource import Resource

class ResourceManager:
    """Manages the player's inventory and resource collection"""
    
    def __init__(self, inventory_size=6):
        """Initialize the resource manager"""
        self.inventory = []
        self.inventory_size = inventory_size
        self.mfu_algorithm = MFUAlgorithm()
    
    def add_resource(self, resource_type):
        """
        Add a resource to inventory
        If inventory is full, use MFU to replace a resource
        
        Args:
            resource_type (str): Type of resource to add
            
        Returns:
            tuple: (success, replaced_resource, toxic_damage)
                - success (bool): Whether the resource was added
                - replaced_resource (Resource or None): The resource that was replaced, if any
                - toxic_damage (int): Amount of damage from toxic replacement, if any
        """
        # Create new resource
        new_resource = Resource(resource_type)
        
        # If inventory has space, simply add the resource
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(new_resource)
            return True, None, 0
        
        # Inventory is full, use MFU to replace a resource
        replaced_index = self.mfu_algorithm.get_replacement_index(self.inventory)
        replaced_resource = self.inventory[replaced_index]
        
        # Check if replacement is toxic (high counter value)
        toxic_damage = 0
        if replaced_resource.counter > replaced_resource.TOXIC_THRESHOLD:
            toxic_damage = 1  # Player takes 1 damage
        
        # Replace the resource
        self.inventory[replaced_index] = new_resource
        
        return True, replaced_resource, toxic_damage
    
    def use_resource(self, resource_type, amount=1):
        """
        Use resources of specified type from inventory
        
        Args:
            resource_type (str): Type of resource to use
            amount (int): Number of resources to use
            
        Returns:
            bool: Whether the resources were successfully used
        """
        # Find resources of the specified type
        available_resources = [r for r in self.inventory if r.type == resource_type]
        
        # Check if we have enough
        if len(available_resources) < amount:
            return False
        
        # Use the resources (increase their counters)
        for i in range(amount):
            resource = available_resources[i]
            resource.use()  # Increases counter
        
        return True
    
    def apply_aging(self):
        """Apply aging to all resources (divide counters by 2)"""
        for resource in self.inventory:
            resource.apply_aging()
    
    def get_resource_count(self, resource_type):
        """Get count of resources of specified type in inventory"""
        return sum(1 for r in self.inventory if r.type == resource_type)
    
    def clear_inventory(self):
        """Clear the inventory"""
        self.inventory = []