import datetime
import user
import documents


def booking(user, document):
    print("Booking func has been initialised")

    if document.summary()["type"] == "book":

        if not user.has_book(document.get_title()):

            if document.get_number_of_copies() > 0:

                if not document.is_reference():
                    init_date = datetime.datetime.toordinal(
                        datetime.datetime.today())

                    if user.get_rank() == 1:
                        exp_date = datetime.datetime.fromordinal(
                            init_date + 28)
                        print("User: " + user +
                              "took book till: " + str(exp_date))
                    else:

                        if document.is_bestseller():
                            exp_date = datetime.datetime.fromordinal(
                                init_date + 14)
                            print("User: " + user +
                                  "took book till: " + str(exp_date))

                        else:
                            exp_date = datetime.datetime.fromordinal(
                                init_date + 21)
                            print("User: " + user +
                                  "took book till: " + str(exp_date))
                    user.add_document(
                        document.get_list_of_copies().pop(0), str(exp_date))

                    return success + " " + str(exp_date)

                return fail
            else:
                return no_copies

    elif document.summary()["type"] == "av":

        if not user.has_book(document.get_title()):

            if document.get_number_of_copies() > 0:
                init_date = datetime.datetime.toordinal(
                    datetime.datetime.today())

                if user.get_rank() == 1:
                    exp_date = datetime.datetime.fromordinal(
                        init_date + 28)
                    print("User: " + user + "took av-file until: " + str(
                        exp_date))
                else:
                    exp_date = datetime.datetime.fromordinal(
                        init_date + 21)
                    print("User: " + user +
                          "took av-file until: " + str(exp_date))
    # elif document.summary()["type"] == "article":


success = "Congratulations! You have been successfully ordered a book until: "
fail = "Unfortunately book is not yet available..."
no_copies = "No copies"


# TODO connect all this shit together. Get that shit together, get things done.
# Just finish class after DB released.
