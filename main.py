from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
import sqlite3
from markupsafe import escape

from datetime import datetime, timedelta

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
exercises_dict = {
    'Bench Press': 'Chest',
    'Incline Bench Press': 'Chest',
    'Chest Fly': 'Chest',
    'Squat': ['Quads','Calfs'],
    'Lunge': 'Quads',
    'Leg Press': 'Quads',
    'PullUp': 'Back',
    'Deadlift': 'Back',
    'Barbell Row': 'Back',
    'Shoulder Press': 'Shoulders',
    'Lateral Raise': ['Shoulders','Triceps'],
    'Arnold Press': 'Shoulders',
    'Bicep Curl': 'Biceps',
    'Tricep Extension': 'Triceps',
    'Hammer Curl': 'Biceps'
}  # make createworkout.html pull from here
weight_standards = {
    'Bench Press': {
        'male': {
            'beginner': 40,        # these values are ballpark and are based on a weight you could do for 8 reps
            'intermediate': 60,
            'advanced': 80
        },
        'female': {
            'beginner': 20,
            'intermediate': 30,
            'advanced': 40
        }
    },
    'Incline Bench Press': {
        'male': {
            'beginner': 30,
            'intermediate': 50,
            'advanced': 70
        },
        'female': {
            'beginner': 15,
            'intermediate': 25,
            'advanced': 35
        }
    },
    'Chest Fly': {
        'male': {
            'beginner': 20,
            'intermediate': 30,
            'advanced': 40
        },
        'female': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        }
    },
    'Squat': {
        'male': {
            'beginner': 60,
            'intermediate': 90,
            'advanced': 120
        },
        'female': {
            'beginner': 30,
            'intermediate': 45,
            'advanced': 60
        }
    },
    'Lunge': {
        'male': {
            'beginner': 20,
            'intermediate': 30,
            'advanced': 40
        },
        'female': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        }
    },
    'Leg Press': {
        'male': {
            'beginner': 100,
            'intermediate': 150,
            'advanced': 200
        },
        'female': {
            'beginner': 50,
            'intermediate': 75,
            'advanced': 100
        }
    },
    'PullUp': {
        'male': {
            'beginner': 70,
            'intermediate': 80,
            'advanced': 90
        },
        'female': {
            'beginner': 35,
            'intermediate': 40,
            'advanced': 45
        }
    },
    'Deadlift': {
        'male': {
            'beginner': 60,
            'intermediate': 100,
            'advanced': 140
        },
        'female': {
            'beginner': 30,
            'intermediate': 50,
            'advanced': 70
        }
    },
    'Barbell Row': {
        'male': {
            'beginner': 30,
            'intermediate': 50,
            'advanced': 70
        },
        'female': {
            'beginner': 15,
            'intermediate': 25,
            'advanced': 35
        }
    },
    'Shoulder Press': {
        'male': {
            'beginner': 20,
            'intermediate': 30,
            'advanced': 40
        },
        'female': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        }
    },
    'Lateral Raise': {
        'male': {
            'beginner': 5,
            'intermediate': 7.5,
            'advanced': 10
        },
        'female': {
            'beginner': 2.5,
            'intermediate': 3.75,
            'advanced': 5
        }
    },
    'Arnold Press': {
        'male': {
            'beginner': 15,
            'intermediate': 25,
            'advanced': 35
        },
        'female': {
            'beginner': 7.5,
            'intermediate': 12.5,
            'advanced': 17.5
        }
    },
    'Bicep Curl': {
        'male': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        },
        'female': {
            'beginner': 5,
            'intermediate': 7.5,
            'advanced': 10
        }
    },
    'Tricep Extension': {
        'male': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        },
        'female': {
            'beginner': 5,
            'intermediate': 7.5,
            'advanced': 10
        }
    },
    'Hammer Curl': {
        'male': {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        },
        'female': {
            'beginner': 5,
            'intermediate': 7.5,
            'advanced': 10
        }
    }
}


