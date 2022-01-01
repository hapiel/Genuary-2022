import vsketch

def css_to_cm(css):
    return vsketch.Vsketch.map(css, 0, 37.7952755905511811, 0, 1)

def css_to_mm(css):
    return vsketch.Vsketch.map(css, 0, 3.77952755905511811, 0, 1)