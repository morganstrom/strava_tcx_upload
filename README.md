# Strava TCX Upload

Streamlit app for uploading TCX files exported from Google Fit to Strava.

## Usage

1. Export your Google Fit data from [Google Takeout](https://takeout.google.com/settings/takeout) as a zip file.
2. Unzip the file and place the `Takeout/Fit/Activities` folder where you can find it later.
3. Run `make install` to install the dependencies and set up the virtual environment.
4. Run `pipenv shell` to activate the virtual environment.
5. Run the app with `make run` and open [this link](http://localhost:8501) in your browser.
6. Authenticate with Strava by clicking the button "Authenticate with Strava"
7. Select the activities you want to upload to Strava and click "Upload to Strava"
8. Profit

## Development

Run `make install-dev` to install the development dependencies and set up the virtual environment.

Run `make test` to run unit tests.

## Prerequisites

[Strava API credentials](https://www.strava.com/settings/api) saved in the `credentials.py` script
    
```
CLIENT_ID = <INSERT ID>
CLIENT_SECRET = <INSERT SECRET>
```