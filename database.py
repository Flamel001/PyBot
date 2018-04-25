import pyodbc
import user
import documents
import ast

__server = 'inno-lib-server.database.windows.net'
__database = 'InnoLib'
__username = 'a.kuspakov'
__password = 'H5j7p1f6_'
__driver = '{ODBC Driver 13 for SQL Server}'
__cnxn = pyodbc.connect(
    'DRIVER=' + __driver + ';PORT=1433;SERVER=' + __server + ';PORT=1443;DATABASE=' + __database + ';UID=' + __username
    + ';PWD=' + __password)

__users_name = "innolib_users"
__docs_name = "innolib_docs"
__logs_name = "innolib_logs"
__key_user_id = "id"
__key_user_alias = "alias"
__key_user_name = "name"
__key_user_mail = "mail"
__key_user_number = "number"
__key_user_address = "address"
__key_user_registration_date = "registration_date"
__key_user_type = "type"
__key_user_librarian_privilege = "privilege"
__key_user_patron_document_list = "docs"
__key_user_patron_debt = "debt"

__key_doc_title = "title"
__key_doc_author = "author"
__key_doc_owner = "owner"
__key_doc_type = "type"
__key_doc_queue = "queue"
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

__key_log = "log"


def create_users_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __users_name + "' and xtype='U') create table "
        + __users_name + "(" + __key_user_id + " int NOT NULL UNIQUE, " + __key_user_alias + " text, " + __key_user_name
        + " text, " + __key_user_mail +" text, " + __key_user_number + " text, " + __key_user_address + " text, "
        + __key_user_registration_date + " text, " + __key_user_type + " text, " + __key_user_librarian_privilege
        + " int, " + __key_user_patron_document_list + " text, " + __key_user_patron_debt + " int)")
    cursor.commit()
    cursor.close()


def create_docs_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __docs_name + "' and xtype='U') create table "
        + __docs_name + "(" + __key_doc_title + " varchar(255) NOT NULL UNIQUE, " + __key_doc_author + " text, "
        + __key_doc_owner + " text, " + __key_doc_type + " text, " + __key_doc_queue + " text, " + __key_doc_copies
        + " text, " + __key_doc_price + " text, " + __key_doc_url + " text, " + __key_doc_publication_date + " text, "
        + __key_doc_publisher + " text, " + __key_doc_year + " text, " + __key_doc_journal + " text, "
        + __key_doc_editor + " text, " + __key_doc_edition + " text, " + __key_doc_genre + " text, "
        + __key_doc_bestseller + " bit, " + __key_doc_reference + " bit)")
    cursor.commit()
    cursor.close()


def create_log_table():
    cursor = __cnxn.cursor()
    cursor.execute(
        "if not exists (select * from sysobjects where name='" + __logs_name + "' and xtype='U') create table "
        + __logs_name + "(" + __key_log + " text)")
    cursor.commit()
    cursor.close()


def __parse(dictionary):
    if dictionary["type"] == "Student" or dictionary["type"] == "Professor" or dictionary["type"] == "Instructor" or \
            dictionary["type"] == "TA" or dictionary["type"] == "VP":
        dictionary.pop("priority")
    list_of_dict_values = list(dictionary.values())
    result = tuple()
    for element in list_of_dict_values:
        if element == True or element == False:
            result = result + tuple([int(element)])
        elif element:
            result = result + tuple([str(element).replace("\'", "\"")])
        else:
            if element == None:
                result = result + tuple([""])
            else:
                result = result + tuple([str(element).replace("\'", "\"")])
    if len(result) == 10 or len(result) == 7 or len(result) == 13 or len(result) == 8:
        return result
    else:
        raise Exception("DATABASE, Insertion. Information was not parsed correctly; please, check it.")


