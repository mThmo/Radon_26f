import numpy as np

def _scale_factor(sinogram, p_max=4.0):
    m = sinogram.max()
    if m <= 0:
        raise ValueError("sinogram must have a positive maximum")
    return p_max / m

def _poisson(p, I0, rng):
    counts = rng.poisson(I0 * np.exp(-p)).astype(float)
    counts = np.maximum(counts, 1.0)          # avoid log(0)
    return -np.log(counts / I0)

def _gaussian(p, sigma, rng):
    return p + rng.normal(0.0, sigma, size=p.shape)

def poisson_noise(sinogram, I0=1e4, p_max=4.0, rng=None):
    """sinogram in original units; I0 = incident photons per ray;
    p_max = largest line integral after internal rescaling."""
    rng = np.random.default_rng(rng)
    s = _scale_factor(sinogram, p_max)
    return _poisson(sinogram * s, I0, rng) / s

def gaussian_noise(sinogram, sigma=0.01, p_max=4.0, rng=None):
    """sigma is in *scaled* units (where the max line integral is p_max),
    so it's a noise level relative to the signal range, independent of
    the sinogram's raw units."""
    rng = np.random.default_rng(rng)
    s = _scale_factor(sinogram, p_max)
    return _gaussian(sinogram * s, sigma, rng) / s

def both_noises(sinogram, I0=1e4, sigma=0.01, p_max=4.0, rng_p=None, rng_g=None):
    rng_p = np.random.default_rng(rng_p)
    rng_g = np.random.default_rng(rng_g)
    s = _scale_factor(sinogram, p_max)       # scale once, shared by both stages
    p = sinogram * s
    p = _poisson(p, I0, rng_p)               # photon statistics first
    p = _gaussian(p, sigma, rng_g)           # then detector/electronic noise
    return p / s