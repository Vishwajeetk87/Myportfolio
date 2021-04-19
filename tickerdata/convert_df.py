import pandas as pd
import os
from . import google_sheets as doc

def sheets_to_df():
    result = doc.read_portfolio()
    df_list=[]
    for res in result:
        values = res.get('values',[])
        tab = res.get('range','').split("!")[0]
        df_list.append(dict(frame=pd.DataFrame(values[1:],columns=values[0]),tab=tab))

    return df_list