def insert(dictionary):
    cursor = __cnxn.cursor()
    type = ""
    params = list()
    print("This is something " + str(dictionary))
    if dictionary:
        if "type" in dictionary.keys():
            type = dictionary["type"]
            params.append(__parse(dictionary))
    print("This is something 2 Hello World " + str(params))
    if type and params:
        if type == "Student" or type == "VP" or type == "TA" or type == "Instructor" or type == "Professor":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_alias + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ", " + __key_user_registration_date + ", " + __key_user_patron_document_list + ", " + __key_user_patron_debt + ")" +
                " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        elif type == "Librarian":
            cursor.executemany(
                "insert into " + __users_name + "(" + __key_user_id + ", " + __key_user_alias + ", " + __key_user_name + ", " + __key_user_mail + ", " + __key_user_number + ", " + __key_user_address + ", " + __key_user_type + ", " + __key_user_librarian_privilege + ") values(?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "Book":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_queue + ", " + __key_doc_copies + ", " + __key_doc_publisher + ", " + __key_doc_year + ", " + __key_doc_edition + ", " + __key_doc_genre + ", " + __key_doc_bestseller + ", " + __key_doc_reference + ") values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "Article":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_queue + ", " + __key_doc_copies + ", " + __key_doc_journal + ", " + __key_doc_publication_date + ", " + __key_doc_editor + ") values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        elif type == "AV":
            cursor.executemany(
                "insert into " + __docs_name + "(" + __key_doc_title + ", " + __key_doc_author + ", " + __key_doc_owner + ", " + __key_doc_url + ", " + __key_doc_type + ", " + __key_doc_queue + ", " + __key_doc_copies + ", " + __key_doc_price + ") values(?, ?, ?, ?, ?, ?, ?, ?)",
                params)
        else:
            raise Exception(
                "DATABASE, Insertion. No acceptable type is provided; acceptable type: Student, Instructor, Professor, Librarian, VP, TA, Book, Article, AV")
        cursor.commit()
        cursor.close()


def insert_log(log_message):
    cursor = __cnxn.cursor()
    cursor.execute("insert into " + __logs_name + "(" + __key_log + ") values(?)", log_message)
    cursor.commit()
    cursor.close()


def __parse_str_to_dict(dict_str):
    dict_str_list = dict_str.replace("{", "").replace("}", "").replace("\"", "").split(", ")
    print("This is dict " + dict_str_list)
    if dict_str_list:
        parsed_dict = dict()
        for i in range(0, len(dict_str_list)):
            if dict_str_list[i]:
                splitted_dict = dict_str_list[i].split(": ")
                print("This is something 3 Jango " + str(dict_str_list[i].split(": ")))
                parsed_dict[splitted_dict[0]] = splitted_dict[1]
        return parsed_dict
    else:
        return dict()


def __parse_str_to_list(list_str):
    str_list = list_str.replace("[", "").replace("]", "").split(", ")
    if str_list:
        return str_list
    else:
        return list()


def __parse_str_to_queue(queue_str):
    print("Yo another print int queue " + str(queue_str[2:][:-2].split("), (")))
    str_queue_unsplit = queue_str[2:][:-2]
    print("Another one " + str(str_queue_unsplit))
    if str_queue_unsplit:
        str_queue = str_queue_unsplit.split("), (")
        print("1 " + str(str_queue))
        queue_str_list = [str_queue[i].split(", ") for i in range(0, len(str_queue))]
        print("2 " + str(queue_str_list))
        result = [(int(queue_str_list[i][0]), queue_str_list[i][1].replace("\'", "")) for i in range(0, len(queue_str_list))]
        return result
    else:
        return []


def __parse_to_object(row):
    print(str(row))
    if len(row) > 6:
        if row[7] == "Librarian":
            return user.Librarian(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5], priv=row[8])
        elif row[7] == "Student":
            return user.Student(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5],
                                reg_date=row[6], doc_list=ast.literal_eval(row[9]), debt=row[10])
        elif row[7] == "Instructor":
            return user.Instructor(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5],
                                   reg_date=row[6], doc_list=ast.literal_eval(row[9]), debt=row[10])
        elif row[7] == "TA":
            return user.TA(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5],
                           reg_date=row[6], doc_list=ast.literal_eval(row[9]), debt=row[10])
        elif row[7] == "Professor":
            return user.Professor(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5],
                                  reg_date=row[6], doc_list=ast.literal_eval(row[9]), debt=row[10])
        elif row[7] == "VP":
            return user.VP(id=row[0], alias=row[1], name=row[2], mail=row[3], number=row[4], address=row[5],
                           reg_date=row[6], doc_list=ast.literal_eval(row[9]), debt=row[10])
        elif row[3] == "Book":
            print("This is something!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " + str(row[4]))
            print(str(ast.literal_eval(row[4])))
            return documents.Book(title=row[0], author=row[1], queue=ast.literal_eval(row[4]),
                                  copies=ast.literal_eval(row[5]), url=row[7], publisher=row[9], year=row[10],
                                  edition=row[13], genre=row[14], bestseller=bool(row[15]), reference=bool(row[16]))
        elif row[3] == "Article":
            return documents.Article(title=row[0], author=row[1], queue=ast.literal_eval(row[4]),
                                     copies=ast.literal_eval(row[5]), url=row[6], publication_date=row[8],
                                     journal=row[11],
                                     editor=row[12])
        elif row[3] == "AV":
            return documents.AV_Materials(title=row[0], author=row[1], copies=ast.literal_eval(row[5]), price=row[6],
                                          url=row[7])


