# Strava TCX Upload

Streamlit app for uploading TCX files exported from Google Fit to Strava.

## Usage

1. Export your Google Fit data from [Google Takeout](https://takeout.google.com/settings/takeout) as a zip file.
2. Unzip the file 
3. Run the app with `PYTHONPATH=. streamlit run main.py`
4. Authenticate with Strava by clicking the button "Authenticate with Strava"
5. Select the activities you want to upload to Strava and click "Upload to Strava"
6. Profit