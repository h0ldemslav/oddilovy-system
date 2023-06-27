import hashlib
from database.database import get_db
import config


class UserService():
    @staticmethod
    def verify(login, password):
        db = get_db()
        hashed_passorwd = hashlib.sha256(f"{password}{config.PASSWORD_SALT}".encode())

        user = db.execute(
            """
                SELECT *
                FROM user
                JOIN role ON (role_id_role = role.id_role)
                WHERE login = ? AND heslo = ?
            """,
             [login, hashed_passorwd.hexdigest()]).fetchone()

        if user:
            return user
        else:
            return None

    @staticmethod
    def register_user(login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni,
                      id_role, je_aktivni=0, id_rodice=None, id_druzina_vede=None, id_druzina_clenem=None):
        hashed_passorwd = hashlib.sha256(f"{heslo}{config.PASSWORD_SALT}".encode())
        hashed_passorwd = hashed_passorwd.hexdigest()
        db = get_db()
        db.execute(
            "INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, je_aktivni, id_rodice, role_id_role, id_druzina_vede, id_druzina_clenem) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [login, hashed_passorwd, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, je_aktivni, id_rodice, id_role, id_druzina_vede, id_druzina_clenem]
        )
        db.commit()

    @staticmethod
    def get_children_by_parent(parent_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE id_rodice = ?", [parent_id]
        ).fetchall()

    @staticmethod
    def get_all_children_by_event(id_akce):
        db = get_db()
        sql = """
                SELECT DISTINCT id_user, jmeno_ditete, prijmeni_ditete, adresa, telefon, email
                FROM
                (SELECT akce_id_akce, id_user, user.jmeno AS jmeno_ditete, prijmeni AS prijmeni_ditete, adresa, telefon, email
                FROM user
                INNER JOIN dochazka ON id_user=user_id_user
                WHERE role_id_role=4 AND dochazka != 0
                ORDER BY jmeno_ditete, prijmeni_ditete) users
                INNER JOIN akce ON users.akce_id_akce=?
            """

        return db.execute(sql, [id_akce]).fetchall()

    @staticmethod
    def get_user_by_id(id):
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE id_user = ?", [id]
        ).fetchone()

    @staticmethod
    def get_user_name_by_id(id):
        db = get_db()
        return db.execute(
            "SELECT jmeno, prijmeni FROM user WHERE id_user = ?", [id]
        ).fetchone()

    @staticmethod
    def get_leaders(id_druziny):
        db = get_db()
        return db.execute(
            "SELECT jmeno, prijmeni FROM user WHERE id_druzina_vede IS NOT NULL AND id_druzina_clenem=?", [id_druziny]).fetchall()

    @staticmethod
    def get_vsechny_vedouci():
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE role_id_role=2"
        ).fetchall()

    @staticmethod
    def get_all_parents():
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE role_id_role=3"
        ).fetchall()