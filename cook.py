import json
import random
from itertools import permutations

from main import Flow

if __name__ == '__main__':
    f = Flow()
    data = f.generate_seed()
    a = json.loads(data.decode())
    # print(a)

    for i, j in enumerate(a):
        print(j)
        # print(a[j])
        # print(type(a[j]))
        f.do_work(a[j])
    # for i in data.decode():
    #     print(i)
