from job import warehouse, run_job, report

def naive(db, day, rows):
    db.executemany("INSERT INTO revenue "
                   "VALUES (?, ?, ?)", rows)

def idempotent(db, day, rows):
    db.begin()  # all or nothing
    db.execute("DELETE FROM revenue "
               "WHERE day = ?", [day])
    naive(db, day, rows)
    db.commit()

for load in (naive, idempotent):
    db = warehouse()  # already holds Oct 6
    run_job(db, load, crash=True)
    run_job(db, load)  # the rerun
    report(db, load.__name__)
