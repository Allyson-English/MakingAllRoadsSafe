import pandas as pd
import numpy as np

import plotly as py
from plotly import __version__
import plotly.graph_objs as go
print(__version__)
import pandas as pd
from scipy.stats import ttest_ind, ttest_ind_from_stats
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=False)

full_dataset = pd.read_csv(r'/Users/allysonenglish/Desktop/workbench/working_data_7_days.csv', low_memory=False).drop(columns=['year', 'quarter', 'one_way', 'surface', 'road_type'])

full_dataset.head()

full_dataset.duplicated()

str(full_dataset.dtypes)

full_dataset.isnull()

full_dataset.shape

def commute_time(x):
    if 21 >= x >= 17:
        return "Evening Commute"
    elif 9 >= x >= 6:
        return "Morning Commute"
    else:
        return ''
        
commute = pd.Series([])

commute = full_dataset['hour_of_day'].apply(commute_time)

full_dataset.insert(0, "commute", commute)

full_dataset = full_dataset[full_dataset.commute != '']

# Both of these show the most frequent occurance in a column 

full_dataset.road_name.mode()[0] == full_dataset['road_name'].value_counts().idxmax()

# Identifying most popular roads during commuting hours 
# Value counts determines the number of times a road appears in a dataset
# Sort values sorts lowest to highest (unless ascending False is specified)
# [:5] indicates that only the top five most frequent roads should be returned

road_freq = full_dataset['road_name'].value_counts().sort_values(ascending=False)[:5]

# From this analysis, the top three most freuqent roads should be evaluated because these roads individually 
# Account for more than double the traffic of other roads in the dataset during commuting hours

road_freq

# Goal was to have a dataset that only included the most traveled roads
# Wasn't sure how to drop rows froma dataframe based on a value in a cell
# seperating full dataset into frames that had the roads I wanted and then concatinating these rows was an effective workaround 

full_dataset_L = full_dataset[full_dataset['road_name'] == 'Limuru Road']
full_dataset_K = full_dataset[full_dataset['road_name'] == 'Kangundo Road']
full_dataset_M = full_dataset[full_dataset['road_name'] == 'Magadi Road']

frames = [full_dataset_L, full_dataset_K, full_dataset_M]

data = pd.concat(frames)

data.head()



# Create visualization for all three roads, evening commute

vio = go.Figure()

vio.add_trace(go.Violin(x=data['road_name'] [data["commute"] == "Morning Commute"],
                        y=data['speed_kph_p85'] [data["commute"] == "Morning Commute"],
                        legendgroup='Free Flow', scalegroup='Free Flow', name='Free Flow',
#                         side='negative', 
                        line_color='#ffa566')
             )

vio.add_trace(go.Violin(x=data['road_name'] [data["commute"] == "Morning Commute"],
                        y=data['speed_kph_mean'] [data["commute"] == "Morning Commute"],
                        legendgroup='Recorded Speed', scalegroup='Recorded Speed', name='Recorded Speed',
#                         side='negative', 
                        line_color='#66bdff')
             )

vio.update_traces(box_visible=False, meanline_visible=True)
vio.update_layout(title='Free Flow vs. Recorded Speeds During Morning Commute on Busiest Roadways',
                  xaxis=dict(title='', zeroline=True), yaxis=dict(title='Speed (KPH)'),
                  violinmode='group', violingap=0, legend_title="Speeds")

vplots_morning = vio.write_html("/Users/allysonenglish/Desktop/forgithub.html")

plot(vio)


# Create visualization for all three roads, evening commute

vio = go.Figure()

vio.add_trace(go.Violin(x=data['road_name'] [data["commute"] == "Evening Commute"],
                        y=data['speed_kph_p85'] [data["commute"] == "Evening Commute"],
                        legendgroup='Free Flow', scalegroup='Free Flow', name='Free Flow',
#                         side='negative', 
                        line_color='#ffa566')
             )

vio.add_trace(go.Violin(x=data['road_name'] [data["commute"] == "Evening Commute"],
                        y=data['speed_kph_mean'] [data["commute"] == "Evening Commute"],
                        legendgroup='Recorded Speed', scalegroup='Recorded Speed', name='Recorded Speed',
#                         side='negative', 
                        line_color='#66bdff')
             )

vio.update_traces(box_visible=False, meanline_visible=True)
vio.update_layout(title='Free Flow vs. Recorded Speeds During Evening Commute on Busiest Roadways',
                  xaxis=dict(title='', zeroline=True), yaxis=dict(title='Speed (KPH)'),
                  violinmode='group', violingap=0, legend_title="Speeds")

vplots_evening = vio.write_html("/Users/allysonenglish/Desktop/forgithub.html")

plot(vio)

