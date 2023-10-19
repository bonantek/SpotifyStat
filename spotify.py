import pandas as pd
import matplotlib.pyplot as plt
import os

path = 'MyData'


def ms_to_min(ms_played):
    minutes = (ms_played / (1000 * 60)) % 60
    return minutes


def ms_to_hours(ms):
    hour = ms / (1000 * 60 * 60)
    return hour


def get_files_with_data(files: list) -> list:
    target_files = [file for file in files if "History" in file]
    return target_files


def create_df(files: list):
    df = pd.concat(pd.read_json(f'{path}\\{file}') for file in files).set_index('endTime')
    df.index = pd.to_datetime(df.index)
    df.insert(3, "minutes", df['msPlayed'].apply(ms_to_min))
    df.insert(4, "hours", df['msPlayed'].apply(ms_to_hours))
    return df


def most_listened_artists(df):
    # top 10:
    artists = df.groupby('artistName')[['hours', 'trackName']].agg({'hours': 'sum', "trackName": "count"})
    artists['hours'] = artists['hours'].round(3)
    artists = artists.rename(columns={'hours': 'Listening Hours', 'trackName': "Numbers of Streams"})
    artists.sort_values(['Listening Hours', "Numbers of Streams"], ascending=False, inplace=True)
    plt.style.use("fivethirtyeight")
    plot = artists.head(15).plot(kind='bar', secondary_y='Numbers of Streams')
    plot.set_xlabel("Artist")
    plot.set_ylabel("Listening Hours")
    plot.right_ax.set_ylabel("Number of Streams")
    plt.title('Most Listened Artists')

    plt.show()


def most_listened_tracks(df):
    best_tracks = df.groupby('trackName')['minutes'].agg(['sum', 'count']).rename(
        columns={'sum': 'Minutes Played', 'count': 'Number of Streams'})
    best_tracks.sort_values(['Minutes Played', 'Number of Streams'], ascending=False, inplace=True)
    plt.style.use('ggplot')
    plot = best_tracks.head(10).plot(kind='bar', secondary_y='Minutes Played')
    plot.set_ylabel("Number of Streams")
    plot.set_xlabel("Name of Song")
    plot.right_ax.set_ylabel("Minutes of Stream")
    plt.show()


def avg_number_of_streams_per_day(df):
    weekdays = {0: "Monday",
                1: "Tuesday",
                2: "Wednesday",
                3: "Thursday",
                4: "Friday",
                5: "Saturday",
                6: "Sunday"}
    firts_record = df.index[0]
    last_record = df.index[-1]
    dates = pd.date_range(start=firts_record, end=last_record)
    wdays_series = pd.Series(dates.weekday.value_counts())
    wdays_series.index = wdays_series.index.map(weekdays)
    wdays_series = wdays_series.reindex(weekdays.values())
    to_divide = df.groupby(df.index.strftime('%A'))['trackName'].count()
    avg_no_of_stream = to_divide.div(wdays_series)
    avg_no_of_stream.plot.pie(title="Average Numbers of Streams Per Day", autopct='%1.0f%%')
    plt.show()


def main(df):
    most_listened_artists(df)
    #
    most_listened_tracks(df)
    avg_number_of_streams_per_day(df)


if __name__ == "__main__":
    print("App will be done soon!")
    files_with_streaming_history = get_files_with_data(os.listdir(path))
    df = create_df(files_with_streaming_history)
    main(df)