app = Flask(__name__)
#permanent = True
#session.permanent_session_lifetime = timedelta(hours = 24)


with sqlite3.connect('login.db') as db:
    db.execute("PRAGMA foreign_keys = ON")


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/account')
def accountedit():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    con = sqlite3.connect('login.db')
    cursor = con.cursor()
    cursor.execute("SELECT Email, Weight, Height, Age, Sex, Bodyfat, Level FROM User WHERE Name=?", (username,))
    row = cursor.fetchone()
    con.close()
    if row:
        email, height, weight, age, sex, bodyfat, level = row#we dont need to prefill password.
    else:
        email = ""
        height = ""
        weight = ""
        age = ""
        sex = ""
        bodyfat = ""
        level = ""
    return render_template('editinfo.html',
                           currentemail=email,
                           currentheight=height,
                           currentweight=weight,
                           age=age,
                           sex=sex,
                           bodyfat=bodyfat,
                           currentlevel=level)

@app.route('/api/get-weekly-count', methods=['GET'])
def get_weekly_workout_count():
    if 'username' not in session:
        return jsonify({"error": "not authorized"}), 401
    username = session['username']
    print(username)
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        datetoday = datetime.today()
        print("datetoday: "+str(datetoday))
        print("timedetladatetoday.weekday: "+str(timedelta(days=datetoday.weekday())))
        print("datetoday.weekday: "+str(datetoday.weekday()))
        monday = datetoday - timedelta(days=datetoday.weekday())
        print("monday: " + str(monday))
        monday_str = monday.strftime('%Y-%m-%d')
        #selets number of distinct dates from workouts
        #distinct incase multipe workouts same day
        cursor.execute("""
            SELECT COUNT(DISTINCT Date) 
            FROM Workouts 
            WHERE User_ID = (SELECT User_ID FROM User WHERE Name = ?)
            AND Date >= ?
        """, (username, monday_str))


        countthisweek = str(cursor.fetchone()[0])
        print(countthisweek)
    return jsonify({"weekly_count": countthisweek})





@app.route('/api/update-user-info', methods=['POST'])
def update_user():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']
    form_data = request.form.to_dict()  # we need to convert the url encoded form to dictionary
    # so that we can iterate through submitted data

    allowed_fields = ['email', 'height', 'weight', 'age', 'sex', 'bodyfat', 'level']
    update = []
    update_values = []

    #through changed data, will be everything since prefills now though
    for field, value in form_data.items():
        if field in allowed_fields:
            update.append(f"{field}=?")
            update_values.append(value)

    update_values.append(username)

    connection = sqlite3.connect('login.db')
    sql_query = f"UPDATE User SET {', '.join(update)} WHERE Name=?"
    connection.execute(sql_query, update_values)
    connection.commit()
    connection.close()



    return f"Updated {update_values} for user"


@app.route('/add', methods=['POST'])  # updated add for new database schema
def add():
    if request.form['password'] != request.form['psw-repeat']:
        flash("Passwords ")
        return redirect(url_for('login'))  #

    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO User (Name, Email, Password, Height, Weight, Age, Sex, Bodyfat, Level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form['username'],
                request.form['email'],
                hashed_password,
                request.form.get('height'),
                request.form.get('weight'),
                request.form.get('age'),
                request.form.get('sex'),
                request.form.get('bodyfat'),
                request.form.get('level')
            ))
            db.commit()
            print("level" + request.form['level'])
            print(str(request.form.get('level')))
            flash(f"User '{request.form['username']}' added !")
            return redirect(url_for('home'))
        except Exception as e:  # let them kno its taken

            flash("An error occurred.")
            return redirect(url_for('login'))


