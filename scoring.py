import numpy as np
import pickle
import matplotlib.pyplot as plt

DICT_FILE = 'user_scores_dict.pkl'
ACCURACY_PLOT_FILE = 'accuracy.png'
SCORES_PLOT_FILE = 'scores.png'

def store_score(beta, x, L, U, user=''):
    def compute_score(beta, x, L, U):
        s_max, s_min, delta, c = 10, -((10 * np.log(99 / 50)) / np.log(50)), 0.4, 100
        def s0_dist(beta, x, L, U):
            s, r, t = (L - x) / c, (U - L) / c, (x - U) / c
            score = t * (-2 / (1 - beta) - s / (1 + t))
            if x < L:
                score = r * (-2 / (1 - beta) - s / (1 + r))
            elif x <= U:
                score = 4 * s_max * r * t / s ** 2 * (1 - s / (1 + s))
            return score
        return max(s0_dist(beta, x, L - delta, U + delta), s_min)

    with open(DICT_FILE, 'rb') as f:
        user_scores_dict = pickle.load(f)
    
    key = user + '_' + str(beta)
    
    if key + '_scores' in user_scores_dict:
        user_scores_dict[key + '_scores'] = user_scores_dict[key + '_scores'].append([compute_score(beta, x, L, U)])
    else:
        user_scores_dict[key + '_scores'] = [[compute_score(beta, x, L, U)]]
    
    n, is_correct = len(user_scores_dict[key + '_scores']), 1 if x >= L and x <= U else 0
    if key + '_accuracy' in user_scores_dict:
        user_scores_dict[key + '_accuracy'] = (user_scores_dict[key + '_accuracy'] * n + is_correct) / (n + 1)
    else:
        user_scores_dict[key + '_accuracy'] = is_correct

    with open(DICT_FILE, 'wb') as f:
        pickle.dump(user_scores_dict, f)

def store_plots(user=''):
    with open(DICT_FILE, 'rb') as f:
        user_scores_dict = pickle.load(f)

    betas, scores, accuracies = [0.5, 0.6, 0.7, 0.8, 0.9], [], []
    for beta in betas:
        key = user + '_' + str(beta)
        scores.extend(user_scores_dict[key + '_scores'])
        accuracies.append(user_scores_dict[key + '_accuracy'])

    plt.figure(figsize=(8, 8))
    plt.scatter(x=betas, y=accuracies, c='b')
    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.xlabel('confidence level')
    plt.ylabel('your accuracy')
    plt.savefig(ACCURACY_PLOT_FILE, dpi=300)

    plt.figure(figsize=(8, 8))
    plt.hist(x=scores, bins=35, c='b')
    plt.xlim((-60, 10))
    plt.xlabel('score')
    plt.ylabel('frequency')
    plt.savefig(SCORES_PLOT_FILE, dpi=300)