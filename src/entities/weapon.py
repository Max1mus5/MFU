"""
Weapon module - Defines weapon entities
"""

class Weapon:
    """Weapon entity that can be repaired using resources"""
    
    # Weapon states
    STATE_NORMAL = "normal"
    STATE_OXIDIZED = "oxidized"
    STATE_DESTROYED = "destroyed"
    
    def __init__(self, weapon_type, config):
        """
        Initialize a weapon
        
        Args:
            weapon_type (str): Type of weapon (e.g., "pistol", "shotgun")
            config (Config): Game configuration object
        """
        self.type = weapon_type
        self.config = config
        self.weapon_data = config.WEAPONS[weapon_type]
        self.name = self.weapon_data["name"]
        self.requirements = self.weapon_data["requirements"]
        self.points = self.weapon_data["points"]
        self.repaired = False
        self.state = self.STATE_NORMAL
        self.state_timer = 0  # Timer for state changes
    
    def can_repair(self, resource_manager):
        """
        Check if the weapon can be repaired with available resources
        
        Args:
            resource_manager (ResourceManager): Resource manager with inventory
            
        Returns:
            bool: Whether the weapon can be repaired
        """
        for resource_type, amount in self.requirements.items():
            if resource_manager.get_resource_count(resource_type) < amount:
                return False
        return True
    
    def repair(self, resource_manager):
        """
        Repair the weapon using resources from inventory
        
        Args:
            resource_manager (ResourceManager): Resource manager with inventory
            
        Returns:
            bool: Whether the weapon was successfully repaired
        """
        # Check if we have all required resources
        if not self.can_repair(resource_manager):
            return False
        
        # Use resources
        for resource_type, amount in self.requirements.items():
            if not resource_manager.use_resource(resource_type, amount):
                return False
        
        # Mark as repaired
        self.repaired = True
        self.state = self.STATE_NORMAL  # Reset state when repaired
        self.state_timer = 0
        return True
        
    def update_state(self, delta_time):
        """
        Update weapon state based on time
        
        Args:
            delta_time (int): Time elapsed since last update in milliseconds
            
        Returns:
            bool: True if state changed to destroyed, False otherwise
        """
        if self.repaired:
            return False
            
        self.state_timer += delta_time
        
        # Check for state transitions
        if self.state == self.STATE_NORMAL and self.state_timer >= self.config.AGING_INTERVAL:
            self.state = self.STATE_OXIDIZED
            self.state_timer = 0
            return False
        elif self.state == self.STATE_OXIDIZED and self.state_timer >= self.config.AGING_INTERVAL:
            self.state = self.STATE_DESTROYED
            self.state_timer = 0
            return True  # Signal that weapon was destroyed
            
        return False