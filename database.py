import pyodbc
import user
import documents

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
__key_user_registration_date = "registration_date"
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
        " text, " + __key_user_number + " text, " + __key_user_address + " text, " + __key_user_registration_date + " text, " + __key_user_type + " text, " +
        __key_user_patron_document_list + " text, " + __key_user_patron_debt + " int)")
    cursor.commit()
    cursor.close()


def create_docs_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __docs_name + "' and xtype='U') create table " + __docs_name + "(" + __key_doc_title + " varchar(255) NOT NULL UNIQUE, " + __key_doc_author + " text, " + __key_doc_owner + " text, " + __key_doc_type + " text, " + __key_doc_copies +
        " text, " + __key_doc_price + " text, " + __key_doc_url + " text, " + __key_doc_publication_date + " text, " +
        __key_doc_publisher + " text, " + __key_doc_year + " text, " + __key_doc_journal + " text, " + __key_doc_editor + " text, " + __key_doc_edition + " text, " + __key_doc_genre + " text, " +
        __key_doc_bestseller + " bit, " + __key_doc_reference + " bit)")
    cursor.commit()
    cursor.close()


def parse(dictionary):
    if dictionary["type"] == "Student" or dictionary["type"] == "Professor" or dictionary["type"] == "Instructor" or dictionary["type"] == "TA" or dictionary["type"] == "VP":
        dictionary.pop("priority")
    elif dictionary["type"] == "Librarian":
        dictionary.pop("alias")
    list_of_dict_values = list(dictionary.values())
    result = tuple()
    for element in list_of_dict_values:
        if element == True or element == False:
            result = result + tuple([int(element)])
        elif element:
            result = result + tuple([element])
        else:
            if element == None:
                result = result + tuple([""])
            else:
                result = result + tuple([str(element)])
    print(str(result))
    return result


def __parse_to_object(row):
    if len(row)>6:
        if row[7] == "Librarian":
            return user.Librarian(id=row[0], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[7] == "Student":
            return user.Student(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[7] == "Instructor":
            return user.Instructor(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[7] == "TA":
            return user.TA(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[7] == "Professor":
            return user.Professor(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[7] == "VP":
            return user.VP(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5])
        elif row[3] == "Book":
            return documents.Book(title=row[0], author=row[1], url=row[6], publisher=row[8], year=row[9], edition=row[12], genre=row[13], bestseller=bool(row[14]), reference=bool(row[15]))
        elif row[3] == "Article":
            return documents.Article(title=row[0], author=row[1], url=row[6], publication_date=row[7], journal=row[10], editor=row[11])
        elif row[3] == "AV":
            return documents.AV_Materials(title=row[0], author=row[1], price=row[5], url=row[6])


def insert(dictionary):
    cursor = __cnxn.cursor()
    type = ""
    params = list()
    commit_or_not = True
    if dictionary:
        if "type" in dictionary.keys():
            type = dictionary["type"]
            params.append(parse(dictionary))
    if type and params:
        if type == "Student" or type == "VP" or type == "TA" or type == "Instructor" or type == "Professor":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_alias + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ", " + __key_user_patron_document_list + ", " + __key_user_patron_debt + ", " + __key_user_registration_date + ")" +
                " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        elif type == "Librarian":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ", " + __key_user_registration_date + ") values(?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "Book":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_copies + ", " + __key_doc_publisher + ", " + __key_doc_year + ", " + __key_doc_edition + ", " + __key_doc_genre + ", " + __key_doc_bestseller + ", " + __key_doc_reference + ") values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "Article":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_copies + ", " + __key_doc_journal + ", " + __key_doc_publication_date + ", " + __key_doc_editor + ") values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "AV":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_copies + ", " + __key_doc_price + ") values(?, ?, ?, ?, ?, ?, ?)",
                params)
        else:
            print("something went wrong")
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
            cursor = __search_query(cursor, __users_name, __key_user_id, id)
        elif title:
            cursor = __search_query(cursor, __docs_name, __key_doc_title, title)
        elif author:
            cursor = __search_query(cursor, __docs_name, __key_doc_author, author)
        elif owner:
            cursor = __search_query(cursor, __docs_name, __key_doc_author, owner)
        elif publisher:
            cursor = __search_query(cursor, __docs_name, __key_doc_publisher, publisher)
        elif year:
            cursor = __search_query(cursor, __docs_name, __key_doc_year, year)
        elif journal:
            cursor = __search_query(cursor, __docs_name, __key_doc_journal, journal)
        elif editor:
            cursor = __search_query(cursor, __docs_name, __key_doc_editor, editor)
        elif genre:
            cursor = __search_query(cursor, __docs_name, __key_doc_genre, genre)
        elif bestseller:
            cursor = __search_query(cursor, __docs_name, __key_doc_bestseller, int(bestseller))
        elif reference:
            cursor = __search_query(cursor, __docs_name, __key_doc_reference, int(reference))
        result_list = list()
        rows = cursor.fetchall()
        for row in rows:
            result_list.append(__parse_to_object(row))
        return result_list
    else:
        print("One argument should be provided")
        return list()


def __search_query(cursor, table, column, arg):
    search_query = "select * from " + table + " where " + column + " like '" + str(arg) + "'"
    return cursor.execute(search_query)


def update(id=None, title=None, author=None, owner=None, publisher=None, year=None, journal=None, editor=None, genre=None,
        bestseller=None, reference=None):
    if title:
        if author or owner or publisher or year or journal or editor or genre or bestseller or reference:
            cursor = __cnxn.cursor()
            if author:
                __update_query(cursor, __docs_name, __key_doc_author, author, title)
            elif owner:
                __update_query(cursor, __docs_name, __key_doc_owner, owner, title)
            elif publisher:
                __update_query(cursor, __docs_name, __key_doc_publisher, publisher, title)
            elif year:
                __update_query(cursor, __docs_name, __key_doc_year, year, title)
            elif journal:
                __update_query(cursor, __docs_name, __key_doc_journal, journal, title)
            elif editor:
                __update_query(cursor, __docs_name, __key_doc_editor, editor, title)
            elif genre:
                __update_query(cursor, __docs_name, __key_doc_genre, genre, title)
            elif bestseller:
                __update_query(cursor, __docs_name, __key_doc_bestseller, int(bestseller), title)
            elif reference:
                __update_query(cursor, __docs_name, __key_doc_reference, int(reference), title)
            cursor.commit()
        else:
            print("Only title was provided, need something else for update")


def __update_query(cursor, table, column, arg, search_arg):
    update_query = "update " + table + " set " + column + " = '" + arg + "' where " + __key_doc_title + " like '" + str(search_arg) + "'"
    return cursor.execute(update_query)
