from os import getenv
import pickle
from pathlib import Path

from gensim.models import KeyedVectors


class Model:
    def __init__(self):
        if getenv("MODEL_PATH") is not None:
            base_path = Path(getenv("MODEL_PATH"))
        else:
            base_path = Path(__file__).parent / "model"

        with open(base_path / 'ingredients_dict.pickle', 'rb') as handle:
            # noinspection PickleLoad
            self.ingredients_dict = pickle.load(handle)
        with open(base_path / 'tokens2names.pickle', 'rb') as handle:
            # noinspection PickleLoad
            self.tokens2names = pickle.load(handle)

        self.model = KeyedVectors.load_word2vec_format(base_path / 'model.bin')

    def most_similar(self, name):
        try:
            return self.model.most_similar(positive=[str(self.ingredients_dict[name])], topn=1)[0]
        except KeyError:
            return [None, None]

    def get_name_from_token(self, token: str):
        return self.tokens2names[int(token)]
