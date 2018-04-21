# ==============================Authentication features======================================================
librarians = dict()
librarians.setdefault(0)


def add_librarian(id):
    librarians[id] = 1


def is_librarian(id):
    if (librarians.get(id) == 1):
        return True
    else:
        return False


professors = dict()
professors.setdefault(0)


def add_professor(id):
    professors[id] = 1


def is_professor(id):
    if (professors.get(id) == 1):
        return True
    else:
        return False


TAs = dict()
TAs.setdefault(0)


def add_ta(id):
    TAs[id] = 1


def is_ta(id):
    if (TAs.get(id) == 1):
        return True
    else:
        return False


instructors = dict()
instructors.setdefault(0)


def add_instructor(id):
    instructors[id] = 1


def is_instructor(id):
    if instructors.get(id) == 1:
        return True
    else:
        return False


VPs = dict()
VPs.setdefault(0)


def add_vp(id):
    VPs[id] = 1


def is_vp(id):
    if (TAs.get(id) == 1):
        return True
    else:
        return False
