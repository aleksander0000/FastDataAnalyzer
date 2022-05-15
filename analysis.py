import pandas as pd
class ImportedFile:
  def __init__(self, file_i: pd.DataFrame):
    self.file_i=file_i

  def return_size(self)->str:
    '''
      returns size of dataframe
    '''
    rows = self.file_i.shape[0]
    columns = self.file_i.shape[1]
    cells = self.file_i.shape[0]*self.file_i.shape[1]
    string = "There is "+str(rows)+" rows,"+str(columns)+" columns, "+str(cells)+ " cells"
    return string

  def return_missing_percentage(self)-> pd.DataFrame:
    '''
      returns table with information about missing cells
    '''
    missing_values = []
    names = self.file_i.columns.values.tolist()
    for emptyrows in self.file_i.isna().sum():
      ratio = round(emptyrows/self.file_i.shape[0],2)
      missing_values.append(str(ratio)+"%")
    table = {'Column name': names, 'Percentage of missing data': missing_values}
    return pd.DataFrame(table)

  def return_statistics(self)-> pd.DataFrame:
    '''
      returns table with statistics
    '''
    only_numeric = self.file_i._get_numeric_data()
    def table_stats(x):
      return pd.Series(index=['min', 'max','10th percentile','median','90th percentile','standard deviation','skewness','most dominant value'],
                       data=[x.min(), x.max(),x.quantile(q=0.1),x.quantile(q=0.5),x.quantile(q=0.9),x.std(),x.skew(),x.mode()])
    stats =only_numeric.apply(table_stats)
    return stats