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

query = '''
SELECT COUNT(*) FROM uber_data WHERE road_name = "Mumias South Road"
'''

pd.read_sql(query, engine)

