import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("CIJ by the numbers")

st.markdown("[Comprehensible Japanese (CIJ)](https://cijapanese.com/) is a \
            video platform for learning Japanese.")

df = pd.read_csv("stats.tsv", sep="\t")

# Plot the WPM histogram
levels = list(df['level'].unique())
colors = ['red', 'green', 'blue', 'yellow']

fig, ax = plt.subplots()

for level, color in zip(levels, colors):
    subset = df[df['level'] == level]
    ax.hist(subset['wpm'], bins=10, edgecolor='black', color=color, alpha=0.5, label=f"Level {level}")

ax.legend(title="Level")
ax.set_xlabel("WPM")
ax.set_ylabel("Frequency")

st.pyplot(fig)