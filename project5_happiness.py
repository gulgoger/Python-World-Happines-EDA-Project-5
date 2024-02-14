import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_style("whitegrid")
from plotly.offline import init_notebook_mode, iplot
import plotly.express as px  # for world map
import plotly.graph_objs as go

plt.style.use("seaborn-notebook")

import warnings
warnings.filterwarnings("ignore")


#read data
df = pd.read_csv("world-happiness-report.csv")

df.head()

describe = df.describe()

df.info()


df2021 = pd.read_csv("world-happiness-report-2021.csv")

df2021.head()

describe2021 = df2021.describe()

df2021.info()

df2021.columns

#unique countries
df2021["Country name"].unique()

#count regional indicator
sns.countplot(df2021["Regional indicator"])
plt.xticks(rotation=60)
plt.show()
plt.figure()


#distribution of feature set 1
list_features = ["Social support","Freedom to make life choices","Generosity","Perceptions of corruption"]
sns.boxplot(data=df2021.loc[:,list_features],orient="v",palette="Set1")
plt.show()


#distribution of feature set 2
list_features = ["Ladder score", "Logged GDP per capita"]
sns.boxplot(data=df2021.loc[:,list_features],orient="v",palette="Set1")
plt.show()

#distribution of feature set 3
list_features = ["Healthy life expectancy"]
sns.boxplot(data=df2021.loc[:,list_features],orient="v",palette="Set1")
plt.show()

#happiest and unhappiest country in 2021
df2021_happiest_unhappiest = df2021[(df2021.loc[:,"Ladder score"] > 7.4) | (df2021.loc[:,"Ladder score"] < 3.5)]
sns.barplot(x="Ladder score",y="Country name", data = df2021_happiest_unhappiest, palette="coolwarm")
plt.title("Happiest and Unhappiest Countries in 2021")
plt.show()

#Ladder Score Distribution by Regional Indicator
plt.figure(figsize=(15,8))
sns.kdeplot(df2021["Ladder score"],hue=df2021["Regional indicator"], fill=True, linewidth=2)
plt.axvline(df2021["Ladder score"].mean(), c="black")
plt.title("Ladder Score Distribution by Regional Indicator")
plt.show()

#Ladder Score Distribution by Countries in Map View

fig = px.choropleth(df.sort_values("year"),
                   locations = "Country name",
                   color = "Life Ladder",
                   locationmode = "country names",
                   animation_frame = "year")
fig.update_layout(title = "Life Ladder Comparison by Countries")
fig.show()

#Most Generous and Ungenerous Countries in 2021

df2021_g = df2021[(df2021.loc[:,"Generosity"]> 0.4) | (df2021.loc[:,"Generosity"]< -0.2)]
sns.barplot(x="Generosity", y="Country name", data=df2021_g, palette="coolwarm")
plt.title("Most Generous and Ungenerous Countries in 2021")
plt.show()

#Generous Distributions by Countries in Map View

fig = px.choropleth(df.sort_values("year"),
                   locations = "Country name",
                   color = "Generosity",
                   locationmode = "country names",
                   animation_frame = "year")
fig.update_layout(title = "Generosity Comparison by Countries")
fig.show()
plt.figure()
#Generous Distributions by Regional Indicator
sns.swarmplot(x ="Regional indicator", y="Generosity", data=df2021)
plt.xticks(rotation=60)
plt.title("Generous Distributions by Regional Indicator")
plt.show()

#Relationship Between Happiness and Income

pop = pd.read_csv("population_total_long.csv")
pop.head()

country_continent = {}
for i in range(len(df2021)):
    country_continent[df2021["Country name"][i]] = df2021["Regional indicator"][i]
all_countries = df["Country name"].value_counts().reset_index()["index"].tolist()
all_countries_2021 = df2021["Country name"].value_counts().reset_index()["index"].tolist()

for x in all_countries:
    if x not in all_countries_2021:
        print(x)

