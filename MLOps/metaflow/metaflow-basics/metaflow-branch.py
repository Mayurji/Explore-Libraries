from metaflow import FlowSpec, step

class BranchFlow(FlowSpec):
    """
    A simple flow that demonstrates the use of branches and joins.
    The flow consists of a start step, two branches (a and b), and a join step.
    The start step initializes a data artifact called x with the value 0.
    The a and b steps set the value of x to 1 and 2, respectively.
    The join step prints the values of x from both branches and calculates the total.
    Finally, the end step is reached.
    The flow demonstrates how to use branches and joins to create parallel execution paths.
    """
    
    @step
    def start(self):
        self.next(self.a, self.b)

    @step
    def a(self):
        self.x = 1
        self.next(self.join)

    @step
    def b(self):
        self.x = 2
        self.next(self.join)

    @step
    def join(self, inputs):
        #Metaflow can execute a and b over multiple CPU cores or over multiple instances in the cloud.
    
        print('a is %s' % inputs.a.x)
        print('b is %s' % inputs.b.x)
        print('total is %d' % sum(input.x for input in inputs))
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    BranchFlow()