from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, column, layout
from bokeh.plotting import figure
from bokeh.models import (Button, ColumnDataSource, Div, CustomJS, DataTable,
                          RangeTool, HoverTool, TableColumn, Slider)
from bokeh.models.widgets import Select, PreText, RadioButtonGroup, Toggle, CheckboxButtonGroup
from bokeh.io import curdoc
from glob import glob
from ast import literal_eval
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
# from bokeh_wordcloud2 import WordCloud2
from bokeh.palettes import Category20

# Notes:
# Color Scheme: darkblue: #234f87
#               black   : #000010
#               lightblue: #add8ed
#               grey     : #42494a
#               white    : #e9edef


# Import Data
# Distributed ledger set
df_dl = pd.read_csv(glob(join(dirname(__file__), 'data', 'DL_bokeh*'))[0])
dl_sa = pd.read_csv(glob(join(dirname(__file__), 'data', 'DL_SA*'))[0])
dl_sa['datetime'] = pd.to_datetime(dl_sa['datetime'])
# AI set
df_ai = pd.read_csv(glob(join(dirname(__file__), 'data', 'AI_bokeh*'))[0])
ai_sa = pd.read_csv(glob(join(dirname(__file__), 'data', 'AI_SA*'))[0])
ai_sa['datetime'] = pd.to_datetime(ai_sa['datetime'])
# London filter df
ldn = pd.read_csv(glob(join(dirname(__file__), 'data', 'london_company_cleaned_filtered.csv'))[0],
                  usecols=['london_company', 'our_company'])
ldn.drop_duplicates(subset='our_company', inplace=True)


# Choice of AI or DL
data_choice = RadioButtonGroup(labels=["Artificial Intelligence", "Distributed Ledger"], active=0)


# Process Data
def process(df):
    '''
    Process the necessary data within the time frame

    :param df: Use filtered df from select_time()
    :param year: Year period
    :param month: Month period
    :return: a filtered df (final index)
    '''

    df1 = df.copy()

    # From the selected data, sum the frequency count
    df1['total_count'] = df1.groupby(['company_name'])['frequncy_count'].transform('sum')

    # Drop the duplicate companies and keep the top 100
    df1.drop_duplicates(subset=['company_name'], inplace=True)
    df1 = df1.sort_values(['total_count'], ascending=False)

    # 100 Companies
    # Num_of_companies = 100
    # df1 = df1[:Num_of_companies]

    # Restart the index from 1
    df1 = df1.reset_index(drop=True)
    df1.index += 1

    # Pick the used columns and rename them
    df1 = df1[['company_name', 'total_count']]
    df1 = df1.reset_index()
    df1.columns = ['Global Rank', 'Company', 'Frequency Count']
    df1 = pd.merge(df1, ldn, how='left', left_on='Company', right_on='our_company')

    return df1


# Select Data
def select_time(df, year, month):
    '''
    Select the necessary time frame

    :param year: year from choices of 'All',2019 and 2018 as int
    :param month: month from choices of 'All', [1,2,3...] as int
    :return: df from filtered time frame
    '''
    if year == 'All' and month == 'All':
        df1 = df.copy()

        return process(df1)

    elif month == 'All':
        df1 = df.copy()
        year = int(year)
        df1 = df1[df1['year'] == year]

        return process(df1)

    elif year == 'All':
        df1 = df.copy()
        month = month_converter(month)
        df1 = df1[df1['month'] == month]

        return process(df1)

    else:
        df1 = df.copy()
        year = int(year)
        month = month_converter(month)
        df1 = df1[df1['year'] == year]
        df1 = df1[df1['month'] == month]

        return process(df1)


# Month conversion function
def month_converter(month):
    '''
    Converts months from string to int
    :param month: string month
    :return: int of month
    '''

    conversion = {'January': 1,
                  'February': 2,
                  'March': 3,
                  'April': 4,
                  'May': 5,
                  'June': 6,
                  'July': 7,
                  'August': 8,
                  'September': 9,
                  'October': 10,
                  'November': 11,
                  'December': 12}

    value = conversion[month]

    return value


