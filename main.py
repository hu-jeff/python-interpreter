from collections import deque
import dis

class VM:
    def __init__(self):
        self.call_stack = deque()
        self.return = None
        self.exception = None

    def push_frame(self, code, callargs={}, global_namespace=None,\
            local_namespace = None):
        if global_namespace is None:
            if self.call_stack:
                global_namespace = self.call_stack[-1].global_namespace
                local_namespace = {}
            else:
                global_namespace = local_namespace = {
                        '__builtins__': __builtins__,
                        '__name__': '__main__',
                        '__doc__': None,
                        '__package__': None,
                    }

        local_namespace.update(callargs)
        new_frame = StackFrame(code, global_namespace, local_namespace, 
                               self.call_stack[-1])
        self.call_stack.append(new_frame)

    def pop_frame(self):
        return self.call_stack.pop()

class StackFrame:
    def __init__(self, code, local_namespace, global_namespace, calling_frame):
        self.datastack = []
        self.code = code
        self.local_namespace = local_namespace
        self.global_namespace = global_namespace
        self.last_instruction = 0
        self.calling_frame = calling_frame
        self.blockstack = []
