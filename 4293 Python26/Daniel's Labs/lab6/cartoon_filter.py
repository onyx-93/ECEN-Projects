import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from preprocessing import read_image, luma_transform

# I used Grok to help me figured out the approximation of the gradient vector
def gradient(G: np.ndarray) -> np.ndarray:
    """Gradient approximation method.
    
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
            filename = input("Enter image filename: ").strip()
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

    grad = gradient(G)

    # Pre-compute max norm so slider range is sensible for any image
    max_norm = np.max(np.linalg.norm(grad, axis=2))
    default_threshold = max_norm / 8.0 if max_norm > 0 else 5.0

    def masked_image(thresh: float):
        """Build the cartoon version: black lines where edges detected."""
        edges = detect_edges(grad, thresh)
        masked = rgb.copy()
        masked[edges] = 0          # sets entire pixel (all 3 RGB channels) to black
        return masked

    # Set up the interactive plot
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.25)   # room for slider

    # Initial display
    initial_masked = masked_image(default_threshold)
    im = ax.imshow(initial_masked)
    ax.set_title("Cartoon Filter")
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
        new_masked = masked_image(new_thresh)
        im.set_data(new_masked)
        fig.canvas.draw_idle()

    thresh_slider.on_changed(update)

    plt.show()