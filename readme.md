# MyMoney

I have a spending problem.

This app does not solve it however it makes allows me to see it better.

This app displays a calendar with the total amount of money spent on each day. Hovering over each day will
display the transactions.
In order to input data there is a form that will accept Commonwealth bank csvs. 

Its a lean FastAPI project with no database.

## Quick start
```shell
poetry shell
```
```shell
poetry install
```
```shell
uvicorn main:app
```

## What it looks like


## Possible future features
- Bank transaction classification. This will allow a display of the percentage of money spent in 
categories like groceries, entertainment, bills, etc.
- Extract information from transaction string to display more informative content. Eg extract nouns,
card number used etc.
- Displaying transactions on a map to get a geographical sense of your purchases. 
- Identifying regular transactions.
- Cross comparing transactions between two selected dates. eg. line graph comparing the spend between
2 weeks or something



## Limitations
- Because banks dont have public API's to use this your forced to first download data from your bank and
then upload here.
- This is sensitive data. Making this site live would involve strong security practices.

