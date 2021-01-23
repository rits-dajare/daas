import tensorflow.keras.layers as layers
from tensorflow.keras import Model
from .nnet import NNET


class CNN(NNET):
    def _make(self):
        max_length = 100
        embed_size = 128
        filter_sizes = (2, 3, 4, 5)
        filter_num = 64

        # input layer
        input_ts = layers.Input(shape=(max_length, ))
        emb = layers.Embedding(0xffff, embed_size)(input_ts)
        emb_ex = layers.Reshape((max_length, embed_size, 1))(emb)
        emb_ex = layers.BatchNormalization()(emb_ex)

        # hidden layer
        convs = []
        for size in filter_sizes:
            conv = layers.Conv2D(filter_num, (size, embed_size),
                                 activation='relu')(emb_ex)
            pool = layers.MaxPooling2D((max_length - size + 1, 1))(conv)
            convs.append(pool)

        convs_merged = layers.Concatenate()(convs)
        reshape = layers.Reshape(
            (filter_num * len(filter_sizes),))(convs_merged)
        fc1 = layers.Dense(64, activation='relu')(reshape)
        bn1 = layers.BatchNormalization()(fc1)
        do1 = layers.Dropout(0.5)(bn1)

        # output layer
        fc2 = layers.Dense(1, activation='sigmoid')(do1)
        # fc2 = layers.Dense(5, activation='softmax')(do1)

        result = Model(inputs=[input_ts], outputs=[fc2])
        if self.weight_exists:
            result.load_weights(self.weight_path)
        return result

    def _compile(self):
        self.nnet.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            # loss='sparse_categorical_crossentropy',
            metrics=['accuracy'],
        )
