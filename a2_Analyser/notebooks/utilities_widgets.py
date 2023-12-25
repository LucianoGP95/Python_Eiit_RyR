import ipywidgets as widgets
from ipywidgets import HBox

def position_chart(mean_slider, range_slider, auto_position_flag=False):
    if auto_position_flag is False:
        mean_slider.disabled = False; range_slider.disabled = False
        range_mapping = [0.05 - 0.0049 * (range_slider.value)]
        yrange = [mean_slider.value - range_mapping[0], mean_slider.value + range_mapping[0]]
    else:
        range_mapping = None; yrange = None
        mean_slider.disabled = True; range_slider.disabled = True
    return yrange

def widget_int_entry(value: int=5, description: str="") -> widgets.IntText:
    int_entry = widgets.IntText(value=value, description=description)
    return int_entry

def widget_selector(options: list=["A", "B"], description: str="", tooltips: list=["",""]) -> widgets.ToggleButtons:
    selector_buttons = widgets.ToggleButtons(options=options, description=description, tooltips=tooltips)
    return selector_buttons