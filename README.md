# MyMoney

I have a spending problem.

This website does not solve it however it makes allows me to see it better.

## What it does
- Uploads Commonwealth bank transactions csv's. You can easily download them from clicking one of your accounts and specifying a data range.
- Displays a calendar with the total amount of money spent on each day. 
- Lists transactions when hovering over day.

## What it looks like
![mymoney_example_image](https://user-images.githubusercontent.com/22492590/129470482-e840cc19-e813-4aec-bff3-b92241ed1f49.png)


## Quick start

This project uses [poetry](https://python-poetry.org/).
So install poetry and have python^3.8 available.

Run these commands in the root directory:
```shell
poetry shell
```
```shell
poetry install
```
```shell
uvicorn main:app
```

## Possible features
I feel you can get very creative with this data
- Bank transaction classification. This will allow a display of the percentage of money spent in 
categories like groceries, entertainment, bills, etc. Its a well studied problem
and would be solvable using something like scikit-learn - although may require 
manual classification...
- Extract information from transaction string to display more informative content. Eg extract nouns,
card number used etc.
- Displaying transactions on a map to get a geographical sense of your purchases. 
- Identifying regular transactions.
- Cross comparing transactions between two selected dates. eg. line graph comparing the spend between
2 weeks or something
- Answer some questions:
  - how much did I spend at the pub on Friday night?
  - did my friend ever pay me back?
  - is my spending inline with my budget?



## Limitations
- Because banks dont have public API's to use this your forced to first download data from your bank and
then upload here.
- This is sensitive data. Making this site live would involve require good security practices and 
a lot of effort.

