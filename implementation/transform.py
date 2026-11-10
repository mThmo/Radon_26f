import numpy as np
import scipy


def RadonTransform(image, n_projectionDistance=100, n_projectionAngles=180, compact=True,):

    #initialize empty sinogram bitmap
    sinogram = np.ndarray(shape=(n_projectionAngles, n_projectionDistance), dtype=np.float32)

    #import/rescale image

    #apply FFT 

    #sums 

    return sinogram



def iRadon(sinogram, kernel, resolution=512):
    ''' INPUT:
        sinogram: np.ndarray(float32)
        kernel: select from a list
        resolution: int
        
        OUTPUT:
        '''

    
    
    
    
    reconstructed_image = np.ndarray(shape=(resolution, resolution), dtype=np.float32)


    return reconstructed_image