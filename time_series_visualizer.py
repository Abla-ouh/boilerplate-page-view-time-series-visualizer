import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# ====== Load and clean data once ======
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Remove top and bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

# ====== 1. Line Plot ======
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig('line_plot.png')
    return fig

# ====== 2. Bar Plot ======
def draw_bar_plot():
    # Prepare data
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Group by year and month and get the average
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reorder months
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped = df_grouped[months_order]

    # Draw the plot
    fig = df_grouped.plot(kind='bar', figsize=(15, 8)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title='Months')
    plt.tight_layout()

    fig.savefig('bar_plot.png')
    return fig

# ====== 3. Box Plots ======
def draw_box_plot():
    # Prepare data
    df_box = df.copy()
    df_box = df_box.reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')  # ensure months are ordered

    # Draw box plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 7), dpi=100)

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig
