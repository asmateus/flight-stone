class SIFTExtractor:
    def __str__(self):
        return 'SIFT Extractor'


class ColorHistogramExtractor:
    def __str__(self):
        return 'Color Histogram Extractor'


DESCRIPTOR_LIST = {
    'SIFT': SIFTExtractor,
    'CHD': ColorHistogramExtractor,
}
