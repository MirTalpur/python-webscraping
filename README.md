# Overview
I used a lot of different libraries for this project. The requirments for it are given in a requirments.txt file. 
Creating a virtualenv out of the requirments.txt is the best way to go about running the project.

# Pre-reqs
### Selenium WebDriver for FireFox
I had to download the geckodriver in order for me to use the Selenium FireFox driver. 
Every OS is different in how to setup a Selenium webdriver to use. 
Installation of the Selenium FireFox driver is really simple. Here is the https://github.com/mozilla/geckodriver/releases driver
I used for linux. But every OS different installation steps
### Virtualenv
Is an virtual environment which will let configure different python projects easily and manage dependencies much simpler.
### Install pip
Pip is a package management system used to install and manage software packages, such as those found in the Python Package Index

# Setup
## Create a virtualenv
```virtualenv <name>```

### Start using the virtualenv
```source <name>/bin/activate```

## Install a virtualenv with requirments
```pip install -r requirements.txt```

## Run the metadata.py script
`python metadata.py`

# Strategy To Solve
So essentially use selenium to get to where u want to go on the browser at least for the March 2010 link (this was ignored later on just to 
save some time for whoever runs the project). Than in order to retrieve the data needed use lxml for the parsing and content in
tree form.

# Special Note
I used selenium to navigate to needed urls and interact with the webpage on the first March 2010 link. After that I stopped using it
just so it can save sometime and directly got to the data required from the pages using `requests.get(URL)`

This could be more modularized and created as a seperate class however, this might be overkill for now but might be a nice to have later.
Also this can use DRY(Don't repeat yourself)
