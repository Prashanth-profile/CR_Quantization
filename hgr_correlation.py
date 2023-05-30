import numpy as np


def calculate_hgr_correlation(X, Y):
    ranks_X = np.argsort(X).argsort() + 1
    ranks_Y = np.argsort(Y).argsort() + 1

    avg_rank_X = np.mean(ranks_X)
    avg_rank_Y = np.mean(ranks_Y)

    numerator = np.sum((ranks_X - avg_rank_X) * (ranks_Y - avg_rank_Y))
    denominator = np.sqrt(np.sum((ranks_X - avg_rank_X) ** 2) * np.sum((ranks_Y - avg_rank_Y) ** 2))

    hgr_correlation = numerator / denominator

    return hgr_correlation


# Example usage
X = [5, 2, 8, 4, 7]
Y = [6, 4, 11, 8, 12]

hgr_corr = calculate_hgr_correlation(X, Y)
print("HGR correlation:", hgr_corr)
