import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from preprocessing import preprocess, read_image
from imgprocessfunc import gradient_center, edge_mask_gradient


def apply_edge_mask(color_img, edge_mask):
    out = color_img.copy()
    out[edge_mask] = 0
    return out

def main():
    while True:
        filename = input("\n\tEnter image filename: ").strip()
        try:
            color_img = read_image(filename)
            break
        except FileNotFoundError:
            print("\n\tFile not found: Please try again.")
        except OSError:
            print("\n\tThat file couldn't be opened as an image. Try a different file.")

    color_img = read_image(filename)
    gray = preprocess(filename)

    grad = gradient_center(gray)

    def choose_threshold(thresh=12):
        while True:
            try:
                thresh_result = int(input("\n\tEnter a threshold to start (suggested is 12): "))
                break
            except ValueError:
                print("\nInvalid input. Enter an integer.")
        return thresh_result

    init_thresh = choose_threshold()

    # Initialize mask and display image
    mask = edge_mask_gradient(grad, init_thresh)
    masked_img = apply_edge_mask(color_img, mask)

    fig, ax = plt.subplots()
    img_artist = ax.imshow(masked_img)
    ax.axis('off')

    fig.subplots_adjust(bottom=0.25)
    axthresh = fig.add_axes([0.25, 0.1, 0.65, 0.03])

    thresh_slider = Slider(
        ax = axthresh,
        label='Threshold',
        valmin=0,
        valmax=255,
        valinit=init_thresh,
    )

    def update(val):
        new_thresh = thresh_slider.val
        new_mask = edge_mask_gradient(grad, new_thresh)
        new_masked = apply_edge_mask(color_img, new_mask)
        img_artist.set_data(new_masked)
        fig.canvas.draw_idle()

    thresh_slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    main()