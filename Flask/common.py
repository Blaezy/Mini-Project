#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tensorflow as tf


# In[2]:


DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255


# In[3]:


def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]


# In[4]:


def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch


# In[5]:


def evaluate(model, dataset):
    psnr_values = []
    for lr, hr in dataset:
        sr = resolve(model, lr)
        psnr_value = psnr(hr, sr)[0]
        psnr_values.append(psnr_value)
    return tf.reduce_mean(psnr_values)


# In[6]:


def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return (x - rgb_mean) / 127.5


# In[7]:


def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean


# In[8]:


def normalize_01(x):
    """Normalizes RGB images to [0, 1]."""
    return x / 255.0


# In[9]:


def normalize_m11(x):
    """Normalizes RGB images to [-1, 1]."""
    return x / 127.5 - 1


# In[10]:


def denormalize_m11(x):
    """Inverse of normalize_m11."""
    return (x + 1) * 127.5


# In[11]:


def psnr(x1, x2):
    return tf.image.psnr(x1, x2, max_val=255)


# In[12]:


def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)

