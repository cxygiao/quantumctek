import pandas as pd
import re

def list_to_dataframe(circ,tra_a,tra_b,initial_mapping_list):
    data = []

    for sublist in circ:
        if sublist[0] == 's':
            b = sublist[5:-1]
            r = r'[,]'
            swap_gate = re.split(r, b)
            if sorted(map(int, swap_gate)) == [tra_a,tra_b]:
                data.append({'k': 'st', 'c': initial_mapping_list[int(swap_gate[0])], 't': initial_mapping_list[int(swap_gate[1])]})
            else:
                data.append({'k': 'swap', 'c': initial_mapping_list[int(swap_gate[0])], 't': initial_mapping_list[int(swap_gate[1])]})
        elif isinstance(sublist[0], str):
            data.append({'k': sublist[0], 'c': -1, 't': initial_mapping_list[sublist[1]]})
        else:
            data.append({'k': 'cz', 'c': initial_mapping_list[sublist[0]], 't': initial_mapping_list[sublist[1]]})

    df = pd.DataFrame(data, columns=['k', 'c', 't'])
    return df


