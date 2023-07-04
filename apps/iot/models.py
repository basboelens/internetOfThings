from apps import db 

class Verbruik(db.Model):

    __tablename__ = "Verbruik"

    id = db.Column(db.Integer, primary_key=True)
    verbruik = db.Column(db.REAL)
    user = db.Column(db.Text, db.ForeignKey("Users.username"))
    date = db.Column(db.DateTime)

    def __init__(self, verbruik, user, date):
        self.verbruik = verbruik
        self.user = user
        self.date = date

    def __repr__(self):
        return f"Gebruiker: {self.user} heeft op datum:{self.date} het volgende verbruikt:{self.verbruik}."
    