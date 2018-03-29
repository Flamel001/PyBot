# ==============================Authentification fitures======================================================
__librarians = dict()


def add_librarian(id: str):
    __librarians[id] = 1


def is_librarian(id: str):
    return __librarians[id] == 1


__professors = dict()


def add_professor(id: str):
    __professors[id] = 1


def is_professor(id: str):
    return __professors[id] == 1


__TAs = dict()


def add_ta(id: str):
    __TAs[id] = 1


def is_ta(id: str):
    return __TAs[id] == 1


__instructors = dict()


def add_instructor(id: str):
    __instructors[id] = 1


def is_instructor(id: str):
    return __instructors[id] == 1


__VPs = dict()


def add_vp(id: str):
    __VPs[id] = 1


def is_vp(id: str):
    return __VPs[id] == 1
