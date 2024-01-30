import os

# Create directory
os.makedirs('DivvyBikeShareDataAnalysis', exist_ok=True)

# Change directory
os.chdir('DivvyBikeShareDataAnalysis')

# Create files
open('__init__.py', 'a').close()
open('data_collection.py', 'a').close()
open('bike_share_analysis.py', 'a').close()