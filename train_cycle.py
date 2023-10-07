from quoridor.model import resnet
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network
from evaluate_best_player import evaluate_best_player

resnet()
for i in range(10):
    print('Train', i, '===============')
    self_play()


    train_network()


    update_best_player = evaluate_network()

    if update_best_player:
        evaluate_best_player()