# Clean Data (SA cities)
def clean_data(df):
    '''
    Cleans the Sentiment Analysis Dataset to account for city filtering
    :param df: sentiment analysis df
    :return: clean df
    '''

    cdf = df.copy()

    # Alternative method that avoids errors
    # Convert the string(list) into a list, skip nan
    # for i in range(len(cdf)):
    #     try:
    #         cdf['cities'][i] = literal_eval(cdf['cities'][i])
    #     except:
    #         pass

    # Tips for searching and fixing names
    # cidf[cidf['city_split'].str.contains("Japan")==True]

    # Drop na
    cdf.dropna(inplace=True)
    cdf = cdf[cdf.cities != '[]']

    # Split to list
    cdf['city'] = cdf['cities'].apply(lambda x: literal_eval(x))

    cdf = cdf.explode('city')

    # save space
    cdf.drop(columns=['cities'], inplace=True)

    # # Split the dataset
    cdf['city_split'] = cdf['city'].str.split(':', n=1, expand=True)[0]
    cdf['growth_split'] = cdf['city'].str.split(':', n=1, expand=True)[1]

    # City name corrections

    # Fill missing nan
    cdf.loc[cdf["city"] == "New York 8985%", ["city_split"]] = "New York"
    cdf.loc[cdf["city"] == "New York 8985%", ["growth_split"]] = "8985%"

    # Rename City
    cdf.loc[cdf["city_split"] == "Tokio", ["city_split"]] = "Tokyo"
    cdf.loc[cdf["city_split"] == "Hong Kong S", ["city_split"]] = "Hong Kong"
    cdf.loc[cdf["city_split"] == "Hong", ["city_split"]] = "Hong Kong"
    cdf.loc[cdf["city_split"] == "Hong Kong Singapore", ["city_split"]] = "Singapore"
    cdf.loc[cdf["city_split"] == "Israel", ["city_split"]] = "Tel Aviv Israel"
    cdf.loc[cdf["city_split"] == "Japans", ["city_split"]] = "Japan"
    cdf.loc[cdf["city_split"] == "East London", ["city_split"]] = "London"

    cdf.loc[cdf["city_split"] == "Us States", ["city_split"]] = "United States"
    cdf.loc[cdf["city_split"] == "Palo Alto United States", ["city_split"]] = "Palo Alto"
    cdf.loc[cdf["city_split"] == "Nj United States", ["city_split"]] = "New Jersey"
    cdf.loc[cdf["city_split"] == "San Francisco S", ["city_split"]] = "San Francisco"
    cdf.loc[cdf["city_split"] == "Santa Clara 2017", ["city_split"]] = "Santa Clara"

    # Note: country changed to capital city
    cdf.loc[cdf["city_split"] == "South Korea S", ["city_split"]] = "Seoul"
    cdf.loc[cdf["city_split"] == "South Korea", ["city_split"]] = "Seoul"
    cdf.loc[cdf["city_split"] == "North Korea S", ["city_split"]] = "Pyongyang"
    cdf.loc[cdf["city_split"] == "North Korea", ["city_split"]] = "Pyongyang"

    return cdf


# Filter SA by cities
def filter_data(dataframe, city):
    '''
    Filter the already clean data by a selection of cities
    :param dataframe: cdf from clean_data() process
    :param city: city choice as a string
    :return: filtered df
    '''

    df = dataframe.copy()
    df = df[df['city_split'] == city]

    return df


# Data Choice function
def ai_or_dl(df_dl, df_ai, dl_sa, ai_sa):
    '''
    Select the dataframe sources based on the initial data choice
    :param df_dl:
    :param df_ai:
    :param dl_sa:
    :param ai_sa:
    :return: sadf,df
    '''
    # Choose AI
    if data_choice.active == 0:
        sadf = ai_sa.copy()
        df = df_ai.copy()

    # Choose DL
    else:
        sadf = dl_sa.copy()
        df = df_dl.copy()

    return sadf, df


# Initialise initial dataset
sadf, df = ai_or_dl(df_dl, df_ai, dl_sa, ai_sa)

##############
# Table Plot #
##############

# Add empty data source
table_source = ColumnDataSource(data=dict())

# Add controls
years = Select(title="Years:", value='2019', options=['All', '2019', '2018', '2017'])
months = Select(title="Months:", value='January', options=['All', 'January', 'February', 'March', 'April',
                                                           'May', 'June', 'July', 'August', 'September',
                                                           'October', 'November', 'December'])

london_filter = CheckboxButtonGroup(labels=['London Filter'], button_type='primary')

