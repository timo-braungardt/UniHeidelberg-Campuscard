# UniHeidelberg-Campuscard
A webscraper for the campuscard website of uni heidelberg. It scrapes all of your transactions made with the campus card.  
This is necessary because the export function is broken.

## Usage
To fetch the data from the website you need to add fetch to the call. With `-s` or `--save` you can save the data to your local storage.  
Fetch will ask you for your username and password for the [campuscard-website](https://campuscard.stw.uni-heidelberg.de/).
```
python scrape.py fetch -s
```
If you saved your data to the local storage, you can load it and recalculate the statistics with load.
```
python scrape.py load
```
