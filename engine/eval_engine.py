# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
# --------------------------------------------------------------------------------------
import os
import re
import numpy as np
from tensorflow.keras import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.models import *
from tensorflow.keras import Sequential
import emoji
from engine import engine
# --------------------------------------------------------------------------------------


class EvalEngine(engine.Engine):
    def __init__(self, model_path='model/model.hdf5'):
        # -----*----- コンストラクタ -----*----- ##
        # set TensorFlow's warning lever
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.__model = self.build_model()


        # load model
        if os.path.exists(model_path):
            self.__model.load_weights(model_path)

    def build_model(self, embed_size=128, max_length=100, filter_sizes=(2, 3, 4, 5), filter_num=64, learning_rate=0.0005):
        input_ts = Input(shape=(max_length, ))

        emb = Embedding(0xffff, embed_size)(input_ts)
        emb_ex = Reshape((max_length, embed_size, 1))(emb)

        convs = []
        for filter_size in filter_sizes:
            conv = Conv2D(filter_num, (filter_size, embed_size), activation='relu')(emb_ex)
            pool = MaxPooling2D((max_length - filter_size + 1 , 1))(conv)
            convs.append(pool)

        convs_merged = Concatenate()(convs)
        reshape = Reshape((filter_num * len(filter_sizes),))(convs_merged)
        fc1 = Dense(64, activation='relu')(reshape)
        bn1 = BatchNormalization()(fc1)
        do1 = Dropout(0.5)(bn1)
        fc2 = Dense(5, activation='softmax')(do1)

        model = Model(
            inputs=[input_ts],
            outputs=[fc2]
        )

        # compile!
        model.compile(
            optimizer=Adam(lr=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=["accuracy"]
        )

        return model

    def eval(self, dajare, max_length=100):
        reading = self.to_reading(dajare)
        for noise in re.findall('[^\u30A1-\u30FF]', reading):
            reading = reading.replace(noise, '')
        print(reading)

        # exclude emoji
        reading = ''.join([ch for ch in reading if ch not in emoji.UNICODE_EMOJI])

        vec = [ord(c) for c in reading]
        # reshape (trimming or padding)
        vec = vec[:max_length]
        if len(vec) < max_length:
            vec += ([0] * (max_length - len(vec)))

        # predict with character level CNN
        pred = self.__model.predict(np.array([vec]))[0]
        bias = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
        bias[np.argmax(pred)] = 0.0
        bias = np.sum(pred * bias) * 10.0
        pred *= np.array([8.4, 0.7, 0.12, 2.3, 0.8])

        # dajare's score (1.0 ~ 5.0)
        score = np.argmax(pred) + bias + 1.0

        while score < 1.0 or score > 5.0:
            if score < 1.0:
                score += abs(bias*0.313)
            if score > 5.0:
                score -= abs(bias*0.313)

        return score

