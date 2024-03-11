import math
import numpy as np

def get_position(shape):
    param= 10000
    l= round(shape.left/param) 
    w=round(shape.width/param)
    t=round(shape.top/param)
    h=round (shape.height/param)
    return (t, l)

def calculate_rel_dist(chart, text):
    """
    Calculates the relative distance between each chart element and text element.
    
    Args:
        chart (dict): A dictionary containing the positions of chart elements
        text (dict): A dictionary containing the positions of text elements

    Returns:
        dict: A dictionary representing the relative distances between chart and text elements
    """
    #slide-level function.
    """
    This function calculates the relative distance between each chart element and text element 
    by iterating through the chart and text dictionaries and computing the distance between their 
    positions. The result is a dictionary with the relative distances for each chart element.
    """

    rel_dist={}
    for ch in chart:
        ch_txt_dist={}
        point1= np.array(chart[ch])
        for tx in text:
            point2= np.array(text[tx])
            ch_txt_dist[tx] =math.dist(chart[ch], text[tx])
        rel_dist[ch]= dict(sorted(ch_txt_dist.items(), key=lambda item: (item[1])))
    return rel_dist