# Add Table Title
table_title = Div(text=data_choice.labels[data_choice.active] + ' Index for ' + months.value +
                       ' ' + years.value,
                  style={'color': '#234f87',
                         'font-size': '26pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width'
                  )


###########################
# Sentiment Analysis Plot #
###########################

# Add data source
sa_source = ColumnDataSource(data=dict(
    x=sadf['datetime'],
    neg=sadf['SA_neg'],
    neu=sadf['SA_neu'],
    pos=sadf['SA_pos'],
    city=sadf['cities'],
    week=sadf['wc']
))

# Add the start and end points
se = pd.DataFrame({'date': ['2012-12-30', '2019-06-30']})
se['date'] = pd.to_datetime(se['date'])
start, end = se.date[0], se.date[1]

# Plot figure
p = figure(plot_width=800, plot_height=350, tools='xpan,box_zoom,tap,reset,save',
           x_axis_type="datetime", x_axis_location="below",
           x_range=(start, end),
           y_range=(0, 100))

p.yaxis.axis_label = 'Percentage of Weekly Sentiment'

p.varea_stack(['neg', 'neu', 'pos'], x='x', color=("#234f87", "#e9edef", '#add8ed'),
              source=sa_source, legend_label=['Negative', 'Neutral', 'Positive'])
p.line('x', 'neg', source=sa_source)


# Adding a plot below to select date portions
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=140, plot_width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#f0f7fa")
range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "#daeef7"
range_tool.overlay.fill_alpha = 0.5

select.line('x', 'pos', source=sa_source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

# add hover tool
select.add_tools(HoverTool(tooltips=[('Date:', "@week"),
                                     ('Positive', '@pos{0.0 a}%'),
                                     ('Neutral', '@neu{0.0 a}%'),
                                     ('Negative', '@neg{0.0 a}%'),
                                     ('Cities', '@city')],
                           show_arrow=True, point_policy='follow_mouse'))

# Hide ticks and add legend
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.ygrid.grid_line_color = None
p.background_fill_color = "#e9edef"
p.legend.location = "top_right"
p.legend.items.reverse()
p.legend.background_fill_alpha = 0.5
p.legend.click_policy = "hide"

# Add plot title
sa_title = Div(text='Percentage of Weekly Sentiment and Cities Mentioned',
                  style={'color': '#42494a',
                         'font-size': '18pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width')


###############################
# Sentiment Analysis Plot 2.1 #
###############################

# Initiate cleaning
cdf = clean_data(sadf)

# Initiate first filter
cdf1 = filter_data(cdf, 'Seoul')

# Add data source
sacity1_source = ColumnDataSource(data=dict(
    x=cdf1['datetime'],
    neg=cdf1['SA_neg'],
    neu=cdf1['SA_neu'],
    pos=cdf1['SA_pos'],
    line=cdf1['SA_tot']*0.5,
    city=cdf1['city_split'],
    rate=cdf1['growth_split'],
    week=cdf1['wc']
))


# Plot figure
p1 = figure(plot_width=800, plot_height=250, tools='xpan,box_zoom,tap,reset,save',
           x_axis_type="datetime", x_axis_location="below",
           x_range=(min(cdf1['datetime']), max(cdf1['datetime'])),
           y_range=(0, 100))

p1.yaxis.axis_label = 'Percentage of Weekly Sentiment'

p1.varea_stack(['neg', 'neu', 'pos'], x='x', color=("#234f87", "#e9edef", '#add8ed'),
               source=sacity1_source, legend_label=['Negative', 'Neutral', 'Positive'])

p1.line('x', 'neg', source=sacity1_source)
p1.line('x', 'line', source=sacity1_source, line_width=4, alpha=0.25, line_color='black')
p1.circle('x', 'line', source=sacity1_source, alpha=1, color='#e9edef', size=3)


# add hover tool
p1.add_tools(HoverTool(tooltips=[('Date:', "@week"),
                                 ('Positive', '@pos{0.0 a}%'),
                                 ('Neutral', '@neu{0.0 a}%'),
                                 ('Negative', '@neg{0.0 a}%'),
                                 ('City', '@city'),
                                 ('Weekly growth', '@rate')],
                       show_arrow=True, point_policy='follow_mouse'))

# Hide ticks and add legend
p1.xaxis.minor_tick_line_color = None
p1.yaxis.minor_tick_line_color = None
p1.ygrid.grid_line_color = None
p1.background_fill_color = "#e9edef"
p1.legend.location = "top_right"
p1.legend.items.reverse()
p1.legend.background_fill_alpha = 0.5
p1.legend.click_policy = "hide"


# Add the selection widget
city_list = sorted(list(cdf.city_split.unique()))
cities = Select(title="City:", value='Seoul', options=city_list)


###############################
# Sentiment Analysis Plot 2.2 #
###############################

# Initiate first filter
cdf2 = filter_data(cdf, 'New York')

# Add data source
sacity2_source = ColumnDataSource(data=dict(
    x=cdf2['datetime'],
    neg=cdf2['SA_neg'],
    neu=cdf2['SA_neu'],
    pos=cdf2['SA_pos'],
    line=cdf2['SA_tot']*0.5,
    city=cdf2['city_split'],
    rate=cdf2['growth_split'],
    week=cdf2['wc']
))


# Plot figure
p2 = figure(plot_width=800, plot_height=250, tools='xpan,box_zoom,tap,reset,save',
           x_axis_type="datetime", x_axis_location="below",
           x_range=(min(cdf2['datetime']), max(cdf2['datetime'])),
           y_range=(0, 100))

p2.yaxis.axis_label = 'Percentage of Weekly Sentiment'

p2.varea_stack(['neg', 'neu', 'pos'], x='x', color=("#234f87", "#e9edef", '#add8ed'),
               source=sacity2_source, legend_label=['Negative', 'Neutral', 'Positive'])

p2.line('x', 'neg', source=sacity2_source)
p2.line('x', 'line', source=sacity2_source, line_width=4, alpha=0.25, line_color='black')
p2.circle('x', 'line', source=sacity2_source, alpha=1, color='#e9edef', size=3)


# Add hover tool
p2.add_tools(HoverTool(tooltips=[('Date:', "@week"),
                                 ('Positive', '@pos{0.0 a}%'),
                                 ('Neutral', '@neu{0.0 a}%'),
                                 ('Negative', '@neg{0.0 a}%'),
                                 ('City', '@city'),
                                 ('Weekly growth', '@rate')],
                       show_arrow=True, point_policy='follow_mouse'))

# Hide ticks and add legend
p2.xaxis.minor_tick_line_color = None
p2.yaxis.minor_tick_line_color = None
p2.ygrid.grid_line_color = None
p2.background_fill_color = "#e9edef"
p2.legend.location = "top_right"
p2.legend.items.reverse()
p2.legend.background_fill_alpha = 0.5
p2.legend.click_policy = "hide"


# Add the selection widget
cities2 = Select(title="City 2:", value='New York', options=city_list)


############################
# Table Plot 2 (frequency) #
############################

# Add empty data source
table_df2 = pd.DataFrame(cdf['city_split'].value_counts()).reset_index()
table_df2.columns = ['city', 'freq']
table2_source = ColumnDataSource(data=dict(
    city=table_df2['city'],
    freq=table_df2['freq']
))

columns2 = [
    TableColumn(field="city", title="City"),
    TableColumn(field="freq", title="Number of Spikes in terms of mentions"),
]

table2 = DataTable(source=table2_source, columns=columns2, width=800,  sortable=True)


#############
# Text Uses #
#############
space = Div(text='   ', style={'color': '#42494a',
                               'font-size': '20pt',
                               'font-family': 'Source Sans Pro'}, sizing_mode='scale_width')
sacity_title = Div(text='Comparison of Sentiment Analysis by City' +
                        ' (' + data_choice.labels[data_choice.active] + ')',
                  style={'color': '#42494a',
                         'font-size': '18pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width'
                  )
city1_title = Div(text=cities.value,
                  style={'color': '#234f87',
                         'font-size': '15pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width',
                  )
city2_title = Div(text=cities2.value,
                  style={'color': '#234f87',
                         'font-size': '15pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width',
                  )
london_filter_txt = Div(text='  ',
                        style={'color': '#42494a',
                        'font-size': '11pt',
                        'font-family': 'Source Sans Pro'},
                        sizing_mode='scale_width',
                        )
bump_title = Div(text='Most discussed companies in the realm of ' + data_choice.labels[data_choice.active],
                  style={'color': '#42494a',
                         'font-size': '18pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width'
                  )
bump_description = Div(text='Each tweet we collect has a dominant topic. Some tweets also identify the companies that ' +
                            'share an association with the dominant topic. Here we rank the companies according to how ' +
                            'often a company appears in the selected topic. *Disclaimer:* This visualisation only ' +
                            'shows sequential topic model on 1000 tweet sample taken per year from either the general ' +
                            'topics Artificial Intelligence or Distributed Ledgers.',
                        style={'color': '#42494a',
                        'font-size': '12pt',
                        'font-family': 'Source Sans Pro'},
                        sizing_mode='scale_width',
                        )
pca_title = Div(text='Multi-Dimensional Topic Model on ' + data_choice.labels[data_choice.active],
                  style={'color': '#42494a',
                         'font-size': '18pt',
                         'font-family': 'Source Sans Pro'},
                  sizing_mode='scale_width'
                  )
pca_description = Div(text='The field of ' + data_choice.labels[data_choice.active] + ' contains many subjects. For each ' +
                            'of these subjects, we conduct topic modelling to observe the interation between areas within ' +
                            'the subjects. Principal Component Analysis is used to reduce the dimensions of this matrix '+
                            'such that we may observe a possible trend/pattern. Each colour represents a topic and each point '+
                            "represents a tweet. Hence, an orange point would mean that tweet's dominant topic is Topic 2. " +
                            'Click on the legend to hide certain topics.',
                        style={'color': '#42494a',
                        'font-size': '12pt',
                        'font-family': 'Source Sans Pro'},
                        sizing_mode='scale_width',
                        )


##############
# Bump Chart #
##############
df_b = pd.read_csv(glob(join(dirname(__file__), 'data', 'sequential','AI_topic_company_*'))[0])
pickle_in = open(glob(join(dirname(__file__), 'data', 'sequential','topic_model*'))[0], "rb")
topic_model = pickle.load(pickle_in)
company_list = ['JP Morgan', 'Etoro', 'Google', 'Visa', 'Goldman Sachs',
               'Unilever', 'Deloitte', 'Samsung', 'Wells Fargo', 'Allianz',
               'Apple', 'Commerzbank']
years_bp = [2013, 2014, 2015, 2016, 2017, 2018, 2019]


def rankme(df, topic_number, year):
    '''
    df = df of all years and all topics
    year in years as int

    Returns a dataframe that has the ranks of the companies respective to topic dominance
    '''

    if topic_number == 'All':
        df3 = df.copy()

    else:
        df3 = df.copy()
        topic_number = int(topic_number)
        df3 = df3[df3.topic_n == topic_number]

    df3 = df3.groupby(['year'])[company_list].sum()
    df3 = df3.T
    df3 = df3.reset_index()
    df3 = df3.melt(id_vars=['index'],
                   var_name="year",
                   value_name="freq")

    df3 = df3[df3['year'] == year]
    df3 = df3.sort_values(by=['freq'], ascending=False).reset_index(drop=True)

    # Add a rank level
    df3.index += 1
    df3.reset_index(inplace=True)

    # rename columns
    OLD_NAMES = ['level_0', 'index']
    NEW_NAMES = ['rank', 'company']
    COLS = dict(zip(OLD_NAMES, NEW_NAMES))

    df3.rename(columns=COLS, inplace=True)
    df3['year'] = df3['year'].apply(str)

    return df3


def bump_plot(DATA, TOPIC_NUM):
    df_b1 = pd.concat([rankme(df=DATA, topic_number=TOPIC_NUM, year=year) for year in years_bp],
                    ignore_index=True)

    source_bp = ColumnDataSource(df_b1)

    line_data = dict()
    for com in df_b1['company'].unique():
        line_data[com] = df_b1[df_b1['company'] == com]

    source_bp_line = ColumnDataSource(line_data)

    # cmap = LinearColorMapper(palette=Blues[256],
    #                          low = min(vis_df["rank"]),
    #                          high = max(vis_df["rank"]))

    # bump = figure(plot_width=800, plot_height=1000,
    #               x_range=df_b1.year.unique(), toolbar_location=None, tools="")
    #
    # bump.circle(x='year', y='rank', size = 15,source=source_bp)
    #
    # for com in df_b1['company'].unique():
    #     bump.line(x='year', y='rank', source=source_bp_line.data[com], line_width = 4, line_color = 'grey', line_alpha=0.5)
    #
    # #          fill_color={"field":"rank", "transform":cmap})
    #
    # # y_range=df3['rank'].unique(),
    #
    # # for x in vis_df['topic_n'].unique():
    # #     vis_df
    # #     src = ColumnDataSource(vis_df[vis_df[topic_n] == x])
    #
    #
    # bump.add_tools(HoverTool(tooltips=[('Company', '@company'),
    #                                 ("Rank", "@rank"),
    #                                 ("Frequency", '@freq')]))
    #
    # # Rename y axis tick
    # keys_ = [1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
    # values_ = list(df_b1[df_b1['year'] == '2013']['company'].unique())
    # bump.yaxis.ticker = keys_
    # bump.yaxis.major_label_overrides = dict(zip(keys_, values_))
    # bump.y_range.flipped = True

    keys_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    values_ = list(df_b1[df_b1['year'] == '2013']['company'].unique())

    return df_b1, source_bp, source_bp_line, keys_, values_


topic_choice = Select(title="Topic Number:", value='1', options=['All', '0', '1', '2', '3', '4', '5', '6', '7',
                                                                 '8', '9', '10', '11', '12', '13', '14', '15',
                                                                 '16', '17', '18', '19'])

df_b1, source_bp, source_bp_line, keys_, values_ = bump_plot(DATA=df_b, TOPIC_NUM=topic_choice.value)

bump = figure(plot_width=800, plot_height=1000,
              x_range=df_b1.year.unique(), toolbar_location=None, tools="")

bump.circle(x='year', y='rank', size=15, source=source_bp)

for com in df_b1['company'].unique():
    bump.line(x='year', y='rank', source=source_bp_line.data[com], line_width=4, line_color='grey', line_alpha=0.5)

bump.add_tools(HoverTool(tooltips=[('Company', '@company'),
                                   ("Rank", "@rank"),
                                   ("Frequency", '@freq')]))

# Rename y axis tick
keys_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
values_ = list(df_b1[df_b1['year'] == '2013']['company'].unique())
bump.yaxis.ticker = keys_
bump.yaxis.major_label_overrides = dict(zip(keys_, values_))
bump.y_range.flipped = True


############
# PCA Plot #
############

# Import main df

# vdf_ = vdf_.drop(columns=['Unnamed: 0'])


# def pca_data(df):
#
#     df1 = df.loc[:, '0':'19']
#     X = df1.to_numpy()
#
#     df2 = df.drop(columns=df1.columns)
#     df2 = df2[['topic_n', 'prob', 'date', 'year']]
#     scaler = StandardScaler() # instantiate
#     scaler.fit(X) # compute the mean and standard which will be used in the next command
#     X_scaled = scaler.transform(X)
#     # fit and transform can be applied together and I leave that for simple exercise
#     # we can check the minimum and maximum of the scaled features which we expect to be 0 and 1
#     # print ("after scaling minimum", X_scaled.min(axis=0))
#     pca = PCA(n_components=2)
#     pca.fit(X_scaled)
#     X_pca = pca.transform(X_scaled)
#     vdf = pd.DataFrame()
#     vdf['x'] = X_pca[:,0]
#     vdf['y'] = X_pca[:,1]
#     # vdf = vdf.reset_index()
#     # vdf = vdf.rename(columns={'index':'doc_id'})
#     vdf = pd.merge(vdf, df2, how='left', left_index=True, right_index=True)
#
#     return vdf

def pca_plot_data(vdf, year):
    # vdf = pca_data(pca_df)

    df3 = vdf[vdf['year'] == year]

    # Create Colormap
    values = Category20[20]
    keys = range(0,20)
    colormap = dict(zip(keys, values))

    df3.loc[:, 'colors'] = [colormap[x] for x in df3.loc[:, 'topic_n']]
    # source = ColumnDataSource(df3)

    return df3


def pca_ai_dl():
    # Choose AI
    if data_choice.active == 0:
        search_word_list = ['Deep Learning', '#ML', '#AI', '#NLP', 'Analytics', 'Artificial Intelligence',
                            'Data Mining', 'Machine Learning', 'Natural Language Processing', 'Neural Network',
                            'Pattern Recognition']
        folder = 'ai'

    else:
        search_word_list = ['distributed ledger', 'Etherium', 'smart contracts']
        folder = 'dl'

    return search_word_list, folder


search_word_list, folder = pca_ai_dl()
search_word = Select(title="Subject:", value='#ML', options=sorted(search_word_list))
# search_word_ = 'vis_ready_' + search_word.value + '*'
vdf_ = pd.read_csv(glob(join(dirname(__file__), 'data', folder, 'vis_ready_' + search_word.value + '*'))[0])

# Create year sliders for PCA
pca_years = list(vdf_['year'].unique())
pca_slider = Slider(start=min(pca_years), end=max(pca_years), value=min(pca_years), step=1, title="Year")

df3 = pca_plot_data(vdf=vdf_, year=pca_slider.value)
# create a new plot with a range set with a tuple
p3 = figure(plot_width=800, plot_height=800, title = '20 topics for ' + search_word.value,
            x_axis_label='PCA 1', y_axis_label='PCA 2')

for x in range(20):
    globals()['pca_source_%s' % x] = ColumnDataSource(df3[df3['topic_n'] == x])
    p3.circle('x', 'y', size=5.5, source = globals()['pca_source_%s' % x], color='colors', alpha =0.8,
              legend_label='Topic ' + str(x))

p3.grid.grid_line_color = None
p3.axis.axis_line_color = None
p3.axis.major_tick_line_color = None
p3.yaxis.minor_tick_line_color = None
p3.xaxis.minor_tick_line_color = None
p3.axis.major_label_standoff = 0
p3.title.text_font_size = '12pt'
p3.title.align = 'center'
p3.legend.click_policy = 'hide'




# p3 = pca_plot(vdf=vdf_, search_word= search_word.value)
# p.legend.orientation = "horizontal"
# p.legend.location ="top_center"

##############
# WORD CLOUD #
##############

'''
Creates and saves a word cloud
'''

# /Users/averysoh/Google Drive (racass1234@gmail.com)/index_viz_clean/static/Deep Learning/blck_Deep Learning_Topic_0.png
# choose
img_path = 'index_viz_clean/static/Natural Language Processing_Topic_0.png'
# p.image_url(url=[img_path],x=x_range[0],y=y_range[1],w=x_range[1]-x_range[0],h=y_range[1]-y_range[0])
div_image = Div(text="""<img src="index_viz_clean/static/Deep Learning/blck_Deep Learning_Topic_0.png" alt="div_image">""",
                width=20, height=12)

# def topic_content_data(topic_content):
#     temp_list = []
#     for x in list(topic_content['topic_n'].unique()):
#         temp = pd.DataFrame(topic_content['content'][x].split('+'))
#         temp = temp[0].str.split('*', expand=True)
#         temp = temp.rename(columns={0: 'prob', 1: 'words'})
#         temp['words'] = temp['words'].str.strip('" ')
#         temp['topic_n'] = x
#         temp = temp[['topic_n', 'prob', 'words']]
#
#         temp_list.append(temp)
#
#     tdf = pd.concat(temp_list)
#     return tdf
#
#
# filename = 'topic_content_Neural Network*'
# topic_content = pd.read_csv(glob(join(dirname(__file__), 'data', folder, filename))[0])
# topic_content = topic_content.drop(columns=['Unnamed: 0'])
#
# topic_df = topic_content_data(topic_content)
# topic_num = 0
# wd = topic_df[topic_df['topic_n'] == topic_num]
#
# src_wc = ColumnDataSource(wd)
# # we will specify just "blue" for the color
# wordcloud = WordCloud2(source=src_wc, wordCol="words",sizeCol="prob")


def update():
    # Change Dataset Initial
    sadf, df = ai_or_dl(df_dl, df_ai, dl_sa, ai_sa)
    cdf = clean_data(sadf)

    year = years.value
    month = months.value
    data_title = data_choice.labels[data_choice.active]

    # Update first table
    table_df = select_time(df, year, month)
    if london_filter.active:
        table_df = table_df[table_df['london_company'].notnull()]
        london_filter_txt.text = 'Showing only companies registered in London'
    else:
        table_df = table_df
        london_filter_txt.text = ' '

    table_source.data = dict(
        rank   =table_df['Global Rank'],
        company=table_df['Company'],
        freq   =table_df['Frequency Count'],
        london =table_df['london_company']
    )

    table_title.text = data_title + ' Index for ' + month + ' ' + year
    sacity_title.text = 'Comparison of Sentiment Analysis by City' + ' (' + data_choice.labels[data_choice.active] + ')'
    bump_title.text = 'Most discussed companies in the realm of ' + data_choice.labels[data_choice.active]

    # Update SA plot for AI or DL
    sa_source.data = dict(
        x=sadf['datetime'],
        neg=sadf['SA_neg'],
        neu=sadf['SA_neu'],
        pos=sadf['SA_pos'],
        city=sadf['cities'],
        week=sadf['wc']
    )

    # Update sa city filter plot
    city = cities.value
    cdf1 = filter_data(cdf, city)
    sacity1_source.data = dict(
        x=cdf1['datetime'],
        neg=cdf1['SA_neg'],
        neu=cdf1['SA_neu'],
        pos=cdf1['SA_pos'],
        line=cdf1['SA_tot']*0.5,
        city=cdf1['city_split'],
        rate=cdf1['growth_split'],
        week=cdf1['wc']
    )
    p1.x_range.start = min(cdf1['datetime'])
    p1.x_range.end = max(cdf1['datetime'])

    city1_title.text = city

    # Update sa city 2 filter plot
    city2 = cities2.value
    cdf2 = filter_data(cdf, city2)
    sacity2_source.data = dict(
        x=cdf2['datetime'],
        neg=cdf2['SA_neg'],
        neu=cdf2['SA_neu'],
        pos=cdf2['SA_pos'],
        line=cdf2['SA_tot']*0.5,
        city=cdf2['city_split'],
        rate=cdf2['growth_split'],
        week=cdf2['wc']
    )
    p2.x_range.start = min(cdf2['datetime'])
    p2.x_range.end = max(cdf2['datetime'])

    city2_title.text = city2

    # Bump updates
    # df_b1_new, source_bp_new, source_bp_line_new, keys_new, values_new = bump_plot(DATA=df_b, TOPIC_NUM=topic_choice.value)
    # source_bp.data = source_bp_new.data
    #
    # for com in df_b1_new['company'].unique():
    #     source_bp_line.data[com] = source_bp_line_new.data[com]
    #
    # bump.yaxis.ticker = keys_new
    # bump.yaxis.major_label_overrides = dict(zip(keys_new, values_new))
    # bump.y_range.flipped = True

    # PCA updates
    search_word_list_new, folder_new = pca_ai_dl()
    search_word.options = search_word_list_new
    vdf_new = pd.read_csv(glob(join(dirname(__file__), 'data', folder_new, 'vis_ready_' + search_word.value + '*'))[0])
    df3_new = pca_plot_data(vdf=vdf_new, year=pca_slider.value)

    pca_years_new = list(vdf_new['year'].unique())
    pca_slider.start = min(pca_years_new)
    pca_slider.end = max(pca_years_new)

    for xx in range(20):
        df3_temp = df3_new[df3_new['topic_n'] == xx]
        globals()['pca_source_%s' % xx].data = dict(
            x=df3_temp['x'],
            y=df3_temp['y'],
            prob=df3_temp['prob'],
            topic_n=df3_temp['topic_n'],
            colors=df3_temp['colors']
        )

    p3.title.text = '20 topics for ' + search_word.value

    # p3_new = pca_plot(vdf=vdf_new, search_word=search_word.value)
    # layout_.children[12].children[0] = p3_new





columns = [
    TableColumn(field="rank", title="Global Rank"),
    TableColumn(field="company", title="Company"),
    TableColumn(field="freq", title="Frequency Count"),
    TableColumn(field="london", title="London Registered Company")
]

table = DataTable(source=table_source, columns=columns, width=800,  sortable=True)
years.on_change('value', lambda attr, old, new: update())
months.on_change('value', lambda attr, old, new: update())
data_choice.on_change('active', lambda attr, old, new: update())
cities.on_change('value', lambda attr, old, new: update())
cities2.on_change('value', lambda attr, old, new: update())
london_filter.on_change('active', lambda attr, old, new: update())
topic_choice.on_change('value', lambda attr, old, new: update())
search_word.on_change('value', lambda attr, old, new: update())
pca_slider.on_change('value', lambda attr, old, new: update())

update()


#############
# Structure #
#############

saplot = column(space, sa_title, p, select)
head = row(data_choice, sizing_mode='scale_width')
b1 = row(london_filter, london_filter_txt)
b = column(space, space, sacity_title, sizing_mode='scale_width')
mid = row(cities, cities2)
mid2 = column(city1_title, p1)
mid3 = column(city2_title, p2)
midmid = column(mid2, mid3)
bump_vis = column(space, space, bump_title, bump_description, topic_choice, bump)
pca_vis = column(space, space, pca_title, pca_description, row(search_word, pca_slider), p3)

layout_ = layout(children=[
    [head],
    [table_title],
    [months, years],
    [b1],
    [table],
    [saplot],
    [b],
    [mid],
    [midmid],
    [table2],
    [bump_vis],
    [pca_vis],
    [div_image]
], sizing_mode='scale_width')

# , sizing_mode='scale_width'

curdoc().add_root(layout_)
curdoc().title = "AI and DL Index"



# import pandas as pd
# from bokeh.models import ColumnDataSource
# from bokeh.io import curdoc
# from bokeh.plotting import figure
# from bokeh.models.widgets import Dropdown, MultiSelect, Slider, Tabs, Panel, RadioButtonGroup
# from bokeh.models import HoverTool, LabelSet
# from bokeh.layouts import layout