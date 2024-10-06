import streamlit as st
import pandas as pd
import altair as alt

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap" rel="stylesheet">
<style>
    .vega-embed * {
        font-family: 'Urbanist', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("CIJ by the numbers")

st.markdown("[Comprehensible Japanese (CIJ)](https://cijapanese.com/) is a \
            video platform for learning Japanese.")

video_df = pd.read_csv("video_data.tsv", sep="\t")

# Plot the WPM histogram

# Data for vertical lines corresponding to each level
line_data = pd.DataFrame({
    'x': [75, 91, 124, 149],
    'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
    'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
})

selection = alt.selection_point(fields=['level'], bind='legend', on='click')

highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

histogram = alt.Chart(video_df).mark_bar(
    opacity=0.5,
    binSpacing=3,
    stroke='black',
    strokeWidth=0,
    cornerRadius=5,
    cursor="pointer"
).encode(
    alt.X(
        'wpm:Q',
        bin=alt.Bin(maxbins=20),
        title='Words per minute',
        axis=alt.Axis(
            labelFontSize=14, 
            titleFontSize=18,
            titleFont='Urbanist',
            titleColor='black',
            titleFontWeight='normal',
            #titleFontStyle='italic',
            titlePadding=20
        )
    ),
    alt.Y(
        'count()', 
        title="Num. videos",
        axis=alt.Axis(
            labelFontSize=14, 
            titleFontSize=18,
            titleFont='Urbanist',
            titleColor='black',
            titleFontWeight='normal',
            #titleFontStyle='italic',
            titlePadding=20,
            tickCount=5
        ),
        scale=alt.Scale(domain=[0,100])
    ).stack(None),
    alt.Color(
        'level:N', 
        scale=alt.Scale(range=['#a5bee4', '#9ad6d8', '#c7aecd', '#dd9e9e']),
        sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        legend=alt.Legend(
            title='CIJ Level',
            titleFont='Urbanist',
            titleFontSize=18,
            titleFontWeight='bolder',
            labelFontSize=16,
            labelFont='Urbanist',
            symbolType='circle',
            symbolSize=200,
            orient='right',
            direction='vertical',
            fillColor='white',
            padding=10,
            cornerRadius=5,
        )
    ),
    tooltip=[
        alt.Tooltip('wpm:Q', title='Words per minute:', bin=True),  # Properly indicate that `wpm` is binned
        alt.Tooltip('level:N', title='Level:'),
        alt.Tooltip('count()', title='Video count:')
    ],
    opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
    strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
).properties(
    #width=750,
    #width='container',
    #height='container',
    #background='beige',
    #padding=50,
    title=alt.TitleParams(
        text='Rate of speech in words per minute (WPM)',
        offset=20,
        #subtitle='(clickable)',
        font='Urbanist',
        fontSize=24,
        fontWeight='normal',
        anchor='middle',
        color='black',
        subtitleFontSize=15,
        subtitleColor='gray'
    )
).add_params(
    selection,
    highlight
)

# Vertical lines corresponding to each level
vertical_lines = alt.Chart(line_data).mark_rule(
    color='red',
    strokeWidth=6,
    strokeDash = [5, 4], # first arg is length, second is gap
).encode(
    x='x:Q',
    tooltip=[
        alt.Tooltip('x:N', title='Median WPM:'),
        alt.Tooltip('level:N', title='Level:')
    ],
    #color=alt.condition(select, 'level:N', alt.value('gray')),  # Link the color with the selection
    color=alt.Color(
        'level:N',
        scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),  # Use the same color scale as the histogram
        sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        legend=None  # No legend for lines, it is already shown in the histogram
    ),
    opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
).add_params(
    selection,
    highlight
)

text_labels = alt.Chart(line_data).mark_text(
    align='left',  # Align text to the left of the line
    dx=5,  # Offset the text to the right by 5 pixels
    dy=-5, # Adjust vertical positioning
    fontSize=16,
    fontWeight='bold'
).encode(
    x='x:Q',
    y=alt.value(0),  # Positioning y at the top of the chart, can be adjusted as needed
    text=alt.Text('x:Q', format='.0f'),  # Display the x value, formatted as an integer
    color=alt.Color(
        'level:N',
        scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
        sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        legend=None
    )
)

#layered_chart = alt.layer(histogram, background='#f6f8fb')
layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='#f6f8fb')

st.altair_chart(layered_chart, use_container_width=True)