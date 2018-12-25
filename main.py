#!/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import scipy
import os
import pickle
import itertools

from keypoints import laplacian
from  PIL import Image

'''
References:
    http://aishack.in/tutorials/sift-scale-invariant-feature-transform-keypoint-orientation/
    https://stackoverflow.com/questions/19815732/what-is-gradient-orientation-and-gradient-magnitude
    http://www.vlfeat.org/api/sift.html
'''

'''
    infos: dict_keys([1, 2, 3, 4])
    infos[1]: dict_keys(['original', 'laplacian', 'std' , 'dog', 'kps'])
    
    infos[1]["laplacian"] = [img0, img1...]
    infos[1]["kps"] = [tuple, tuple1...]
'''


'''
    The size of the "orientation collection region" around the keypoint depends
    on
    it's scale. The bigger the scale, the bigger the collection region.
'''

### Compute gradient magnitude
def gradient_m(i,j, picture):
    ft = (picture[i,j+1] - picture[i,j-1]) ** 2
    st = (picture[i+1,j] - picture[i-1,j]) ** 2
    return np.sqrt(ft + st)

### Compute gradient orientation
def gradient_theta(i,j,picture):
    #To avoid error division by zero
    eps = 1e-5
    nb_bins = 36
    ft = picture[i+1,j] - picture[i-1,j]
    st = (picture[i,j+1] - picture[i,j-1]) + eps


    ret = np.arctan(ft/st)
    print(ret)
    return ret
    #return (nb_bins / (2 * np.pi)) * (np.pi + np.arctan(quotient))

def pronostic(theta_list):
    print("MIN")
    print(min(theta_list))
    
    print("MAX")
    print(max(theta_list))
    print("MEAN")
    print(sum(theta_list) / len(theta_list))
    
    print()
    
def create_histogram(i,j,picture,std):
    truncate = 4.0
    kernel_size = 2 * int(std * truncate + .5) + 1
    window  = list(range(-kernel_size, kernel_size + 1))
    
    diag  = list(set(itertools.permutations(window, 2)))
    rooti, rootj = i,j
    m_list, theta_list =  [], []
    for ii, jj in diag:
        x = rooti + ii
        y = rootj + jj
        
        if x - 1 < 0 or y - 1 < 0 or x + 1 > picture.shape[0] - 1 \
            or y + 1 > picture.shape[1] -1:
            continue
        m_list.append(gradient_m(x,y,picture))
        theta_list.append(gradient_theta(x,y,picture))
    #pronostic(theta_list)    

def assign_orientation(infos):
    index = 0 
    for octave in infos.keys():
        kps = infos[octave]['kps']
        std = infos[octave]["std"][index]
        #picture = infos[octave]['laplacian'][index].astype('float64')
        picture = infos[octave]['original']
        for i, j in kps: 
             create_histogram(i,j,picture,std)
    return infos

### Showing keypoints for the first octave's picture
def show_keypoints(infos):
    #pic = np.zeros(infos[1]['laplacian'][0].shape)
    pic = infos[1]['laplacian'][0]
    for x,y in infos[1]['kps']:
        pic[x,y] = 255
    
    plt.imshow(pic, cmap="gray")
    plt.show()

def run(load=None, img=None):
    infos = None
    if load  is not None:
        infos = pickle.load(open(load, "rb"))
        assign_orientation(infos)
        show_keypoints(infos)
    if img is not None:
        infos = laplacian.run(img) 
    return infos 

if __name__ == "__main__":
    path_paris = '/Users/franckthang/work/PersonalWork/sift/resources/paris.jpg'
    path_cat = '/Users/franckthang/work/PersonalWork/sift/resources/cat.jpg'
    img = np.array(Image.open(path_cat).convert('L'))
    run(load="pickle/infos_paris.pickle")
    
    #infos = run(img=img)
    #pickle.dump(infos, open("pickle/infos_cat.pickle", "wb"))
    #run(load="pickle/infos_cat_laplacian.pickle")
