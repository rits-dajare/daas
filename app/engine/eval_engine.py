import os
import numpy as np
from . import engine


class EvalEngine(engine.Engine):
    def _sub_init(self):
        self.score_cache = []

        self.__max_length = 100
        self.__model = self.nnet()

    def nnet(self, weight_path='ckpt/cnn.h5'):
        from .nnet import cnn

        result = cnn.nnet(max_length=self.__max_length)
        result = cnn.compile(result)
        if os.path.exists(weight_path):
            result.load_weights(weight_path)
        else:
            raise Exception('学習済みモデル%sが存在しません' % weight_path)

        return result

    def execute(self, text, use_api=True):
        # キャッシュを確認
        for cache in self.score_cache:
            if cache['text'] in text or text in cache['text']:
                return cache['score']

        # スコア化
        katakana = self.text_service.katakanize(text, False)
        vec = self.text_service.conv_vector(katakana, self.__max_length)
        score = self.__eval(vec)

        # キャッシュ
        if len(self.score_cache) >= 10:
            self.score_cache.pop(0)
            self.score_cache[-1] = {'text': text, 'score': score}
        else:
            self.score_cache.append({'text': text, 'score': score})

        return score

    def __eval(self, vec):
        pred = self.__model.predict(np.array([vec]))[0]
        result = abs((pred[0] - 0.5638) / 0.02292)
        result = result * 4.0 + 1.0

        while result < 1.0 or result > 5.0:
            if result < 1.0:
                result += 2.0
            if result > 5.0:
                result -= 2.5

        return result

    def train(self, data, weight_path='ckpt/cnn.h5'):
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

        self.__model.fit(
            np.array(x),
            np.array(y),
            batch_size=64,
            epochs=20,
            validation_split=0.1,
        )

        self.__model.save_weights(weight_path)
