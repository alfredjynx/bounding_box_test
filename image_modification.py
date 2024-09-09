import numpy as np

def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

import numpy as np

def apply_transform(image, A):

    image_ = np.zeros_like(image)

    Xd = criar_indices(0, image.shape[0], 0, image.shape[1])
    Xd = np.vstack((Xd,np.ones((1,Xd.shape[1]))))
    
    X = np.linalg.inv(A) @ Xd

    X = X.astype(int)
    Xd = Xd.astype(int)

    filtro = (X[0,:]>=0)&(X[0,:]<image_.shape[0])&(X[1,:]>=0)&(X[1,:]<image_.shape[1])
    Xd = Xd[:,filtro]
    X = X[:,filtro]

    image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]
    
    return image_


def resize_image_matrix(image, width, height):
    
    tw_image = width / image.shape[1]
    th_image = height / image.shape[0]

    return np.array([
        [th_image, 0, 0], 
        [0, tw_image, 0], 
        [0, 0, 1]
    ])
    
def resize_image(image, width, height):
    A = resize_image_matrix(image, width, height)
    return apply_transform(image, A)
    
def translate_image_matrix(x, y):
    return np.array([
        [1, 0, y], 
        [0, 1, x], 
        [0, 0, 1]
    ])
    
def translate_center_matrix(image):
    return np.array([
        [1, 0, int(-image.shape[0]/2)], 
        [0, 1, int(-image.shape[1]/2)], 
        [0, 0, 1]
    ])
    
def rotate_image_matrix(deg):
    
    return np.array([
        [np.cos(np.radians(deg)), -np.sin(np.radians(deg)), 0], 
        [np.sin(np.radians(deg)), np.cos(np.radians(deg)), 0], 
        [0, 0,1]
    ])
    
def rotate_image(image, deg):
    B = translate_center_matrix(image)
    A = rotate_image_matrix(deg)
    C = np.linalg.inv(B) @ A @ B
    return apply_transform(image, C)

def reshape(x, shape):
    if x == 0:
        return int(shape/5)
    return int(x*4/5)

