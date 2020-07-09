import sqlalchemy

# Establish (lazy) connection to mysql
# Initialize pathway to MySQL db 

engine = sqlalchemy.create_engine(pathway, echo=True)

# Import CSV of Nairobi traffic data

filepath = ''

full_dataset = pd.read_csv(filepath, low_memory=False)

# Is this begin engine clause necessary to ensure the changes to the database are persistent? **

engine.begin()

full_dataset.to_sql(
    name = 'uber_data',
    con = engine,
    index = True,
    if_exists = 'append'
)

# Cross check most popular roads using SQL (ORDER BY COUNT) and pandas (.value_counts())

full_dataset['road_name'].value_counts()
popular_roads = '''
SELECT road_name FROM uber_data GROUP BY road_name ORDER BY COUNT(road_name) DESC LIMIT 5
'''

# Seems like there should be a more elegant way to transition from a dataframe into a list... *
pop_rds = pd.read_sql(popular_roads, engine)
pop_rds = pop_rds.values.tolist()
pop_rds = [item for sublist in pop_rds for item in sublist]

# Testing out queries by selecting morning commute hours and evening commute hours and manipulating respective dataframes

query = '''
SELECT road_name, speed_kph_p85, speed_kph_mean, hour_of_day FROM uber_data WHERE hour_of_day >= 17 AND hour_of_day <= 21
'''

evening_commute = pd.read_sql(query, engine)

evening_commute['speed_kph_p85'].mean()
evening_commute['speed_kph_mean'].mean()

query = '''
SELECT road_name, speed_kph_p85, speed_kph_mean, hour_of_day FROM uber_data WHERE hour_of_day >= 5 AND hour_of_day <= 10
'''
morning_commute['speed_kph_p85'].mean()
morning_commute['speed_kph_mean'].mean()

# Sort roads based on count (frequency in df) to determine which roads are most traveled, these will have the best data to make comparisons off of
# Since .count() is counting will generate the same number across variables (speed variables and hour or day), selecting hour of day to sort values by is arbitrary

morning_commute.groupby('road_name').count().sort_values(by=['hour_of_day'], ascending = False)
evening_commute.groupby('road_name').count().sort_values(by=['hour_of_day'], ascending = False)

# Challenge with this data is that the 'Free Flow Speed' is calculated as the 85th percentile of travel speeds
# This means that it will, in almost all cases, be higher than the recorded speed
# To circumvent this limitation, instead of doing a two-way t test for difference in means between FFS and traveling speed for the same hour, 
# it may make more sense to compare average traveling speed for each hour in the day on a given road to identify when, if ever, these speeds differ from one another significantly


def data_by_roadway(pop_rd, engine):
    
    # Returns dictionary of dataframes for hourly speeds on road indictaed
    hourlyspeeds_dict = {}
    
    temp_dict = {}
    
    for i in range(0,24):
        avrg_spds = f'''SELECT speed_kph_mean FROM uber_data WHERE road_name = '{pop_rd}' AND hour_of_day = {i}'''
    
        temp_dict[i] = pd.read_sql(avrg_spds, engine)
    
    hourlyspeeds_dict[pop_rd] = temp_dict
    
    return hourlyspeeds_dict

Limuru = data_by_roadway("Limuru Road", engine)


# Visually check to ensure that data for each group is normally distributed
# (In this case, "group" refers to hour of day during which speeds were recorded)

for i in range(0, 24):
    Limuru['Limuru Road'][i].plot.hist("speed_kph_mean", alpha=0.5)

 
# Function to check for standard deviatiation and standard variance across each group
    
def variance_and_stdeviation(datadict, roadname):
    
    for i in range(0, 24):
        df = datadict[roadname][i]
        
        speeds = df.values.tolist()
        speeds_lst = [item for sublist in speeds for item in sublist]

        valuesum = 0
        simple_mean = 0
        sumsqrs_numerator = 0
        checksum = 0

        for j in speeds_lst:
            valuesum += j

        simple_mean = valuesum/len(speeds_lst)

        for k in speeds_lst:
            temp = round(k - simple_mean, 2)
            checksum += temp
            t = temp **2
            sumsqrs_numerator += t

        sample_variance = sumsqrs_numerator/ (len(speeds_lst)-1)

        stdeviation = math.sqrt(sample_variance)

        datadict[roadname][i]["sample_variance"] = sample_variance
        datadict[roadname][i]["stdeviation"] = stdeviation

        print(sample_variance)
        print(stdeviation)
   
