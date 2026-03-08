#每一個狀態的具體情況
class State:
    def __init__(self, owner):
        self.owner = owner

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

#處理狀態轉變的過程
class StateMachine:
    def __init__(self):
        self.current_state = None

    def change_state(self, new_state_instance):
        if self.current_state:
            self.current_state.exit()
        
        self.current_state = new_state_instance
        
        if self.current_state:
            self.current_state.enter()

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
