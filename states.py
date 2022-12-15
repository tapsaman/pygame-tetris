from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self):
        self.canReEnter = False

    @abstractmethod
    def Enter(self, arguments = None): pass
    
    @abstractmethod
    def Update(self): pass

    @abstractmethod
    def Exit(self): pass

class DrawState(State):
    @abstractmethod
    def Draw(self): pass

class StateMachine:
    def __init__(self, initialStateKey : str, states : dict):
        self.states = states
        self.currentStateKey = initialStateKey
        self.currentState = self.states[initialStateKey]
    
    def TransitionTo(self, stateKey : str, arguments : dict = None):
        if self.states[stateKey] == self.currentState \
        and self.currentState.canReEnter != True:
            return
        
        self.currentState.Exit()
        self.currentStateKey = stateKey
        self.currentState = self.states[stateKey]
        self.currentState.Enter()
    
    def Update(self):
        self.currentState.Update()
    
    def Draw(self):
        self.currentState.Draw()
