import numpy as np
import scipy

#------------------------------------------------------------------------------------

def iRadon(sinogram, kernel, resolution=512):
    ''' 
    INPUT:
        sinogram: np.ndarray(float32)
        kernel: function, selected from a list
        resolution: int
        
    OUTPUT:
        reconstructed_image: np.ndarray(float32)
        '''

    
    reconstructed_image = np.zeros(shape=(resolution, resolution), dtype=np.float32)

    for x in reconstructed_image:
        for y in reconstructed_image[x]:

            y = 0 #0 is placeholder, numerical integration using for loop
                # over all lines in sinogram,
                # multiplied by ramp filter, 
                # multiplied by dirac delta which is 0 when the line is not incident with (x,y) and 0 otherwise,
                # or some other way of only integrating over the lines incident to the point


    return reconstructed_image




#-----------------------------------------------------------------------------------------

def RadonTransform(image, n_projectionDistance=100, n_projectionAngles=180, compact=True,):
    # (Not going to use this, just writing as an exercise.)
    # Use skimage Radon instead, 
    # Or use the closed-form transformation of ellipses for generating sinograms of ellipse phantoms.
    ''' 
    INPUT:

    
    OUTPUT:
    '''

    return 



def _filter_response(L, tau, kernel):
    """Frequency response of the (windowed) Ram-Lak filter on a length-L FFT grid."""
    n = np.arange(-(L // 2), L // 2)
    h = np.zeros(L)
    # build Ram-Lak spatial kernel, with h[0] at index 0 (circular layout)
    odd = (n % 2 != 0)
    h_vals = np.where(n == 0, 1 / (4 * tau**2),
                      np.where(odd, -1 / (np.pi**2 * np.where(n == 0, 1, n)**2 * tau**2), 0.0))
    h[n % L] = h_vals
    H = np.fft.fft(h).real                   # symmetric kernel -> real response

    f = np.fft.fftfreq(L)                    # cycles/sample, Nyquist = 0.5
    windows = {
        "ramp":        np.ones_like(f),
        "shepp-logan": np.sinc(f),           # sin(pi f)/(pi f)
        "cosine":      np.cos(np.pi * f),
        "hamming":     0.54 + 0.46 * np.cos(2 * np.pi * f),
    }
    return H * windows[kernel]

def filter_projections(sinogram, kernel="ramp", tau=1.0):
    """sinogram shape: (n_detectors, n_angles), as returned by skimage.radon."""
    n_det = sinogram.shape[0]
    L = 1 << int(np.ceil(np.log2(2 * n_det - 1)))   # zero-pad to power of 2 >= 2N-1
    H = _filter_response(L, tau, kernel)
    P = np.fft.fft(sinogram, n=L, axis=0)           # pads with zeros along axis 0
    q = np.fft.ifft(P * H[:, None], axis=0).real[:n_det]
    return tau * q

def inverseRadon(sinogram, theta_deg, kernel="ramp", resolution=512):
    n_det, n_ang = sinogram.shape
    q = filter_projections(sinogram, kernel)
    theta = np.deg2rad(theta_deg)

    # pixel coordinates relative to the center (skimage uses size//2 as the center)
    ax = np.arange(resolution) - resolution // 2
    X, Y = np.meshgrid(ax, ax)

    det_axis = np.arange(n_det)
    recon = np.zeros((resolution, resolution))
    for i, th in enumerate(theta):
        s = X * np.cos(th) - Y * np.sin(th) + n_det // 2  # detector coordinate of each pixel
        recon += np.interp(s.ravel(), det_axis, q[:, i], left=0, right=0).reshape(s.shape)

    recon *= np.pi / n_ang
    return recon.astype(np.float32)


