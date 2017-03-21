import numpy as np
import sys
sys.path.append(r'C:\Users\kyle\Documents\GitHub\flika')
from qtpy import QtWidgets, QtCore, QtGui
import skimage.filters
import flika
flika_version = flika.__version__
from flika import global_vars as g
from flika.process.BaseProcess import BaseProcess, WindowSelector, SliderLabel, CheckBox, ComboBox
from flika.window import Window
from flika.roi import ROI_rectangle, makeROI
from flika.process import generate_random_image, gaussian_blur, threshold
from scipy import ndimage

class Count_clouds(BaseProcess):
    """ cloud_counter(blur_amount, threshold_value, keepSourceWindow=False)
    This function counts clouds in images of noise.

    Parameters:
        | blur_amount (int) -- The amount to blur your image
        | threshold_value (float) -- The threshold value
    Returns:
        newWindow
    """

    def __init__(self):
        super().__init__()

    def gui(self):
        if g.currentWindow is None:
            generate_random_image(500, 128)  # Normally you would not need to generate a random image when writing this function
        self.gui_reset()
        nFrames = 1
        if g.currentWindow is not None:
            nFrames = g.currentWindow.image.shape[0]
        blur_amount = SliderLabel()
        blur_amount.setRange(0, 5)
        threshold_value = SliderLabel(2)
        threshold_value.setRange(g.currentWindow.image.min(),g.currentWindow.image.max())
        self.items.append({'name': 'blur_amount', 'string': 'Blur Amount', 'object': blur_amount})
        self.items.append({'name': 'threshold_value', 'string': 'Threshold', 'object': threshold_value})
        super().gui()

    def get_init_settings_dict(self):
        s = dict()
        s['blur_amount'] = 4
        s['threshold_value'] = .05
        return s

    def __call__(self, blur_amount, threshold_value, keepSourceWindow=False):
        """
        __call__() needs to
        1) begin with self.start(keepSourceWindow)
        2) define self.newname as the name of the new window
        3) define self.newtif
        4) return self.end()
        """
        self.start(keepSourceWindow)
        blurred_image = skimage.filters.gaussian(self.tif.astype(np.float64), blur_amount, mode='constant')
        binary_image = blurred_image > threshold_value
        label_objects, nb_labels = ndimage.label(binary_image)
        g.alert('Number of clouds counted: {}'.format(nb_labels))
        self.newtif = binary_image
        self.newname = self.oldname + ' - Cloud Counter'
        return self.end()

count_clouds = Count_clouds()


def launch_docs():
    url='https://github.com/flika-org/flika_plugin_template'
    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

