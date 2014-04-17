import printrun_interface

class core_interface:

    def __init__(self, func=None):
        self.name = 'core'
        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        print(self.name)



    