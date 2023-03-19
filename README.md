# Cryptocurrency Data Aggregator

This project retrieves real-time data related to different cryptocurrencies, tokens, and fiats from the Cryptofolio API and sends it to a Google Spreadsheet. The Google Spreadsheet serves as a centralized repository for all the data retrieved from the Cryptofolio API, and provides users with a convenient way to analyze trends, compare different assets, and make informed decisions about their investments.

# Getting Started

To get started with this project, you will need to have a few prerequisites installed on your system. These include:

Python 3.7 or later
Pip package manager
Google Cloud Console account

Once you have these prerequisites installed, you can proceed with the following steps:

- Clone this repository to your local machine using git clone
- Create a virtual environment and activate it using python3 -m venv venv and source venv/bin/activate
- Install the required packages using pip install -r requirements.txt
- Configure your Google Cloud Console account by following the instructions in the Google Sheets API documentation
- Run the main.py script using python main.py
- The main.py script will retrieve data from the Cryptofolio API and send it to a Google Spreadsheet.
