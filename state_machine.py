#每一個狀態的具體情況
class State:
    def __init__(self, owner):
        self.owner = owner

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, events = None):
        pass

    def draw(self, screen):
        pass

#處理狀態轉變的過程
class StateMachine:
    def __init__(self, owner=None):
        self.owner = owner
        self.current_state = None
        self.states = {}

    def add_state(self, state_name, state_instance):
        self.states[state_name] = state_instance

    def change_state(self, state_name):
        if state_name not in self.states:
            print(f"Warning: State '{state_name}' not found in StateMachine.")
            return

        if self.current_state:
            self.current_state.exit()
        
        self.current_state = self.states[state_name]
        
        if self.current_state:
            self.current_state.enter()

    def update(self, events = None):
        if self.current_state:
            self.current_state.update(events)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
