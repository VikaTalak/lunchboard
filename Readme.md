# Lunchboard [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/amaier-um/lunchboard/main/lunchboard.py)


A streamlit app showing a map of lunch places around the office.

## Installation

First install `pipenv`

    $ pip install pipenv

Then you can use pipenv to install all the necessary python dependencies

    $ pipenv install

After this you need to preprocess the data before you can start the lunchboard

    $ pipenv shell
    $ python preprocess.py

## Start 
To start the lunchboard do

    $ pipenv shell
    $ streamlit run lunchboard.py

    You can now view your Streamlit app in your browser.
    
    Local URL: http://localhost:8501
    Network URL: http://192.168.2.6:8501



