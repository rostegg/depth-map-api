import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3' if (os.getenv('FLASK_CONFIG_TYPE') == 'prod') else '0'

import numpy as np
import re
import time
import tensorflow as tf
import scipy.misc
import matplotlib as mpl
import matplotlib.cm
from .monodepth_model import *
from .monodepth_dataloader import *
from .average_gradients import *
from io import BytesIO
from PIL import Image

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))

class MonodepthBridge(object):
    
    self_width = 512
    self_height = 256
    sessions = {}

    AVAILABLE_MODELS = ["kitti","cityscapes","eigen"]
 
    def __init__(self, image_bytes):
        self.image_bytes = image_bytes

    def post_process_disparity(self, disp):
        _, h, w = disp.shape
        l_disp = disp[0,:,:]
        r_disp = np.fliplr(disp[1,:,:])
        m_disp = 0.5 * (l_disp + r_disp)
        l, _ = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
        l_mask = 1.0 - np.clip(20 * (l - 0.05), 0, 1)
        r_mask = np.fliplr(l_mask)
        return r_mask * l_disp + l_mask * r_disp + (1.0 - l_mask - r_mask) * m_disp
    
    @staticmethod
    def init_env():
        params = monodepth_parameters(
            encoder='vgg',
            height=MonodepthBridge.self_height,
            width=MonodepthBridge.self_width,
            batch_size=2,
            num_threads=1,
            num_epochs=1,
            do_stereo=False,
            wrap_mode="border",
            use_deconv=False,
            alpha_image_loss=0,
            disp_gradient_loss_weight=0,
            lr_loss_weight=0,
            full_summary=False)

        MonodepthBridge.left  = tf.placeholder(tf.float32, [2, MonodepthBridge.self_height, MonodepthBridge.self_width, 3])
        MonodepthBridge.model = MonodepthModel(params, "test", MonodepthBridge.left, None)

        config = tf.ConfigProto(allow_soft_placement=True)

        for model_name in MonodepthBridge.AVAILABLE_MODELS:
            session= tf.Session(config=config)

            train_saver = tf.train.Saver()

            session.run(tf.global_variables_initializer())
            session.run(tf.local_variables_initializer())

            restore_path = "{}/models/model_{}".format(CURRENT_DIR,model_name)   
            train_saver.restore(session, restore_path)

            MonodepthBridge.sessions[model_name] = session

    def generate_depth_map(self, model):
        input_image = scipy.misc.imread(self.image_bytes, mode="RGB")
        original_height, original_width, num_channels = input_image.shape
        input_image = scipy.misc.imresize(input_image, [self.self_height, self.self_width], interp='lanczos')
        input_image = input_image.astype(np.float32) / 255
        input_images = np.stack((input_image, np.fliplr(input_image)), 0)

        session = self.sessions[model]

        disp = session.run(self.model.disp_left_est[0], feed_dict={self.left: input_images})
        disp_pp = self.post_process_disparity(disp.squeeze()).astype(np.float32)

        disp_to_img = scipy.misc.imresize(disp_pp.squeeze(), [original_height, original_width])

        cm_gray = mpl.cm.get_cmap('gray')
        im = cm_gray(disp_to_img)
        im = np.uint8(im * 255)
        im = Image.fromarray(im)
        
        depth_map = BytesIO()
        im.save(depth_map, format='PNG')
        depth_map.seek(0)
        return depth_map