def get(id=None, alias=None, name=None, mail=None, number=None, address=None, type_user=None, privilege=None, title=None, author=None,
        owner=None, type_book=None, publisher=None, year=None, journal=None, editor=None, genre=None,
        bestseller=None, reference=None):
    counter = 0
    if id:
        counter += 1
    if alias:
        counter += 1
    if name:
        counter += 1
    if mail:
        counter += 1
    if number:
        counter += 1
    if address:
        counter += 1
    if type_user:
        counter += 1
    if privilege:
        counter += 1
    if title:
        counter += 1
    if author:
        counter += 1
    if owner:
        counter += 1
    if type_book:
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
            cursor = __search_query(cursor, __users_name, __key_user_id, id, False)
        elif alias:
            cursor = __search_query(cursor, __users_name, __key_user_alias, alias, False)
        elif name:
            cursor = __search_query(cursor, __users_name, __key_user_name, name, False)
        elif mail:
            cursor = __search_query(cursor, __users_name, __key_user_mail, mail, False)
        elif number:
            cursor = __search_query(cursor, __users_name, __key_user_number, number, False)
        elif address:
            cursor = __search_query(cursor, __users_name, __key_user_address, address, False)
        elif type_user:
            cursor = __search_query(cursor, __users_name, __key_user_type, type_user, False)
        elif title:
            cursor = __search_query(cursor, __docs_name, __key_doc_title, title, False)
        elif author:
            cursor = __search_query(cursor, __docs_name, __key_doc_author, author, False)
        elif owner:
            cursor = __search_query(cursor, __docs_name, __key_doc_author, owner, False)
        elif type_book:
            cursor = __search_query(cursor, __docs_name, __key_doc_type, type_book, False)
        elif publisher:
            cursor = __search_query(cursor, __docs_name, __key_doc_publisher, publisher, False)
        elif year:
            cursor = __search_query(cursor, __docs_name, __key_doc_year, year, False)
        elif journal:
            cursor = __search_query(cursor, __docs_name, __key_doc_journal, journal, False)
        elif editor:
            cursor = __search_query(cursor, __docs_name, __key_doc_editor, editor, False)
        elif genre:
            cursor = __search_query(cursor, __docs_name, __key_doc_genre, genre, False)
        elif bestseller:
            cursor = __search_query(cursor, __docs_name, __key_doc_bestseller, int(bestseller), False)
        elif reference:
            cursor = __search_query(cursor, __docs_name, __key_doc_reference, int(reference), False)
        result_list = list()
        rows = cursor.fetchall()
        for row in rows:
            result_list.append(__parse_to_object(row))
        cursor.close()
        return result_list
    else:
        raise Exception("DATABASE, Fetching. One argument should be provided")


def __search_query(cursor, table, column, arg, dont_replace):
    if dont_replace:
        search_query = "select * from " + table + " where " + column + " like '" + str(arg) + "'"
    else:
        search_query = "select * from " + table + " where " + column + " like '" + str(arg).replace("\'", "\"") + "'"
    return cursor.execute(search_query)


