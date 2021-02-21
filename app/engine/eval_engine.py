from functools import lru_cache
import numpy as np
from .engine import Engine
from .nnet.cnn import CNN


class EvalEngine(Engine):
    def _sub_init(self):
        self.score_cache = []

        self.__max_length = 100
        self.__nnet = CNN()

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        text = self.text_service.cleaned(text)

        # 曖昧キャッシュを確認
        for cache in self.score_cache:
            if cache['text'] in text or text in cache['text']:
                return cache['score']

        # スコア化
        katakana = self.text_service.katakanize(text, False)
        vec = self.text_service.conv_vector(katakana, self.__max_length)
        score = self.__eval(vec)

        # 曖昧キャッシュ
        if len(self.score_cache) >= 10:
            self.score_cache.pop(0)
            self.score_cache[-1] = {'text': text, 'score': score}
        else:
            self.score_cache.append({'text': text, 'score': score})

        return score

    def __eval(self, vec):
        np.random.seed(sum(vec))
        result = np.random.normal(2, 1.3) + 1.0
        if result > 5.0:
            return 5.0 - np.random.rand() / 5
        return result

        # pred = self.nnet.predict(np.array([vec]))
        # result = abs((pred[0] - 0.5638) / 0.02292)
        # result = result * 4.0 + 1.0

        # while result < 1.0 or result > 5.0:
        #     if result < 1.0:
        #         result += 2.0
        #     if result > 5.0:
        #         result -= 2.5

        # return result

    def train(self, data):
        # data: [text:str, score:float]
        import tqdm

        x = []
        y = []
        print('データセットを作成...')
        for row in tqdm.tqdm(data):
            katakana = self.text_service.katakanize(row[0], False)
            x.append(self.text_service.conv_vector(
                katakana, self.__max_length))
            y.append(row[1] / 5.0)

        self.nnet.train(
            np.array(x),
            np.array(y),
        )

    @property
    def nnet(self):
        return self.__nnet
