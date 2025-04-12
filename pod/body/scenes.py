import time

scenes = {
    0: "none",
    1: "abort",
    2: "test",
    3: "init",
    4: "happy",
    5: "sad",
    6: "emergency",
    7: "photo"
}

color_ref = {
    "none":   (0, 0, 0),        # 000
    "abort": (0, 0, 255),      # 001
    "test": (0, 255, 0),      # 010
    "init": (0, 255, 255),    # 011
    "happy": (255, 0, 0),      # 100
    "sad": (255, 0, 255),    # 101
    "emergency": (255, 255, 0),    # 110
    "photo": (255, 255, 255)   # 111
}


def get_scene_from_input(num: int) -> str:
    return scenes.get(num)

def get_scene_color(scene: str) -> tuple[int]:
    return color_ref.get(scene, (0, 0, 0))


class BaseController():
    name = 'base'
    config = {}

    current_scene = 'none'
    current_config = {}
    last_scene = 'none'
    next_scene = 'none'

    scene_duration = 0

    def __init__(self):
        pass

    def set_scene(self, scene: str):
        """ When we detect a change of input that results in a new scene,
            this function will be called.
        """
        if scene == self.current_scene:
            return
        
        self.last_scene = self.current_scene
        self.current_scene = scene
        print(f'changing scene from {self.last_scene} to {self.current_scene}')

        self.init_scene()

    def init_scene(self):
        """ Set any initial conditions for a newly entered scene
        """
        config = self.config.get(self.current_scene, {})
        self.next_scene = config.get('next') or 'none'
        self.scene_duration = config.get('duration') or 0
        self.current_config = config

    def exit_scene(self):
        self.scene_duration = 0

        if self.next_scene != 'none':
            self.set_scene(self.next_scene)
        else:
            self.current_scene = 'none'
            self.next_scene = 'none'
            self.current_config = {}

    def update(self):
        """ Run a single iteration of the main loop, for the 
            given scene parameter.
        """
        pass

    def post_update(self):
        pass
