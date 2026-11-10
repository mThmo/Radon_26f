


def PoissonNoise(sinogram, intensity, variance):

    #initialize noised image
    noisy_sinogram = sinogram

    #index each line/sensor
    for angle, theta in range(sinogram.shape[0]), range(sinogram.shape[1]):

        #apply noise to each line
        noisy_sinogram.shape[angle][theta] = sinogram.shape[angle][theta] #apply noise here

    return noisy_sinogram



def GaussianNoise(sinogram, intensity, variance):
    
    #initialize noised image
    noisy_sinogram = sinogram

    #index each line/sensor
    for angle, theta in range(sinogram.shape[0]), range(sinogram.shape[1]):

        #apply noise to each line
        noisy_sinogram.shape[angle][theta] = sinogram.shape[angle][theta] #apply noise here

    return noisy_sinogram


