# Fails 2
def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        from collections import deque
        banned = set(banned)
        arr = tuple(0 if i in banned else (1 if i == p else 0) for i in range(n))
        queue = deque([(arr, p, 0)])  # Add a third element to the tuple to store the number of
        ans = [-1] * n
        visited = set()

        while queue:
            cur_arr, cur_pos, ops = queue.popleft()
            
            if cur_pos not in visited:
                visited.add(cur_pos)
                ans[cur_pos] = ops

                for i in range(n):
                    for j in range(i + k, n + 1):
                        new_arr = cur_arr[:i] + tuple(reversed(cur_arr[i:j])) + cur_arr[j:]
                        new_pos = new_arr.index(1)
                        
                        if new_pos not in banned and (new_arr, new_pos) not in visited:
                            queue.append((new_arr, new_pos, ops + 1))

        return ans

# Fails 1
def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        from collections import deque
        banned = set(banned)
        arr = tuple(0 if i in banned else (1 if i == p else 0) for i in range(n))
        queue = deque([(arr, p, 0)])  # Add a third element to the tuple to store the number of operations
        ans = [-1] * n
        visited = set()

        while queue:
            cur_arr, cur_pos, ops = queue.popleft()
            
            if cur_pos not in visited:
                visited.add(cur_pos)
                ans[cur_pos] = ops

                for i in range(n):
                    for j in range(i + k, n + 1):
                        # Check if the subarray to be reversed contains any banned positions
                        if any(cur_arr[i:x] for x in range(i, j) if x in banned):
                            continue
                        
                        new_arr = cur_arr[:i] + tuple(reversed(cur_arr[i:j])) + cur_arr[j:]
                        new_pos = new_arr.index(1)
                        
                        if new_pos not in banned and (new_arr, new_pos) not in visited:
                            queue.append((new_arr, new_pos, ops + 1))

        return ans