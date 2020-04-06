from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, column, layout
from bokeh.models import (Button, ColumnDataSource, CustomJS, DataTable,
                          NumberFormatter, RangeSlider, TableColumn)
from bokeh.models.widgets import Select
from bokeh.io import curdoc

# Import Data
df = pd.read_csv(join(dirname(__file__), 'salary_data.csv'))


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
    Num_of_companies = 100
    df1 = df1[:Num_of_companies]

    # Restart the index from 1
    df1 = df1.reset_index(drop=True)
    df1.index += 1

    # Pick the used columns and rename them
    df1 = df1[['company_name', 'total_count']]
    df1 = df1.reset_index()
    df1.columns = ['Rank', 'Company', 'Frequency Count']

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
        df1 = df1[df1['year'] == year]

        return process(df1)

    elif year == 'All':
        df1 = df.copy()
        df1 = df1[df1['month'] == month]

        return process(df1)

    else:
        df1 = df.copy()
        df1 = df1[df1['year'] == year]
        df1 = df1[df1['month'] == month]

        return process(df1)




# Add empty data source
table_source = ColumnDataSource(data=dict())

# Add controls
years = Select(title="Years:", value=2019, options=['All', 2019, 2018, 2017])
months = Select(title="Months:", value=1, options=['All', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

def update():
    year = years.value
    month = months.value

    table_df = select_time(df, year, month)
    table_source.data = dict(
        rank   =table_df['Rank'],
        company=table_df['Company'],
        freq   =table_df['Frequency Count']
    )


columns = [
    TableColumn(field="rank", title="Rank"),
    TableColumn(field="company", title="Company"),
    TableColumn(field="freq", title="Frequency Count")
]

table = DataTable(source=table_source, columns=columns, width=800,  sortable=True)

update()

layout = layout([
    [months, years],
    [table]
], sizing_mode='scale_width')

curdoc().add_root(layout)
curdoc().title = "AI and DL Index"

# import pandas as pd
# from bokeh.models import ColumnDataSource
# from bokeh.io import curdoc
# from bokeh.plotting import figure
# from bokeh.models.widgets import Dropdown, MultiSelect, Slider, Tabs, Panel, RadioButtonGroup
# from bokeh.models import HoverTool, LabelSet
# from bokeh.layouts import layout