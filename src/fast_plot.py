import subprocess

from PIL import Image, ImageDraw

import numpy as np
import matplotlib.pyplot as plt

# should work like...
# import fast_plot as fp
# fp.plot()

def map_value_to_color(value, colormap='viridis'):

    norm = plt.Normalize(vmin=0, vmax=255)
    cmap = plt.get_cmap(colormap)
    color = cmap(norm(value), bytes=True)

    return color

def rescale(arr, lo: float, hi: float, vmin: float | None = None, vmax: float | None = None, end_type: type | None = None, log_scale: bool = False):

    # if vmin/vmax not set, you just choose the min max of the image
    # clip the min/max of the image if it is set
    if vmin is None:
        vmin = np.min(arr)
    else:
        arr[arr < vmin] = vmin

    if vmax is None:
        vmax = np.max(arr)
    else:
        arr[arr > vmax] = vmax

    if log_scale:
        arr[arr<0] = np.NaN
        arr = np.log10(arr)
        vmin = np.log10(vmin)
        vmax = np.log10(vmax)

    # shift from vmin to lo
    arr = arr - vmin + lo
    # rescales from lo to hi
    arr = arr * (hi-lo)/(vmax-vmin)

    if end_type is not None:
        arr = arr.astype(end_type)

    return arr

def imshow(arr, scale: float | None = None, int_scale: int | None = None, log_scale: bool = False, vmin: float | None = None, vmax: float | None = None):

    arr = rescale(arr, 0, 255, vmin=vmin, vmax=vmax, end_type=np.uint8, log_scale=log_scale)

    # Create and save the image
    image = Image.fromarray(arr)
    sy, sx = arr.shape

    # used for integer factor sizing
    if int_scale is not None:
        image = image.resize((sx*int_scale, sy*int_scale), Image.Resampling.NEAREST)

    # float factor scaling
    if scale is not None:
        image = image.resize((int(sx*scale), int(sy*scale)), Image.Resampling.LANCZOS)

    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    return image

def plot(plot_xs, plot_ys, x_vmin=None, x_vmax=None, y_vmin=None, y_vmax=None, size=(300,300)):
    sy, sx = size

    padding = 10
    hi_x = sx - padding
    hi_y = sy - padding

    rs_xs = rescale(plot_xs, padding, hi_x, vmin=x_vmin, vmax=x_vmax)
    rs_ys = rescale(plot_ys, padding, hi_y, vmin=y_vmin, vmax=y_vmax)

    img = Image.new('L', size)
    draw = ImageDraw.Draw(img)

    xs = [padding, sx-padding]
    lower_ys = [padding, padding]
    upper_ys = [sy-padding, sy-padding]
    draw.line(list(zip(xs,lower_ys)), fill=120, width=2) # bottom horizontal line
    draw.line(list(zip(xs,upper_ys)), fill=120, width=2) # top horizontal line

    draw.line(list(zip(rs_xs, rs_ys)), fill=255, width=2) # data

    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    return img

def make_mp4(pattern, save_path, framerate):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-r', f'{framerate:d}', '-i', f'{pattern}', '-vcodec', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', f'{save_path}'])

def show_mp4(filename):
    subprocess.run(['ffplay', '-loop', '0', filename])
