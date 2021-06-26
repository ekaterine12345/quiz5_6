from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///country.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(30), nullable=False)
    population = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'country: {self.country_name}; population: {self.population}; area: {self.area}'


# db.create_all()
# b1 = Country.query.first()
# print(b1)


def get_info():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    r = requests.get(url)
    print(r)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')
    all_countries = tbody.find_all('tr')
    for each in all_countries:
        info = each.find_all('td')
        position = info[0].text
        country = info[1].text
        population = info[2].text
        land_area = info[6].text
        population = population.replace(',', '')
        land_area = land_area.replace(',', '')
        print(position, country, float(population), float(land_area))
        c = Country(id=position, country_name=country, population=float(population), area=float(land_area))

        db.session.add(c)
        db.session.commit()

# get_info()

@app.route('/home')
@app.route('/')
def home():
    all_countries = Country.query.all()
    return render_template('index.html', all_countries=all_countries)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('Please enter all fields!', 'error')
        else:
            session['username'] = username
            return redirect(url_for('user'))

    return render_template('login.html')


@app.route('/user')
def user():
    my_countries = ['Georgia', 'France', 'USA', 'China', 'Japan', 'England']
    return render_template('user.html', my_countries=my_countries)


@app.route('/country_images')
def country_images():
    return render_template('country_images.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)
