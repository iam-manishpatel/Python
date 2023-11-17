# This script aims to automate the identification of trading signals
# #based on a Supertrend strategy, providing a summary of Buy and Sell
# decisions with associated prices and times.

import os

import pandas as pd

# Get input file path from the user
input_file = input("Enter the full path of the input Excel file: ")

# Validate if the file exists
if not os.path.isfile(input_file):
    print("File not found. Please provide a valid file path.")
    exit()

# Get user input for the start time in hh:mm:ss format
start_time = input("Enter the Start time for signal processing (hh:mm:ss) [default: 09:30:00]: ") or '09:30:00'

# Get user input for the end time in hh:mm:ss format
end_time = input("Enter the End time for signal processing (hh:mm:ss) [default: 15:15:00]: ") or '15:15:00'

# Derive the temp file name with a prefix
temp_file = "temp_" + os.path.basename(input_file)
temp_file = os.path.join(os.path.dirname(input_file), temp_file)

# Derive the output file name with a prefix
new_file = "updated_" + os.path.basename(input_file)
new_file = os.path.join(os.path.dirname(input_file), new_file)

# Read the Excel file
df = pd.read_excel(input_file)

# Extract date and time components from the 'Date' column
df['Date'] = pd.to_datetime(df['Date'].str[:24], format='%a %b %d %Y %H:%M:%S')

# Extract the date and time into separate columns
df['Date_only'] = df['Date'].dt.date
df['Time_only'] = df['Date'].dt.time

# Display the updated DataFrame

# Save the updated DataFrame to a new Excel file if needed
df.to_excel(temp_file, index=False)


# Read the 'temp.xlsx' file
df = pd.read_excel(temp_file)

# Initialize variables
result = []

# Iterate through unique dates
for date in df['Date_only'].unique():
    date_df = df[df['Date_only'] == date].reset_index(drop=True)

    BuySell = None
    Buy = None
    Sell = None
    Type = None

    # Iterate through the records for the current date
    i = 1
    while i < len(date_df):
        current_record = date_df.iloc[i]
        previous_record = date_df.iloc[i - 1]

        if current_record['Time_only'] == end_time:
            break  # Stop processing for the current date at 15:15:00

        if current_record['Time_only'] == start_time:
            if current_record['Supertrend'] > previous_record['Close']:
                BuySell = 'Sell'
                Type = 'Sell'
                Time = current_record['Time_only']
                Sell = previous_record['Close']
                # Look for the next record meeting the condition
                next_index = i + 1
                while next_index < len(date_df):
                    next_record = date_df.iloc[next_index]
                    previous_next_record = date_df.iloc[next_index - 1]

                    if next_record['Time_only'] == end_time or (
                            next_record['Supertrend'] < previous_next_record['Close']):
                        Buy = previous_next_record['Close']
                        result.append([date, Time, Type, Buy, Sell])
                        break
                    next_index += 1
                i = next_index  # Skip to the next iteration of the outer loop

            elif current_record['Supertrend'] < previous_record['Close']:
                BuySell = 'Buy'
                Type = 'Buy'
                Time = current_record['Time_only']
                Buy = previous_record['Close']
                # Look for the next record meeting the condition
                next_index = i + 1
                while next_index < len(date_df):
                    next_record = date_df.iloc[next_index]
                    previous_next_record = date_df.iloc[next_index - 1]
                    if next_record['Time_only'] == end_time or (
                            next_record['Supertrend'] > previous_next_record['Close']):
                        Sell = previous_next_record['Close']
                        result.append([date, Time, Type, Buy, Sell])
                        break
                    next_index += 1
                i = next_index  # Skip to the next iteration of the outer loop


        elif BuySell == 'Sell' and current_record['Supertrend'] < previous_record['Close']:
            BuySell = 'Buy'
            Type = 'Buy'
            Time = current_record['Time_only']
            Buy = previous_record['Close']
            # Look for the next record meeting the condition
            next_index = i + 1
            while next_index < len(date_df):
                next_record = date_df.iloc[next_index]
                previous_next_record = date_df.iloc[next_index - 1]
                if next_record['Time_only'] == end_time or (
                        next_record['Supertrend'] > previous_next_record['Close']):
                    Sell = previous_next_record['Close']
                    result.append([date, Time, Type, Buy, Sell])
                    break
                next_index += 1
            i = next_index  # Skip to the next iteration of the outer loop


        elif BuySell == 'Buy' and current_record['Supertrend'] > previous_record['Close']:
            BuySell = 'Sell'
            Type = 'Sell'
            Time = current_record['Time_only']
            Sell = previous_record['Close']
            # Look for the next record meeting the condition
            next_index = i + 1
            while next_index < len(date_df):
                next_record = date_df.iloc[next_index]
                previous_next_record = date_df.iloc[next_index - 1]
                if next_record['Time_only'] == end_time or (
                        next_record['Supertrend'] < previous_next_record['Close']):
                    Buy = previous_next_record['Close']
                    result.append([date, Time, Type, Buy, Sell])
                    break
                next_index += 1
            i = next_index  # Skip to the next iteration of the outer loop

        i += 1  # Move to the next record if none of the conditions are met


# Create a new DataFrame from the result list
result_df = pd.DataFrame(result, columns=['Date', 'Time', 'Type', 'Buy', 'Sell'])

# Print or save the result DataFrame as needed
print(result_df)
result_df.to_excel(new_file, index=False)
# Replace 'output_file.xlsx' with your desired output file name

# Remove the temporary file after processing
os.remove(temp_file)