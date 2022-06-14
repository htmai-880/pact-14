from gensim.models import KeyedVectors
import numpy as np

INGREDIENTS_LIST = np.load('ingredients.npy', allow_pickle=True).tolist()
model = KeyedVectors.load_word2vec_format('../server/ai/app/ai/model/model.bin')

i = 0
for i, ing in enumerate(INGREDIENTS_LIST):
    print(ing + ' : ')
    for v in model.most_similar(positive=str(i), topn=10):
        print(f'{INGREDIENTS_LIST[int(v[0])]} : {v[1]}')
    i += 1
    if i == 10:
        exit()
