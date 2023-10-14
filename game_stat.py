import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import random

import sys
sys.path.append("../")

from game import State

class TestState(State):
    def is_draw(self):
        return self.turn > 1000
    
def play(state: TestState):
    legal_actions = state.legal_actions()
    if len(legal_actions) == 0:
        return state.next(None)
    else:
        return state.next(random.choice(legal_actions))

repeat = 1000
turn_list = []

for i in tqdm(range(repeat)):
    state = TestState()

    while not state.is_done():
        for _ in range(4):
            state = play(state)
            if state.is_done():
                break

    turn_list.append(state.turn)

## Save pickle
with open("turn_distribution.pickle","wb") as fw:
    pickle.dump(turn_list, fw)
 
## Load pickle
# with open("turn_distribution.pickle","rb") as fr:
#     data = pickle.load(fr)

plt.boxplot(turn_list, vert=False)
plt.title("turn distribution box plot")
plt.xlabel("turn")
plt.savefig("turn_distribution_box_plot")
plt.close()

plt.hist(turn_list)
plt.title("turn distribution hist")
plt.xlabel("turn")
plt.ylabel("count")
plt.savefig("turn_distribution_hist")
plt.close()

sns.kdeplot(turn_list)
plt.title("turn distribution kde")
plt.xlabel("turn")
plt.ylabel("density")
plt.savefig("turn_distribution_kde")

