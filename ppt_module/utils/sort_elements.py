from ppt_module.utils.position import get_position

def sort_elements(prs_data):
    """
    Sorts the elements in each slide of the presentation data dictionary.
    Args:
        pra data (dict): A dictionary representing the structure of a PowerPoint presentation
    Returns: 
        dict: The updated dictionary with sorted elements
    """

    for no, slide in prs_data.items():
        text =slide["text"]
        text ={k: v for k, v in sorted (text.items(), key=lambda item: item[1])}
        slide["text"] =text

        chart =slide["chart"]
        chart ={k: v for k, v in sorted(chart.items(), key=lambda item: item[1])}
        slide["chart"] =chart

        table= slide["table"]
        table= {k: v for k, v in sorted (table.items(), key=lambda item: item[1])}
        slide["table"]=table

        img =slide["image"]
        img= {k: v for k, v in sorted (img.items(), key=lambda item: item[1])}
        slide["image"]=img

        id_pos_dict={}
        for idd, shp in slide["ids"].items():
            id_pos_dict[idd]=get_position(shp)
        id_pos_dict ={k: v for k, v in sorted(id_pos_dict.items(), key=lambda item: item[1])} 
        slide["id_pos"]= id_pos_dict

    return prs_data