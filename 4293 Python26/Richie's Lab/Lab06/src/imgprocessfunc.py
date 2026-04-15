import numpy as np

def gradient_center(G: np.ndarray):
    G = G.astype(float)
    H, W = G.shape
    grad = np.zeros((H, W, 2), dtype=float)

    #interior pts
    grad[1:-1, 1:-1, 0] = (G[1:-1, 2:] - G[1:-1, :-2]) / 2.0 # d/dx 
    grad[1:-1, 1:-1, 1] = (G[2:, 1:-1] - G[:-2, 1:-1]) / 2.0 # d/dy

    return grad

def edge_mask_gradient(grad: np.ndarray, threshold: float):
    gx = grad[..., 0]
    gy = grad[..., 1]
    mag = np.sqrt(gx**2 + gy**2) # L2 norm
    mask = mag > threshold
    return mask

