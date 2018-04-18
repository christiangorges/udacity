import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ["january", "february", "march", "april", "may", "june"]
DAY_LIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

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
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city == "new york":
            city = "new york city"
        if city in CITY_DATA:
            break
        else:
            print('Uphs! Wrong input! Try again!\n')


    # defaults
    month = "all"
    day = "all"

    while True:
        choice = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
        if choice in ["month", "day", "both", "none"]:
            break
        else:
            print('Uphs! Wrong input! Try again!\n')

    if choice == "month":
        while True:
            month = input('Which month? January, February, March, April, May, or June?\n').lower()
            if month in MONTH_LIST:
                break
            else:
                print('Uphs! Wrong input! Try again!\n')

    elif choice == "day":
        while True:
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            if day in DAY_LIST:
                break
            else:
                print('Uphs! Wrong input! Try again!\n')

    elif choice == "both":
        while True:
            month = input('Which month? January, February, March, April, May, or June?\n').lower()
            if month in MONTH_LIST:
                break
            else:
                print('Uphs! Wrong input! Try again!\n')

        while True:
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            if day in DAY_LIST:
                break
            else:
                print('Uphs! Wrong input! Try again!\n')


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week, and start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_LIST.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df = df[df['day_of_week'] == day.title()]

    # uncomment for testing
    print(df.head())
    print(df.info())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', MONTH_LIST[popular_month-1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().reset_index(name='counts').sort_values(by='counts',ascending=False).iloc[0]
    #print(popular_combination)
    print('Most Popular Combination is from {} to {} ({} times)'.format(popular_combination.loc["Start Station"],popular_combination.loc["End Station"],popular_combination.loc["counts"]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = df['Trip Duration'].sum()
    #print(total_time_sec)
    total_time_hour = int(total_time_sec//3600)
    total_time_min = int((total_time_sec%3600)//60)
    total_time_sec = int((total_time_sec%3600)%60)
    print('Total Travel Time: {} hour(s), {} minute(s), {} second(s)'.format(total_time_hour,total_time_min,total_time_sec))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    avg_time_hour = int(avg_time//3600)
    avg_time_min = int((avg_time%3600)//60)
    avg_time_sec = int((avg_time%3600)%60)
    print('Average Travel Time: {} hour(s), {} minute(s), {} second(s)'.format(avg_time_hour,avg_time_min,avg_time_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types: {} Subscriber(s), {} Customer(s)'.format(user_types["Subscriber"],user_types["Customer"]))

    if city in ["chicago","new york city"]:
        # Display counts of gender
        user_gender = df['Gender'].value_counts()
        print('Counts of Gender: {} Female(s), {} Male(s)'.format(user_gender["Female"],user_gender["Male"]))

        # Display earliest, most recent, and most common year of birth
        user_birth_earliest = int(df['Birth Year'].min())
        print('Earliest Birth:', user_birth_earliest)
        user_birth_most_recent = int(df['Birth Year'].max())
        print('Most Recent Birth:', user_birth_most_recent)
        user_birth_most_common = int(df['Birth Year'].mode()[0])
        print('Most Common Birth:', user_birth_most_common)

    else:
        print('No Gender and Birth Data available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
