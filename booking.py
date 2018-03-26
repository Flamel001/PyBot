import datetime
import user
import documents


def order_book(usr, document):
    print(usr.summary())
    if not usr.has_book(document.get_title()):

        if document.get_title():

            if not document.is_reference():
                init_date = datetime.datetime.toordinal(
                    datetime.datetime.today())

                if usr.get_rank() == 1:
                    exp_date = datetime.datetime.fromordinal(
                        init_date + 28)
                    print("User: " + usr.get_name() + " took book till: " + str(exp_date))

                    print("**SUCCESS**")
                    return success + " " + str(exp_date)
                else:
                    if document.is_bestseller():
                        exp_date = datetime.datetime.fromordinal(
                            init_date + 14)
                        print("User: " + usr.get_name() +
                              " took book till: " + str(exp_date))

                        print("**SUCCESS**")
                        return success + " " + str(exp_date)
                    else:
                        exp_date = datetime.datetime.fromordinal(
                            init_date + 21)

                        print("User: " + str(usr.get_name()) +
                              " took book till: " + str(exp_date))

                        print("**SUCCESS**")
                        return success + " " + str(exp_date)
                # usr.add_document(
                #     document.get_list_of_copies().pop(0), str(exp_date))

            else:
                print("ERR. Unfortunately this doc is a reference material")
                return reference
        else:
            return no_copies
    else:
        print("ERR. User: " + usr.get_name() + " already has " + document.get_title())
        return you_own


def order_av(usr, document):
    print("**av-file DETECTED")
    if not usr.has_book(document.get_title()):
        # IMPORTANT: MAKE A CHECK FROM A DATABASE FOR A COPY VIA checked() METHOD
        if document.get_title():
            init_date = datetime.datetime.toordinal(
                datetime.datetime.today())

            if usr.get_rank() == 1:
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
        return you_own


def order_article(usr, document):
    print("**article DETECTED")
    if not usr.has_book(document.get_title()):
        if document.get_title():
            init_date = datetime.datetime.toordinal(
                datetime.datetime.today())

            if usr.get_rank() == 1:
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


success = "Congratulations! You have been successfully ordered a book until: "
fail = "Unfortunately this doc is not yet available..."
reference = "Unfortunately, You are trying to book a reference material which is unavailable. "
no_copies = "No copies left."
you_own = "You already have this book."

student = user.Patron("9123124", "Student", "name.surname@innopolis.ru", "1234567", "@student", "Innopolis City")
prof = user.Faculty("9123124", "Professor", "name.surname1@innopolis.ru", "1234568", "@professor", "Innopolis City")

book1 = documents.Book("Book1", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "false", "false")
book2 = documents.Book("Book5", "Author Uknown", "Innopolis", "2018", "1st", "Fantastica", "Url", "true", "false")
book3 = documents.Book("Reference", "Author Uknown", "Innopolis", "2018", "1st", "Reference", "Url", "false", "true")

article1 = documents.Article("Article", "Blogger", "InnoTimes", "2018", "Inno", "URL")
av_file1 = documents.AV_Materials("Title", "JimmyHendrix", "200$", "URL")

booking(student, book1)

print(str(student.summary()))
