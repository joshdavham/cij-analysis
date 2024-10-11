import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='What makes comprehensible input comprehensible?',
    page_icon='favicon.svg'
)


#st.markdown("""
#<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap" rel="stylesheet">
#<style>
#    .vega-embed * {
#        font-family: 'Urbanist', sans-serif;
#    }
#</style>
#""", unsafe_allow_html=True)

@st.cache_data
def load_dataframes():

    video_df = pd.read_csv("video_data.tsv", sep="\t")
    word_coverage_df = pd.read_csv('word_coverage_df_plot.tsv', sep='\t')
    num_video_df = pd.read_csv('num_video_df.tsv', sep='\t')

    return video_df, word_coverage_df, num_video_df

video_df, word_coverage_df, num_video_df = load_dataframes()


st.markdown("Note: this analysis is meant to viewed on a computer and not a phone (sorry!)")

st.markdown("[Code can be found [here](https://github.com/joshdavham/cij-analysis)]")

st.markdown("# What makes comprehensible input *comprehensible*?")

st.markdown("**Comprehensible input** (or CI, for short) is a language teaching technique where teachers \
            speak in a way that is understandable to their students. \
            It is believed by many that CI is one of the most optimal and natural \
             ways to acquire a foreign language \
            ...but, what exactly is about CI that makes it comprehensible?")



st.markdown("To answer this question, I'll be analyzing the videos on \
            [cijapanese.com](https://cijapanese.com/) (CIJ), a \
            video platform for learning Japanese.")

# Plot the WPM histogram

st.markdown("## How fast is CI?")

st.markdown("If we measure how fast the teachers speak on CIJ, we find that \
            they speak more slowly in videos meant for beginners and more quickly \
            for advanced learners.")

#st.markdown("### Rate of speech in words per minute (WPM)")

@st.cache_data
def get_wpm_chart(show_medians=False):

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


    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart


if st.checkbox('Show medians'):

    layered_chart = get_wpm_chart(show_medians=True)

else:
    
    layered_chart = get_wpm_chart(show_medians=False)

st.altair_chart(layered_chart, use_container_width=True)

st.markdown("To put this data into perspective, native Japanese speakers \
            tend to speak at rates of over 200 wpm, meaning that most of the videos \
            on CIJ have been adapted to be a lot slower than that!")

# wpm vs sps chart

