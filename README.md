# PyBot
Innopolis Library Management System implemented via Telegram Bot Api

###### Before using project you will be needed to download file config.py. To download it, you should contact one of the contributers.

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


## Telebot2.py:
There are methods for all the buttons from GUI
```@bot.message_handler```  
Used for catch commands and callback data from buttons perform actions according to them

```bot.send_message(message.chat.id, "text", reply_markup=bot_features.get_inline_markup(markup))```
Used to send new messages to user. 
__Message.chat.id__ holds id of chat to answer,
“text” is a text of message, 
__reply_markup=__ used to show what buttons are needed under textmessage “text”

```
bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                      text="text”))
bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,                             reply_markup=bot_features.get_inline_markup(markup))
```
__bot.edit_message_text__ – used to change text of needed message(using message_id) from needed chat(using chat_id)  to “text”
__bot.edit_message_reply_markup__ used to update butons from need chat of needed message to “markup”


```bot.register_next_step_handler(call, auth)```
used to catch some information from user and use it in one of the other program methods


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

