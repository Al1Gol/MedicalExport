import os
import pandas as pd

df = pd.read_excel(rf'{os.getcwd()}\client_org.xlsx', sheet_name='client')
print(df.values)