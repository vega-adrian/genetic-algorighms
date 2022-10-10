import numpy as np
import math
import time


exp_len = 10000
vector_len = 15
math_results = []
np_results = []

print('Doing math...')
start_math_time = time.time()
for i in range(exp_len):
    sum_ = np.sum(np.random.rand(1, vector_len))
    start_it_ = time.time()
    math_tanh = math.tanh(sum_)
    math_results.append(time.time() - start_it_)
print(f"Math took {(time.time() - start_math_time)*1000:.4f}ms")
print(f"With an average of {(np.mean(math_results)*1000):.4f}ms")
print(max(math_results))


print('Doing np...')
start_np_time = time.time()
for i in range(exp_len):
    sum_ = np.sum(np.random.rand(1, vector_len))
    start_it_ = time.time()
    math_tanh = np.tanh(sum_)
    np_results.append(time.time() - start_it_)
print(f"Numpy took {(time.time() - start_np_time)*1000:.4f}ms")
print(f"With an average of {(np.mean(np_results)*1000):.4f}ms")
print(max(np_results))