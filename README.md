# PyBot
Innopolis Library Management System implemented via Telegram Bot Api

## Purpose of Bot:
Bot is developed for Library use.

## Dependencies:
*python
*pyTelegramBotAPI
*pyodbc
*Microsoft Azure

## Installation:
#### Requirements:
1. python3
2. pip3
3. git
4. python IDE

#### Preparing:
1.  Install all libraries stated in the requirements.txt by typing the command below in command line.

      ``` pip3 install -r requirements.txt ```

2.  Install Microsoft Azure drivers [link](https://www.microsoft.com/en-us/download/details.aspx?id=53339)
3.  Download repository from [GitHub](https://github.com/homycdev/PyBot)

## Running:
To run the application with default parameters just typing the command below in command line.

      ``` python3 telebot2.py ```


# DOCUMENTATION:
## Authentication
Authentication need if user open bot first time, after it checking for system including will happen automatically. For first run bot asking user to write his e-mail in @innopolis domain, other cases will not be valid. In this step, system checks that e-mail, to know, who is this user: Faculty member or Student. Bot send pin code to users e-mail, and user need to verify it. After this step user need to give for bot personal information: name, number and address, after it registration in completed.

## Faculties base:
Base, which contain Faculties e-mail, for checking user belonging to Faculty

## Utilities:
Contain some strings for authentication interface, also have some objects such documents and users, for testing. 

## Documents and Users:
OOP representation for classes, need to link all fields in and from database

## Booking:
Method|Description
------|-----------
 booking(usr,document,time)| booking method which call order_book, order_av, order_article methods depending on what kind of type document comes in
 order_book(usr,document,time)| makes a reservation of the book
 order_article(usr, document, time)| makes a reservation of the article
 order_av(usr,av,time)| makes a reservation of the av file
 add_to_queue(usr)| adds user to waiting list
 pop_from_queue(waiting_list)| pops a user from waiting list

