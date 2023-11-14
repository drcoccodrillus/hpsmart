# HP Smart

HP Smart is a Python application that allows you to send print jobs to HP printers that support ePrint. This application is useful in scenarios where you need to send print jobs to a remote printer.

***

## Before using it

Before using this application you need to make sure that you have a HP printer that supports ePrint, connected to the internet and registered at [HP Smart](https://www.hpsmart.com)

This app uses tkinter to display the GUI.

If you are a Windows user you don't need to install anything.

If you are using a Linux distribution you need to install the tkinter package.

If you are using a Debian based distribution you can install them by running the following command:

`sudo apt install python3-tk`

If you are using a Fedora based distribution you can install them by running the following command:

`sudo dnf install python3-tkinter`

If you are using a Arch based distribution you can install them by running the following command:

`sudo pacman -S tk`

If you are using a MacOS distribution you can install them by running the following command:

`brew install python-tk`

## How to use it

Using this app is  is very simple. You just need to download the latest release and run it.

Through the GUI you can select the PDF file you want to print and send it to your printer.

## How to configure it

Before using this app you need to configure it. You can do it by editing the config.json file.

The config.json file is structured as follows:

```json
{
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "smtp_username": "crocodile@river.com",
    "smtp_password": "1l0v3cr0c0d1l3",
    "sender_email": "crocodile@river.com",
    "allowed_domain": "hpeprint.com",
    "default_printer_email": "crocoprinter@hpeprint.com"
}
```

- smtp_server: the smtp server of your email provider
- smtp_port: the smtp port of your email provider
- smtp_username: the username of your email account
- smtp_password: the password of your email account
- sender_email: the email address of your email account
- allowed_domain: the hpsmart domain of your printer
- default_printer_email: the email address of your printer

You can also use the gui to configure the app. You just need to click on the Change Config button and fill the form.

## Run from source code

If you want to run the app from the source code you can clone the repository by running the following command:

`git clone git@github.com:drcoccodrillus/hpsmart.git`

Finally you can run the app by running the following command:

`python3 hpsmart.py`

## Disclaimer
This app is not affiliated with HP in any way.