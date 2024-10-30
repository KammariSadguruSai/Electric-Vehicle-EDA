#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


# In[11]:


p=pd.read_csv("G:/My Drive/INNO_INTERN/DATASETS/project2.csv")


# In[3]:


p.info()


# In[4]:


p.head()


# In[5]:


p.tail()


# In[7]:


p.describe()


# In[14]:


# ------------- Univariate Analysis -------------
# 1. Distribution of Model Year
plt.figure(figsize=(10, 6))
sns.histplot(p['Model Year'], kde=True, bins=30, color='green')
plt.title('Distribution of Model Year')
plt.xlabel('Model Year')
plt.ylabel('Count')
plt.show()


# In[17]:


# 2. Distribution of Electric Vehicle Type
plt.figure(figsize=(10, 6))
sns.countplot(data=p, x='Electric Vehicle Type', palette='Set3')
plt.title('Count of Electric Vehicle Types')
plt.xlabel('Electric Vehicle Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


# In[18]:


# 3. Distribution of Electric Range
plt.figure(figsize=(10, 6))
sns.histplot(p['Electric Range'], kde=True, bins=30, color='red')
plt.title('Distribution of Electric Range')
plt.xlabel('Electric Range (miles)')
plt.ylabel('Count')
plt.show()


# In[19]:


# ------------- Bivariate Analysis -------------
# 4. Electric Range vs. Model Year
plt.figure(figsize=(10, 6))
sns.scatterplot(data=p, x='Model Year', y='Electric Range', hue='Electric Vehicle Type', palette='coolwarm')
plt.title('Electric Range vs. Model Year')
plt.xlabel('Model Year')
plt.ylabel('Electric Range (miles)')
plt.legend(title='Electric Vehicle Type')
plt.show()


# In[22]:


# 5. Electric Range by Make
plt.figure(figsize=(10, 6))
sns.boxplot(data=p, x='Make', y='Electric Range', palette='Set1')
plt.title('Electric Range by Vehicle Make')
plt.xlabel('Make')
plt.ylabel('Electric Range (miles)')
plt.xticks(rotation=90)
plt.show()


# In[23]:


# 6. Base MSRP vs Electric Range
plt.figure(figsize=(10, 6))
sns.scatterplot(data=p, x='Base MSRP', y='Electric Range', hue='Electric Vehicle Type', palette='viridis')
plt.title('Base MSRP vs Electric Range')
plt.xlabel('Base MSRP (USD)')
plt.ylabel('Electric Range (miles)')
plt.legend(title='Electric Vehicle Type')
plt.show()


# In[24]:


# 7. Count of Clean Alternative Fuel Vehicle Eligibility
plt.figure(figsize=(10, 6))
sns.countplot(data=p, x='Clean Alternative Fuel Vehicle (CAFV) Eligibility', palette='Set1')
plt.title('Count of CAFV Eligibility')
plt.xlabel('CAFV Eligibility')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


# In[26]:


# Missing Data Check
print(p.isnull().sum())



# In[27]:


import seaborn as sns
import matplotlib.pyplot as plt

# Heatmap to visualize missing data
plt.figure(figsize=(10, 6))
sns.heatmap(p.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Data Heatmap')
plt.show()


# In[29]:


# Boxplot for outlier detection in Electric Range
plt.figure(figsize=(10, 6))
sns.boxplot(data=p, y='Electric Range')
plt.title('Boxplot of Electric Range (Outlier Detection)')
plt.show()

# Boxplot for outlier detection in Base MSRP
plt.figure(figsize=(10, 6))
sns.boxplot(data=p, y='Base MSRP')
plt.title('Boxplot of Base MSRP (Outlier Detection)')
plt.show()


# In[31]:


# Correlation matrix and heatmap
plt.figure(figsize=(10, 6))
corr_matrix = p[['Electric Range', 'Model Year', 'Base MSRP']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()


# In[32]:


# Boxplot for Electric Range by CAFV Eligibility
plt.figure(figsize=(10, 6))
sns.boxplot(data=p, x='Clean Alternative Fuel Vehicle (CAFV) Eligibility', y='Electric Range')
plt.title('Electric Range by CAFV Eligibility')
plt.xlabel('CAFV Eligibility')
plt.ylabel('Electric Range (miles)')
plt.xticks(rotation=45)
plt.show()


# In[34]:


# Electric Range by City (Top 10 Cities)
top_cities = p['City'].value_counts().nlargest(10).index
filtered_data = p[p['City'].isin(top_cities)]

plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data, x='City', y='Electric Range', palette='Set3')
plt.title('Electric Range by City (Top 10 Cities)')
plt.xlabel('City')
plt.ylabel('Electric Range (miles)')
plt.xticks(rotation=90)
plt.show()


# # Task 2: Create a Choropleth using plotly.express to display the number of EV vehicles based on location.

# In[35]:


get_ipython().system('pip install plotly')


# In[36]:


import plotly.express as px


# In[37]:


scatter_plot = px.scatter(p, x="Electric Range", y="Base MSRP", title="Scatter Plot: Electric Range vs Base MSRP")
scatter_plot.show()


# In[39]:


box_plot = px.box(p, x="Electric Vehicle Type", y="Electric Range", title="Box Plot: Electric Vehicle Type vs Electric Range")
box_plot.show()


# In[40]:


vehicle_type_count = p['Electric Vehicle Type'].value_counts().reset_index()
vehicle_type_count.columns = ['Electric Vehicle Type', 'Count']
pie_chart = px.pie(vehicle_type_count, names='Electric Vehicle Type', values='Count', title="Pie Chart: Distribution of Electric Vehicle Types")
pie_chart.show()


# In[41]:


vehicle_count_by_state = p['State'].value_counts().reset_index()
vehicle_count_by_state.columns = ['State', 'Vehicle Count']

choropleth = px.choropleth(vehicle_count_by_state,
                           locations="State",
                           locationmode="USA-states",
                           color="Vehicle Count",
                           scope="usa",
                           title="Choropleth Map: Number of EV Vehicles by State")
choropleth.show()


# In[43]:


animated_choropleth = px.choropleth(p,
                                    locations="State",
                                    locationmode="USA-states",
                                    color="Electric Range",
                                    animation_frame="Model Year",
                                    scope="usa",
                                    title="Animated Choropleth: Electric Range over Model Year by State")
animated_choropleth.show()


# # Task 3: Create a Racing Bar Plot to display the animation of EV Make and its count each year.

# In[44]:


get_ipython().system('pip install bar_chart_race')


# In[47]:


# Assuming you have already loaded your dataset
# Create a pivot table with counts of vehicles by 'Make' and 'Model Year'
pivot_data = p.pivot_table(index="Model Year", columns="Make", aggfunc="size", fill_value=0)

# Sort the columns by sum of vehicle counts
pivot_data = pivot_data.loc[:, pivot_data.sum(axis=0).sort_values(ascending=False).index]


# In[46]:


import bar_chart_race as bcr


# In[49]:


# Create a pivot table with counts of vehicles by 'Make' and 'Model Year'
pivot_data = p.pivot_table(index="Model Year", columns="Make", aggfunc="size", fill_value=0)

# Reset index to make 'Model Year' a column
pivot_data.reset_index(inplace=True)
melted_data = pivot_data.melt(id_vars=["Model Year"], var_name="Make", value_name="Count")

# Create an animated bar plot
fig = px.bar(melted_data,
             x='Count',
             y='Make',
             color='Make',
             animation_frame='Model Year',
             range_x=[0, melted_data['Count'].max() + 10],  # Adjust range for better visualization
             title='Year-wise EV Make Sales Animation',
             orientation='h')


fig.update_layout(
    title_font=dict(size=30), 
    xaxis_title_font=dict(size=20), 
    yaxis_title_font=dict(size=20),  
    width=1000,  
    height=600,  
    bargap=0.1,  
)

