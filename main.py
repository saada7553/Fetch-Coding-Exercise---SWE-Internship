import pandas as pd
import sys
import json


'''
 Dictionary which stores the total number of points for each payer
 Key: Name of the payer
 Value: Total points the payer has contributed
'''
all_payer_points = {}


def build_initial_data_frame(csv_name: str):
    """
    This function takes the original CSV file and calculates the amount of points
    each payer has before any points are spent. It stores this data in a dictionary
    called all_payer_points.

    :param csv_name: The name of the CSV file which is read from
    :return: This dataframe is the CSV file as a pandas dataframe
    """

    data_frame = pd.read_csv(csv_name)

    # Iterate over each row in the data frame
    for index, row in data_frame.iterrows():
        # Payer of the current row
        curr_payer = row['payer']
        # Points the current payer contributed
        curr_points = row['points']
        # If the payer already exists in the payer_points dictionary,
        # points are incremented accordingly.
        if curr_payer in all_payer_points:
            all_payer_points[curr_payer] += curr_points
        # If player does not exist, a new entry is made in the dictionary
        else:
            all_payer_points[curr_payer] = curr_points

    return data_frame


def sort_data_frame(data_frame):
    """
    This function sorts the inputted data frame according to the timestamp.
    This is done in  oldest-first order

    :param data_frame: An unsorted pandas data frame
    :return: A sorted version of the inputted data_frame
    """

    # Convert timestamp to pandas datetime object
    data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'])
    # Use datetime object to sort dataframe
    data_frame = data_frame.sort_values('timestamp')

    return data_frame


def spend_points(points: int, data_frame):
    """
    This function takes the sorted data frame, and spends the points.

    :param points: The number of points that need to be spent
    :param data_frame: Contains the payers and points in sorted order
    """

    # Iterate over rows in the data frame, iterated from oldest to newest transaction
    for index, row in data_frame.iterrows():
        # The current number of total points the current payer has
        curr_payer_total_points = all_payer_points[row['payer']]
        # The number of points the current payer contributed in the current row
        curr_payer_oldest_points = row['points']

        # Make sure that negative values are not possible
        if points >= curr_payer_oldest_points and curr_payer_total_points >= curr_payer_oldest_points:
            points -= curr_payer_oldest_points
            all_payer_points[row['payer']] -= curr_payer_oldest_points
        # If current oldest can pay off all points, we do that
        else:
            all_payer_points[row['payer']] -= points
            points = 0

        if points == 0:
            break


def build_json_response():
    """
    This function takes the payer_points dictionary and converts it into
    a JSON object.

    :return: JSON version of the payer_points
    """
    response = json.dumps(all_payer_points, indent=4)
    return response


def main():
    """
    This function runs all the helper functions in the correct order
    """

    # Collect points to spend and file name from command line
    points_to_spend = int(sys.argv[1])
    file_name = str(sys.argv[2])

    # Build the initial data frame
    initial_data_frame = build_initial_data_frame(file_name)
    # Sort the initial data frame
    sorted_data_frame = sort_data_frame(initial_data_frame)
    # Spend points based on the sorted data frame
    spend_points(points_to_spend, sorted_data_frame)
    print(build_json_response())


main()
