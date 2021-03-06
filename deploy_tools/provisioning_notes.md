Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

e.g.,, on Ubuntu:

	sudo apt-get install nginx git python3 python3-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.example.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.example.com
* replace EMAIL_USER with email account user
* replace EMAIL_PASSWORD with email account password

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
	└── SITENAME
		├── database
		├── source
		├── static
		└── virtualenv
