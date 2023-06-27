from database.database import get_db
# import config


class ProgramService():
    @staticmethod
    def new_program(misto, popis, delka, doporuceny_vek=None):
        db = get_db()
        db.execute(
            "INSERT INTO program (misto_program, popis_program, delka, doporuceny_vek) VALUES (?, ?, ?, ?)",
            [misto, popis, delka, doporuceny_vek]
        )
        db.commit()

    
    @staticmethod
    def get_all_programs():
        db = get_db()
        return db.execute(
            "SELECT * FROM program"
        ).fetchall()

    @staticmethod
    def delete_program_with_id(id):
        db = get_db()
        db.execute("DELETE FROM program WHERE id_program=?", [id])    
        db.commit()   

    @staticmethod
    def get_program_by_id(id_program):
        db = get_db()
        return db.execute(
            "SELECT * FROM program WHERE id_program=?", [id_program]
        ).fetchone()     

    @staticmethod
    def update_program_by_id(program_data):
        db = get_db()
        db.execute(
            "UPDATE program SET misto_program=?, popis_program=?, delka=?, doporuceny_vek=? WHERE id_program=?", program_data
        )
        db.commit()    