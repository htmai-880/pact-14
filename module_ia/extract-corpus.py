import json  # for .json files
import numpy as np  # for .npy files
import csv  # for csv files
import pickle  # for dumping DATABASE

from ingredient_parser.en import parse  # ingredient parser
# {'measure': '2 liters', 'name': 'milk'}

# for training gensim model
from gensim.models import Word2Vec

# load recipes_corpus.pickle if exists
try:
    print("Try loading saved recipes, ingredients,...")
    # useless if not retraining
    # with open('recipes_corpus.pickle', 'rb') as handle:
    #     DATABASE = pickle.load(handle)
    with open('../server/ai/app/ai/model/ingredients_dict.pickle', 'rb') as handle:
        INGREDIENTS = pickle.load(handle)
    with open('ingredients-list.pickle', 'rb') as handle:
        INGREDIENTS_LIST = pickle.load(handle)

except FileNotFoundError:
    DATABASE = []

    # ** EXTRACT .npy files **
    print("Starting npy extraction...")
    INGREDIENTS_LIST = np.load('ingredients.npy', allow_pickle=True).tolist()
    # ['salt' 'pepper' 'butter' ... 'corn flakes cereal']

    recipes = np.load('recipes.npy', allow_pickle=True)
    # [array([ 233, 2754,   42,  120,  560,  345,  150, 2081,   12,   21])
    #  ...
    #  array([ 28,   2, 247,  47,   0,   4, 348,   8])]
    for recipe in recipes:
        DATABASE.append(recipe.tolist())

    print("Building hashtable...")
    INGREDIENTS = {}
    MAX = len(INGREDIENTS_LIST) - 1
    # build hashtable of the ingredients
    for k, ing in enumerate(INGREDIENTS_LIST):
        INGREDIENTS[ing] = k

    # ** EXTRACT 8portions **
    print("Starting 8portions extraction...")
    for file in ['recipes_raw_nosource_ar.json', 'recipes_raw_nosource_epi.json', 'recipes_raw_nosource_fn.json']:
        # read file
        with open('eightportions/' + file, 'r') as f:
            d = json.load(f)
        # parse ingredients and recipe
        for _, v in d.items():
            # print(v['title'])
            # print(v['instructions'])
            try:
                recipe = []
                for ing in v['ingredients']:
                    parsed = parse(ing)['name']
                    k = INGREDIENTS.get(parsed)  # None if key does not exist
                    if k is None:
                        INGREDIENTS[parsed] = MAX + 1
                        INGREDIENTS_LIST.append(parsed)
                        MAX += 1
                        recipe.append(MAX)
                    else:
                        recipe.append(k)
                DATABASE.append(recipe)
            except KeyError:  # some recipe do not have ingredients (ERROR)
                pass


    # ** EXTRACT food.com **
    def parse_text_list(text):
        return [s[1:-1] for s in text[1:-1].split(", ")]


    print("Starting food.com extraction...")
    with open('foodcomrecipes/RAW_recipes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # skip head row
        for row in reader:
            # print(row[0])  # name
            # print(row[9])  # description
            # print(parse_text_list(row[8]))  # steps
            recipe = []
            for ing in parse_text_list(row[10]):  # ingredients
                k = INGREDIENTS.get(ing)  # None if key does not exist
                if k is None:
                    INGREDIENTS[ing] = MAX + 1
                    INGREDIENTS_LIST.append(ing)
                    MAX += 1
                    recipe.append(MAX)
                else:
                    recipe.append(k)
            DATABASE.append(recipe)

    print("Dumping DATABASE (~60Mo)...")
    # dump DATABASE to disk
    # Arrays to save to the file. Since it is not possible for Python to know the names of the arrays outside savez, the arrays will be saved with names “arr_0”, “arr_1”, and so on. These arguments can be any expression.
    with open('recipes_corpus.pickle', 'wb') as handle:
        pickle.dump(DATABASE, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # numpy.savez_compressed(file, *args, **kwds)

    print("Dumping Tokens...")
    with open('../server/ai/app/ai/model/ingredients_dict.pickle', 'wb') as handle:
        pickle.dump(INGREDIENTS, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('ingredients-list.pickle', 'wb') as handle:
        pickle.dump(INGREDIENTS_LIST, handle, protocol=pickle.HIGHEST_PROTOCOL)

# * loading Ingredient2Vec model *
try:
    model = Word2Vec.load('../server/ai/app/ai/model/model.bin')
except FileNotFoundError:
    # train gensim Word2Vec model
    print("Converting DATABASE to string...")
    DATABASE_STR = [[str(x) for x in r] for r in DATABASE]
    print("Training model...")
    # TODO : install Cython to use multiple workers
    model = Word2Vec(DATABASE_STR, size=200, sg=1, window=99, min_count=2)
    # size: (default 100) The number of dimensions of the embedding, e.g. the length of the dense vector to represent each token (word).
    # window: (default 5) The maximum distance between a target word and words around the target word.
    #   use 99 to remove window effect
    # min_count: (default 5) The minimum count of words to consider when training the model; words with an occurrence less than this count will be ignored.
    # workers: (default 3) The number of threads to use while training.
    # sg: skip gram (1), CBOW (0). USE SKI GRAM FOR INFREQUENT INGREDIENTS
    print("Training done.")

    print("Saving model (~4Mo)...")
    # save model to file
    model.wv.save_word2vec_format('../server/ai/app/ai/model/model.bin')

