
import streamlit as st
import os
import json
import pandas as pd
from collections import OrderedDict

def app():
    '''
    crea el mkdocs y lo arranca y lo incrusta en el st si esta disponible
    '''
    st.markdown("[Reset Documentation](/%F0%9F%93%9A_Documentacion)")

    files = sorted(os.listdir(f'assets/bookmarks'))
    files = [array for array in files if "bookmarks" in array]
    st.write(files[-1])
    with open('assets/bookmarks/'+files[-1], "r") as f:
        bb = json.load(f)
    df=pd.DataFrame(bb['children'][1]['children'])
    df=df.fillna('')
    tags=[]
    for i,r in df.iterrows():
        tags.append(r.tags.split(',')[0])
        # st.write(r.tags)
        # st.write(r.tags.split(','))
    # st.write(tags)
    tagss=list(OrderedDict.fromkeys(tags))

    # st.write(tagss)

    print(tagss[3])



    tag = st.selectbox(
        'Tags',
       tagss,)

    st.write('You selected:', tag)

    for i,r in df.iterrows():
        if tag in r.tags :
            st.write(f'''[{r.title}]({r.uri})''')

if __name__ == "__main__":
    app()
