from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "twoj-tajny-klucz-zmien-mnie"


# TODO: Skonfiguruj połączenie z bazą danych SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ski.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()

# TODO: Zainicjalizuj SQLAlchemy
db.init_app(app)

# TODO: Stwórz model Form (formularz rejestracji na wyjazd narciarski)


class Form(db.Model):
    __tablename__ = "forms"

    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), nullable=False)
    nazwisko = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    poziom_narciarski = db.Column(db.String(50), nullable=False)
    uwagi = db.Column(db.Text, nullable=True)
    data_rejestracji = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "email": self.email,
            "telefon": self.telefon,
            "poziom_narciarski": self.poziom_narciarski,
            "uwagi": self.uwagi,
            "data_rejestracji": self.data_rejestracji.isoformat(),
        }

    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    # password_hash = db.Column(db.String(256), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # articles = db.relationship('Article', backref='author', lazy=True, cascade='all, delete-orphan')

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }


@app.route("/")
def index():
    """Strona główna - lista wszystkich formularzy"""
    # TODO: Pobierz wszystkie formularze z bazy danych

    all = Form.query.all()

    print(all)

    # Tymczasowo - pusta lista
    forms = []

    return render_template("index.html", forms=forms)


@app.route("/formularz/<int:form_id>")
def formularz_detail(form_id):
    """Strona szczegółów pojedynczego formularza"""
    # TODO: Pobierz formularz o podanym ID

    # Tymczasowo - przykładowy obiekt
    form = {
        "id": form_id,
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "email": "jan@example.com",
        "telefon": "123456789",
        "poziom_narciarski": "średniozaawansowany",
        "uwagi": "Brak",
        "data_rejestracji": "2024-01-11",
    }

    return render_template("detail.html", form=form)


@app.route("/nowy", methods=["GET", "POST"])
def nowy_formularz():
    """Tworzenie nowego formularza rejestracji"""
    if request.method == "POST":
        # TODO: Pobierz dane z formularza
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")
        email = request.form.get("email")
        telefon = request.form.get("telefon")
        poziom_narciarski = request.form.get("poziom_narciarski")
        uwagi = request.form.get("uwagi")

        # TODO: Stwórz nowy obiekt Form

        new_form = Form(
            imie=imie,
            nazwisko=nazwisko,
            email=email,
            telefon=telefon,
            poziom_narciarski=poziom_narciarski,
            uwagi=uwagi,
        )

        # TODO: Dodaj do bazy danych i zapisz

        db.session.add(new_form)
        db.session.commit()

        flash("Formularz został pomyślnie utworzony!", "success")
        return redirect(url_for("index"))

    return render_template("nowy.html")


@app.route("/usun/<int:form_id>", methods=["POST"])
def usun_formularz(form_id):
    """Usuwanie formularza"""
    # TODO: Znajdź formularz i usuń go

    flash("Formularz został usunięty!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # TODO: Utwórz tabele w bazie danych przy pierwszym uruchomieniu

    with app.app_context():
        db.create_all()

    app.run(debug=True)
