from flika import global_vars as g

LOW = 5

def calc_h_index():
    old_h_index = LOW
    flika_factor = 15
    new_h_index = flika_factor * old_h_index
    g.alert('Congratulations! After using Flika your new h-index is {}!'.format(new_h_index))
