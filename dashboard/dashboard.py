import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="dark")

# Load data
day_df = pd.read_csv("dashboard/day.csv")
day_df.head()

# Drop unnecessary columns
drop_column = ['windspeed']
for i in drop_column:
    day_df.drop(i, axis=1, inplace=True)

# Rename columns
day_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Map numerical values to descriptive labels
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Define functions to create DataFrames
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    }).reindex([
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], fill_value=0).reset_index()
    return monthly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    }).reset_index()
    return weather_rent_df

# Get min and max dates
min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()

# Sidebar for date filtering
with st.sidebar:
    st.image("https://miro.medium.com/v2/resize:fit:2000/0*TZ0bsPAR7gGvOoEu")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on date range
main_df = day_df[(day_df['date'] >= str(start_date)) &
                 (day_df['date'] <= str(end_date))]

# Create DataFrames
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Streamlit dashboard
st.header('Bike Rental Dashboard 🚲')

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value=daily_rent_total)

st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df['month'],
    monthly_rent_df['count'],
    marker='o',
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader('Seasonly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

st.subheader('Weatherly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

colors = ["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Weekday, Workingday, and Holiday Rentals')

# Weekday, Workingday, and Holiday Rentals
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

colors1 = ["tab:blue", "tab:orange"]
colors2 = ["tab:blue", "tab:orange"]
colors3 = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

sns.barplot(
    x='workingday',
    y='count',
    hue='workingday',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0],
    legend=False
)

for index, row in enumerate(workingday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

sns.barplot(
    x='holiday',
    y='count',
    hue='holiday',
    data=holiday_rent_df,
    palette=colors2,
    ax=axes[1],
    legend=False
)

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

sns.barplot(
    x='weekday',
    y='count',
    hue='weekday',
    data=weekday_rent_df,
    palette=colors3,
    ax=axes[2],
    legend=False
)

for index, row in enumerate(weekday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.markdown(
    "<div style='text-align: center;'>Copyright (c) Muhamad Chaerul Anwar 2024</div>",
    unsafe_allow_html=True
)