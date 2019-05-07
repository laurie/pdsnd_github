import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        global city
        city = input("\nWhich city? - Chicago, New York City or Washington? ").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("Hmm.. That's not quite right. Please enter Chicago, New York City or Washington")

    # Get user input for month (all, january, february, ... , june)
    while True:
        global month
        month = input("\nWould you like to filter by month? (y or n) ").lower()
        if month == 'y':
            month = input("Please enter Jan, Feb or Mar etc: ").lower()
            if month in ('jan', 'feb', 'mar', 'apr', 'may', 'jun'):
                break
            else:
                print("That's not quite right. Please enter Jan, Feb, Mar, Apr, Jun, Jul, Aug, Sep, Oct, Nov or Dec")
        elif month == 'n':
            break
        else:
            print("That's not quite right. Please enter y or n :")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        global day
        day = input("\nWould you like to filter by day? (y or n) ").lower()
        if day == 'y':
            chosen_day = input("Please enter Mon, Tue or Wed etc: ").lower()
            if chosen_day in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
                break
            else:
                print("That's not quite right. Please enter Mon, Tue, Wed, Thu, Fri, Sat or Sun :")
        elif day == 'n':
            break
        else:
            print("That's not quite right. Please enter y or n :")

    print("\nYou selected ", [city])

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "n" to apply no month filter
        (str) day - name of the day of week to filter by, or "n" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city]).dropna()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'n':
        # Use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'n':

        # Filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    df['month'] = df['Start Time'].dt.month
    print("The most common month is ", df['month'].mode())

    # Display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    print("The most common day of the week is ", df['day_of_week'].mode())

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most popular starting is hour is", df['hour'].mode())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode())

    # Display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode())

    # Display most frequent combination of start station and end station trip
    print("The most frequent combination of stations are", df[['Start Station', 'End Station']].mode().loc[1: 2])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("The total travel time for all trips in city database is", df['Trip Duration'].count(), "minutes")

    # Display mean travel time
    print("The average travel time is", df['Trip Duration'].mean(), "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    while True:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

    # Display counts of user types
        print("Number of user types:")
        user_types = df['User Type'].value_counts()
        print(user_types)

        if city == 'washington':
            break
        else:
    # Display counts of gender
            gender = df['Gender'].value_counts()
            print(gender)

    # Display earliest, most recent, and most common year of birth
            print("The earliest year of birth provided is :", int(df['Birth Year'].min()))
            print("The most recent year of birth is :", int(df['Birth Year'].max()))
            print("The most common year of birth is :", int(df['Birth Year'].mode()))

            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw = input('Would you like to see raw data? Please enter y or n :').lower()
        n = 0
        if raw != 'y':
            break
        else:
            n+=5
            print(df.head(n))
            more = input('Would you like to see more? Please enter y or n :').lower()
            while more == 'y' and n < df.shape[0]:
                n+=5
                print(df.head(n))
                more = input('Would you like to see more? Please enter y or n :').lower()


        restart = input('\nWould you like to restart? Please enter y or n :\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
