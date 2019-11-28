from keras import layers
from keras.models import Model

def model(hparams, X, model_name='autoencoder1') :
    tensor = layers.Conv2D(4, (3, 3), activation='relu', padding='same')(X)
    # (64, 64, 4)
    tensor = layers.MaxPooling2D((2, 2), padding='same')(tensor)
    # (32, 32, 4)

    tensor = layers.Conv2D(1, (3, 3), activation='relu', padding='same')(tensor)
    # (32, 32, 1)
    tensor = layers.MaxPooling2D((2, 2), padding='same')(tensor)
    # (16, 16, 1)    

    for_reconstruct = layers.Flatten(name='embeddings')(tensor)

    pold = layers.Reshape((16, 16, 1))(for_reconstruct)
    tensor = layers.UpSampling2D((2, 2))(pold)
    # (32, 32, 1)

    tensor = layers.Deconvolution2D(4, 3, 3, activation='relu', border_mode='same')(tensor)
    tensor = layers.BatchNormalization(momentum=0.9)(tensor)
    # (32, 32, 4)
    tensor = layers.UpSampling2D((2, 2))(tensor)
    # (64, 64, 4)
    
    tensor = layers.Deconvolution2D(1, 3, 3, activation='sigmoid', border_mode='same')(tensor)
    # (64, 64, 1)
    model = Model(X, tensor)
    return model