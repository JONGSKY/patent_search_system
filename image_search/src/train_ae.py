from load_images import load_image, Dataset
from autoencoder import model
import pickle, time, argparse, os, sys, json
from PIL import Image
import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.layers import Input
from keras.optimizers import Adam
from keras.models import Model
from keras.callbacks import Callback
import keras.backend.tensorflow_backend as K

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--image_dir', type=str, default='patent_images')
parser.add_argument('--n_process', type=int, default=6)
parser.add_argument('--data_load', default='True')
parser.add_argument('--learning_rate', type=float, default=0.001)
parser.add_argument('--save_every', type=int, default=1000)
parser.add_argument('--run_name', type=str, default='run1')
parser.add_argument('--print_every', type=int, default=100)
parser.add_argument('--embd_dim', type=int, default=768)
parser.add_argument('--shape', default=(64, 64))
parser.add_argument('--epochs', default = 100, type = int)
parser.add_argument('--reconstruct_every', default=5, type=int)
CHECKPOINT_DIR = 'ckpt_dir'

def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def main() :
    args = parser.parse_args()
    learning_rate = args.learning_rate
    if args.data_load == 'True' :
        images = np.load('images.npy')
        labels = np.load('labels.npy')
    elif args.data_load == 'False' :
        dataset = load_image(args.image_dir, args.n_process, args.shape)
        images, labels = dataset
        np.save('images.npy', images)
        np.save('labels.npy', labels)
    else : 
        print('Data load 인자 확인요망')
        return
    print('Dataset Shape :', images.shape)
    counter = 1
    epoch = 1
    counter_path = os.path.join(CHECKPOINT_DIR, args.run_name, 'counter.json')
    if os.path.exists(counter_path) :
        with open(counter_path, 'r') as f :
            ce = json.load(f)
            counter = ce['counter']
            epoch = ce['epoch']
    model_path = os.path.join(CHECKPOINT_DIR, args.run_name, 'best_model.h5')
    mckpt = ModelCheckpoint(filepath = model_path, monitor = 'val_loss', verbose = 1, save_best_only = True)
    input_image = Input(shape=args.shape+(1,))
    c_ae = model(args, input_image)
    c_ae.compile(optimizer = Adam(lr=args.learning_rate), loss = 'binary_crossentropy')
    c_ae.summary()
    # images = images / 255.
    c_ae.fit(images, images,
            batch_size = args.batch_size,
            epochs = args.epochs,
            shuffle = True,
            validation_split = 0.2,
            callbacks = [mckpt, SampleAndReconstruct(args)])

class SampleAndReconstruct(Callback) :
    def __init__(self, args) :
        self.args = args

    def set_model(self, model) :
        self.model = model

    def on_epoch_end(self, epoch, logs = None) :
        if epoch % self.args.reconstruct_every == 0:
            n_val = self.validation_data[0].shape[0]
            idx = np.random.choice(n_val-1, 1)[0]
            sample = self.validation_data[0][idx:idx+1]
            output = self.model.predict(sample)
            sample = (sample * 255).reshape(self.args.shape).astype('uint8')
            output = (output * 255).reshape(self.args.shape).astype('uint8')
            origin = Image.fromarray(sample, mode = 'L')
            reconstructed = Image.fromarray(output, mode = 'L')
            image_path = os.path.join(CHECKPOINT_DIR, self.args.run_name, 'sample')
            origin.save(os.path.join(image_path, 'Origin_epoch_{}.png'.format(epoch)))
            reconstructed.save(os.path.join(image_path, 'Reconstructed_epoch_{}.png'.format(epoch)))


if __name__ == '__main__' :
    main()