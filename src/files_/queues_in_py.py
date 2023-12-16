from collections import deque

q = deque()
q.append(1)
q.append(2)

print(q)
w = q.popleft()
print(w)
print(q)
