# Counting hours app / Interface for recording working hours in the company
Interface for recording working hours in the company. Every worker can make profile and use it for count working hours per month. Every day is saved to database and worker can access it every time. Worker can count how many money he earn for month.
Now i have my applicatin live on server. http://bulays.pythonanywhere.com/

# Features

-  In json file is saved every working day of year 2021. This data i scrape by bs4 from https://kalendar.beda.cz/ 
-  After user login in or make account he can use "counting hours" this mean if he save some day to database this day is no longer in choosefield. 
-  In "Actual month" user see every day he saved. He can click on day and update it or delete it. Below this days there is menu where he can count how mouch money he can get or if he work on holiday he can add it. 
-  In "History" user can search every already past month he want and if he missed day he can add it here.

# Venv

Create a virtualenv with `virtualenv env` and install dependencies with `pip install -r requirements.txt`

# Video preview

[<img src="https://cdn.freebiesupply.com/logos/large/2x/youtube-logo-png-transparent.png" width="" height="100">](https://youtu.be/3R52NHLcnzE)
