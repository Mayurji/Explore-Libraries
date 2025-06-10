from metaflow import FlowSpec, step, card

class LinearFlow(FlowSpec):

    """
    A simple linear flow that demonstrates the use of a data artifact.
    Each step in the flow can access the data artifact created in the previous step.
    The flow consists of three steps: start, a, and end.
    The start step initializes a data artifact called my_var with the value 'hello world'.
    The a step prints the value of my_var and then proceeds to the end step.
    The end step prints the value of my_var again to demonstrate that it is still accessible.
    """
    @card
    @step
    def start(self):
        self.my_var = 'hello world'
        self.next(self.a)

    @card
    @step
    def a(self):
        print('the data artifact is: %s' % self.my_var)
        self.next(self.end)

    @card
    @step
    def end(self):
        print('the data artifact is still: %s' % self.my_var)

if __name__ == '__main__':
    LinearFlow()