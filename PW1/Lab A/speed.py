from decay import simulate, simulate_loop
import time

t1 = time.perf_counter()
simulate(200000, 0.4)
t2 = time.perf_counter()

t3 = time.perf_counter()
simulate_loop(200000, 0.4)
t4 = time.perf_counter()

print(f"Simulate:\nStart:{t1}\nEnd:{t2}\nSimulate Loop:\nStart:{t3}\nEnd:{t4}")
print(f"NumPy: {(t2-t1)}s\Python: {(t4-t3)}s\n")
print(f"{(t4-t3)/(t2-t1)} times faster")