@st.cache_data
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
    ).configure(
        background='white'
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

st.markdown("We can also measure the rate of speech in syllables per second (SPS) \
            and compare it to words per minute.")

st.markdown("(Also, FYI, most of these **graphs are \
            interactive** so please click around.)")

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

@st.cache_data
def get_sentence_length_hist(show_medians=False):

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [7.60, 10.45, 16.17, 19.39],
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
            'mean_sentence_length:Q',
            bin=alt.Bin(maxbins=30),
            title='Average sentence length',
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
            alt.Tooltip('mean_sentence_length:Q', title='Average sentence length:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='Average number of words per sentence (sentence length)',
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
            alt.Tooltip('x:N', title='Median average sentence length:'),
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
        text=alt.Text('x:Q', format='.2f'),  # Display the x value, formatted as an integer
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    if show_medians:

        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')

    else:

        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='sentence_length'):

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

@st.cache_data
def get_repetition_hist(show_medians=False):

    video_df['average_rel_reps_perc'] = 100.0 * video_df['average_rel_reps']

    #if show_medians:
    #    sub_video_df = video_df[video_df['average_rel_reps_perc'] <= 2.0]
    #else:
    #    sub_video_df = video_df
    # take the sub data frame for easier viewing
    sub_video_df = video_df[video_df['average_rel_reps_perc'] <= 2.0]

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [0.99, 0.62, 0.37, 0.23],
        'level': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
        'text': ['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced']
    })

    selection = alt.selection_point(fields=['level'], bind='legend', on='click')

    highlight = alt.selection_point(name="highlight", fields=['level'], on='mouseover', empty=False)

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
            title='Average relative repetitions (%)',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20,
                #format='.1f%'
            ),
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
            alt.Tooltip('average_rel_reps:Q', title='Average relative repetitions:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='Relative repetitions of words',
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
        alt.X(
            'x:Q'
        ),
        tooltip=[
            alt.Tooltip('x:N', title='Median average relative repetitions:'),
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
        strokeWidth=alt.condition(highlight, alt.value(20), alt.value(1)),
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
        alt.X(
            'x:Q'
        ),
        y=alt.value(0),  # Positioning y at the top of the chart, can be adjusted as needed
        text=alt.Text('x:Q', format='.2f'),  # Display the x value, formatted as an integer
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    if show_medians:

        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')

    else:

        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='repetition'):

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

# word coverage chart

@st.cache_data
def get_word_coverage_chart(zoom=False):

    if zoom:
        word_coverage_df_sub = word_coverage_df.loc[word_coverage_df['coverage_perc']>=90]
    else:
        word_coverage_df_sub = word_coverage_df

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
    ).encode(
        x=alt.X(
            'rank:Q',
            scale=alt.Scale(domain=[1000,16000]) if zoom else alt.Scale(domain=[-10,16000]),
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
            scale=alt.Scale(domain=[90,101]) if zoom else alt.Scale(domain=[0,105]),
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

    layered_chart = alt.layer(line_chart, vertical_lines, text_labels, background='white')

    return layered_chart

if st.checkbox('Zoom in'):

    word_coverage_chart = get_word_coverage_chart(zoom=True)

else:

    word_coverage_chart = get_word_coverage_chart(zoom=False)

st.altair_chart(word_coverage_chart, use_container_width=True)

st.markdown("Using the same method of calculating word coverage as before, \
            we can also calculate how many of the top words you need to know \
            to achieve 98% word coverage in each video.")

@st.cache_data
def get_ne_spot_hist(show_medians=False):

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [3859, 5229, 6698, 7925],
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
            'ne_spot:Q',
            bin=alt.Bin(maxbins=30),
            title='Number of most common CIJ words known',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=20,
                #format='.1f%'
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
            scale=alt.Scale(domain=[0,40])
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
            alt.Tooltip('ne_spot:Q', title='Vocab size needed for 98% cov:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='Vocab size needed for 98% coverage',
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
            alt.Tooltip('x:N', title='Median vocab size needed for 98% cov:'),
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

    
    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='ne_spot'):

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

@st.cache_data
def get_tfplr_hist(show_medians=False):

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [3.82, 4.30, 4.76, 5.21],
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
            'tfp_log_ranks_unique:Q',
            bin=alt.Bin(maxbins=30),
            title='Log ranks',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=30,
                #format='.1f%'
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
            scale=alt.Scale(domain=[0,80])
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
            alt.Tooltip('tfp_log_ranks_unique:Q', title='25th percentile word-frequency log rank:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='25th percentile word-frequency log ranks',
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
            alt.Tooltip('x:N', title='Median 25th percentile word-frequency log rank:'),
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
        text=alt.Text('x:Q', format='.2f'),  # Display the x value, formatted as an integer
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    #layered_chart = alt.layer(histogram, background='white')
    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='tfplr'):

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

# grammar table

###
# GRAMMAR
###
st.markdown("## Grammar")

st.markdown("Easier videos tend to use less [subordinating conjunctions](https://universaldependencies.org/u/pos/SCONJ.html) than harder videos.")

@st.cache_data
def get_sconj_hist(show_medians=False):

    video_df['sconj_props_perc'] = 100.0 * video_df['sconj_props']

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [2.64, 4.73, 6.63, 7.67],
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
            'sconj_props_perc:Q',
            bin=alt.Bin(maxbins=30),
            title='Percentage of words',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=30,
                #format='.1f%'
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
            scale=alt.Scale(domain=[0,50])
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
            alt.Tooltip('sconj_props_perc:Q', title='Percentage of subordinating conjunctions:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='Percentages of subordinating conjunctions',
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
            alt.Tooltip('x:N', title='Median percentage of subordinating conjunctions:'),
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
        text=alt.Text('x:Q', format='.2f'),  # Display the x value, formatted as an integer
        color=alt.Color(
            'level:N',
            scale=alt.Scale(range=['red', 'green', 'blue', 'orange']),
            sort=['Complete Beginner', 'Beginner', 'Intermediate', 'Advanced'],
            legend=None
        ),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.1)),  # Link opacity with selection
    )

    
    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='sconj'):

    sconj_hist = get_sconj_hist(show_medians=True)

else:
    
    sconj_hist = get_sconj_hist(show_medians=False)

st.altair_chart(sconj_hist, use_container_width=True)

st.markdown("We also notice differences in the use of other types of words.")

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
        # This is where we target the top-left index column reader
        '': [
            {'selector': '.index_name', 'props': [('color', 'green'), ('font-weight', 'bold')]}
        ]
}).set_properties(**{'background-color': 'white'}).format("{:.2%}")

