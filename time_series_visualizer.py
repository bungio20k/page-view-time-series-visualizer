from typing import Sized
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates = True, index_col = "date")

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12,5))

    plt.plot(df, color = "red")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    cbar = df_bar.groupby([df.index.year, df.index.month],)['value'].agg(np.mean).rename_axis(['year', 'month'])
    cbar = cbar.reset_index()

    df_pivtab = pd.pivot_table(cbar, values = 'value', index = 'year', columns = 'month')
    ax = df_pivtab.plot(kind='bar')
    fig = ax.get_figure()
    fig.set_size_inches(9,9)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], title = 'Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    df_box.rename(columns= {"value" : "Page Views"}, inplace= True)
    
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(figsize=(12,5))
    
    ax = plt.subplot(1,2,1)
    sns.boxplot(x = "Year", y = "Page Views", data = df_box)
    plt.title("Year-wise Box Plot (Trend)")
    
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax = plt.subplot(1,2,2)
    sns.boxplot(x = "Month", y = "Page Views", data = df_box, order = month_order)
    plt.title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
