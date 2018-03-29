import pyodbc
import user

__server = 'inno-lib-server.database.windows.net'
__database = 'InnoLib'
__username = 'a.kuspakov'
__password = 'H5j7p1f6_'
__driver = '{ODBC Driver 13 for SQL Server}'
__cnxn = pyodbc.connect(
    'DRIVER=' + __driver + ';PORT=1433;SERVER=' + __server + ';PORT=1443;DATABASE=' + __database + ';UID=' + __username + ';PWD=' + __password)

__users_name = "innolib_users"
__docs_name = "innolib_docs"
__key_user_id = "id"
__key_user_alias = "alias"
__key_user_name = "name"
__key_user_mail = "mail"
__key_user_number = "number"
__key_user_address = "address"
__key_user_type = "type"
__key_user_patron_document_list = "docs"
__key_user_patron_debt = "debt"

__key_doc_title = "title"
__key_doc_author = "author"
__key_doc_owner = "owner"
__key_doc_type = "type"
__key_doc_copies = "copies"
__key_doc_price = "price"
__key_doc_url = "url"
__key_doc_publication_date = "publication_date"
__key_doc_publisher = "publisher"
__key_doc_year = "year"
__key_doc_journal = "journal"
__key_doc_editor = "editor"
__key_doc_edition = "edition"
__key_doc_genre = "genre"
__key_doc_bestseller = "bestseller"
__key_doc_reference = "reference"


def create_users_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __users_name + "' and xtype='U') create table " + __users_name + "(" + __key_user_id + " int NOT NULL UNIQUE, " + __key_user_alias + " text, " + __key_user_name + " text, " + __key_user_mail +
        " text, " + __key_user_number + " text, " + __key_user_address + " text, " + __key_user_type + " text, " +
        __key_user_patron_document_list + " text, " + __key_user_patron_debt + " int)")
    cursor.commit()
    cursor.close()


def create_docs_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __docs_name + "' and xtype='U') create table " + __docs_name + "(" + __key_doc_title + " text NOT NULL UNIQUE, " + __key_doc_author + " text, " + __key_doc_owner + " text, " + __key_doc_type + " text, " + __key_doc_copies +
        " text, " + __key_doc_price + " text, " + __key_doc_url + " text, " + __key_doc_publication_date + " text, " +
        __key_doc_publisher + " text, " + __key_doc_year + " text, " + __key_doc_journal + " text, " + __key_doc_editor + " text, " + __key_doc_edition + " text, " + __key_doc_genre + " text, " +
        __key_doc_bestseller + " bit, " + __key_doc_reference + " bit)")
    cursor.commit()
    cursor.close()


def __parse(dictionary):
    list_of_dict_values = list()
    list_of_dict_values.append(dictionary[user.user_id])
    list_of_dict_values.append(dictionary[user.user_alias])
    list_of_dict_values.append(dictionary[user.user_name])
    list_of_dict_values.append(dictionary[user.user_mail])
    list_of_dict_values.append(dictionary[user.user_number])
    list_of_dict_values.append(dictionary[user.user_address])
    list_of_dict_values.append(dictionary[user.user_type])
    list_of_dict_values.append(str(dictionary[user.user_document_list]))
    list_of_dict_values.append(dictionary[user.user_debt])
    return tuple(list_of_dict_values)


def insert(dictionary):
    cursor = __cnxn.cursor()
    type = ""
    params = list()
    commit_or_not = bool
    if dictionary:
        if "type" in dictionary.keys():
            type = dictionary["type"]
            params.append(__parse(dictionary))
    if type and params:
        if type == "student" or type == "faculty":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_alias + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ", " + __key_user_patron_document_list + ", " + __key_user_patron_debt + ")" +
                " values (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        elif type == "librarian":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_alias + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ") values(?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "book":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_publisher + ", " + __key_doc_year + ", " + __key_doc_edition + ", " + __key_doc_genre + ", " + __key_doc_bestseller + ", " + __key_doc_reference + ") values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "article":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_journal + ", " + __key_doc_publication_date + ", " + __key_doc_editor + ") values(?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "av":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_price + ") values(?, ?, ?, ?, ?, ?)",
                params)
        else:
            commit_or_not = False
        if commit_or_not:
            cursor.commit()
        cursor.close()


def get(id=None, title=None, author=None, owner=None, publisher=None, year=None, journal=None, editor=None, genre=None,
        bestseller=None, reference=None):
    counter = 0
    if id:
        counter += 1
    if title:
        counter += 1
    if author:
        counter += 1
    if owner:
        counter += 1
    if publisher:
        counter += 1
    if year:
        counter += 1
    if journal:
        counter += 1
    if editor:
        counter += 1
    if genre:
        counter += 1
    if bestseller:
        counter += 1
    if reference:
        counter += 1
    if counter == 1:
        cursor = __cnxn.cursor()
        if id:
            __search_query(cursor, __users_name, __key_user_id, id)
        elif title:
            __search_query(cursor, __docs_name, __docs_name, title)
        elif author:
            __search_query(cursor, __docs_name, __key_doc_author, author)
        elif owner:
            __search_query(cursor, __docs_name, __key_doc_author, owner)
        elif publisher:
            __search_query(cursor, __key_doc_publisher, __docs_name, publisher)
        elif year:
            __search_query(cursor, __key_doc_year, __docs_name, year)
        elif journal:
            __search_query(cursor, __key_doc_journal, __docs_name, journal)
        elif editor:
            __search_query(cursor, __key_doc_editor, __docs_name, editor)
        elif genre:
            __search_query(cursor, __key_doc_genre, __docs_name, genre)
        elif bestseller:
            __search_query(cursor, __key_doc_bestseller, __docs_name, int(bestseller))
        elif reference:
            __search_query(cursor, __key_doc_reference, __docs_name, int(reference))
        result_list = list()
        for row in cursor.fetchall():
            result_list.append(row)
        return result_list
    else:
        print("One argument should be provided")
        return list()


def __search_query(cursor, table, column, arg):
    return cursor.execute("select * from " + table + " where " + column + " like '" + str(arg) + "'")