def update(id=None, alias=None, name=None, mail=None, number=None, address=None, privilege=None, docs=None, debt=None, new_id=None,
           title=None, author=None,
           owner=None, queue=None, copies=None, price=None, url=None, publication_date=None, publisher=None, year=None,
           journal=None, editor=None, edition=None,
           genre=None,
           bestseller=None, reference=None, new_title=None):
    if title and id:
        raise Exception("DATABASE, Update. Only id or title should be provided")
    elif title or id:
        # print("Update is in process")
        if id:
            if alias or name or mail or number or address or docs or docs == dict() or debt or privilege or new_id:
                cursor = __cnxn.cursor()
                if alias:
                    __update_query(cursor, __users_name, __key_user_alias, alias, __key_user_id, id)
                elif name:
                    __update_query(cursor, __users_name, __key_user_name, name, __key_user_id, id)
                elif mail:
                    __update_query(cursor, __users_name, __key_user_mail, mail, __key_user_id, id)
                elif number:
                    __update_query(cursor, __users_name, __key_user_number, number, __key_user_id, id)
                elif address:
                    __update_query(cursor, __users_name, __key_user_address, address, __key_user_id, id)
                elif privilege:
                    __update_query(cursor, __users_name, __key_user_librarian_privilege, privilege, __key_user_id, id)
                elif docs or docs == dict():
                    __update_query(cursor, __users_name, __key_user_patron_document_list, docs, __key_user_id, id)
                elif debt:
                    __update_query(cursor, __users_name, __key_user_patron_debt, debt, __key_user_id, id)
                elif new_id:
                    __update_query(cursor, __users_name, __key_user_id, new_id, __key_user_id, id)
                cursor.commit()
                cursor.close()
            else:
                raise Exception("DATABASE, Update. Only id was provided, need something else for an update")
        if title:
            if author or owner or queue or queue == list() or copies or copies == list() or price or url or publisher or year or journal or editor or genre or bestseller or reference or new_title:
                cursor = __cnxn.cursor()
                if author:
                    __update_query(cursor, __docs_name, __key_doc_author, author, __key_doc_title, title)
                elif owner:
                    __update_query(cursor, __docs_name, __key_doc_owner, owner, __key_doc_title, title)
                elif queue or queue == list():
                    __update_query(cursor, __docs_name, __key_doc_queue, queue, __key_doc_title, title)
                elif copies or copies == list():
                    __update_query(cursor, __docs_name, __key_doc_copies, copies, __key_doc_title, title)
                elif price:
                    __update_query(cursor, __docs_name, __key_doc_price, price, __key_doc_title, title)
                elif url:
                    __update_query(cursor, __docs_name, __key_doc_url, url, __key_doc_title, title)
                elif publication_date:
                    __update_query(cursor, __docs_name, __key_doc_publication_date, publication_date, __key_doc_title,
                                   title)
                elif publisher:
                    __update_query(cursor, __docs_name, __key_doc_publisher, publisher, __key_doc_title, title)
                elif year:
                    __update_query(cursor, __docs_name, __key_doc_year, year, __key_doc_title, title)
                elif journal:
                    __update_query(cursor, __docs_name, __key_doc_journal, journal, __key_doc_title, title)
                elif editor:
                    __update_query(cursor, __docs_name, __key_doc_editor, editor, __key_doc_title, title)
                elif edition:
                    __update_query(cursor, __docs_name, __key_doc_edition, edition, __key_doc_title, title)
                elif genre:
                    __update_query(cursor, __docs_name, __key_doc_genre, genre, __key_doc_title, title)
                elif bestseller:
                    __update_query(cursor, __docs_name, __key_doc_bestseller, int(bestseller), __key_doc_title, title)
                elif reference:
                    __update_query(cursor, __docs_name, __key_doc_reference, int(reference), __key_doc_title, title)
                elif new_title:
                    __update_query(cursor, __docs_name, __key_doc_title, new_title, __key_doc_title, title)
                cursor.commit()
                cursor.close()
            else:
                raise Exception("DATABASE, Update. Only title was provided, need something else for an update")
    else:
        raise Exception("DATABASE, Update. Please, provide one argument")


def __update_query(cursor, table, column, arg, search_column, search_arg):
    # print(str(arg) + " jnd " + str(search_arg))
    update_query = "update " + table + " set " + column + " = '" + str(arg).replace("\'", "\"") + "' where " + search_column + " like '" + str(search_arg).replace("\'", "\"") + "'"
    print("This query " + update_query)
    return cursor.execute(update_query)


def delete(id=None, title=None):
    if id and title:
        raise Exception("DATABASE, Deletion. Provide one argument")
    elif id or title:
        cursor = __cnxn.cursor()
        if id:
            __delete_query(cursor, __users_name, __key_user_id, id)
        else:
            __delete_query(cursor, __docs_name, __key_doc_title, title)
        cursor.commit()
        cursor.close()
    else:
        raise Exception("DATABASE, Deletion. Please provide one argument")


def __delete_query(cursor, table, column, arg):
    delete_query = "delete from " + table + " where " + column + " like '" + str(arg) + "'"
    return cursor.execute(delete_query)


