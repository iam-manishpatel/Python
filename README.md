# Supertrade Signal Processor

This Python program aims to automate the identification of trading signals based on a Supertrend strategy, providing a summary of Buy and Sell decisions with associated prices and times.

It is designed for financial signal processing on time-series data in an Excel file. Here's a short overview:

# Overview: Supertrade Signal Processor

User Input:

Takes user input for the path of an input Excel file containing financial data.
Prompts the user to specify start and end times for signal processing.
File Validation:

Checks if the input file exists. Exits if not, with an error message.
Data Processing:

Reads the Excel file into a Pandas DataFrame.
Extracts date and time components from the 'Date' column.
Signal Processing:

Identifies buying and selling signals based on the 'Supertrend' column values.
Processes data to determine Buy and Sell signals, along with corresponding prices and times.
Result DataFrame:

Creates a new DataFrame with columns 'Date', 'Time', 'Type', 'Buy', and 'Sell' to store the processed results.
Output:

Prints the result DataFrame.
Saves the result DataFrame to a new Excel file with a prefix 'updated_'.

Assumptions:
Assumes the existence of columns like 'Date', 'Time', 'Supertrend', and 'Close' in the input Excel file.
