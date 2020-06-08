
def delete_from_dict(dict_delete, structure):
    dict_del = dict_delete.copy()

    for key in structure:
        if key in dict_del:
            if dict_del[key] == None:
                continue
            
            depper_level_strucure = structure[key]
            depper_level_dict_del = dict_del[key]

            if isinstance(depper_level_strucure, str):
                dict_del[key].pop(depper_level_strucure)

            elif isinstance(depper_level_strucure, dict):
                delete_from_dict(depper_level_dict_del, depper_level_strucure)

            elif isinstance(depper_level_strucure, list):
                for index, item in enumerate(depper_level_strucure):
                    if isinstance(item, str):
                        depper_level_dict_del.pop(item)

                    elif isinstance(item, dict):
                        delete_from_dict(depper_level_dict_del, item)
                    
                    elif isinstance(item, list):
                        raise TypeError('Listas não podem estar empilhadas')
    return dict_del