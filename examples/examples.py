import numpy as np
import flashplot as fp

def main():

    #
    # fp.imshow
    #

    # generate a random image, should just be static
    A = np.random.rand(200,200)
    img = fp.imshow(A)

    #
    # fp.plot
    #

    # generate a sine wave plot
    xs = np.linspace(0,10,100)
    ys = np.sin(xs)

    img = fp.plot(xs, ys)

    #
    # fp.make_mp4_from_data
    #

    # generate a bunch of static data and make an mp4
    frames = []
    n_frames = 100
    for i in range(n_frames):
        A = np.random.rand(200,200)
        frames.append(A)

    fp.make_mp4_from_data(frames, 'frames.mp4')

    #
    # fp.show_mp4
    #

    # now show the movie we just made
    fp.show_mp4('frames.mp4')

if __name__=='__main__':
    main()