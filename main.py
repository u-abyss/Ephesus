import csv

import numpy as np
import pandas as pd
from scipy import sparse

u_data_org = pd.read_csv('./u.data', sep='\t', names=['user_id','item_id', 'rating', 'timestamp'])

# ユーザ数✖️アイテム数の配列を作成する(R)
shape = (u_data_org.max().loc['user_id'], u_data_org.max().loc['item_id'])
R = np.zeros(shape)
for i in u_data_org.index:
    row = u_data_org.loc[i]
    R[row['user_id'] -1 , row['item_id'] - 1] = row['rating']

def similarity(item1, item2):
    # item1 と item2 のどちらも評価済であるユーザの集合
    common = np.logical_and(item1 != 0, item2 != 0)

    v1 = item1[common]
    v2 = item2[common]

    sim = 0.0
    # 共通評価者が 2以上という制約にしている
    if v1.size > 1:
        sim = 1.0 - np.cos(v1, v2)

    return sim

def compute_item_similarities(R):
    # n: movie counts
    # return elements in a row (shape[1])
    n = R.shape[1]
    sims = np.zeros((n,n))

    for i in range(n):
        for j in range(i, n):
            if i == j:
                sim = 1.0
            else:
                # R[:, i] は アイテム i に関する全ユーザの評価を並べた列ベクトル
                sim = similarity(R[:,i], R[:,j])

            sims[i][j] = sim
            sims[j][i] = sim

    return sims

sims = compute_item_similarities(R)
print(sims)