import time
import pandas as pd
import numpy as np

#data used, lists and dictionaries
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def check_user_input(inputstr):
    while True:
        userinput = input(inputstr).lower().rstrip()
        if userinput.isalpha():
            print(userinput)
            break
        else:
            print(f"Please only type letters {userinput}")
    return userinput

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    city = check_user_input("Which city would you like to explore its data? (Chicago, New York City or Washington)")
    month = check_user_input("Which month? (Choose a month from January to June, or all)")
    day = check_user_input("Which day? (Choose a day from Monday to Sunday, or all)")

    while city not in cities:
        city = check_user_input(f"Please choose one of the cities in the list")
    while month not in months:
        month = check_user_input(f"Please choose one of the months in the list")
    while day not in days:
        day = check_user_input(f"Please choose one of the days in the list")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        num = months.index(month) + 1
        df = df[df['Month'] == num]

    if day != 'all':
        df = df[df['Day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df["Month"].mode()[0]
    print(f'the most common month is {common_month}')

    # display the most common day of week
    common_day_of_week = df["Day_of_week"].mode()[0]
    print(f'the most common day of week is {common_day_of_week}')

    # display the most common start hour
    common_start_hour = df["Hour"].mode()[0]
    print(f'the most common start hour is {common_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'the most common start station is {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'the most common end station is {common_end_station}')

    # display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station','End Station']).size().nlargest(1).mode()[0]
    print(f'the most common combination is {common_combo}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'the total travel time is {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'the mean travel time is {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print(f'user types stats {count_user_type}')

    # Display counts of gender
    if city != 'washington':
        count_gender = df['Gender'].value_counts()
        print(f'Gender stats: {count_gender}')
        # Display earliest, most recent, and most common year of birth
        old_birthdate = df['Birth Year'].min()
        print(f'the earliest year of birth is: {old_birthdate}')
        recent_birthdate = df['Birth Year'].max()
        print(f'the most recent year of birth is: {recent_birthdate}')
        common_birthdate = df['Birth Year'].mode()[0]
        print(f'the most common year of birth is: {common_birthdate}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = check_user_input('\nWould you like to view 5 rows of the data used to calculate these stats? yes or no: \n')
    start_loc = 0
    while True:
        if view_data == 'no':
            break
        elif view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_data = check_user_input('\nDo you wish to continue and see 5 more rows? yes or no: \n')
        else:
            print("Please try again. You must type yes or no")
            check_user_input('\nWould you like to view 5 rows of the data used to calculate these stats? yes or no: \n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        restart = check_user_input('\nWould you like to restart? Enter yes or no: \n')
        if restart == 'no':
            break
        elif restart == 'yes':
            continue
        else:
            print("Please try again. You must type yes or no")
            check_user_input('\nWould you like to restart? Enter yes or no: \n')

if __name__ == "__main__":
    main()

