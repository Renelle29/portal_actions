FROM jupyter/minimal-notebook

USER root

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

# Install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.29.1-linux64.tar.gz
RUN mv geckodriver /usr/local/bin/

USER $NB_UID
