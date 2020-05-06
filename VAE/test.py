import os
from glob import glob
import numpy as np

from models.VAE import VariationalAutoencoder
from keras.preprocessing.image import ImageDataGenerator

# run params
section = "vae"
run_id = "0001"
# data 이름
data_name = "shirts"
if not os.path.exists("test_run/"):
    os.mkdir("test_run/")
    os.mkdir(os.path.join("test_run/", section))
RUN_FOLDER = "test_run/{}/".format(section)
RUN_FOLDER += "_".join([run_id, data_name])

if not os.path.exists(RUN_FOLDER):
    os.mkdir(RUN_FOLDER)
    os.mkdir(os.path.join(RUN_FOLDER, "viz"))
    os.mkdir(os.path.join(RUN_FOLDER, "images"))
    os.mkdir(os.path.join(RUN_FOLDER, "weights"))

mode = "load"  #'load' #

# input data folder path
DATA_FOLDER = "./data/"

INPUT_DIM = (128, 128, 3)
BATCH_SIZE = 32

filenames = np.array(glob(os.path.join(DATA_FOLDER, "*/*.jpg")))

NUM_IMAGES = len(filenames)

vae = VariationalAutoencoder(
    input_dim=INPUT_DIM,
    encoder_conv_filters=[16, 64, 64, 64],
    encoder_conv_kernel_size=[3, 3, 3, 3],
    encoder_conv_strides=[2, 2, 2, 2],
    decoder_conv_t_filters=[32, 32, 16, 3],
    decoder_conv_t_kernel_size=[3, 3, 3, 3],
    decoder_conv_t_strides=[2, 2, 2, 2],
    z_dim=50,
    use_batch_norm=False,
    use_dropout=False,
)

if mode == "build":
    vae.save(RUN_FOLDER)
else:
    vae.load_weights("./weights/weights.h5")

print(vae.encoder.summary())
print(vae.decoder.summary())

# LEARNING_RATE = 0.0005
# R_LOSS_FACTOR = 10000
# EPOCHS = 200
# PRINT_EVERY_N_BATCHES = 100
# INITIAL_EPOCH = 0
# vae.compile(LEARNING_RATE, R_LOSS_FACTOR)
# vae.train_with_generator(
#     data_flow
#     , epochs = EPOCHS
#     , steps_per_epoch = NUM_IMAGES / BATCH_SIZE
#     , run_folder = RUN_FOLDER
#     , print_every_n_batches = PRINT_EVERY_N_BATCHES
#     , initial_epoch = INITIAL_EPOCH
# )
