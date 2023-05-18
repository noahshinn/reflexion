
def timeout_handler(_, __):
    raise TimeoutError()

import os, json
def to_jsonl(dict_data, file_path):
    with open(file_path, 'a') as file:
        json_line = json.dumps(dict_data)
        file.write(json_line + os.linesep)

from threading import Thread
class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
    

def function_with_timeout(func, args, timeout):
    result_container = []

    def wrapper():
        result_container.append(func(*args))

    thread = PropagatingThread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError()
    else:
        return result_container[0]
    
# Py tests

# if __name__ == "__main__":
#     formatter = PySubmissionFormatter()
#     leetcode_1 = 'class Solution:\n    def solveSudoku(self, board: List[List[str]]) -> None:\n        """\n        Do not return anything, modify board in-place instead.\n        """\n        '
#     humaneval_1 = 'def solveSudoku(self, board: List[List[str]]) -> None:\n        """\n        Do not return anything, modify board in-place instead.\n        """\n'

#     assert leetcode_1 == formatter.to_leetcode(humaneval_1)
#     assert humaneval_1 == formatter.to_humaneval(leetcode_1)




