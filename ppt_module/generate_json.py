from ppt_module.extract.extract import extract_data

def generate_output(meta_json):
    output ={}
    for slide_no, value in meta_json.items():
        output[slide_no] = {}

        # Content
        content=""
        for shape_id, shape_pos in value["id_pos"].items(): 
            content += extract_data(meta_json[slide_no]["ids"][shape_id])
        output[slide_no]["content"]= content

        #text
        text = "" 
        for shape_id, shape_pos in value["text"].items(): 
            text += extract_data(meta_json[slide_no]["ids"][shape_id]) 
        output[slide_no]["text"] = text

        #table

        for table_no, (shape_id, shape_pos) in enumerate(value["table"].items()): 
            table_data = extract_data(meta_json[slide_no]["ids"][shape_id]) 
            output[slide_no][f"table_{table_no}"]=table_data

        #chart

        for chart_no, (shape_id, shape_pos) in enumerate(value["chart"].items()): 
            try:
                chart_data= eval(extract_data(meta_json[slide_no]["ids"][shape_id]))
            except Exception as e:
                try:
                    filtered_data = {key: value for key, value in chart_data.items() if not all(v is None for v in value.values())}
                    if len(filtered_data) > 0:
                        output[slide_no][f"chart_{chart_no}"] = filtered_data
                except Exception as e:
                    #traceback.print exc()
                    filtered_data ={key: [v for v in value if v is not None] for key, value in chart_data.items()}
                    continue
                        
                    if len(tab_val) > 0:
                        output[slide_no][f"chart_{chart_no}"] =filtered_data
                        j+=1

        #image
        image=""
        for shape_id, shape_pos in value["image"].items():
            image += extract_data(meta_json[slide_no]["ids"][shape_id])
        output[slide_no]["text"] = image

    # speaker notes
    # output[slide_no]["speaker notes"] =extract_speaker_notes(slide)
    return output

