"""Lab 6: Cartoon Filter via Gradient-Based Edge Detection
This script fulfills all requirements:
- Accepts image filename from user (with error handling for invalid files)
- Loads and preprocesses using the provided preprocessing.py module
- Computes gradient (Step 3 basic version provided; Step 6 replacement used in main program)
- Detects edges with L2 norm and customizable threshold
- Displays masked original color image with black edge lines
- Interactive matplotlib slider updates the display (reuses precomputed gradient)
- Handles any image size/aspect ratio
- No undesired code runs on import
- Step 6 replacement: Sobel-style gradient using more pixels + coefficients + off-axis pixels

Save this as cartoon_filter.py in the same folder as preprocessing.py and the images/ folder.
Run with: python cartoon_filter.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Import from the provided preprocessing module (no self-test code runs because of the if __name__ guard)
from preprocessing import read_image, luma_transform


def compute_gradient_basic(G: np.ndarray) -> np.ndarray:
    """STEP 3: Centered finite difference gradient approximation with h=1.
    Returns a (height, width, 2) array of [∂G/∂x, ∂G/∂y] for each pixel.
    Outer edges (where centered difference is impossible) are set to (0, 0).
    This matches the description in Task 2 of Section 3.8.4.
    """
    m, n = G.shape
    grad = np.zeros((m, n, 2), dtype=float)

    # Horizontal gradient (x-direction) - uses pixels j-1 and j+1
    grad[:, 1:-1, 0] = (G[:, 2:] - G[:, :-2]) / 2.0

    # Vertical gradient (y-direction) - uses pixels i-1 and i+1
    # (row index increases downward, which is standard for image arrays)
    grad[1:-1, :, 1] = (G[2:, :] - G[:-2, :]) / 2.0

    return grad


def compute_gradient_own(G: np.ndarray) -> np.ndarray:
    """STEP 6 REPLACEMENT: My own gradient approximation method.
    
    Design decisions:
    - Uses a 3x3 neighborhood (more pixels than the basic 2-pixel centered difference).
    - Applies Sobel-style coefficients (-1, -2, -1 | 1, 2, 1) for smoothing in the
      perpendicular direction while approximating the derivative. This incorporates
      off-axis (diagonal) pixels.
    - No explicit division (scale is handled by the adjustable threshold slider).
    - Boundaries still set to zero gradient (same handling as basic version).
    
    Qualitative effect on the transformed image:
    - Produces thicker, more continuous, and cleaner edges.
    - Much less sensitive to small noise/artifacts in the original photo.
    - Results in a more "cartoon-y" look with prominent structural lines and
      fewer stray pixels compared to the basic central-difference method.
    """
    m, n = G.shape
    grad = np.zeros((m, n, 2), dtype=float)

    # Interior region where full 3x3 kernel fits (rows/cols 1 to -2)
    # Sobel Gx (horizontal gradient)
    grad[1:-1, 1:-1, 0] = (
        -G[:-2, :-2] - 2 * G[1:-1, :-2] - G[2:, :-2] +
         G[:-2, 2:]  + 2 * G[1:-1, 2:]  + G[2:, 2:]
    )

    # Sobel Gy (vertical gradient)
    grad[1:-1, 1:-1, 1] = (
        -G[:-2, :-2] - 2 * G[:-2, 1:-1] - G[:-2, 2:] +
         G[2:, :-2]  + 2 * G[2:, 1:-1]  + G[2:, 2:]
    )

    return grad


def detect_edges(grad: np.ndarray, threshold: float) -> np.ndarray:
    """Return boolean mask (same shape as image) where L2 norm of gradient exceeds threshold.
    L2 (Euclidean) norm chosen as it is the most common and gives smooth, natural-looking edges.
    """
    norms = np.linalg.norm(grad, axis=2)  # equivalent to sqrt(dx² + dy²)
    return norms > threshold


if __name__ == "__main__":
    # Get valid image filename from user (requirement: does not crash on invalid input)
    while True:
        try:
            filename = input("Enter image filename (e.g. images/hallett_peak.jpg): ").strip()
            if not filename:
                print("Please enter a filename.")
                continue
            rgb = read_image(filename)          # original color image
            G = luma_transform(rgb)             # grayscale for gradient computation
            print(f"Loaded {filename} ({G.shape[0]}x{G.shape[1]} grayscale)")
            break
        except Exception as e:
            print(f"Error loading image: {e}")
            print("Please try a different filename (or full path).")

    # Compute gradient ONCE (reused for all slider updates - performance requirement)
    # NOTE: Using the STEP 6 replacement method.
    # To switch back to the basic Step 3 version, change this line to:
    # grad = compute_gradient_basic(G)
    grad = compute_gradient_own(G)

    # Pre-compute max norm so slider range is sensible for any image
    max_norm = np.max(np.linalg.norm(grad, axis=2))
    default_threshold = max_norm / 8.0 if max_norm > 0 else 5.0

    def create_masked_image(thresh: float):
        """Build the cartoon version: black lines where edges detected."""
        edges = detect_edges(grad, thresh)
        masked = rgb.copy()
        masked[edges] = 0          # sets entire pixel (all 3 RGB channels) to black
        return masked

    # Set up the interactive plot
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.25)   # room for slider

    # Initial display
    initial_masked = create_masked_image(default_threshold)
    im = ax.imshow(initial_masked)
    ax.set_title("Cartoon Filter (adjust threshold below)")
    ax.axis("off")

    # Threshold slider
    slider_ax = plt.axes([0.2, 0.12, 0.6, 0.04])
    thresh_slider = Slider(
        slider_ax,
        "Edge Threshold",
        valmin=0.0,
        valmax=max_norm * 1.2,
        valinit=default_threshold,
        valfmt="%.2f"
    )

    def update(val):
        """Slider callback: rebuild mask with new threshold (gradient is reused)."""
        new_thresh = thresh_slider.val
        new_masked = create_masked_image(new_thresh)
        im.set_data(new_masked)
        fig.canvas.draw_idle()

    thresh_slider.on_changed(update)

    plt.show()