@app.route('/verify', methods=['POST'])
def verify():
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT Password FROM User WHERE Name=?",
                      #we have to modify to select the password relative to a username
                       # rather than selecting both as now password is hashed.
                       (request.form['username'],))
        result = cursor.fetchone()
        print(result)
        # changed to fetch one instead of fetch all
        #becuase we don't want to access password from an array.

        #if len(result) == 0:  this if statment is no longer sufficient
        # as we need to use bcyprt in the backend to check if login valid.
           # return 'Username or password not recognized.'
        print(bcrypt.check_password_hash(result[0], request.form['password']))
        if not result or not bcrypt.check_password_hash(result[0], request.form['password']):
            flash("invalid password / username")

            return redirect(url_for('login'))
        else:
            session.permanent = True
            session['username'] = request.form['username']
            #get email also unless we force usernames to be unique
            return redirect(url_for('home'))


@app.route('/un')
def un():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in.'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/create_workout')
def createworkout():
    if 'username' not in session:  # ion my testing just becuase theres a username in session inst very good security, change
        return redirect(url_for('login'))
    return render_template('create_workout.html')


@app.route('/my_workouts')
def myworkouts():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('my_workouts.html')


@app.route('/weight-log')
def weight_log():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('weight_log.html')



@app.route('/muscleusage', methods=['POST'])
def muscleusage():
    if 'username' not in session:
        return jsonify({"error": "not authored"}), 401

    username = session['username']
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, Weight, Bodyfat, Level, Sex FROM User WHERE Name = ?", (username,))
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return jsonify({"error": "Username not in db, error"}), 404

    user_id = user_data[0]
    user_weight = user_data[1]
    user_bodyfat = user_data[2]  # shoudl already be percentage
    user_level = user_data[3]
    user_sex = user_data[4]

    # next check if there is already a user body for the particular user, if not create one
    cursor.execute("SELECT * FROM User_Body WHERE User_ID = ?", (user_id,))
    user_body = cursor.fetchone()
    if not user_body:
        cursor.execute("""
            INSERT INTO User_Body 
            (User_ID, Shoulders_Percent, Chest_Percent, Biceps_Percent, Triceps_Percent,
             Forearms_Percent, Abs_Percent, Quads_Percent, Calfs_Percent, Back_Percent, Last_Reset)
            VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, DATE('now'))
        """, (user_id,))
        conn.commit()
        cursor.execute("SELECT * FROM User_Body WHERE User_ID = ?", (user_id,))
        user_body = cursor.fetchone()

    if int(user_sex) == 0:
        user_gender = 'male'
    else:
        user_gender = 'female'
    level_dict = {'0': 'beginner', '1': 'intermediate', '2': 'advanced'}

    user_level_string = level_dict[str(user_level)]


    # first for loop below checks for any weight usage higher than standard
    # and creates a target volume for the user
    #we are going to adjust teh default if we are taking the default by the lean mass.
    user_exercise_ideal = {}  # dict going to map exercise name  ideal volume for that exercise
    for exercise_name in exercises_dict.keys():
        try:
            default_weight = weight_standards[exercise_name][user_gender][user_level_string]
        except Exception as e:
            print("VERY BIG PROBLEM, weight standards is missing something." + e)
            default_weight = 0
        default_ideal = default_weight * 12 * 8  # default ideal volume

        #select all exercises user has ever done
        cursor.execute("""
            SELECT No_Sets, No_Reps_Per_Set, Weight 
            FROM Exercise 
            JOIN Workouts ON Exercise.Workout_ID = Workouts.Workout_ID 
            WHERE Workouts.User_ID = ? AND Exercise.Exercise_Name = ?
        """, (user_id, exercise_name))
        records = cursor.fetchall()
        if not records:
            # if no record use the default ideal volume
            user_exercise_ideal[exercise_name] = default_ideal
        else:

            max_override = default_ideal #we need total volem greater than this in order to overide
            for rec in records:
                try:
                    sets_val = int(rec[0])
                    reps_val = int(rec[1])
                    weight_val = float(rec[2])
                except Exception as e:
                    print(e)
                    continue
                if reps_val < 5:
                    continue
                # if the user did >8 reps and used a weight higher than default, compute override ideal
                if reps_val > 8 and weight_val > default_weight:
                    override_ideal = weight_val * 12 * 8 # if exercise meets these requiremtns overide

                else:
                    override_ideal = default_ideal



                if override_ideal > max_override: # after calcuating the volume of a valid set, check its greater, then set.
                    max_override = override_ideal
            user_exercise_ideal[exercise_name] = max_override
            print("users exercise ideal is : "+ str(user_exercise_ideal[exercise_name]))



            
    # p2
    week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("""
           SELECT exercises.Exercise_Name, exercises.No_Sets, exercises.No_Reps_Per_Set, exercises.Weight 
           FROM Exercise as exercises
           JOIN Workouts ON exercises.Workout_ID = Workouts.Workout_ID 
           WHERE Workouts.User_ID = ? AND Workouts.Date >= ?
       """, (user_id, week_ago))
    weekly_exercises = cursor.fetchall()

    muscle_percentages = {}  # will accumulate exercise percentages per muscle group

    print("done ")
    print(weekly_exercises)
    for exercise in weekly_exercises:
        exercise_name, number_of_sets, number_of_reps, weight_used = exercise
        try:
            number_of_sets = int(number_of_sets)
            number_of_reps = int(number_of_reps)
            weight_used = float(weight_used)
        except Exception:
            continue
        if number_of_reps < 5:
            continue
       #volume calc
        actual_volume = number_of_sets * number_of_reps * weight_used

        # getting target volume set above
        ideal_exercise_volume = user_exercise_ideal[exercise_name]

        # calculate percent of ideal volume (as if they could only do that one exercse for those musle groups)

        exercise_percentage = (actual_volume / ideal_exercise_volume) * 100

        # get the muscle releveat to the exercise
        targetmuscle = exercises_dict[exercise_name] #muscle the exercise effects
        if isinstance(targetmuscle, str):  # make sure it's a list for iteration
            target_muscles = [targetmuscle]
        else:
            target_muscles = targetmuscle

        #now go back though and add percentages
        for muscle in target_muscles:
            if muscle in muscle_percentages:
                muscle_percentages[muscle] += exercise_percentage
            else:
                muscle_percentages[muscle] = exercise_percentage

    conn.close()
    print("User ideal vol per exercise:", user_exercise_ideal)
    print("Weekly percentage :", muscle_percentages)
    return jsonify(muscle_percentages)






