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
    def __str__(self):
        return 'Color Histogram Extractor'

    def __init__(self, fragment_size=20):
        self.fragment_size = fragment_size
        self.working_img = None

        # Instance a fragment list
        self.horizontal_fragments = list()
        self.vertical_fragments = list()

        # Instance a description list, a description is a Fragment, Histogram pair
        self.vertical_descriptions = list()
        self.horizontal_descriptions = list()

        # Initialize possible bins for histogram
        self.bins = self.generateBins()

    def generateBins(self):
        # Each dimesion will have 50 different possible intensity values
        dim_1 = list(range(0, 255, 5))[1:]
        dim_2 = [i * 1000 for i in dim_1]
        dim_3 = [i * 1000 for i in dim_2]

        res_list = [i + j + k for i in dim_3 for j in dim_2 for k in dim_1]
        return res_list

    def getDescription(self, tarea):
        self.working_img = tarea

        # Extract fragments from image
        self.verticalFragmentation()
        self.horizontalFragmentation()

        # Extract the histograms of each Fragment
        self.extractHistograms(self.horizontal_fragments, self.horizontal_descriptions)
        self.extractHistograms(self.vertical_fragments, self.vertical_descriptions)

        print('** Vertical Descriptions **')
        for i in self.vertical_descriptions:
            print(set(i[1]))

        print('** Horizontal Descriptions **')
        for i in self.horizontal_descriptions:
            print(set(i[1]))

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

        # Select amount to trim the image from up and down
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
    def extractHistograms(self, fragment_set, description_set):
        for fragment in fragment_set:
            r_ch = fragment.data[:, :, 0].flatten()
            g_ch = fragment.data[:, :, 1].flatten()
            b_ch = fragment.data[:, :, 2].flatten()

            t_ch = r_ch * 1e6 + g_ch * 1e3 + b_ch
            hist, binss = np.histogram(t_ch, bins=self.bins)

            # Append the histogram to the vertical description list, paired with its fragment
            description_set.append([fragment, hist])


DESCRIPTOR_LIST = {
    'SIFT': SIFTExtractor,
    'CHD': ColorHistogramExtractor,
}
