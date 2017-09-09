from collections import namedtuple
import numpy as np

Fragment = namedtuple('Fragment', ['x', 'y', 'data'])


def checkImg(func):
        def check(*args):
            if args[0].working_img is not None:
                    func(*args)
            else:
                print('No working image')
                return
        return check


class SIFTExtractor:
    def __str__(self):
        return 'SIFT Extractor'


class ColorHistogramExtractor:
    def __init__(self, fragment_size=20):
        self.fragment_size = fragment_size
        self.working_img = None

        # Instance a fragment list
        self.horizontal_fragments = list()
        self.vertical_fragments = list()

        # Instance a description list, a description is a Fragment, Histogram pair
        self.vertical_descriptions = list()
        self.horizontal_descriptions = list()

    def getDescription(self, tarea):
        self.working_img = tarea

        # Extract fragments from image
        self.verticalFragmentation()
        self.horizontalFragmentation()

        # Extract the histograms of each Fragment
        self.extractVerticalHistograms()
        self.extractHorizontalHistograms()

        print('** Vertical Descriptions **')
        for i in self.vertical_descriptions:
            print(i)

        print('** Horizontal Descriptions **')
        for i in self.horizontal_descriptions:
            print(i)

    @checkImg
    def verticalFragmentation(self):
        # Get elimination factor for x
        y, x, _ = self.working_img.shape

        # Set fragment sizes
        x_frag_size = self.fragment_size
        y_frag_size = y // 2

        frag_amount_x = x // x_frag_size
        elimination_factor_x = x - x_frag_size * frag_amount_x

        # Select amount to trim the image from left and right
        if elimination_factor_x % 2:  # odd
            trim_left, trim_right = elimination_factor_x // 2 + 1, elimination_factor_x // 2
        else:
            trim_left, trim_right = elimination_factor_x // 2, elimination_factor_x // 2

        # Get elimination factor for y
        y_frag_size = y // 2
        frag_amount_y = y // y_frag_size
        elimination_factor_y = y - y_frag_size * frag_amount_y

        # Select amount to trim the image from left and right
        if elimination_factor_y % 2:  # odd
            trim_up, trim_down = elimination_factor_y // 2 + 1, elimination_factor_y // 2
        else:
            trim_up, trim_down = elimination_factor_y // 2, elimination_factor_y // 2

        trimmed_w_img = self.working_img.copy()
        y, x, _ = trimmed_w_img.shape
        trimmed_w_img = trimmed_w_img[
            trim_up: y - trim_down,
            trim_left: x - trim_right
        ]

        # Extract vertical fragments
        for i in range(frag_amount_x):
            for j in range(frag_amount_y):
                data_fragment = trimmed_w_img[
                    j * y_frag_size: (j + 1) * y_frag_size,
                    i * x_frag_size: (i + 1) * x_frag_size
                ]
                frag = Fragment(
                    x=i * x_frag_size,
                    y=j * y_frag_size,
                    data=data_fragment,
                )
                self.vertical_fragments.append(frag)

    @checkImg
    def horizontalFragmentation(self):
        # Get elimination factor for x
        y, x, _ = self.working_img.shape
        x_frag_size = x // 2
        y_frag_size = self.fragment_size
        frag_amount_x = x // x_frag_size
        elimination_factor_x = x - x_frag_size * frag_amount_x

        # Select amount to trim the image from left and right
        if elimination_factor_x % 2:  # odd
            trim_left, trim_right = elimination_factor_x // 2 + 1, elimination_factor_x // 2
        else:
            trim_left, trim_right = elimination_factor_x // 2, elimination_factor_x // 2

        # Get elimination factor for y
        frag_amount_y = y // y_frag_size
        elimination_factor_y = y - y_frag_size * frag_amount_y

        # Select amount to trim the image from left and right
        if elimination_factor_y % 2:  # odd
            trim_up, trim_down = elimination_factor_y // 2 + 1, elimination_factor_y // 2
        else:
            trim_up, trim_down = elimination_factor_y // 2, elimination_factor_y // 2

        trimmed_w_img = self.working_img.copy()
        y, x, _ = trimmed_w_img.shape
        trimmed_w_img = trimmed_w_img[
            trim_up: y - trim_down,
            trim_left: x - trim_right
        ]

        # Extract vertical fragments
        for i in range(frag_amount_x):
            for j in range(frag_amount_y):
                data_fragment = trimmed_w_img[
                    j * y_frag_size: (j + 1) * y_frag_size,
                    i * x_frag_size: (i + 1) * x_frag_size
                ]
                frag = Fragment(
                    x=i * x_frag_size,
                    y=j * y_frag_size,
                    data=data_fragment,
                )
                self.horizontal_fragments.append(frag)

    @checkImg
    def extractVerticalHistograms(self):
        for fragment in self.vertical_fragments:
            bins = range(256)

            r_ch = fragment.data[:, :, 0]
            g_ch = fragment.data[:, :, 1]
            b_ch = fragment.data[:, :, 2]

            hist_r_ch, _ = np.histogram(r_ch.flatten(), bins=bins, density=True)
            hist_g_ch, _ = np.histogram(g_ch.flatten(), bins=bins, density=True)
            hist_b_ch, _ = np.histogram(b_ch.flatten(), bins=bins, density=True)

            hist = np.stack([hist_r_ch, hist_g_ch, hist_b_ch])

            # Append the histogram to the vertical description list, paired with its fragment
            self.vertical_descriptions.append([fragment, hist])

    @checkImg
    def extractHorizontalHistograms(self):
        for fragment in self.horizontal_fragments:
            bins = range(256)

            r_ch = fragment.data[:, :, 0]
            g_ch = fragment.data[:, :, 1]
            b_ch = fragment.data[:, :, 2]

            hist_r_ch, _ = np.histogram(r_ch.flatten(), bins=bins, density=True)
            hist_g_ch, _ = np.histogram(g_ch.flatten(), bins=bins, density=True)
            hist_b_ch, _ = np.histogram(b_ch.flatten(), bins=bins, density=True)

            hist = np.stack([hist_r_ch, hist_g_ch, hist_b_ch])

            # Append the histogram to the horizontal description list, paired with its fragment
            self.horizontal_descriptions.append([fragment, hist])

    def __str__(self):
        return 'Color Histogram Extractor'


DESCRIPTOR_LIST = {
    'SIFT': SIFTExtractor,
    'CHD': ColorHistogramExtractor,
}
