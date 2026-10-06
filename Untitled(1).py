#!/usr/bin/env python
# coding: utf-8

# In[7]:

from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# In[8]:

DATA_DIR = Path(__file__).resolve().parent
DATA_CANDIDATES = (DATA_DIR / "Netflix.csv", DATA_DIR / "netflix.csv")
DATA_PATH = next((path for path in DATA_CANDIDATES if path.is_file()), None)
if DATA_PATH is None:
    raise FileNotFoundError(
        f"Could not find Netflix.csv or netflix.csv beside {Path(__file__).name}."
    )
netflix = pd.read_csv(DATA_PATH)


# In[9]:


netflix


# In[10]:


#data cleaning
netflix.shape #is used for find how many rows and colums in dataset


# In[26]:


netflix.info() #is used for all information odf data like data tpye and null value


# In[27]:


netflix.isnull().sum() # to check total null value in data


# In[28]:


netflix.duplicated().sum()


# In[29]:


netflix.describe()#is used for see stastastical information in dataset


# In[30]:


netflix["Watch_Date"]=pd.to_datetime(netflix["Watch_Date"])


# In[31]:


netflix.info()


# In[32]:


netflix.dtypes


# In[38]:


netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",title="region wise revenue")


# In[13]:


netflix.groupby("Subscription_Plan")["Rating"].sum().plot(kind="line",ylabel="Rating",title="Subscription Plan wise rating")


# In[14]:


netflix["Rating"].value_counts().plot(kind="bar")


# In[61]:


netflix.groupby("Category")["Monthly_Revenue"].sum().plot(kind="pie",ylabel="Monthly_Revenue",title="category wise rating")


# In[ ]:
