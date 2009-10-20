from pyre.components.Component import Component

class ForcefieldLoader(Component):
    
    def __init__(self, name='manualEntry', facility='forcefield'):
        Component.__init__(self, name, facility)
    
    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text