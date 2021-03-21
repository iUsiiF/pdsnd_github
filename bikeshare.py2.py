import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    month = 'all'
    day= 'all'
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington? \n')
        city.lower()
        if city in CITY_DATA:
            break
            
    while True:
        choice = input('Would you like to filter the data by month, day, or none? \n').lower()
        if choice in ('month','day','none'):
            break
            
    if choice.lower()== 'month':
        while True:
            month = input('Which month - January, February, March, April, May, or June? \n')
            month.lower()
            if month in ('january','february','march','april','may'):
                break
        
    elif choice.lower()== 'day':
        while True:   
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n')
            day.lower()
            if day in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
                break



    


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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print('FileNotFoundError')
        return

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] +' ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print ('Most common month:',common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print ('Most common day of week:',common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print ('The most common start hour:',common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_ss= df['Start Station'].mode()[0]
    print('Most commonly used start station:',common_ss)
     

    # display most commonly used end station
    common_es = df['End Station'].mode()[0]
    print('Most commonly used end station:',common_es)
    # display most frequent combination of start station and end station trip
    mfc = df['trip'].mode()[0]
    print ('Most frequent combination of start station and end station trip:', mfc)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time:', total_travel)

    # display mean travel time
    mean_tt = df['Trip Duration'].mean()
    print('Average travel time',mean_tt )
   


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_type = df['User Type'].value_counts()
    print ('Counts of user types:', counts_type)

    # Display counts of gender
    if city != 'washington':
        counts_of_gender = df['Gender'].value_counts()
        print('Counts of gender:',counts_of_gender)
        earliest = df['Birth Year'].min()
        print('Earliest year of birth: ', earliest)
        recent = df['Birth Year'].max()
        print('Most recent year of birth: ', recent)
        common_year = df['Birth Year'].mode()[0]
        print('Earliest year of birth: ', common_year)

        

    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while True:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ")
        if view_data.lower() != 'yes':
            break

                              

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df:

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            display_data(df)
        

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart in ('yes', 'no'):
                break
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()