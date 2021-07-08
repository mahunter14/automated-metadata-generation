class PcAlignMetadata():
    def __init__(self, datafile):
        self.datafile=datafile

    @property
    def data(self):
        if not hasattr(self, '_data'):
            with open(self.datafile, 'r') as f:
                lines = f.readlines()
                self._data = [l.strip() for l in lines]
        return self._data

    @property
    def vertical_accuracy_test_name(self):
        return 'Median vertical offset as reported by NASA Ames Stereo Pipeline pc-align'

    @property 
    def median_error(self):
        for l in self.data:
            if 'Median' in l:
                median = float(l.split(':')[-1])
                return median

    @property
    def vertical_accuracy_value(self):
        return self.median_error
            