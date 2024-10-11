import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='What makes comprehensible input comprehensible?',
    page_icon='favicon.svg'
)

# colors white the index columns of rendered dataframes
st.markdown(
    """
    <style>
    .dataframe-div {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# functions for loading data
@st.cache_data
def load_dataframes():

    video_df = pd.read_csv("video_data.tsv", sep="\t")
    word_coverage_df = pd.read_csv('word_coverage_df_plot.tsv', sep='\t')
    num_video_df = pd.read_csv('num_video_df.tsv', sep='\t')

    return video_df, word_coverage_df, num_video_df

def get_grammar_table():

    data = {
        'Complete Beginner': [0.02638719922016275 ,0.0192492959834, 0.00476028625918155, 0.2503071253071253, 0.18554386037363785, 0.01622086690206438, 0.04537920642893019, 0.1203097143691203],
        'Beginner': [0.0473047304730473, 0.0266429840142095, 0.005813953488372, 0.2454068241469816, 0.1773049645390071, 0.01384083044982699, 0.02676864244741874, 0.13333333333333333],
        'Intermediate': [0.06625719079578135, 0.03514773095199635, 0.0087719298245614, 0.23239271705403663, 0.1587691162151326, 0.010784997932175352, 0.022392603507910194, 0.13379268084136123],
        'Advanced': [0.0766787658802177, 0.0373056994818652, 0.0108588351431391, 0.2237101220953131, 0.14922184925236498, 0.009050978304272594, 0.020185708518368994, 0.1364369670430975]
    }
    df = pd.DataFrame(data)

    row_labels = ['Median Perc. Subordinating Conjunctions', 'Median Perc. Adverbs', 'Median Perc. Determiners', 'Median Perc. Nouns', 'Median Perc. Auxiliaries', 'Median Perc. Numerals', 'Median Perc. Pronouns', 'Median Perc. Verbs']
    df.index = row_labels

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
            ]
    }).set_properties(**{'background-color': 'white'}).format("{:.2%}")

    return styled_df

def get_word_origin_table():

    data = {
        'Complete Beginner': [0.06999874574159035, 0.8578043261266064, 0.03301790801790795],
        'Beginner': [0.0955284552845528, 0.8399311531841652, 0.0279441117764471],
        'Intermediate': [0.1165702954621605, 0.8259877335615461, 0.0241447813837379],
        'Advanced': [0.1303328645100797, 0.8225274725274725, 0.0157535445475231],
    }
    df = pd.DataFrame(data)

    row_labels = ['Median Perc. Kango (漢語)', 'Median Perc. Wago (和語)', 'Median Perc. Garaigo (外来語)']
    df.index = row_labels

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
    }).set_properties(**{'background-color': 'white'}).format("{:.2%}")

    return styled_df

# functions for loading data visualizations
@st.cache_data
def get_wpm_chart(show_medians=False):

    line_data = pd.DataFrame({
        'x': [75, 91, 124, 149],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

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
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
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
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
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
            alt.Tooltip('wpm:Q', title='Words per minute:', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        height=500,
        title=alt.TitleParams(
            text='Rate of speech in words per minute (WPM)',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median WPM:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.0f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )


    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_wpm_vs_sps_chart(interactive=False):

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
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20
            )
        ),
        y=alt.Y(
            'sps:Q',
            title='Syllables per second',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
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
                orient='right',
                direction='vertical',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('video:N', title='Video number:'),
            alt.Tooltip('wpm:Q', title='WPM:'),
            alt.Tooltip('sps:Q', title='SPS:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.2)),
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Rate of speech: Syllables per second vs. words per minute',
            offset=20,
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
    ).configure(
        background='white'
    )

    if interactive:
        return scatter_plot.interactive()
    else:
        return scatter_plot

@st.cache_data
def get_sentence_length_hist(show_medians=False):

    line_data = pd.DataFrame({
        'x': [7.60, 10.45, 16.17, 19.39],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'mean_sentence_length:Q',
            bin=alt.Bin(maxbins=30),
            title='Words per sentence',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
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
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
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
            alt.Tooltip('mean_sentence_length:Q', title='Average sentence length:', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Average sentence length (words per sentence)',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median avg. sentence length:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.2f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    if show_medians:

        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')

    else:

        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_repetition_hist(show_medians=False):

    video_df['average_rel_reps_perc'] = 100.0 * video_df['average_rel_reps']

    sub_video_df = video_df[video_df['average_rel_reps_perc'] <= 2.0]

    line_data = pd.DataFrame({
        'x': [0.99, 0.62, 0.37, 0.23],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(sub_video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'average_rel_reps_perc:Q',
            bin=alt.Bin(maxbins=30),
            title='Word repetitions (%)',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
            ),
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
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
                titleFontSize=18,
                titleFontWeight='bolder',
                labelFontSize=16,
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
            alt.Tooltip('average_rel_reps:Q', title='Average repetitions (%):', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Average amount of repetition per word',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        alt.X(
            'x:Q'
        ),
        tooltip=[
            alt.Tooltip('x:N', title='Median avg. repetitions (%):'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1)),
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        alt.X(
            'x:Q'
        ),
        y=alt.value(0),
        text=alt.Text('x:Q', format='.2f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    if show_medians:

        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')

    else:

        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_word_coverage_chart(zoom=False):

    if zoom:
        word_coverage_df_sub = word_coverage_df.loc[word_coverage_df['coverage_perc']>=90]
    else:
        word_coverage_df_sub = word_coverage_df

    line_data = pd.DataFrame({
        'x': [4295, 5606, 6853, 9085],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    line_chart = alt.Chart(word_coverage_df_sub).mark_line(
        cursor='pointer',
        point=False,
    ).encode(
        x=alt.X(
            'rank:Q',
            scale=alt.Scale(domain=[1000,16000]) if zoom else alt.Scale(domain=[-10,16000]),
            title='Number of words known',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20
            )
        ),
        y=alt.Y(
            'coverage_perc:Q',
            scale=alt.Scale(domain=[90,101]) if zoom else alt.Scale(domain=[0,105]),
            title='% of words understood',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
                tickCount=5
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
                orient='right',
                direction='vertical',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('word:N', title='Word: '),
            alt.Tooltip('rank:Q', title="CIJ rank: "),
            alt.Tooltip('coverage_perc_str:N', title='Word coverage: '),
            alt.Tooltip('level:N', title='Curve: ')
        ],
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.2)),
        strokeWidth=alt.condition(selection | highlight, alt.value(6), alt.value(2))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Word coverage curves',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=4,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Words needed to reach 98%:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.0f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    layered_chart = alt.layer(line_chart, vertical_lines, text_labels, background='white')

    return layered_chart

@st.cache_data
def get_ne_spot_hist(show_medians=False):

    line_data = pd.DataFrame({
        'x': [3859, 5229, 6698, 7925],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'ne_spot:Q',
            bin=alt.Bin(maxbins=30),
            title='Number of words known',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
                tickCount=5
            ),
            scale=alt.Scale(domain=[0,40])
        ).stack(None),
        alt.Color(
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
                symbolStrokeWidth=0,
                orient='right',
                direction='vertical',
                fillColor='white',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('ne_spot:Q', title='Vocab size for 98%.:', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Vocab size needed for 98% coverage (videos)',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median vocab size needed for 98% cov:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.0f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    
    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_tfplr_hist(show_medians=False):

    line_data = pd.DataFrame({
        'x': [3.82, 4.30, 4.76, 5.21],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'tfp_log_ranks_unique:Q',
            bin=alt.Bin(maxbins=30),
            title='Log ranks',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=30,
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
                tickCount=5
            ),
            scale=alt.Scale(domain=[0,80])
        ).stack(None),
        alt.Color(
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
                symbolStrokeWidth=0,
                orient='right',
                direction='vertical',
                fillColor='white',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('tfp_log_ranks_unique:Q', title='25th perc. log rank:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='25th percentile word-frequency log ranks',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median 25th perc. log rank:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.2f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_sconj_hist(show_medians=False):

    video_df['sconj_props_perc'] = 100.0 * video_df['sconj_props']

    line_data = pd.DataFrame({
        'x': [2.64, 4.73, 6.63, 7.67],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'sconj_props_perc:Q',
            bin=alt.Bin(maxbins=30),
            title='Percentage of sub. conj.',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=30,
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
                tickCount=5
            ),
            scale=alt.Scale(domain=[0,50])
        ).stack(None),
        alt.Color(
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
                symbolStrokeWidth=0,
                orient='right',
                direction='vertical',
                fillColor='white',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('sconj_props_perc:Q', title='Perc. sub. conj:', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Frequency of subordinating conjunctions',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median perc. of sub. conj:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.2f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    
    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def get_kango_hist(show_medians=False):

    video_df['kan_props_perc'] = 100.0 * video_df['kan_props']

    line_data = pd.DataFrame({
        'x': [7.00, 9.55, 11.66, 13.03],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    histogram = alt.Chart(video_df).mark_bar(
        opacity=0.5,
        binSpacing=3,
        stroke='black',
        strokeWidth=0,
        cornerRadius=5,
        cursor="pointer"
    ).encode(
        alt.X(
            'kan_props_perc:Q',
            bin=alt.Bin(maxbins=30),
            title='Percentage of kango',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=30,
            )
        ),
        alt.Y(
            'count()', 
            title="Num. videos",
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                titleColor='black',
                titleFontWeight='normal',
                titlePadding=20,
                tickCount=5
            ),
            scale=alt.Scale(domain=[0,40])
        ).stack(None),
        alt.Color(
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
                symbolStrokeWidth=0,
                orient='right',
                direction='vertical',
                fillColor='white',
                padding=10,
                cornerRadius=5,
            )
        ),
        tooltip=[
            alt.Tooltip('kan_props_perc:Q', title='Percentage of kango:', bin=True),
            alt.Tooltip('count()', title='Video count:'),
            alt.Tooltip('level:N', title='Level:'),
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        width='container',
        height=500,
        title=alt.TitleParams(
            text='Frequency of kango',
            offset=20,
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

    vertical_lines = alt.Chart(line_data).mark_rule(
        color='red',
        strokeWidth=6,
        strokeDash = [10, 2],
    ).encode(
        x='x:Q',
        tooltip=[
            alt.Tooltip('x:N', title='Median perc. kango:'),
            alt.Tooltip('level:N', title='Level:')
        ],
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'yellow']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1))
    ).add_params(
        selection,
        highlight
    )

    text_labels = alt.Chart(line_data).mark_text(
        align='center',
        dx=0,
        dy=-10,
        fontSize=16,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y=alt.value(0),
        text=alt.Text('x:Q', format='.0f'),
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),
    )

    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

@st.cache_data
def render_vanilla_heatmap():

    corr_matrix = num_video_df.corr()

    variable_of_interest = 'Level'

    sorted_vars = corr_matrix[variable_of_interest].sort_values(ascending=False).index

    sorted_corr_matrix = corr_matrix.loc[sorted_vars, sorted_vars]

    plt.figure(figsize=(10, 8))
    sns.heatmap(sorted_corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")

    st.pyplot(plt.gcf())

@st.cache_data
def render_level_row_unordered():

    corr_matrix = num_video_df.drop(['Proportion of determiners', 'Proportion of nouns', 'Proportion of wago', 'Proportion of gairaigo', 'Proportion of verbs', 'Proportion of numerals'], axis=1).corr()

    variable_of_interest = 'Level'

    sorted_vars = corr_matrix[variable_of_interest].sort_values(ascending=False).index

    sorted_vars = sorted_vars.drop(variable_of_interest)

    first_row_matrix = corr_matrix.loc[[variable_of_interest], sorted_vars]

    plt.figure(figsize=(10, 1))
    sns.heatmap(first_row_matrix, annot=True, cmap='coolwarm', fmt=".3f", cbar_kws={'label': 'Correlation'})

    st.pyplot(plt.gcf())

@st.cache_data
def render_level_col_ordered():

    corr_matrix = num_video_df.drop(['Proportion of determiners', 'Proportion of nouns', 'Proportion of wago', 'Proportion of gairaigo', 'Proportion of verbs', 'Proportion of numerals'], axis=1).corr()

    variable_of_interest = 'Level'

    correlations = corr_matrix[variable_of_interest]

    sorted_vars = correlations.abs().sort_values(ascending=False).index

    sorted_vars = sorted_vars.drop(variable_of_interest)

    sorted_corr_matrix = corr_matrix.loc[[variable_of_interest], sorted_vars]

    transposed_corr_matrix = sorted_corr_matrix.T

    plt.figure(figsize=(2, 3))
    sns.heatmap(transposed_corr_matrix, annot=True, cmap='coolwarm', fmt=".3f", cbar_kws={'label': 'Correlation'})

    st.pyplot(plt.gcf())

# load the data
video_df, word_coverage_df, num_video_df = load_dataframes()
grammar_table = get_grammar_table()
word_origin_table = get_word_origin_table()

# allows interactivity in the vega altair plots
selection = alt.selection_point(fields=['level'], bind='legend', on='click')
highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

###
# INTRO
###
st.markdown("Note: this analysis is meant to viewed on a computer and not a phone (sorry!)")

st.markdown("[Code and data can be found [here](https://github.com/joshdavham/cij-analysis)]")

st.markdown("# What makes comprehensible input *comprehensible*?")

st.markdown("**Comprehensible input** (or CI, for short) is a language teaching technique where teachers \
            speak in a way that is understandable to their students. \
            It is believed by many that CI is one of the most optimal and natural \
             ways to acquire a foreign language \
            ...but, what exactly is about CI that makes it comprehensible?")

st.markdown("To answer this question, I'll be analyzing the videos on \
            [cijapanese.com](https://cijapanese.com/) (CIJ), a \
            video platform for learning Japanese.")

###
# RATE OF SPEECH
###
st.markdown("## How fast is CI?")

st.markdown("If we measure how fast the teachers speak on CIJ, we find that \
            they speak more slowly in videos meant for beginners and more quickly \
            for advanced learners.")

st.markdown("**(THESE GRAPHS ARE CLICKABLE)**")

if st.checkbox('Show medians', value=True, key='wpm'):
    layered_chart = get_wpm_chart(show_medians=True)
else:
    layered_chart = get_wpm_chart(show_medians=False)

st.altair_chart(layered_chart, use_container_width=True)

st.markdown("To put this data into perspective, native Japanese speakers \
            can speak at rates of over 200 wpm, meaning that most of the videos \
            on CIJ have been adapted to be a lot slower than that!")
    
if st.checkbox('Enable zooming and panning ( ↕ / ↔️ )'):
    wpm_vs_sps_chart = get_wpm_vs_sps_chart(interactive=True)
else:
    wpm_vs_sps_chart = get_wpm_vs_sps_chart(interactive=False)

st.altair_chart(wpm_vs_sps_chart, use_container_width=True)

st.markdown("We can also measure the rate of speech in syllables per second (SPS) \
            and compare it to words per minute.")

###
# STATISTICS LESSON
###
st.markdown("## A quick statistics lesson")

st.markdown("Before we continue this analysis, there's some basic things you should know.")

st.markdown("### The data")

st.markdown("The dataset we'll be analyzing comprises of just under 1,000 videos. \
            In particular, we'll be analyzing the subtitles of the videos.")

st.markdown('Every video has a Level: **Complete Beginner**, **Beginner**, \
            **Intermediate**, or **Advanced**.')

st.markdown("### The statistics")

st.markdown("The goal of this analysis is to find features in the video data that lead \
            to a specific pattern called an \"ordering\".")

st.markdown("We're specifically looking for *any* statistic that can lead to an \
            ordering of the levels in one of the two following orders:")

st.markdown("> Complete Beginner < Beginner < Intermediate < Advanced")
st.markdown("or")
st.markdown("> Complete Beginner > Beginner > Intermediate > Advanced")

st.markdown("For example: if a statistic is small for Complete Beginnner videos, but gets bigger \
            for Beginner, Intermediate, then Advanced videos, it suggests \
            that this is a good statistic for determining what makes a video comprehensible. \
            In fact, we already saw this above when measuring the **words per minute** statistic.")

st.markdown("Okay! Now we can continue.")

###
# SENTENCE LENGTH
###
st.markdown("## Sentence length")

st.markdown("Videos meant for beginners tend to have shorter sentences on average.")

if st.checkbox('Show medians', value=True, key='sentence_length'):
    sentence_length_hist = get_sentence_length_hist(show_medians=True)
else:
    sentence_length_hist = get_sentence_length_hist(show_medians=False)

st.altair_chart(sentence_length_hist, use_container_width=True)

st.markdown("This makes sense because long sentences generally tend to be more complex and packed with information \
            whereas short sentences are usually easier to understand.")

###
# AMOUNT OF REPETITION
###
st.markdown("## Amount of repetition")

st.markdown("Words are repeated more often in easier videos.")

if st.checkbox('Show medians', value=True, key='repetition'):
    repetition_hist = get_repetition_hist(show_medians=True)
else:
    repetition_hist = get_repetition_hist(show_medians=False)

st.altair_chart(repetition_hist, use_container_width=True)

st.markdown("If you don't catch a word the first time it's said, there's more opportunities \
            in the easier videos to hear that word again.")

###
# HOW MANY WORDS
###
st.markdown("## How many words you need to know")

st.markdown("A popular statistic in language learning circles is that you generally \
            need to know around 98% of words in a given piece of content to understand it well. \
            This statistic is known as 'word coverage', the percentage of words you know in a given text.")

st.markdown("How many words do you need to know to understand 98% of the words in each level?")

st.markdown("If we take all the words in CIJ, count them then order them from most common, to least common, \
             we can calculate the word coverage you get at different vocabulary sizes. \
            For example, if we learn the top 500 words from CIJ, then we'll know around 80% of the words in the \
            Complete Beginner videos. And if we learn the top 4,295 words, then we'll know 98% of the words in that category.")

if st.checkbox('Zoom in'):
    word_coverage_chart = get_word_coverage_chart(zoom=True)
else:
    word_coverage_chart = get_word_coverage_chart(zoom=False)

st.altair_chart(word_coverage_chart, use_container_width=True)

st.markdown("Using the same method of calculating word coverage as before, \
            we can also calculate how many of the top words you need to know \
            to achieve 98% word coverage in each video.")

if st.checkbox('Show medians', value=True, key='ne_spot'):
    ne_spot_hist = get_ne_spot_hist(show_medians=True)
else:
    
    ne_spot_hist = get_ne_spot_hist(show_medians=False)

st.altair_chart(ne_spot_hist, use_container_width=True)

st.markdown("In general, easier videos require smaller vocabulary sizes to understand.")

###
# WORD RARENESS
###
st.markdown("## Word rareness")

st.markdown("More advanced videos tend to use rare/uncommon words more often than easier videos.")

if st.checkbox('Show medians', value=True, key='tfplr'):
    # tfplr stands for "twenty fifth percentile log rank"
    tfplr_hist = get_tfplr_hist(show_medians=True)
else:
    tfplr_hist = get_tfplr_hist(show_medians=False)

st.altair_chart(tfplr_hist, use_container_width=True)

st.markdown("How common a word is, is known as its 'rank'. The most common word \
            in a text would be rank 1 and the fifth most common would be rank 5. \
            A word with a low rank is a commonly used word (e.g., 'it', 'walk', 'up') whereas a word with a high rank \
            is an uncommon or 'rare' word (e.g., 'esoteric', 'gauche', 'gallant').")

st.markdown("The words in the videos were compared to the ranks of words generated from a frequency list made from over 4,000 Japanese Netflix \
            TV episodes and movies. Duplicate ranks in the videos were removed, scaled with a log \
            function then used to compute the 25th percentile. This was necessary due \
            to power-law nature of word frequency distributions.")

st.markdown("(It's okay ff the above didn't quite make sense to you - just know that the above graph \
            demonstrates that easier videos tend to use more common words whereas \
            advanced videos tend to use more rare words!)")

###
# GRAMMAR
###
st.markdown("## Grammar")

st.markdown("Easier videos tend to use less [subordinating conjunctions](https://universaldependencies.org/ja/pos/SCONJ.html) than harder videos.")

if st.checkbox('Show medians', value=True, key='sconj'):
    sconj_hist = get_sconj_hist(show_medians=True)
else:
    sconj_hist = get_sconj_hist(show_medians=False)

st.altair_chart(sconj_hist, use_container_width=True)

st.markdown("We also notice differences in the use of other types of words.")

st.markdown(
    '<div class="dataframe-div">' + grammar_table.to_html() + "</div>"
    , unsafe_allow_html=True)

###
# WORD ORIGIN
###
st.markdown("## What type of word")

st.markdown("There are three main categories of words in Japanese:")
st.markdown("(1) Wago (和語), (2) Kango (漢語) and (3) Gairaigo (外来語)")
st.markdown("Wago are native Japanese words, Kango are Chinese words and Gairaigo are foreign words.")

st.markdown("Harder videos tend to use more Kango than easier videos")

if st.checkbox('Show medians', value=True, key='kango'):
    kango_hist = get_kango_hist(show_medians=True)
else:
    kango_hist = get_kango_hist(show_medians=False)

st.altair_chart(kango_hist, use_container_width=True)

st.markdown("In Japanese, Kango are somewhat analogous to French words in English. \
            These words tend to be more technical or sophisticated than other words.")

st.markdown("We also notice orderings when counting the percentage of Wago and Gairaigo as well.")

st.markdown(
    '<div class="dataframe-div">' + word_origin_table.to_html() + "</div>"
    , unsafe_allow_html=True)

###
# MOST IMPORTANT FACTORS
###
st.markdown("## Which factors matter the most?")

st.markdown("We've just found a number of statistics that lead to orderings in the data \
            but which statistics matter the most?")

st.markdown("To answer this, we can look at a correlation heatmap between each of the variables \
            and observe which statistics correlate the most strongly with the video's level.")

render_vanilla_heatmap()

st.markdown("In case you're not familiar with stuff like this, numbers close to 1 or -1 \
            represent a high level or correlation and numbers close to 0 represent a low level of correlation. \
            Positive numbers represent a positive relationship between the variables and negative numbers represent a \
            reverse relationship between the variables.")

st.markdown("Using a statistics rule of thumb and removing all variables that have correlations \
            weaker than 0.3 (and more than -0.3), we can identify the variables with the strongest correlations.")

if st.checkbox('Flip and sort by correlation strength'):
    render_level_col_ordered()
else:
    render_level_row_unordered()


st.markdown("To summarize (and simplify), this suggests that the most important factors in comprehensibility are:")

st.markdown("1. Rate of Speech")
st.markdown("2. Sentence length")
st.markdown("3. Amount of repetition of words")
st.markdown("4. How common/rare the words are")
st.markdown("5. Amount of subordinating conjunctions")
st.markdown("6. Vocabulary size")
st.markdown("7. Amount of pronouns")
st.markdown("8. Amount of adverbs")
st.markdown("9. Amount of auxiliaries")
st.markdown("10. Amount of Chinese words")

st.markdown("## Dicussion")

#st.markdown('')

st.markdown("### Thanks for reading ✌️")

st.markdown("---")

st.markdown("#### Futher discussion for hardcore nerds")

st.markdown("- No tests of statistical significance were conducted. This was purely meant as an EDA. \
            However, you can get the data from the repo linked at the top and conduct them yourself if you'd like. \
            I'd recommend starting with non-parametric tests like Kruskal-Wallis and moving on to pairwise tests \
            with a bonferonni correction if it's significant. Parametric tests may also be interesting.")

st.markdown("- Technically, I computed 'moras per second' - not syllables per second. I'm aware that this \
            is technically linguistically incorrect, but it still serves as close approximation and is easier \
            to understand for readers unfamiliar with Japanese linguistics.")

st.markdown("- The Mecab and Sudachi parsers (through Fugashi and Spacy) were used to analyze the transcripts. These parsers are not always 100% accurate.")

st.markdown("- When computing the statistics for repetition, word coverage and word frequency, lemmas were used rather than tokens.")

st.markdown("- Of the parsed words, while I did remove punctuation, I didn't otherwise verify that each token was an actual word. \
            There is likely some amount of noise in the data such as mis-parses, etc.")

st.markdown("- If you're like me, the word coverage plots also probably evoked a resemblance to Heap's Law. \
            More research would need to be done, but I suspect one may be able to find a link between word coverage and Heap's Law.")

st.markdown("- One should bare in mind that the learner levels were labelled by a small group of experts and not a large number of learners. \
            In other words, the difficulty levels are not objective, but rather an approximation of difficulty / natural acquistion order.")

st.markdown("- There were a number of statistics I also tried but didn't get orderings from:")

st.markdown("1. **Audibility** - My hypothesis was that the teachers would speak more clearly in easy videos and less clearly in harder videos. \
            To test this, I generated whisper transcripts for each video's audio file, converted both the whisper transcript \
            and the original transcript to katakana and compared the character error rate. I found no differences in the levels. \
            Furthermore I can't tell if this moreso invalidates my original hypothesis or if whisper is just that good.")

st.markdown("2. **Word length** - At least in English and French (the languages I know the best), longer words are generally considered harder. \
            My hypothesis was that the easier videos would use shorter words while the harder videos would use bigger words. \
            To test this, I parsed the transcripts and converted all words to katakana \
            to get a measure of how long the words were orally. I found no differences between the levels.")

st.markdown("3. **Range of vocabulary** - I suspected that easier videos may limit themselves to a smaller range of vocabulary than harder videos. \
            To measure this, I calculated unique word occurences / total word occurences but I found no ordering in the levels.")

st.markdown("4. **Other parts of speech** - I did test for orderings between the levels for other parts of speech such as: \
            proportion of adjectives, adpositions, coordinating conjunctions, interjections, particles and proper nouns \
            but ultimately didn't find any obvious orderings.")