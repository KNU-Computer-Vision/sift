import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy
import os
import pickle
from keypoints import laplacian
from  PIL import Image

'''
References:
    http://aishack.in/tutorials/sift-scale-invariant-feature-transform-keypoint-orientation/
    https://stackoverflow.com/questions/19815732/what-is-gradient-orientation-and-gradient-magnitude
'''

'''
    infos: dict_keys([1, 2, 3, 4])
    infos[1]: dict_keys(['laplacian', 'dog', 'kps'])
    
    infos[1]["laplacian"] = [img0, img1...]
    infos[1]["kps"] = [tuple, tuple1...]
'''


'''
    The size of the "orientation collection region" around the keypoint depends on
    it's scale. The bigger the scale, the bigger the collection region.
'''

### Compute gradient magnitude
def gradient_m(i,j, picture):
    ft = (picture[i,j+1] - picture[i,j-1]) ** 2
    st = (picture[i+1,j] - picture[i-1,j]) ** 2
    return np.sqrt(ft + st)

### Compute gradient orientation
def gradient_theta(i,j,picture):
    eps = 1e-5
    ft = picture[i+1,j] - picture[i-1,j]
    st = (picture[i,j+1] - picture[i,j-1]) + eps
    quotient = ft / st
    return np.arctan(quotient)

def is_correct_pos(i,j,shape):
    return i > 0 and j > 0 and i < shape[0] - 1 and j < shape[1] - 1
    


def assign_orientation(infos):
    for octave in infos.keys():
        laplacian = infos[octave]['laplacian']
        kps = infos[octave]['kps']
        picture  = laplacian[0].astype("float64")
        for i, j in kps: 
            if not is_correct_pos(i,j,picture.shape):
                continue
            local_m = gradient_m(i,j,picture)
            local_t = gradient_theta(i,j,picture)
            print("Orientations: {}, Magnitude: {}\n".format(local_t, local_m))
    return infos

### Showing keypoints for the first octave's picture
def show_keypoints(infos):
    pic = np.zeros(infos[1]['laplacian'][0].shape)
    for x,y in infos[1]['kps']:
        pic[x,y] = 255
    plt.imshow(pic, cmap="gray")
    plt.show()

def run(load=None, img=None):
    infos = None
    if load is not None:
        infos = pickle.load(open(load, "rb"))
        assign_orientation(infos)
        #show_keypoints(infos)
    if img is not None:
        infos = laplacian.run(img) 
    return infos 

if __name__ == "__main__":
    #path_paris = '/Users/franckthang/Work/PersonalWork/sift/resources/paris.jpg'
    path_cat = '/Users/franckthang/Work/PersonalWork/sift/resources/cat.jpg'
    img = np.array(Image.open(path_cat).convert('L'))
    run(load="pickle/infos_paris.pickle")
    #run(load="pickle/infos_paris_laplacian.pickle")
    
    '''
    infos = run(img=img)
    pickle.dump(infos, open("pickle/infos_cat_laplacian.pickle", "wb"))
    run(load="pickle/infos_cat_laplacian.pickle")
    '''