region = []
for i in range(len(df)):
    if df["Country name"][i] == "Angola":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "Belize":
        region.append("Latin America and Caribbean")
    elif df["Country name"][i] == "Congo (Kinshasa)":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "Syria":
        region.append("Middle East and North Africa")
    elif df["Country name"][i] == "Trinidad and Tobago":
        region.append("Latin America and Caribbean")
    elif df["Country name"][i] == "Cuba":
        region.append("Latin America and Caribbean")
    elif df["Country name"][i] == "Qatar":
        region.append("Middle East and North Africa")
    elif df["Country name"][i] == "Sudan":
        region.append("Middle East and North Africa")
    elif df["Country name"][i] == "Central African Republic":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "Djibouti":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "Somaliland region":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "South Sudan":
        region.append("Middle East and North Africa")
    elif df["Country name"][i] == "Somalia":
        region.append("Sub-Saharan Africa")
    elif df["Country name"][i] == "Oman":
        region.append("Middle East and North Africa")
    elif df["Country name"][i] == "Guyana":
        region.append("Latin America and Caribbean")
    elif df["Country name"][i] == "Bhutan":
        region.append("South Asia")
    elif df["Country name"][i] == "Suriname":
        region.append("Latin America and Caribbean")
    else:
        region.append(country_continent[df["Country name"][i]])

df["region"] = region

df.head()

all_countries = df["Country name"].value_counts().reset_index()["index"].to_list()
all_countries_pop = pop["Country Name"].value_counts().reset_index()["index"].to_list()

del_cou = []
for x in all_countries:
    if x not in all_countries_pop:
        del_cou.append(x)
del_cou

pop_df = df[['Log GDP per capita','Life Ladder','Country name','year','Social support',
             'Healthy life expectancy at birth','Freedom to make life choices','Generosity','region',
            'Perceptions of corruption']].copy()
pop_df.head()


pop_df = pop_df[~pop_df["Country name"].isin(del_cou)]
pop_df = pop_df[~pop_df.year.isin([2006,2005,2007,2018,2019,2020,2021])]
pop_dict = {x: {} for x in range(2008,2018)}
for i in range(len(pop)):
    if (pop["Year"][i] in range(2008,2018)):
        pop_dict[pop["Year"][i]][pop["Country Name"][i]] = pop["Count"][i]


population = []
for i in pop_df.index:
    population.append(pop_dict[pop_df["year"][i]][pop_df["Country name"][i]])
pop_df["population"] = population

pop_df.head()

fig = px.scatter(pop_df,
                x="Log GDP per capita",
                y = "Life Ladder",
                animation_frame = "year",
                animation_group = "Country name",
                size = "population",
                template = "plotly_white",
                color = "region",
                hover_name = "Country name",
                size_max = 60)
fig.update_layout(title= "Life Ladder and Log GDP per capita Comparison by Countries via Regions for each Year")
fig.show()


# Relationship Between Happiness and Freedom

fig = px.scatter(pop_df,
                x="Freedom to make life choices",
                y = "Life Ladder",
                animation_frame = "year",
                animation_group = "Country name",
                size = "population",
                template = "plotly_dark",
                color = "region",
                hover_name = "Country name",
                size_max = 60)
fig.update_layout(title= "Life Ladder and Freedom Comparison by Countries via Regions for each Year")
fig.show()


#Relationship Between Happiness and Corruption

fig = px.scatter(pop_df,
                x="Perceptions of corruption",
                y = "Life Ladder",
                animation_frame = "year",
                animation_group = "Country name",
                size = "population",
                template = "plotly_dark",
                color = "region",
                hover_name = "Country name",
                size_max = 60)
fig.update_layout(title= "Life Ladder and Corruption Comparison by Countries via Regions for each Year")
fig.show()

# Relationship Between Features
sns.heatmap(df.corr(),annot=True, fmt=".2f",linewidth =.7)
plt.title("Relationship Between Features")
plt.show()


sns.clustermap(df.corr(),center=0, cmap="vlag",dendrogram_ratio = (0.1,0.2), annot=True,linewidths=.7,figsize=(10,10))
plt.show()


"""
plotly plots does not work in Spyder
"""
















