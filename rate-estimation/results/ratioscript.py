import pandas as pd
import matplotlib.pyplot as plt
df1 = pd.read_csv ('testoutput4.csv')
df2 = pd.read_csv ('testoutput3.csv')
df = pd.DataFrame()
df['L1SeedName'] = df1['L1SeedName']
df['R(rate0)'] = df1['rate0']/df2['rate0']
df['R(pure0)'] = df1['pure0']/df2['pure0']
df['R(propotional0)'] = df1['propotional0']/df2['propotional0']
df.dropna(inplace=True)
#df
df0 = df[df['R(rate0)']!= 1]
#df2
plt.figure(figsize=(20,15))
plt.style.use('seaborn-whitegrid')
plt.scatter( df["R(rate0)"],df["L1SeedName"],marker="+")
#plt.show()
plt.savefig("ratio.png")