def get_all_similar_info(id=None, alias=None, name=None, mail=None, number=None, address=None, type_user=None,
                         title=None, author=None,
                         owner=None, type_book=None, publisher=None, year=None, journal=None, editor=None, genre=None,
                         bestseller=None, reference=None, log=None):
    counter = 0
    if id:
        counter += 1
    if alias:
        counter += 1
    if name:
        counter += 1
    if mail:
        counter += 1
    if number:
        counter += 1
    if address:
        counter += 1
    if type_user:
        counter += 1
    if title:
        counter += 1
    if author:
        counter += 1
    if owner:
        counter += 1
    if type_book:
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
    if log:
        counter += 1
    if counter == 1:
        cursor = __cnxn.cursor()
        if id:
            cursor = __search_similar_query(cursor, __users_name, __key_user_id)
        elif alias:
            cursor = __search_similar_query(cursor, __users_name, __key_user_alias)
        elif name:
            cursor = __search_similar_query(cursor, __users_name, __key_user_name)
        elif mail:
            cursor = __search_similar_query(cursor, __users_name, __key_user_mail)
        elif number:
            cursor = __search_similar_query(cursor, __users_name, __key_user_number)
        elif address:
            cursor = __search_similar_query(cursor, __users_name, __key_user_address)
        elif type_user:
            cursor = __search_similar_query(cursor, __users_name, __key_user_type)
        elif title:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_title)
        elif author:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_author)
        elif owner:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_author)
        elif type_book:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_type)
        elif publisher:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_publisher)
        elif year:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_year)
        elif journal:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_journal)
        elif editor:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_editor)
        elif genre:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_genre)
        elif bestseller:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_bestseller)
        elif reference:
            cursor = __search_similar_query(cursor, __docs_name, __key_doc_reference)
        elif log:
            cursor = __search_similar_query(cursor, __logs_name, __key_log)
        result_list = list()
        rows = cursor.fetchall()
        for row in rows:
            result_list.append(row[0])
        cursor.close()
        return result_list
    else:
        raise Exception("DATABASE, Fetching. One argument should be provided")


def __search_similar_query(cursor, table, arg):
    search_similar_query = "select " + str(arg) + " from " + table
    return cursor.execute(search_similar_query)


def search(search_title, list_of_titles):
    result = list()
    splitted_titles = list()
    print("Search title " + str(search_title))
    if "AND" in search_title:
        splitted_titles = search_title.split(" AND ")
        print("This is splitted titles " + str(search_title))
        temp_list = list()
        for title in list_of_titles:
            for spl_title in splitted_titles:
                if spl_title in title:
                    temp_list.append(True)
                else:
                    temp_list.append(False)
            do_add = True
            print("This is title in search " + str(title))
            print("Here are bools " + str(temp_list))
            for i in range(0, len(temp_list)):
                if not temp_list[i]:
                    do_add = False
                    break
            if do_add:
                result.append(title)
            temp_list = list()
    elif "OR" in search_title:
        splitted_titles = search_title.split(" OR ")
        temp_list = list()
        print("This is splitted title " + str(splitted_titles))
        for title in list_of_titles:
            for spl_title in splitted_titles:
                if spl_title in title:
                    temp_list.append(True)
                else:
                    temp_list.append(False)
            do_add = False
            for i in range(0, len(temp_list)):
                if temp_list[i]:
                    do_add = True
                    break
            if do_add:
                result.append(title)
            temp_list = list()
    else:
        for title in list_of_titles:
            if search_title == title:
                result.append(title)
    print("This is from search method " + str(result))
    if not result:
        for title in list_of_titles:
            if match(search_title, 0, title, 0, 0):
                result.append(title)
    return result


def match(search_string:str, search_string_i:int, title:str, i:int, miss:int):
    if i == len(title) or search_string_i == len(search_string) or miss >= 0.2 * len(search_string):
        if search_string_i >= 0.8 * len(search_string) and miss < 0.2 * len(search_string):
            return True
        else:
            return False
    elif title[i] == search_string[search_string_i]:
        return match(search_string, search_string_i + 1, title, i + 1, miss)
    else:
        b1 = match(search_string, search_string_i + 1, title, i + 1, miss + 1)
        b2 = match(search_string, search_string_i, title, i + 1, miss)
        return True if b1 else b2
