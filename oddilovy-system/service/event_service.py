from database.database import get_db
import config

class EventService():
    @staticmethod
    def new_big_event(jmeno, datum, misto, zacatek_akce, konec_akce, popis=None, druzina=None, vedouci=None):
        db = get_db()
        c1 = db.cursor()
        c1.execute(
            "SELECT max(id_program) FROM program"
        )
        id_programu = c1.fetchone()[0]

        db.execute(
            """
                INSERT INTO akce (jmeno, datum, misto, zacatek_akce, konec_akce, popis, program_id_program, je_public)
                VALUES (?, STRFTIME('%d.%m.%Y', ?), ?, STRFTIME('%d.%m.%Y', ?), STRFTIME('%d.%m.%Y', ?), ?, ?, false)
            """,
            [jmeno, datum, misto, zacatek_akce, konec_akce, popis, id_programu]
        )
        db.commit()
        
        c2 = db.cursor()
        c2.execute(
            "SELECT max(id_akce) FROM akce"
        )
        id_akce = c2.fetchone()[0]
        for d in druzina:
            db.execute(
                "INSERT INTO druzina_akce (akce_id_akce, druzina_id_druzina) VALUES (?, ?)",
                [id_akce, d]
            )
        for v in vedouci:
            db.execute(
                "INSERT INTO user_akce (user_id_user, akce_id_akce) VALUES (?, ?)",
                [v, id_akce]
            )
        db.commit()


    @staticmethod
    def get_all_events_with_program():
        db = get_db()
        return db.execute(
            """
                SELECT a.id_akce AS id_akce, a.jmeno AS jmeno, a.datum AS datum, a.misto AS misto, a.zacatek_akce AS zacatek_akce, a.konec_akce AS konec_akce, a.popis AS popis, 
                a.je_public AS je_public, b.id_program AS id_program, b.misto_program AS misto_program, b.popis_program AS popis_program, b.delka AS delka, b.doporuceny_vek AS doporuceny_vek,
                c.akce_id_akce AS akce_id_akce, c.user_id_user AS user_id_user, d.jmeno AS vedouci_jmeno, d.prijmeni AS vedouci_prijmeni
                FROM akce a LEFT JOIN program b ON(program_id_program=id_program) LEFT JOIN user_akce c ON(akce_id_akce=id_akce) LEFT JOIN user d ON(user_id_user=id_user) 
                ORDER BY (SUBSTR(datum, 7, 4) || '-' || SUBSTR(datum, 4, 2) || '-' || SUBSTR(datum, 1, 2))
            """
            # https://stackoverflow.com/questions/21438088/sqlite-order-by-date-yyyy-mm-dd-format thanks to Rahul Panzade
        ).fetchall()

    @staticmethod
    def get_all_events_with_druzina():
        db = get_db()
        return db.execute(
            """ 
                SELECT druzina.jmeno AS jmeno_druziny, id_akce, id_druzina 
                FROM druzina 
                INNER JOIN druzina_akce ON druzina_id_druzina=id_druzina
                INNER JOIN akce ON akce_id_akce=id_akce
                ORDER BY (SUBSTR(datum, 7, 4) || '-' || SUBSTR(datum, 4, 2) || '-' || SUBSTR(datum, 1, 2))
            """
        ).fetchall()

    @staticmethod
    def get_event_by_id(id_akce):
        db = get_db()
        return db.execute(
            "SELECT * FROM akce WHERE id_akce=?", [id_akce]
        ).fetchone()

    @staticmethod
    def update_event_by_id(akce_data):
        db = get_db()
        db.execute(
            "UPDATE akce SET jmeno=?, datum=STRFTIME('%d.%m.%Y', ?), misto=?, zacatek_akce=STRFTIME('%d.%m.%Y', ?), konec_akce=STRFTIME('%d.%m.%Y', ?), popis=? WHERE id_akce=?", akce_data
        )
        db.commit()

    @staticmethod
    def delete_event_by_id(id_akce):
        db = get_db()
        db.execute(
            "DELETE FROM akce WHERE id_akce=?", [id_akce]
        )
        db.commit()

    @staticmethod
    def get_dochazka_by_user_and_akce_id(id_user, id_akce):
        db = get_db()
        return db.execute(
            "SELECT * FROM dochazka WHERE user_id_user=? AND akce_id_akce=?", [id_user, id_akce]
        ).fetchone()
   
    @staticmethod
    def change_dochazka(dochazka, id_user, id_akce, duvod=""):
        db = get_db()
        already_in = db.execute(
            "SELECT * FROM dochazka WHERE user_id_user=? AND akce_id_akce=?", [id_user, id_akce]
        ).fetchone()

        if already_in is None:
            db.execute(
                "INSERT INTO dochazka (dochazka, duvod, user_id_user, akce_id_akce) VALUES(?, ?, ?, ?)", [dochazka, duvod, id_user, id_akce]
            )
            db.commit()
        else:
            db.execute(
                "UPDATE dochazka SET dochazka=?, duvod=? WHERE user_id_user=? AND akce_id_akce=?", [dochazka, duvod, id_user, id_akce]
            )
            db.commit()
    
    @staticmethod
    def set_public(id_akce):
        db = get_db()
        db.execute(
            "UPDATE akce SET je_public=1 WHERE id_akce=?", [id_akce]
        )
        db.commit()
