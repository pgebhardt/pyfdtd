import sys
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd


def main():
    # progress function
    history = []

    def progress(t, deltaT, field):
        xShape, yShape = field.oddFieldX['flux'].shape
        interval = xShape * yShape * 5e-9 / (256e6 / 4.0)

        # save history
        if t / deltaT % (interval / deltaT) < 1.0:
            history.append(field.oddFieldX['field'] + field.oddFieldY['field'])

        # print progess
        if t / deltaT % 100 < 1.0:
            print '{}'.format(t * 100.0 / 5e-9)

    # create solver
    job = pyfdtd.Job()
    job.load(sys.argv[1])

    solver = job.get_solver()

    # iterate
    solver.solve(job.config['duration'], progressfunction=progress)

    # show plot
    fig = plt.figure(1)

    ims = []
    for f in history:
        im = plt.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 20.0))
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50)

    plt.show()

if __name__ == '__main__':
    main()
