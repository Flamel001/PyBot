# PyBot
Innopolis Library Management System implemented via Telegram Bot Api

###### Before using project you will be needed to download file config.py. To download it, you should contact one of the contributers.

## How it works:
![alt text](https://github.com/homycdev/PyBot/blob/master/workflow.png)

### Team members:
Abdulkhamid Muminov - @homycdev

Amadey Kuspakov - @AmadeyKuspakov

Nikita Kostenko - @Flamel001

Ramil Askarov - @Rome314

## Purpose of Bot:
Bot is developed for Library use.

## Dependencies:
* python
* pyTelegramBotAPI
* pyodbc
* Microsoft Azure

###### Note: all needed dependencies are in requirements.txt. They should be imported into your enviroment.

## Installation:
#### Requirements:
1. python3
2. pip3
3. git
4. python IDE

#### Preparing:
1.  Install all libraries stated in the requirements.txt by typing the command below in command line.

      ``` pip3 install -r requirements.txt ```

2.  Install Microsoft Azure [drivers](https://www.microsoft.com/en-us/download/details.aspx?id=53339)
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


## Main_bot.py:
Method|Description
------|-----------
greeting(message)| sends greetings message
admin(call)| let in to admins GUI
man_lib(call)| method that manages librarians
log(call)| returns log file
auth(call)| initializes authentification
pin_checker(call)| checks the pin, calls pin_checker.py
name(call)| relates to authentification, saves user name
number(call)| relates to authentification, saves user numb
address(call)| relates to authentification, saves user address
my_docs(call)| shows user's docs
reserve(call)| reserves a doc
return_doc(call)| returns a doc
tech_sup(call)| calls tech support
library(call)| gui of librarian
initialize_librarian(call)| initializes librarian
search_patron(call)| relates to search(call), searches patron through database
search_doc(call)| relates to search(call), searches doc
search(call)| searches everything
edit(call)| Edit button
editing(call)| enters parameter to edit
edited(call)| pops up a message that patron/doc edited
delete(call)| deletes patron/doc
add(call)| adds patron/doc
adding(call)| adds patron/doc
get_info(call)| pops up a message with detailed info of user/doc
back(call)| Back button
edit_attr(attr, new_attr, id)| main edit that does all background work
is_human(id)| checks user's type


## DataBase.py:
Method|Description
------|-----------
create_user_table()| creates a table of users in AzureDB
create_doc_table()| creates a table of docs
\__parse(dictionary)\__ | parsing formatted data
insert(dictionary)| inserts any type of info (id, title, etc)
\__parse_str_to_dict(dict_str)\__ | parses string dict to dict
\__parse_str_to_list(list_str)\__ | parses string list to list
get(id,alias,name,mail,...,reference)| gets all needed info
update(id,alias,name,mail,...,reference) | updates needed required data
\__search_query(cursor, table, column, arg)\__ | creates query for search
\_update_query(cursor, table, column, arg, search_column, search_arg)\__ | updates query
\__delete_query(cursor, table, column, arg)\__ | deletes query
delete(id=None, title=None) | deletes whether id(user), or title
get_all_similar_info(id,alias,name,mail,...,reference) | gets information from the same column in DB
\__search_similar_query(cursor, table, arg)\__ | searches similar query


## Verification.py:
Method|Description
------|-----------
pin_generator()| generates a random pin (used for authentification)
pin_sender(email,pin) | calls pin_generator() and sends pin to email



## Parsing.py
Method|Description
------|-----------
__parse_str_to_dict(dict_str)|parses string line to dictionary
__parse_str_to_list(list_str)|parses string line to list
__parse_str_to_queue(queue_str)|parses string line to queue
__parse|parses dict to string and tuples

## Dictkeys.py
Stores default keys for arguments of user, document classes.

## Authentification.py
Method|Description
------|-----------
check(alias)| check wheter user exists in system

