# LoanX Calculator

LoanX is a student loan payment calculator developed with Python that also creates an amortization schedule to help borrowers see monthly payment breakdowns. Designed using the Flask web framework, the calculator web application implements a dynamic table with Python’s NumPy and Pandas libraries to visualize the schedule data. 

Borrowers can also explore how to reach their debt-free goals quicker! Through its "Explore" feature, LoanX offers an overview of the duration of years and months it will take to pay off a loan when increasing the monthly payment amount. Borrowers can simply add an additional payment to see faster loan repayment outcomes.

## Table of Contents

* [Installation](https://github.com/t-mcneal/loanx/blob/master/README.md#installation)
* [Usage](https://github.com/t-mcneal/loanx/blob/master/README.md#usage)
* [Website](https://github.com/t-mcneal/loanx/blob/master/README.md#website)

## Installation

1. **Install Python 3**

    If not currently installed on your computer, download and install [Python 3](https://www.python.org/downloads/).

2. **Download Project**

    Download a zip of the LoanX Calculator project from GitHub or clone the repository.

3. **Create a Virtual Environment**

    It is best to locally run a Flask application using a virtual environment. To get setup with a virtual 
    environment, follow the quick [guide](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) 
    on the Flask website, which has instructions for both Windows and Mac OS X. The guide will walk you through 
    how to create a virtual environment within the project directory and install Flask in the environment. 
    
    >> **Note:** The Flask guide uses the command line. If you are not familiar with terminal commands, read this 
    >> [blog](https://scotch.io/bar-talk/10-need-to-know-mac-terminal-commands) by scotch.io to learn 10 commonly
    >> used terminal commands - #10 is a fun one!

    Once you have created the virtual environment, start the environment via the command line, then enter the following command line syntax to install project requirements.
    
    ```
    $ pip install -U flask-cors
    $ pip install numpy
    $ pip install pandas
    $ pip install typing-extensions
    ``` 
    
## Usage

Next, you will need to run the LoanX Flask application in your newly created virtual environment.
Once you have enabled the virtual environment and installed the requirements, you can now run the 
app to start a local server using the following command line syntax.

```
$ export FLASK_APP=loanx
$ export FLASK_ENV=development
$ flask run
```

This step enables the development environment, including the interactive debugger and reloader, and then starts the server on `http://localhost:5000/`. Copy the server link from the command line, then place it in your browser to access the LoanX Calculator web app.

## Website

Click this [link](https://loanxcalculator.herokuapp.com/) to visit the LoanX Calculator website, which is deployed to Heroku. 

![LoanX Screenshot](https://github.com/t-mcneal/loanx/blob/master/readme_images/loanx_screenshot.png)