import time

t0 = time.time()
a = 2000
for i in range(a):
    for j in range(a):
            for k in range(a):
                continue

t1 = time.time()

print("Time elapsed: ", t1 - t0)
