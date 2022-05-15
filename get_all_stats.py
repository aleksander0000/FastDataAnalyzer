import analysis
import sys
import pandas as pd
path = sys.argv[1]
df = pd.read_csv(path)
analysis_object = analysis.ImportedFile(df)
print(analysis_object.return_size())
print(analysis_object.return_missing_percentage())
print(analysis_object.return_statistics())

#python get_all_stats.py /home/alek/Pobrane/silver.csv
