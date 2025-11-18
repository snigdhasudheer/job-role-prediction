import streamlit as st
import pandas as pd
# import matplot.pyplot as plt
# import seaborn as sns

@st.cache
def load_data():
    df=pd.read_csv("resume_data.csv")
    return df

df=load_data()  


def show_explore_page():
    st.title("Explore the job roles")
    st.write(
        
    )
plt.figure(figsize=(15,4))
plt.xticks(rotation=90)
ax=sns.countplot(x='Category',data=df,palette='Set2')
for p in ax.patches:
    ax.annotate(str(p.get_height()),(p.get_x()*1.01,p.get_height()*1.01))
    
st.write("""#### Number of data of different job roles""")
st.pyplot(plt)
    
