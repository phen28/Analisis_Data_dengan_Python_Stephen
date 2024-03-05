import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_daily_df(df):
    daily_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_df

def create_daily_casual_df(df):
    daily_casual_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_df

def create_daily_registered_df(df):
    daily_registered_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_df
    
def create_season_df(df):
    season_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_df

def create_monthly_df(df):
    monthly_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_df = monthly_df.reindex(ordered_months, fill_value=0)
    return monthly_df

def create_weekday_df(df):
    weekday_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_df

def create_workingday_df(df):
    workingday_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_df

def create_holiday_df(df):
    holiday_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_df

def create_weather_df(df):
    weather_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_df

day_df = pd.read_csv("days.csv")

min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/phen28/dashboard/main/logo_dashboard.png", width=150)
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]


daily_df = create_daily_df(main_df)
daily_casual_df = create_daily_casual_df(main_df)
daily_registered_df = create_daily_registered_df(main_df)
season_df = create_season_df(main_df)
monthly_df = create_monthly_df(main_df)
weekday_df = create_weekday_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)
weather_df = create_weather_df(main_df)


st.header('Stephen\'s Bike Dashboard')

col1, col2, col3 = st.columns(3)

with col1:
    daily_casual = daily_casual_df['casual'].sum()
    st.metric('Casual User', value= daily_casual)

with col2:
    daily_registered = daily_registered_df['registered'].sum()
    st.metric('Registered User', value= daily_registered)
 
with col3:
    daily_total = daily_df['count'].sum()
    st.metric('Total User', value= daily_total)


st.subheader('Monthly Sharing Bike Reports')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_df.index,
    monthly_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_df,
    label='Registered',
    color='tab:orange',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_df,
    label='Casual',
    color='tab:grey',
    ax=ax
)

for index, row in season_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


st.subheader('Weatherly Sharing Bike Reports')

fig, ax = plt.subplots(figsize=(18, 8))

colors=["tab:orange", "tab:grey", "tab:pink"]

sns.barplot(
    x=weather_df.index,
    y=weather_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


st.subheader('Weekday, Workingday, and Holiday Sharing Bike Reports')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12,10))

colors1=["tab:orange", "tab:grey"]
colors2=["tab:orange", "tab:grey"]
colors3=["tab:orange", "tab:grey", "tab:pink", "tab:red", "tab:brown", "tab:blue", "tab:green"]

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Sharing Bike based on Workingday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=15)

sns.barplot(
  x='holiday',
  y='count',
  data=holiday_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Sharing Bike based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=15)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='count',
  data=weekday_df,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(weekday_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Sharing Bike based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=15)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright © 2024 Stephen J. Rusli')