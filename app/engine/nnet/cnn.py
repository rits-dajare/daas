import os
import tensorflow.keras.layers as layers
from tensorflow.keras import Model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def nnet(max_length=100, embed_size=128, filter_sizes=(2, 3, 4, 5), filter_num=64):
    input_ts = layers.Input(shape=(max_length, ))

    emb = layers.Embedding(0xffff, embed_size)(input_ts)
    emb_ex = layers.Reshape((max_length, embed_size, 1))(emb)
    emb_ex = layers.BatchNormalization()(emb_ex)

    convs = []
    for size in filter_sizes:
        conv = layers.Conv2D(filter_num, (size, embed_size),
                             activation='relu')(emb_ex)
        pool = layers.MaxPooling2D((max_length - size + 1, 1))(conv)
        convs.append(pool)

    convs_merged = layers.Concatenate()(convs)
    reshape = layers.Reshape((filter_num * len(filter_sizes),))(convs_merged)
    fc1 = layers.Dense(64, activation='relu')(reshape)
    bn1 = layers.BatchNormalization()(fc1)
    do1 = layers.Dropout(0.5)(bn1)
    #fc2 = layers.Dense(5, activation='softmax')(do1)
    fc2 = layers.Dense(1, activation='sigmoid')(do1)

    return Model(inputs=[input_ts], outputs=[fc2])


def compile(model):
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        #loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )

    return model
