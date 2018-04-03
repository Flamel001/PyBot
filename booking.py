import datetime
import user
import documents
import queue
import collections
import heapq
import database as db

qu = []


def order_book(usr, document):
    ordered_times = 0

    print(usr.summary())
    usr = db.get(id=usr.user_id)
    if document.get_list_of_copies().size() > 0:
        if usr.has_book(document.get_title()):
            # if db.get(title=document.get_title()):
            ordered_times += 1
            if ordered_times > 1:

                if document.get_title():

                    if not document.is_reference():
                        init_date = datetime.datetime.toordinal(
                            datetime.datetime.today())

                        if usr.get_type() == "Faculty":
                            exp_date = datetime.datetime.fromordinal(
                                init_date + 28)
                            print("User: " + usr.get_name() + " took book till: " + str(exp_date))

                            print("**SUCCESS**")
                            document.get_list_of_copies().size() - 1
                            db.update(id=usr.get_id(), copies=usr.append(document.get_title()))
                            db.update(title=document.get_title(), queue=add_to_queue(usr))  # adding to the queue
                            add_to_queue(usr)
                            if pop_from_queue(qu)[usr.get_id()] == usr.get_id():
                                db.update(id=usr.get_id(), docs=usr.get_docs_list())  # adding to db
                            return success + " " + str(exp_date)
                        else:
                            if document.is_bestseller():
                                exp_date = datetime.datetime.fromordinal(
                                    init_date + 14)
                                print("User: " + usr.get_name() +
                                      " took book till: " + str(exp_date))

                                print("**SUCCESS**")
                                document.get_list_of_copies().size() - 1
                                db.update(id=usr.get_id(), copies=usr.append(document.get_title()))
                                db.update(id=usr.get_id(), queue=str(qu))  # adding to the queue
                                add_to_queue(usr)
                                if pop_from_queue(qu)[usr.get_id()] == usr.get_id():
                                    db.update(id=usr.get_id(), docs=usr.get_docs_list())  # adding to db
                                return success + " " + str(exp_date)
                            else:
                                exp_date = datetime.datetime.fromordinal(
                                    init_date + 21)

                                print("User: " + str(usr.get_name()) +
                                      " took book till: " + str(exp_date))

                                print("**SUCCESS**")
                                document.get_list_of_copies().size() - 1
                                db.update(id=usr.get_id(), copies=usr.append(document.get_title()))
                                db.update(id=usr.get_id(), queue=str(qu))  # adding to the queue
                                add_to_queue(usr)
                                if pop_from_queue(qu)[usr.get_id()] == usr.get_id():
                                    db.update(id=usr.get_id(), docs=usr.get_docs_list())  # adding to db
                                return success + " " + str(exp_date)
                    else:
                        print("ERR. Unfortunately this doc is a reference material")
                        return reference
                else:
                    return no_copies

            else:
                print("ERR. User: " + usr.get_name() + " already renewed " + document.get_title())
                return max_renew_alert
    else:
        return no_copies


def order_av(usr, document):
    print("**av-file DETECTED")
    if not usr.has_book(document.get_title()):
        # IMPORTANT: MAKE A CHECK FROM A DATABASE FOR A COPY VIA checked() METHOD
        if document.get_title():
            init_date = datetime.datetime.toordinal(
                datetime.datetime.today())

            if usr.get_type() == "Faculty":
                exp_date = datetime.datetime.fromordinal(
                    init_date + 28)
                print("User: " + usr.get_name() + " took av-file until: " + str(exp_date))
                print("**SUCCESS**")
                return success + " " + str(exp_date)
            else:
                exp_date = datetime.datetime.fromordinal(
                    init_date + 21)
                print("User: " + usr.get_name() +
                      "took av-file until: " + str(exp_date))

                print("**SUCCESS**")
                return success + " " + str(exp_date)
        else:
            print("ERR. No copies left.")
            return no_copies

    else:
        print("ERR. User: " + usr.get_name() + " already has " + document.get_title())
        return max_renew_alert


def order_article(usr, document):
    print("**article DETECTED")
    if not usr.has_book(document.get_title()):
        if document.get_title():
            init_date = datetime.datetime.toordinal(
                datetime.datetime.today())

            if usr.get_type() == "Faculty":
                exp_date = datetime.datetime.fromordinal(
                    init_date + 28)
                print("User: " + usr.get_name() + " took av-file until: " + str(exp_date))
            else:
                exp_date = datetime.datetime.fromordinal(
                    init_date + 21)
                print("User: " + usr.get_name() +
                      " took article until: " + str(exp_date))


def booking(usr, document):
    print("**Booking func has been initialised")

    if document.summary()["type"] == "book":
        order_book(usr, document)

    elif document.summary()["type"] == "av":
        order_av(usr, document)

    elif document.summary()["type"] == "article":
        order_article(usr, document)


def add_to_queue(usr):
    heapq.heappush(db.update(queue=qu), (usr.get_prior(), usr.get_id()))
    return qu


def pop_from_queue(qu):
    heapq.heappop(qu)
    return qu


now = datetime.datetime.now()
today_format1 = now.strftime("%H:%d:%m:%Y")
second_id = now.second
userqueue = []

success = "Congratulations! You have been successfully ordered a book until: "
fail = "Unfortunately this doc is not yet available..."
reference = "Unfortunately, You are trying to book a reference material which is unavailable. "
no_copies = "No copies left."
max_renew_alert = "You have reached maximum amount of renews. :( "
no_copies = "No copies of current book were found."
"""
student = user.Student("stud", "Student", "name.surname@innopolis.ru", "1234567", "@student", "Innopolis City")
prof = user.Faculty("prof", "Professor", "name.surname1@innopolis.ru", "1234568", "@professor", "Innopolis City")
vp = user.VP("pidor", "VP", "dqdewfe.surname@innopolis.ru", "1231241", "@vp", "Inno")
student_pidor = user.Student("Ramil", "Ramil", "name.surname@innopolis.ru", "1234567", "@student", "Innopolis City")
student_jopaenota = user.Student("Nikita", "Nikita", "name.surname@innopolis.ru", "1234567", "@jopaenota",
                                 "Innopolis City")
# instructor = user.Instructors("129313213", "Instructor", "name.surname11@innopolis.ru", "212314", "@pidor", "Inno")
ta = user.TA("986543", "TA", "name.surname11@innopolis.ru", "212314", "@pidor", "Inno")

book1 = documents.Book("Book1", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "false", "false")
book2 = documents.Book("Book5", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "true", "false")
book3 = documents.Book("Reference", "Author Uknown", "Innopolis", "2018", "1st", "Reference", "Url", "false", "true")

article1 = documents.Article("Article", "Blogger", "InnoTimes", "2018", "Inno", "URL")
av_file1 = documents.AV_Materials("Title", "JimmyHendrix", "200$", "URL")

add_to_queue(student)
add_to_queue(prof)
add_to_queue(vp)
add_to_queue(student_jopaenota)
add_to_queue(student_pidor)
add_to_queue(ta)
# print(qu)
pop_from_queue(qu)

# print(qu)

# print()
# print(ta.summary())
# booking(student, book1)

# print(second_id)
"""
