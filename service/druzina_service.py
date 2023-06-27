from database.database import get_db

class DruzinaService():
    @staticmethod
    def get_all():
        db = get_db()
        return db.execute(
            "SELECT * FROM druzina"
        ).fetchall()
    
class NovaDruzinaService():
    @staticmethod
    def new_group(jmeno, nejmladsi_vek, popis):
        db = get_db()
        db.execute("INSERT INTO druzina (jmeno, nejmladsi_vek, popis) VALUES (?, ?, ?)", [jmeno, nejmladsi_vek, popis])
        db.commit()
