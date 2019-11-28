import os, sys, pickle
import numpy as np
import cv2
from time import time
from tqdm import tqdm
from multiprocessing import Process
def readImg(img_file, image_shape = (64, 64)):
    im = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    im = cv2.resize(im, image_shape, cv2.INTER_AREA)
    im = im.reshape((1,)+image_shape+(1,))
    return im / 255.

def read_patent_id_dict(path='patent_three_digit.pkl') :
    with open(path, 'rb') as f:
        patent_dict = pickle.load(f)
    return patent_dict

def load_image(path, n_process, image_shape = (64, 64)) :
    def readImg(image_files, image_shape = (64, 64)):
        for sample, img_file in tqdm(enumerate(image_files)):
            file_path = os.path.join(path, img_file)
            im = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            im = cv2.resize(im, image_shape, cv2.INTER_AREA)
            im = im.reshape((1,)+image_shape+(1,))
            result[sample, :, :, :] = im / 255.
            labels[sample, :] = patent_dict[img_file.split('-')[0][2:]]
    patent_dict = read_patent_id_dict()
    cur_dir = os.getcwd()
    target_path = os.path.join(cur_dir, path)
    image_list = os.listdir(target_path)
    n_images = len(image_list)
    result = np.empty(shape=(n_images,)+image_shape+(1,), dtype=np.float32)
    labels = np.empty(shape=(n_images, 127))
    present_time = time()
    readImg(image_list, image_shape)
    end_time = time()
    print('끝난 시간 : ', end_time - present_time)
    return result, labels

class Dataset :
    def __init__(self, dataset, batch_size=32, shuffle=True) :
        self.dataset = dataset
        self.batch_size = batch_size
        self.n_batchs = int(dataset.shape[0] / self.batch_size)
        self.shuffle = shuffle
        if shuffle :
            self.shuffle_dataset()
        self.idx = 0

    def shuffle_dataset(self) :
        np.random.shuffle(self.dataset)

    def get_batch(self) :
        epoch = 0
        if self.idx > self.n_batchs :
            self.initialize()
            epoch = 1
        batch = self.dataset[self.idx*self.batch_size : (self.idx+1)*self.batch_size]
        self.idx += 1
        return batch, epoch

    def initialize(self) :
        self.shuffle_dataset()
        self.idx = 0