''' newer but not latest
@app.route('/muscleusage', methods=['POST'])
def muscleusage():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()

    # Get userid as normal
    cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    user_id = user[0]


    cursor.execute("SELECT * FROM User_Body WHERE User_ID = ?", (user_id,))
    user_body = cursor.fetchone()
    if not user_body:
        # create record with new muscle percentages (much more now)
        cursor.execute("""
            INSERT OR IGNORE INTO User_Body 
            (User_ID, Shoulders_Percent, Chest_Percent, Biceps_Percent, Triceps_Percent, Forearms_Percent, Abs_Percent, Quads_Percent, Calfs_Percent, Last_Reset)
            VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, DATE('now'))
        """, (user_id,))
        conn.commit()

    # query the  current muscle usage values
    cursor.execute("""
        SELECT Shoulders_Percent, Chest_Percent, Biceps_Percent, Triceps_Percent, Forearms_Percent, Abs_Percent, Quads_Percent, Calfs_Percent 
        FROM User_Body WHERE User_ID = ?
    """, (user_id,))
    data = cursor.fetchone()
    conn.close()


    if not data:
        return jsonify({
            "shoulders": 0,
            "chest": 0,
            "biceps": 0,
            "triceps": 0,
            "forearms": 0,
            "abs": 0,
            "quads": 0,
            "calfs": 0
        })


    return jsonify({
        "shoulders": data[0],
        "chest": data[1],
        "biceps": data[2],
        "triceps": data[3],
        "forearms": data[4],
        "abs": data[5],
        "quads": data[6],
        "calfs": data[7]
    })

'''






