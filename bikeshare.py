import time
import pandas as pd
import numpy as np
import sys

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

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
    while True:
        city = input('Please choose a city: Chicago, New York City, Washington. Or type q to quit.').lower()
        if city == 'q':
            sys.exit()
        if city == 'new york city' or city == 'washington' or city == 'chicago':
            break

    while True:
        print('Would you like to filter the data? Please choose month, day, both, or none for no filters.')
        data_options = ['month', 'day', 'both', 'none']
        data_choice = input().lower()
        if data_choice == 'month' or data_choice == 'day' or data_choice == 'both' or data_choice == 'none':
            while data_choice not in data_options:
                print('Please choose a valid entry: month, day, both, or none.')

            if data_choice == 'month':
                while True:
                    print('Please choose a month: January, February, March, April, May, or June.')
                    month = input().lower()
                    day = 'all'
                    if month in MONTHS:
                        break

            elif data_choice == 'day':
                while True:
                    print('Please choose a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.')
                    day = input().lower()
                    month = 'all'
                    if day in DAYS:
                        break

            elif data_choice == 'both':
                while True:
                    print('Please choose a month: January, February, March, April, May, or June.')
                    month = input().lower()
                    if month in MONTHS:
                        break
                while True:
                    print('Please choose a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.')
                    day = input().lower()
                    if day in DAYS:
                        break

            else:
                month = 'all'
                day = 'all'
            break


    print('\n')
    print('='*40)

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

    df = pd.read_csv(CITY_DATA[city])

    # Converts Start Time to datetime and creating additional columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['month_name'] = df['Start Time'].dt.month_name()
    df['dow_name'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['station_route'] = df['Start Station'] + ' <----> ' + df['End Station']

    # Filters DataFrame by month and day of week
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['dow_name'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    mode_hour = df.mode()['hour'][0]
    mode_weekday = df.mode()['dow_name'][0]
    mode_month = df.mode()['month_name'][0]

    # display the most common start hour
    print(f'Most popular hour of the day to travel: {mode_hour}')
    # display the most common day of week
    print(f'Most popular day of the week to travel: {mode_weekday}')
    # display the most common month
    print(f'Most popular month to travel: {mode_month}')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Routes...\n')
    start_time = time.time()

    mode_start_station = df.mode()['Start Station'][0]
    mode_end_station = df.mode()['End Station'][0]
    # mode_route = df.mode()['station_route'][0]

    # display most commonly used start station
    print(f'Most popular start station: {mode_start_station}')
    # display most commonly used end station
    print(f'Most popular end station: {mode_end_station}')

    # Displays the counts for the top 5 most frequent start station and stop station trips
    print('\n')
    print('Displaying counts for the top 5 most common routes:')
    print(df['station_route'].value_counts(sort=True).nlargest(5))
    print('\n')


    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    count_trips = df.count()['Trip Duration']
    sum_duration = df.sum()['Trip Duration'] / 60
    avg_duration = df.mean()['Trip Duration'] / 60

    # display total count of trips
    print(f'Total number of trips: {count_trips} trips')
    # display total travel time
    print(f'Total trip duration: {round(sum_duration, 2)} minutes')
    # display mean travel time
    print(f'Average trip duration: {round(avg_duration, 2)} minutes per trip')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df.groupby(['User Type'])['User Type'].count().to_string() + '\n')

    #Display counts of gender
    if 'Gender' in df.columns:
        print(df.groupby(['Gender'])['Gender'].count().to_string() + '\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_year = df.min()['Birth Year']
        max_year = df.max()['Birth Year']
        mode_year = df.mode()['Birth Year'][0]
        print(f'Earliest year of birth: {int(min_year)}')
        print(f'Most recent year of bith: {int(max_year)}')
        print(f'Most common year of birth: {int(mode_year)}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # Dipslays 5 rows of raw data for user to view

    start_loc = 0
    while True:
        show_data = input('Would you like to see 5 lines of raw data? Enter yes or no.')
        if show_data.lower() == 'yes':
            print("\nDisplaying only 5 rows of data.\n")
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        elif show_data.lower() == 'no':
            break
        else:
            show_data = input('Would you like to see 5 lines of raw data? Enter yes or no.')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
