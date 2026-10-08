from job import naive, crash_and_rerun
def idempotent(db, day, rows):
    db.begin()  # all or nothing
    db.execute("DELETE FROM revenue "
               "WHERE day = ?", [day])
    naive(db, day, rows)  # the same insert
    db.commit()
crash_and_rerun(naive)
crash_and_rerun(idempotent)
