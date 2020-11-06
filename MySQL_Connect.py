import sqlalchemy
import scipy.stats as stats
from pingouin import pairwise_tukey
import statsmodels.api as sm
from statsmodels.formula.api import ols

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

# Calculate F Statistic and P Value to determine whether speeds vary significantly on Limuru road across times of day
fvalue, pvalue = stats.f_oneway(roadway_datadict['Limuru Road'][0]['speed_kph_mean'], 
                                roadway_datadict['Limuru Road'][1]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][2]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][3]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][4]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][5]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][6]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][7]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][8]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][9]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][10]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][11]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][12]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][13]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][14]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][15]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][16]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][17]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][18]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][19]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][20]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][21]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][22]['speed_kph_mean'],
                                roadway_datadict['Limuru Road'][23]['speed_kph_mean'])

print(fvalue, pvalue)

# Above function indicated that speeds to vary signficiantly across times of day
# Note that this tells us a statistically signficant relationship exists but does not indicate the hours between which this relationship is found to be significant
# Create seperate dataset for Limuru road only to prepare data to be tested, in order to understand *which* hours vary significantly from others

Limuru = full_dataset[full_dataset.road_name == 'Limuru Road'].copy()

Limuru = Limuru.drop(columns = ['year', 'quarter', 'osm_way_id', 'speed_kph_stddev', 'speed_kph_p85', 'road_name', 'one_way', 'surface', 'road_type'])

Limuru0 = Limuru[Limuru.hour_of_day == 0].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "0"}).reset_index().drop(columns='index')

Limuru1 = Limuru[Limuru.hour_of_day == 1].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "1"}).reset_index().drop(columns='index')

Limuru2 = Limuru[Limuru.hour_of_day == 2].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "2"}).reset_index().drop(columns='index')

Limuru3 = Limuru[Limuru.hour_of_day == 3].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "3"}).reset_index().drop(columns='index')

Limuru4 = Limuru[Limuru.hour_of_day == 4].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "4"}).reset_index().drop(columns='index')

Limuru5 = Limuru[Limuru.hour_of_day == 5].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "5"}).reset_index().drop(columns='index')

Limuru6 = Limuru[Limuru.hour_of_day == 6].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "6"}).reset_index().drop(columns='index')

Limuru7 = Limuru[Limuru.hour_of_day == 7].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "7"}).reset_index().drop(columns='index')

Limuru8 = Limuru[Limuru.hour_of_day == 8].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "8"}).reset_index().drop(columns='index')

Limuru9 = Limuru[Limuru.hour_of_day == 9].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "9"}).reset_index().drop(columns='index')

Limuru10 = Limuru[Limuru.hour_of_day == 10].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "10"}).reset_index().drop(columns='index')

Limuru11 = Limuru[Limuru.hour_of_day == 11].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "11"}).reset_index().drop(columns='index')

Limuru12 = Limuru[Limuru.hour_of_day == 12].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "12"}).reset_index().drop(columns='index')

Limuru13 = Limuru[Limuru.hour_of_day == 13].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "13"}).reset_index().drop(columns='index')

Limuru14 = Limuru[Limuru.hour_of_day == 14].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "14"}).reset_index().drop(columns='index')

Limuru15 = Limuru[Limuru.hour_of_day == 15].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "15"}).reset_index().drop(columns='index')

Limuru16 = Limuru[Limuru.hour_of_day == 16].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "16"}).reset_index().drop(columns='index')

Limuru17 = Limuru[Limuru.hour_of_day == 17].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "17"}).reset_index().drop(columns='index')

Limuru18 = Limuru[Limuru.hour_of_day == 18].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "18"}).reset_index().drop(columns='index')

Limuru19 = Limuru[Limuru.hour_of_day == 19].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "19"}).reset_index().drop(columns='index')

Limuru20 = Limuru[Limuru.hour_of_day == 20].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "20"}).reset_index().drop(columns='index')

Limuru21 = Limuru[Limuru.hour_of_day == 21].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "21"}).reset_index().drop(columns='index')

Limuru22 = Limuru[Limuru.hour_of_day == 22].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "22"}).reset_index().drop(columns='index')

