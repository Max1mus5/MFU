"""
Scene Manager module - Manages game scenes and transitions
"""

class SceneManager:
    """Manages different game scenes and transitions between them"""
    
    def __init__(self):
        """Initialize the scene manager"""
        self.scenes = {}
        self.active_scene = None
    
    def add_scene(self, scene_id, scene):
        """
        Add a scene to the manager
        
        Args:
            scene_id (str): Unique identifier for the scene
            scene (Scene): Scene object to add
        """
        self.scenes[scene_id] = scene
    
    def set_active_scene(self, scene_id):
        """
        Set the active scene
        
        Args:
            scene_id (str): ID of scene to activate
            
        Returns:
            bool: Whether the scene was successfully activated
        """
        if scene_id in self.scenes:
            # If there's a current scene, exit it
            if self.active_scene:
                self.active_scene.on_exit()
            
            # Set and enter new scene
            self.active_scene = self.scenes[scene_id]
            self.active_scene.on_enter()
            
            # Start playing the appropriate background music
            # We need to access the game instance from the scene
            if hasattr(self.active_scene, 'game'):
                self.active_scene.game.play_background_music(scene_id)
                
            return True
        
        return False
    
    def handle_event(self, event):
        """
        Pass event to active scene
        
        Args:
            event: Pygame event to handle
        """
        if self.active_scene:
            self.active_scene.handle_event(event)
    
    def update(self):
        """Update the active scene"""
        if self.active_scene:
            self.active_scene.update()
    
    def draw(self, surface):
        """
        Draw the active scene
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.active_scene:
            self.active_scene.draw(surface)