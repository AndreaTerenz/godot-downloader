# godot-downloader

A simple python script to quickly download the latest version of the Godot Game Engine, controlled through a CLI. It asks the user whether it should download the latest *stable* or *beta* release and memorizes the last one it downloaded so that it can alert the user of a potentially "useless" download

## Requirements

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) is used to parse webpages and extract the url of the file to be downloaded, while [PyColorText](https://github.com/roshanlam/PyCTlink) is used to embelish the UI

## Installation

Simply clone the repo and launch the script with `python godot_downloader.py`

## To-Do

- Add possibility to download a specific version or a specific beta of it
