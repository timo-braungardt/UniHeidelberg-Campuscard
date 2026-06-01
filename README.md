# UniHeidelberg-Campuscard
A webscraper for the campuscard website of uni heidelberg. It scrapes all of your transactions made with the campus card.  
This is necessary because the export function is broken.

## Account
For this script to work, you need an account at the studierendenwerk [campuscard-website](https://campuscard.stw.uni-heidelberg.de/).

> [!WARNING]
> This is not your uni-id but a different account!

The script can also use your keepass file so you dont need to recall your password.
Simply fill in the `PATH_TO_KEEPASS_FILE` path variable with the global path.
It will search for a entry with the url `https://campuscard.stw.uni-heidelberg.de/`.

## Usage
To get the current balance of your card, run
```
python scrape.py balance
```
To fetch your old data from the website you run fetch. With `-s` or `--save` you can save the data to your local storage.  
```
python scrape.py fetch -s
```
If you saved your data to the local storage, you can load it and recalculate the statistics with load.
```
python scrape.py load
```

### creating a venv
To create a virtual environment, go to this repository directory and type in `python3 -m venv .venv`.  
After that, you can run `source .venv/bin/activate` and install all required packages with `pip install -r requirements.txt`

### putting it on PATH
Add this to your `.bashrc` to create a alias:
```bash
scrape() {
 ~/<path_to_project>/.venv/bin/python3 ~/<path_to_project>/scrape.py "$@";
}
```
After reloading the `.bashrc` you can call it with `scrape`.