'''
old muscle usge
@app.route('/muscleusage', methods=['POST'])
def muscleusage():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']

    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()

    cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
    #reused code often needed to fetch userid (not more secure in reality)
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404 #handle no user.

    user_id = user[0]

    cursor.execute("SELECT * FROM User_Body WHERE User_ID = ?", (user_id,))
    user_body = cursor.fetchone()
    # above line just checks if they already have a user_body.
    if not user_body:
        cursor.execute("""
            INSERT OR IGNORE INTO User_Body (User_ID, Shoulders_Percent, Back_Percent,
            Arms_Percent, Legs_Percent, Chest_Percent, Last_Reset)
            VALUES (?, 0, 0, 0, 0, 0, DATE('now'))
        """, (user_id,))
        #create basebody statistics if its not there
        # this is ran when user first accesses the home page,
        #, so there should be no chance their user body doesnt exist when we try update it.
        conn.commit()

    cursor.execute("""
        SELECT Shoulders_Percent, Back_Percent, Arms_Percent, Legs_Percent, Chest_Percent 
        FROM User_Body WHERE User_ID = ?
    """, (user_id,))
    data = cursor.fetchone() # creates touple of user body
    print(data)
    conn.close()

    if not data:
        return jsonify({"shoulders": 0, "back": 0, "arms": 0, "legs": 0, "chest": 0})

    return jsonify({
        "shoulders": data[0],
        "back": data[1],
        "arms": data[2],
        "legs": data[3],
        "chest": data[4] # return as dict.
    })
'''

## api section, mabe seperate file .
@app.route('/create-workout/submit', methods=['POST'])
def create_workout_submit():
    if 'username' not in session:
        return redirect(url_for('login'))
    print("session useranem:" + session['username'])

    username = session['username']
    with sqlite3.connect(
            'login.db') as db:  # we need to connect with foregn keeys enabled always, FIXES BUG WHERE STUFF DOESNT AUTOINCREMENT
        cursor = db.cursor()
        cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return "User not found", 404

        user_id = user[0]

        cursor.execute("""
            INSERT INTO Workouts (User_ID, Date, Field) VALUES (?, DATE('now'), 'General')
        """, (user_id,))
        workout_id = cursor.lastrowid
        exercises = zip(
            request.form.getlist('name[]'),
            request.form.getlist('sets[]'),
            request.form.getlist('reps[]'),
            request.form.getlist('weight[]')
        )

        for name, sets, reps, weight in exercises:
            cursor.execute("""
                INSERT INTO Exercise (Workout_ID, Exercise_Name, No_Sets, No_Reps_Per_Set, Weight)
                VALUES (?, ?, ?, ?, ?) 
            """, (workout_id, name, sets, reps, weight))  #question mark is %s

            # now udate user percents

            cursor.execute("SELECT * FROM User_Body WHERE User_ID = ?", (user_id,))
            user_body = cursor.fetchone()
            muscleused = exercises_dict[name]
            print(muscleused)

            amnttoadd = (int(sets) / 12) * 100
            print(muscleused)

            if type(muscleused) == str:
                cursor.execute(f"""
                UPDATE User_Body SET {muscleused}_Percent = {muscleused}_Percent + ?
                where User_ID = ?
                """, (amnttoadd, user_id))
            else:
                for muscle in muscleused:
                    cursor.execute(f"""
                    UPDATE User_Body SET {muscle}_Percent = {muscle}_Percent + ?
                    where User_ID = ?
                    """, (amnttoadd, user_id))

        db.commit()

    return redirect(url_for('myworkouts'))


