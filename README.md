# Omega Slackbot

This project is meant to be a full framework for a slack bot interface.

This is being coded as modularly as possible, to allow for 'plugins' or 'modules' to extend functionality.

## Prerequisites

The base installation of Omega Slackbot requires the following non-python module programs are installed and running:

### Database

Currently, Omega Slackbot requires [PostgreSQL](https://www.postgresql.org) is available for use. This database is used for event logging and file storage.

TODO: plugins to allow for different database types

### Python Dependencies

All dependencies should be handled when installing from the requirements.txt file. If you prefer to install manually:

+ [pyYAML](https://pypi.org/project/PyYAML/) required for Omega Slackbot's configuration module
+ [requests](https://pypi.org/project/requests/) handle file downloads from slack
+ [slack-bolt](https://pypi.org/project/slack-bolt/) slack api access
+ [psycopg2](https://pypi.org/project/psycopg2/) postgres database

---

+ [PyMuPDF](https://pypi.org/project/PyMuPDF/) required by Omega Slackbot's Parsefile module
+ [pandas](https://pypi.org/project/pandas/) required by Omega Slackbot's Parsefile module
+ [tabulate](https://pypi.org/project/tabulate/) required by Omega Slackbot's Parsefile module
+ [cryptography](https://pypi.org/project/cryptography/) required by Omega Slackbot's Parsefile module

## Installation

### Create a virtual python environment

Development branch is using 3.12.2

```bash
python -m venv .venv
```

### Activate virtual environment

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create configuration file

Copy config-example.yml to config.yml

```bash
cp config-example.yml config.yml
```

edit config.yml:

+ input and output directory paths
+ database information
+ your slack tokens (bot, api)

## Running the bot

The Slack bot can be run manually or via a systemd service (to keep running after restarts or network restarts)

### Manual running

Simply run the python script:

```bash
python omega-slackbot.py
```

### Systemd service

#### Create a systemd service file for the bot

Edit the omega-slackbot.service file
Copy the file to `/etc/systemd/system`

```bash
cp omega-slackbot.service /etc/systemd/system
```

#### Enable and run the systemd service

```bash
sudo systemctl enable omega-slackbot.service
sudo systemctl start omega-slackbot.service
```

The status of the bot can be checked with

```bash
sudo systemctl status omega-slackbot
```

The log files of each bot can be checked with

```bash
sudo journalctl -u omega-slackbot
```

To STOP the running bot process

```bash
sudo systemctl stop omega-slackbot
```

To DISABLE to bot

```bash
sudo systemctl disable omega-slackbot
```

## TODO

[ ] Better modular / plugin system

+ mostly there

[ ] Plugin development documentation
[ ] Plugin master list

## Pull Requests

Pull requests are welcome. Feel free to grab something off of the TODO list.
