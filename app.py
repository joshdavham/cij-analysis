import streamlit as st
import pandas as pd
import altair as alt

#st.set_page_config(layout="wide")


#st.markdown("""
#<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap" rel="stylesheet">
#<style>
#    .vega-embed * {
#        font-family: 'Urbanist', sans-serif;
#    }
#</style>
#""", unsafe_allow_html=True)

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
            #titleFont='Urbanist',
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
            #titleFont='Urbanist',
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
            #titleFont='Urbanist',
            titleFontSize=18,
            titleFontWeight='bolder',
            labelFontSize=16,
            #labelFont='Urbanist',
            symbolType='circle',
            symbolSize=200,
            symbolStrokeWidth=0,
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
    height=500,
    #background='beige',
    #padding=50,
    title=alt.TitleParams(
        text='Rate of speech in words per minute (WPM)',
        offset=20,
        #subtitle='(clickable)',
        #font='Urbanist',
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
    strokeDash = [10, 2], # first arg is length, second is gap
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
    align='center',  # Align text to the left of the line
    dx=0,  # Offset the text to the right by 5 pixels
    dy=-10, # Adjust vertical positioning
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
    ),
    opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
)


if st.checkbox('Show medians'):
    layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='#f6f8fb')
else:
    layered_chart = alt.layer(histogram, background='#f6f8fb')

st.altair_chart(layered_chart, use_container_width=True)

# wpm vs sps chart

def get_wpm_vs_sps_chart(interactive=False):

    selection = alt.selection_point(fields=['level'], bind='legend', on='click')

    highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

    # Create the scatter plot
    scatter_plot = alt.Chart(video_df).mark_circle(
        cursor='pointer',
        size=80,
    ).encode(
        x=alt.X(
            'wpm:Q',
            scale=alt.Scale(domain=[30,215]),
            title='Words per minute',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20
            )
        ),
        y=alt.Y(
            'sps:Q',
            title='Syllables per second',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20,
                #tickCount=5
            ),
        ),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['#a5bee4', '#9ad6d8', '#c7aecd', '#dd9e9e']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=alt.Legend(
                title='CIJ Level',
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
                symbolType='circle',
                symbolSize=200,
                #symbolStrokeWidth=3,
                orient='right',
                direction='vertical',
                #fillColor='black',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('video:N', title='Video number:'),
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('wpm:Q', title='WPM:'),
            alt.Tooltip('sps:Q', title='SPS:'),

        ],
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.2)),
        #strokeWidth=alt.condition(selection | highlight, alt.value(6), alt.value(2))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Rate of speech: Syllables per second vs. words per minute',
            offset=20,
            #subtitle='(clickable)',
            #font='Urbanist',
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

    # Display the plot
    if interactive:
        return scatter_plot.interactive()
    else:
        return scatter_plot
    
if st.checkbox('Enable zooming and panning ( ↕ / ↔️ )'):
    wpm_vs_sps_chart = get_wpm_vs_sps_chart(interactive=True)
else:
    wpm_vs_sps_chart = get_wpm_vs_sps_chart(interactive=False)

st.altair_chart(wpm_vs_sps_chart, use_container_width=True)

# word coverage chart