@app.route('/workout/<workout_id>')
def workout_detail(workout_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
        user = cursor.fetchone()
        if not user: # fetch userid using username
            return "User not found", 404 # handle not being valid.
        user_id = user[0]

        cursor.execute("""
            SELECT 
                Exercise.Exercise_Name,
                Exercise.No_Sets,
                Exercise.No_Reps_Per_Set, 
                Exercise.Weight
            FROM Workouts
            JOIN Exercise ON Workouts.Workout_ID = Exercise.Workout_ID
            WHERE Workouts.Workout_ID = ? AND Workouts.User_ID = ?
        """, (workout_id, user_id))
        exercises = cursor.fetchall()
    # return all data for exercise in a workout, and pass that when rendering the html template.
    return render_template('workoutindividual.html', workout_id=workout_id, exercises=exercises)


@app.route('/api/get-workouts', methods=['GET'])
def get_workouts_api():
    if 'username' not in session:
        return {"message": "Unauthorized"}, 401
        #handle not being logged in.

    username = session['username']

    with sqlite3.connect('login.db') as db:

        cursor = db.cursor()

        cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return {"message": "User not found"}, 404
        user_id = user[0]
    #connectto db and using quried userid from username,
    # get all workout info for userid.
        cursor.execute("""
            SELECT 
                Workouts.Workout_ID,
                Workouts.Date, 
                Exercise.Exercise_Name, 
                Exercise.No_Sets, 
                Exercise.No_Reps_Per_Set, 
                Exercise.Weight
            FROM Workouts
            JOIN Exercise ON Workouts.Workout_ID = Exercise.Workout_ID
            WHERE Workouts.User_ID = ?
            ORDER BY Workouts.Date DESC
        """, (user_id,))
        workouts = cursor.fetchall()
    formatworkouts = [
        {
            "workout_id": row[0],
            "date": row[1],
            "exercise": row[2],
            "sets": row[3],## then return as dictionary
            "reps": row[4],
            "weight": row[5]
        }
        for row in workouts
    ]

    return {"workouts": formatworkouts}, 200


@app.route('/api/get-weight-log', methods=['GET'])
def get_weight_log():
    if 'username' not in session:
        return 401 # check if current user is logged in

    username = session['username']  # needs work when we implement better security / hashing

    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
        user = cursor.fetchone()  # to get the first row, but since user is unique it doesn't matter, but kinda safer
        if not user:
            return 404
        print(user)  # debuig
        user_id = user[0]

        cursor.execute("SELECT Date, Weight FROM WeightLog WHERE User_ID = ? ORDER BY Date ASC", (user_id,))
        weight_data = cursor.fetchall()

    formatted_data = [{"date": row[0], "weight": row[1]} for row in weight_data]
    print(formatted_data)
    return {"weight_log": formatted_data}, 200 # return weights for a user as a 2d array


# format to render with html.

@app.route('/api/add-weight', methods=['POST'])
def add_weight():
    if 'username' not in session:
        return {"message": "unauthorized"}, 401

    username = session['username']
    weight = request.get_json().get('weight')

    try:
        weight = float(weight)  # check number put in try because causing errors
    except ValueError:
        return {"message": "didnt enter"}, 400

    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()

        cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (username,))
        user = cursor.fetchone() # above select correct user id for username in session, rather than storing userid in session.
        # this may be more secure as not dependant on front end value? user potentially could access other users weight or something.
        if not user:
            return {"message": "user not found"}, 404

        user_id = user[0]

        cursor.execute("INSERT INTO WeightLog (User_ID, Weight, Date) VALUES (?, ?, DATE('now'))", (user_id, weight))
        db.commit() #add new row into db for new weight

    return {"message": " successful"}, 201


@app.route('/api/get-streak', methods=['POST'])
def get_streak():
    if 'username' not in session:
        return jsonify({"error": "Not logged in"}), 401
    username = session['username']


    with sqlite3.connect('login.db') as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT Date FROM Workouts 
            WHERE User_ID = (SELECT User_ID FROM User WHERE Name = ?)
        """, (username,))

        rows = cursor.fetchall()

    workout_dates = {datetime.strptime(row[0], '%Y-%m-%d').date() for row in rows}
    streak = 0
    current_date = datetime.today().date()
    while current_date in workout_dates:
        streak += 1
        current_date -= timedelta(days=1)
    return jsonify({"streak": streak})



app.secret_key = 'the random string'
app.run(port=5021, debug=True)
