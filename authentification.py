import database as db
def check(id: str):
    info = db.get(id=id)
    if info:
        return True
    else:
        return False









