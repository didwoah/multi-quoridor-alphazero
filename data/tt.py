import pickle
import os
from pathlib import Path

#병합
history_path0 = sorted(Path('./data').glob('*.history'))[0]
history_path1 = sorted(Path('./data').glob('*.history'))[1]

with history_path0.open(mode='rb') as f:
    first = pickle.load(f)
    with history_path1.open(mode='rb') as ff:
        second = pickle.load(ff)

        summed = first + second

        print(len(first))
        print(len(second))
        print(len(summed))

        os.makedirs('./data/', exist_ok=True)
        path = './data/20231013.history'
        with open(path, mode='wb') as fff:
            pickle.dump(summed, fff)

# #검증
# history_path0 = sorted(Path('./data').glob('*.history'))[0]
# history_path1 = sorted(Path('./data').glob('*.history'))[1]
# history_path2 = sorted(Path('./data').glob('*.history'))[2]
    
# with history_path0.open(mode='rb') as f:
#     lst = pickle.load(f)
#     print(len(lst))

# with history_path1.open(mode='rb') as f:
#     lst = pickle.load(f)
#     print(len(lst))

# with history_path2.open(mode='rb') as f:
#     lst = pickle.load(f)
#     print(len(lst))