def get_word_coverage_chart():

    word_coverage_df = pd.read_csv('word_coverage_df_plot.tsv', sep='\t')

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [4295, 5606, 6853, 9085],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    selection = alt.selection_point(fields=['level'], bind='legend', on='click')

    highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

    line_chart = alt.Chart(word_coverage_df).mark_line(
        cursor='pointer',
        point=False,
    ).encode(
        x=alt.X(
            'rank:Q', 
            scale=alt.Scale(domain=[-10,16000]),
            #scale=alt.Scale(domain=[1000,16000]),
            title='Number of words known',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20
            )
        ),
        y=alt.Y(
            'coverage_perc:Q', 
            scale=alt.Scale(domain=[0,105]), 
            #scale=alt.Scale(domain=[90,101]),
            title='% of words understood',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20,
                tickCount=5
            ),
        ),
        #x=alt.X('rank:Q', scale=alt.Scale(domain=[1000,16000])),
        #y=alt.Y('coverage_perc:Q', scale=alt.Scale(domain=[90,101])),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['#a5bee4', '#9ad6d8', '#c7aecd', '#dd9e9e']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=alt.Legend(
                title='CIJ Level',
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
                symbolType='circle',
                symbolSize=200,
                #symbolStrokeWidth=3,
                orient='right',
                direction='vertical',
                #fillColor='black',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('word:N', title='Word: '),
            alt.Tooltip('rank:Q', title="CIJ rank: "),
            alt.Tooltip('coverage_perc_str:N', title='Word coverage: '),
            alt.Tooltip('level:N', title='Level: ')
        ],
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.2)),
        strokeWidth=alt.condition(selection | highlight, alt.value(6), alt.value(2))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Word coverage curves',
            offset=20,
            #subtitle='(clickable)',
            #font='Urbanist',
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
        strokeWidth=4,
        strokeDash = [10, 2], # first arg is length, second is gap
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Words needed to reach 98%:'),
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
    )#.interactive()

    text_labels = alt.Chart(line_data).mark_text(
        align='center',  # Align text to the left of the line
        dx=0,  # Offset the text to the right by 5 pixels
        dy=-10, # Adjust vertical positioning
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
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    #layered_chart = alt.layer(line_chart, background='#f6f8fb')
    layered_chart = alt.layer(line_chart, vertical_lines, text_labels, background='#f6f8fb')

    return layered_chart


def get_zoomed_word_coverage_chart():

    word_coverage_df = pd.read_csv('word_coverage_df_plot.tsv', sep='\t')

    word_coverage_df_sub = word_coverage_df.loc[word_coverage_df['coverage_perc']>=90]

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [4295, 5606, 6853, 9085],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    selection = alt.selection_point(fields=['level'], bind='legend', on='click')

    highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

    line_chart = alt.Chart(word_coverage_df_sub).mark_line(
        cursor='pointer',
        point=False,
        strokeWidth=6
    ).encode(
        x=alt.X(
            'rank:Q', 
            #scale=alt.Scale(domain=[-10,16000]),
            scale=alt.Scale(domain=[1000,16000]),
            title='Number of words known',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20
            )
        ),
        y=alt.Y(
            'coverage_perc:Q', 
            #scale=alt.Scale(domain=[0,105]), 
            scale=alt.Scale(domain=[90,101]),
            title='% of words understood',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20,
                tickCount=5
            ),
        ),
        #x=alt.X('rank:Q', scale=alt.Scale(domain=[1000,16000])),
        #y=alt.Y('coverage_perc:Q', scale=alt.Scale(domain=[90,101])),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['#a5bee4', '#9ad6d8', '#c7aecd', '#dd9e9e']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=alt.Legend(
                title='CIJ Level',
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
                symbolType='circle',
                symbolSize=200,
                #symbolStrokeWidth=3,
                orient='right',
                direction='vertical',
                #fillColor='black',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('word:N', title='Word: '),
            alt.Tooltip('rank:Q', title="CIJ rank: "),
            alt.Tooltip('coverage_perc_str:N', title='Word coverage: '),
            alt.Tooltip('level:N', title='Level: ')
        ],
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.2)),
        #strokeWidth=alt.condition(selection | highlight, alt.value(6), alt.value(2))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Word coverage curves',
            offset=20,
            #subtitle='(clickable)',
            #font='Urbanist',
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
        strokeWidth=4,
        strokeDash = [10, 2], # first arg is length, second is gap
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Words needed to reach 98%:'),
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
        #strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )#.interactive()

    text_labels = alt.Chart(line_data).mark_text(
        align='center',  # Align text to the left of the line
        dx=0,  # Offset the text to the right by 5 pixels
        dy=-10, # Adjust vertical positioning
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
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    #layered_chart = alt.layer(line_chart, background='#f6f8fb')
    layered_chart = alt.layer(line_chart, vertical_lines, text_labels, background='#f6f8fb')

    return layered_chart


if st.checkbox('Zoom in'):

    word_coverage_chart = get_zoomed_word_coverage_chart()

else:

    word_coverage_chart = get_word_coverage_chart()

st.altair_chart(word_coverage_chart, use_container_width=True)
# grammar table

data = {
    'Complete Beginner': [0.02638719922016275 ,0.0192492959834, 0.00476028625918155, 0.2503071253071253],
    'Beginner': [0.0473047304730473, 0.0266429840142095, 0.005813953488372, 0.2454068241469816],
    'Intermediate': [0.06625719079578135, 0.03514773095199635, 0.0087719298245614, 0.23239271705403663],
    'Advanced': [0.0766787658802177, 0.0373056994818652, 0.0108588351431391, 0.2237101220953131]
}
df = pd.DataFrame(data)

row_labels = ['Median Perc. Subordinating Conjunctions', 'Median Perc. Adverbs', 'Median Perc. Determiners', 'Median Perc. Nouns']
df.index = row_labels

# Apply header-specific styling using set_table_styles
styled_df = df.style.set_table_styles(
    {
        'Complete Beginner': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(165, 190, 228, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Beginner': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(154, 214, 216, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Intermediate': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(199, 174, 205, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Advanced': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(221, 158, 158, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
}).format("{:.2%}")

# Display the styled DataFrame
st.markdown(styled_df.to_html(), unsafe_allow_html=True)

# word origin table

data = {
    'Complete Beginner': [0.06999874574159035, 0.8578043261266064, 0.03301790801790795],
    'Beginner': [0.0955284552845528, 0.8399311531841652, 0.0279441117764471],
    'Intermediate': [0.1165702954621605, 0.8259877335615461, 0.0241447813837379],
    'Advanced': [0.1303328645100797, 0.8225274725274725, 0.0157535445475231],
}
df = pd.DataFrame(data)

row_labels = ['Median Perc. Kango (漢語)', 'Median Perc. Wago (和語)', 'Median Perc. Garaigo (外来語)']
df.index = row_labels

# Apply header-specific styling using set_table_styles
styled_df = df.style.set_table_styles(
    {
        'Complete Beginner': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(165, 190, 228, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Beginner': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(154, 214, 216, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Intermediate': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(199, 174, 205, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
        'Advanced': [
            {'selector': 'th.col_heading.level0', 'props': [('background-color', 'rgba(221, 158, 158, 0.45)')]},
            {'selector': 'td:hover', 'props': [('background-color', '#e0f7fa')]}
        ],
}).format("{:.2%}")

# Display the styled DataFrame
st.markdown(styled_df.to_html(), unsafe_allow_html=True)