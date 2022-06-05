from flask import Flask, jsonify, url_for, render_template, request, redirect, abort
from flask_migrate import Migrate
from models import db, Person, Team
import sys

app = Flask(__name__)

# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/folio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    teams = Team.query.all()
    return render_template('index.html', teams=teams)


@app.route('/teams/<int:team_id>')
def get_team(team_id):
    team = Team.query.get(team_id)
    persons = []
    if team:
        persons = team.persons
    return render_template('team.html', team=team, persons=persons)


@app.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    new_team_name = request.form.get('team_name', None)
    if new_team_name is None:
        return abort(400)

    team = Team.query.get(team_id)
    if team is None:
        return abort(400)

    try:
        team.name = new_team_name
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get(team_id)
    if team is None:
        return abort(400)

    try:
        db.session.delete(team)
        # db.session.delete(team2)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        "message": "Delete Successful"
    })


@app.route('/teams', methods=['GET'])
def create_team_form():
    return render_template('add_team.html')


@app.route('/teams', methods=['POST'])
def create_team():
    team_name = request.form.get('team_name', None)
    if team_name is not None:
        try:
            team = Team(name=team_name)
            db.session.add(team)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    return redirect(url_for('index'))


@app.route('/persons')
def get_person():
    search_term = request.args.get("search_term", None)
    user = Person.query.filter(Person.firstname == search_term)
    return render_template('person.html', user=user)


# Launch
if __name__ == '__main__':
    app.run(port=1234, debug=True)
