import os
import numpy as np
from . import engine


class EvalEngine(engine.Engine):
    def _setup(self):
        self.score_cache = []

        self.__max_length = 100
        self.__model = self.nnet()

    def nnet(self, weight_path='ckpt/cnn.h5'):
        from .nnet import cnn

        result = cnn.nnet(max_length=self.__max_length)
        if os.path.exists(weight_path):
            result.load_weights(weight_path)
        else:
            raise Exception('学習済みモデル%sが存在しません' % weight_path)

        return result

    def eval(self, text):
        # キャッシュを確認
        for cache in self.score_cache:
            if cache['text'] in text or text in cache['text']:
                return cache['score']

        vec = self.__text_to_vector(text)

        # スコア化
        pred = self.__model.predict(np.array([vec]))[0]
        bias = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
        bias[np.argmax(pred)] = 0.0
        bias = np.sum(pred * bias) * 10.0
        pred *= np.array([8.4, 0.7, 0.12, 2.3, 0.8])
        score = np.argmax(pred) + bias + 1.0

        while score < 1.0 or score > 5.0:
            if score < 1.0:
                score += abs(bias*0.313)
            if score > 5.0:
                score -= abs(bias*0.313)

        # キャッシュ
        if len(self.score_cache) >= 10:
            self.score_cache.pop(0)
            self.score_cache[-1] = {'text': text, 'score': score}
        else:
            self.score_cache.append({'text': text, 'score': score})

        return score

    def __text_to_vector(self, text):
        reading = self.to_reading(text)

        # 文字コードのベクトルに変換
        result = list(map(ord, reading))
        # トリミング
        result = result[:self.__max_length]
        # パディング
        result += [0] * (self.__max_length - len(result))

        return result
