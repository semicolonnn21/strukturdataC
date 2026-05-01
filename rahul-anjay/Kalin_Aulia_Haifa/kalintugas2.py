import streamlit as st
from collections import Counter
import pandas as pd

st.title("Word Count Komentar Sosial Media")

text = st.text_area("Masukkan komentar:" , "Dubai chewy cookie ditoko ini ya lumayan, luarnya kaya ngga  pake marshmallow malah kaya adonan mochi, kunafanya juga manis banget rasanya kaya remukan chocolatos dan pistchionya kurang berasa jadi harga 30k 10cs kurang worth it ya ngga merekomendasikan untuk repurchase")


if text:
    words = text.split()
    freq = Counter(words)
    df = pd.DataFrame(freq.items(), columns=["Kata", "Frekuensi"])
    
    st.write(df)
    st.bar_chart(df.set_index("Kata"))