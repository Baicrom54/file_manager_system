from collections import deque

def appender():
    stack=deque([])
    def append_stack(record_dict=None):
        nonlocal stack
        if record_dict:
            stack.append(record_dict)
        return stack





                    

                


