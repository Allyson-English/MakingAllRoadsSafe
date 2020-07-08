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