# Inject CSS to ensure the background is white in the markdown section
st.markdown(
    """
    <style>
    .dataframe-divv {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the styled DataFrame
st.markdown(
    '<div class="dataframe-divv">' + styled_df.to_html() + "</div>"
    , unsafe_allow_html=True)

###
# WORD ORIGIN
###
st.markdown("## What type of word")

st.markdown("There are three main categories of words in Japanese:")
st.markdown("(1) Wago (和語), (2) Kango (漢語) and (3) Gairaigo (外来語)")
st.markdown("Wago are native Japanese words, Kango are Chinese words and Gairaigo are foreign words.")

st.markdown("Harder videos tend to use more Kango than easier videos")

@st.cache_data
def get_kango_hist(show_medians=False):

    video_df['kan_props_perc'] = 100.0 * video_df['kan_props']

    # Data for vertical lines corresponding to each level
    line_data = pd.DataFrame({
        'x': [7.00, 9.55, 11.66, 13.03],
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
            'kan_props_perc:Q',
            bin=alt.Bin(maxbins=30),
            title='Percentage of words',
            axis=alt.Axis(
                labelFontSize=14, 
                titleFontSize=18,
                #titleFont='Urbanist',
                titleColor='black',
                titleFontWeight='normal',
                #titleFontStyle='italic',
                titlePadding=30,
                #format='.1f%'
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
            scale=alt.Scale(domain=[0,40])
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
            alt.Tooltip('kan_props_perc:Q', title='Percentage of kango:', bin=True),  # Properly indicate that `wpm` is binned
            alt.Tooltip('level:N', title='Level:'),
            alt.Tooltip('count()', title='Video count:')
        ],
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.1)),
        strokeWidth=alt.condition(highlight, alt.value(2), alt.value(1))
    ).properties(
        #width=750,
        width='container',
        #height='container',
        height=500,
        #background='beige',
        #padding=50,
        title=alt.TitleParams(
            text='Percentages of kango (漢語)',
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
            alt.Tooltip('x:N', title='Median percentage of kango:'),
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

    if show_medians:
        layered_chart = alt.layer(histogram, vertical_lines, text_labels, background='white')
    else:
        layered_chart = alt.layer(histogram, background='white')

    return layered_chart

if st.checkbox('Show medians', key='kango'):

    kango_hist = get_kango_hist(show_medians=True)

else:
    
    kango_hist = get_kango_hist(show_medians=False)

st.altair_chart(kango_hist, use_container_width=True)

st.markdown("In Japanese, Kango are somewhat analogous to French words in English. \
            These words tend to be more technical or sophisticated than other words.")

st.markdown("We also notice orderings when counting the percentage of Wago and Gairaigo as well.")

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
}).set_properties(**{'background-color': 'white'}).format("{:.2%}")

# Display the styled DataFrame
st.markdown(
    '<div class="dataframe-divv">' + styled_df.to_html() + "</div>"
    , unsafe_allow_html=True)

# heatmap

st.markdown("## Which factors matter the most?")

st.markdown("We've just found a number of statistics that lead to orderings in the data \
            but which statistics matter the most?")

st.markdown("To answer this, we can look at a correlation heatmap between each of the variables \
            and observe which statistics correlate the most strongly with the video's level.")

@st.cache_data
def render_vanilla_heatmap():

    # Compute the correlation matrix
    corr_matrix = num_video_df.corr()

    # Specify the variable of interest (e.g., 'target_variable')
    variable_of_interest = 'Level'

    # Sort the variables based on correlation with the variable of interest
    sorted_vars = corr_matrix[variable_of_interest].sort_values(ascending=False).index

    # Reorder the correlation matrix
    sorted_corr_matrix = corr_matrix.loc[sorted_vars, sorted_vars]

    # Create a heatmap using seaborn with the sorted correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(sorted_corr_matrix, annot=True, cmap='coolwarm', fmt=".3f")

    # Display the heatmap
    #plt.show()
    st.pyplot(plt.gcf())

render_vanilla_heatmap()

st.markdown("In case you're not familiar with stuff like this, numbers close to 1 or -1 \
            represent a high level or correlation and numbers close to 0 represent a low level of correlation. \
            Positive numbers represent a positive relationship between the variables and negative numbers represent a \
            reverse relationship between the variables.")

st.markdown("Using a statistics rule of thumb and removing all variables that have correlations \
            weaker than 0.3 (and more than -0.3), we can identify the variables with the strongest correlations.")


@st.cache_data
def render_level_row_unordered():

    # Compute the correlation matrix
    corr_matrix = num_video_df.drop(['Proportion of determiners', 'Proportion of nouns', 'Proportion of wago', 'Proportion of gairaigo'], axis=1).corr()

    # Specify the variable of interest (e.g., 'Level')
    variable_of_interest = 'Level'

    # Sort the variables based on correlation with the variable of interest
    sorted_vars = corr_matrix[variable_of_interest].sort_values(ascending=False).index

    # Remove 'Level' from the sorted variables to exclude the self-correlation
    sorted_vars = sorted_vars.drop(variable_of_interest)

    # Reorder the correlation matrix and exclude 'Level' column from the first row
    first_row_matrix = corr_matrix.loc[[variable_of_interest], sorted_vars]

    # Create a heatmap using seaborn with the single row of the correlation matrix
    plt.figure(figsize=(10, 1))  # Adjust the figure size to make it more appropriate for a single row
    sns.heatmap(first_row_matrix, annot=True, cmap='coolwarm', fmt=".3f", cbar_kws={'label': 'Correlation'})

    # Display the heatmap
    #plt.show()
    st.pyplot(plt.gcf())

@st.cache_data
def render_level_col_ordered():

    # Compute the correlation matrix
    corr_matrix = num_video_df.drop(['Proportion of determiners', 'Proportion of nouns', 'Proportion of wago', 'Proportion of gairaigo'], axis=1).corr()

    # Specify the variable of interest (e.g., 'Level')
    variable_of_interest = 'Level'

    # Get the correlations of the variable of interest
    correlations = corr_matrix[variable_of_interest]

    # Sort the variables based on the absolute value of the correlation with the variable of interest
    sorted_vars = correlations.abs().sort_values(ascending=False).index

    # Remove 'Level' from the sorted variables (to exclude the self-correlation)
    sorted_vars = sorted_vars.drop(variable_of_interest)

    # Reorder the correlation matrix, excluding the self-correlation
    sorted_corr_matrix = corr_matrix.loc[[variable_of_interest], sorted_vars]

    # Transpose the matrix to make it vertical
    transposed_corr_matrix = sorted_corr_matrix.T

    # Create a heatmap using seaborn with the transposed correlation matrix
    plt.figure(figsize=(2, 3))  # Adjust the figure size to make it more appropriate for a vertical layout
    sns.heatmap(transposed_corr_matrix, annot=True, cmap='coolwarm', fmt=".3f", cbar_kws={'label': 'Correlation'})

    # Display the heatmap
    #plt.show()
    st.pyplot(plt.gcf())

if st.checkbox('Flip and sort'):
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
st.markdown("7. Amount of adverbs")
st.markdown("8. Amount of Chinese words")

st.markdown("### Thanks for reading ✌️")

st.markdown("---")

#st.markdown("In the unlikely chance that you happen to be a CI instructor or a CI content creator, I want to talk to you! \
#            I can be reached at hamiltonjoshuadavid@gmail.com and I'm interested in learning \
#            more about what you do. Please also add a link to your work if you decide to reach out.")

#st.markdown("Special thanks to [CIJ](https://cijapanese.com/). I'm a happy subscriber and I recommend you also pick up a \
#             a membership if you're a Japanese learner!")

#st.markdown("---")
#st.markdown("**Some extra notes:**")
#st.markdown("1. No statistical tests of significance were conducted. This was just meant to be a light and unrigorous EDA.")
#st.markdown("2. It should be noted that the levels of the videos were determined by experts, and not by learners. They do not reflect objective difficulty.")
#st.markdown("3. While I stated that Japanese learners tend to speak at rates of over 200 wpm, I unfortunately haven't been able to find any good sources on this. \
#            The actual average Japanese WPM is likely even higher than 200 wpm, but unfortunately I haven't found any good research on this.")
#st.markdown("4. Technically, I didn't actually compute syllables per second, but rather moras per second which served as an approximation for syllables. \
#            I understand that this is linguistically incorrect, but I didn't want to confuse the reader who might not know any Japanese or linguistics.")
#st.markdown("5. More data cleaning could've been done to create better frequency lists, however, this was unnecessary in order to establish statistical patterns in a one-off analysis.")
#st.markdown("6. As a disclaimer, I do not think that CI instructors should base how they create their content off of the findings in this analysis. \
#            They should only use these findings for inspiration and to get them thinking more analytically about what they're doing.")