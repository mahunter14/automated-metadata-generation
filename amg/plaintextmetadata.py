class PcAlignMetadata():
    """
    This class supports metadata as written by the
    NASA Ames Stereo Pipeline pc_align application.

    Parameters
    ----------
    datafile : str
               The path to the input data

    Attributes
    ----------
    data : list
           of lines read from the plaintext file

    vertical_accuracy_test_name : str
                                  The name or description of the test 
                                  used to assess vertical accuracy

    median_error : float
                   The median offset between the DTM and whatever 
                   ground source was used by pc_align

    vertical_accuracy_value : float
                              The value to be reported for the vertical 
                              accuracy of this metadata object. This
                              is currently the median, but this class
                              can be extended to support any value 
                              reported by pc_align.                            
    """
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
            