Limuru23 = Limuru[Limuru.hour_of_day == 23].copy().drop(columns = 'hour_of_day').rename(columns={"speed_kph_mean": "23"}).reset_index().drop(columns='index')

df_concat = pd.concat([Limuru0, Limuru1, Limuru2, Limuru3, Limuru4, Limuru5, Limuru6, Limuru7, Limuru8, Limuru9, Limuru10,
                      Limuru11, Limuru12, Limuru13, Limuru14, Limuru15, Limuru16, Limuru17, Limuru18, Limuru19,
                      Limuru20, Limuru21, Limuru22, Limuru23], axis=1)

d_melt = pd.melt(df_concat.reset_index(), id_vars=['index'], value_vars=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])

d_melt.columns = ['index', 'treatments', 'value']

model = ols('value ~ C(treatments)', data=d_melt).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

anova_table

m_comp = pairwise_tukey(data=d_melt, dv='value', between='treatments')

# Since there are so many relationships to compare across, examining the table in slices, as indicated below, is best
m_comp[0:24]










#### Below contains a set of functions/ operations that are seeking to recreate the ANOVA calculations above
# Created in order to practice understanding of ANOVA application

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
# Potential follow on: these histograms would look nicer in plotly, consider stylizing them? ** 

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
        datadict[roadname][i]["simple_mean"] = simple_mean

#         print(sample_variance)
#         print(stdeviation)

# Check that variance and standard deviation were added to roadway dictionary correctly
# one simple check to make sure the formula in the function is working correctly is to make sure the variance is equivalent to standard deviation squared 

roadway_datadict['Limuru Road'][0]['simple_mean']


# Conducting ANOVA (Analysis of Variance)
# Hypothesis: mean traveling speed on a given roadway does not differ depending on time of day 
# (avrg spd at 1am == avrg spd at 2am == avrg speed at 3am...)

# Calculate F statistic by comparing the sample variance in each group (F statistic should always be a positive number) 

for i in range(0,22):
    if roadway_datadict['Limuru Road'][i]['sample_variance'][0] >= roadway_datadict['Limuru Road'][i+1]['sample_variance'][0]:
        f_stat = roadway_datadict['Limuru Road'][i]['sample_variance'][0]/roadway_datadict['Limuru Road'][i]['sample_variance'][0]
        print("Hour ", i, " compared to hour ", i+1, "\n\t F statistic: ", f_stat, "\n")
        
    else:
        f_stat = roadway_datadict['Limuru Road'][i+1]['sample_variance'][0]/roadway_datadict['Limuru Road'][i]['sample_variance'][0]
        print("Hour ", i + 1, " compared to hour ", i, "\n\t F statistic: ", f_stat, "\n")

# Determine group mean (average speed on roadway across all hours of the day) 

group_mean = 0

for i in range(0,23):
    group_mean += roadway_datadict['Limuru Road'][i]['stdeviation'][0]

group_mean = group_mean/24
group_mean


class UniqueRoadway:
    def __init__(self, name, df):
        self.__df = df
        self.name = name
        self.p85 = self.__df['speed_kph_p85']
        
    def review(self, num1, num = 0):
        display(self.__df[num:num1])
        return
        
    def cols(self):
        return self.__df.columns
    
    def anova_oneway(self, colname):
        
        li = [kamiti[kamiti.hour_of_day == i][colname] for i in range(24)]
            
        stat, p = scipy.stats.f_oneway(*li)
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p > alpha:
            print('Same distributions (fail to reject H0)')
        else:
            print('Different distributions (reject H0)')
            
    def hour_of_day(self, num):
        
        return self.__df[self.__df.hour_of_day == num]
    
    def morning_commute(self):
        
        temp = pd.DataFrame()
        
        for i in range(6,10):
            
            t = self.__df[self.__df.hour_of_day == i]
            
            temp = temp.append(t, sort=False)
        
        return temp
    
    def evening_commute(self):
        
        temp = pd.DataFrame()
        
        for i in range(17,22):
            
            t = self.__df[self.__df.hour_of_day == i]
            
            temp = temp.append(t, sort=False)
        
        return temp
