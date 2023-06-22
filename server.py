from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from q_set import get_members, get_class, get_class_registrations, get_registrations_members
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sgdjkdgjdfgkdjfgk"
db_path = 'data_netball/netball.sqlite'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/draw')
def draw():
    sql = """ select d.draw_id as "game_id", 
    strftime('%Y-%m-%d ', d.draw_date) as "Date",
    strftime('%H:%M', d.draw_date) as "Time", 
    b.team_name as "team_1", 
    c.team_name as "team_2"
    from draw d
    join team b on  d.team_1 = b.team_id
    join team c on  d.team_2 = c.team_id 
    order by Date desc, Time asc"""
    draw = run_search_query_tuples(sql, (), db_path, True)
    return render_template("draw.html", games=draw)


@app.route('/results')
def results():
    sql = """ select d.draw_id as "game_id", 
    strftime('%Y-%m-%d ', d.draw_date) as "Date", 
    d.score_1 as "score_1", 
    d.score_2 as "score_2", 
    b.team_name as "team_1", 
    c.team_name as "team_2"
    from draw d
    join team b on  d.team_1 = b.team_id
    join team c on  d.team_2 = c.team_id """
    scores = run_search_query_tuples(sql,(),db_path, True)
    return render_template("results.html", scores=scores)


@app.route('/addscore' , methods=['GET', 'POST'])
def addscore():
    data = request.args
    print(data)
    if request.method == 'GET':
        sql = """select 
        b.team_name as "team_1", 
        c.team_name as "team_2"
        from draw d
        join team b on  d.team_1 = b.team_id
        join team c on  d.team_2 = c.team_id 
        where d.draw_id = ?"""
        values_tuple = (data['id'],)
        print(type(values_tuple))
        team_data = run_search_query_tuples(sql, values_tuple, db_path, True)
        return render_template("netball_U_score.html", team_data=team_data[0], id=data['id'])
    elif request.method == 'POST':
        f = request.form
        print(f)
        sql="update draw set score_1=?,score_2=? where draw_id=?"
        values_tuple = (f['score_1'],f['score_2'],data['id'])
        result = run_commit_query(sql, values_tuple,db_path)
        return redirect(url_for('index'))


@app.route('/allscores' , methods=['GET', 'POST'])
def allscores():
    data = request.args
    complete = False
    if 'complete' in data.keys():
        complete = True
    sql = """ select 
        d.draw_id as "game_id",
        d.draw_date as "game_date",
        d.score_1 as "score_1",
        d.score_2 as "score_2",
        b.team_name as "team_1", 
        c.team_name as "team_2"
        from draw d
        join team b on  d.team_1 = b.team_id
        join team c on  d.team_2 = c.team_id 
        """
    value_tuple = ()
    team_data = run_search_query_tuples(sql, value_tuple, db_path, True)
    if request.method == 'GET':
        return render_template("netball_manage_scores.html", team_data=team_data, complete=complete)
    elif request.method == 'POST':
        data = request.args
        f = request.form
        print(f)
        sql = "update draw set score_1=?,score_2=? where draw_id=?"
        values_tuple = (f['score_1'], f['score_2'], data['id'])
        result = run_commit_query(sql, values_tuple, db_path)
        return redirect(url_for('allscores', complete="True"))


@app.route('/addgame', methods=['GET', 'POST'])
def addgame():
    if request.method == "GET":
        # get teams for option list
        sql = "select team_id, team_name from team"
        values_tuple=()
        result = run_search_query_tuples(sql,values_tuple,db_path, True)
        data=request.args
        if 'id' in data.keys():
            sql = "select draw_date, team_1, team_2 from draw where draw_id=?"
            values_tuple = (data['id'],)
            selected_draw = run_search_query_tuples(sql, values_tuple, db_path, True)
            draw_date=selected_draw[0]['draw_date'].replace(" ", "T")
            print(draw_date)
            return render_template("addgame.html",
                                   teams=result,
                                   draw_date = draw_date,
                                   selected_draw=selected_draw[0],
                                   id=data['id'])
        else:
            return render_template("addgame.html", teams=result)
    elif request.method == "POST":
        f = request.form
        data = request.args
        if all(value in data.keys() for value in ['id', 'task']):
            if data['task'] == "update":
                sql = "update draw set draw_date=? , team_1 = ?, team_2 = ? where draw_id =?"
                draw_date = f['draw_date'].replace("T", " ")
                values_tuple = (draw_date, f['team_1'], f['team_2'], data['id'])
                result = run_commit_query(sql, values_tuple, db_path)
                print("Updating")
                return redirect(url_for('draw'))
            elif data['task'] == "delete":
                sql = "delete from draw where draw_id=?"
                values_tuple= (data['id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                return redirect(url_for('draw'))
            else:
                return "<h1>  Draw: Something went wrong </h1>"
        else:
            draw_date = f['draw_date'].replace("T", " ")
            print(draw_date)
            sql = """ insert into draw( draw_date, team_1, team_2)
            values(?,?,?)"""
            values_tuple = (draw_date, f['team_1'], f['team_2'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('draw'))


@app.route('/member')
def member():
    result = get_members(db_path)
    return render_template("member.html", members = result)


@app.route('/classes')
def classes():
    result = get_class(db_path)
    return render_template("class.html", classes = result)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    message = None
    errormessage = None
    if request.method == "GET":
        data = request.args
        if 'id' not in data.keys():
            return render_template("error.html", message="No valid id")
        elif 'title' not in data.keys():
            return render_template("error.html", message="No valid title")
        if 'message' in data.keys():
            message = data['message']
        if 'errormessage' in data.keys():
            message = data['errormessage']
        if 'delete_id' in data.keys():
            sql = "delete from registration where member_id = ? and class_id=?"
            values_tuple = (data['delete_id'],data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
        result = get_class_registrations(data['id'], db_path)
        member_result = get_members(db_path)
        return render_template("registration.html",
                               id=data['id'],
                               title=data['title'],
                               registrations=result,
                               members=member_result,
                               message=message,
                               errormessage=errormessage)
    elif request.method == "POST":
        f = request.form
        data = request.args
        sql = """insert into registration(member_id, class_id, registration_date, attendance)
         values(
         (select member_id from member where member_name=?),
         (select class_id from class where class_name=? ), 
         date('now'), 0)"""
        values_tuple=(f['member'], f['title'])
        result = run_commit_query(sql, values_tuple, db_path)
        if result is False:
            errormessage = "Something went wrong, please check that name is not already in this course"
        else:
            message = "Successfully added"
        return redirect(url_for('registration',
                                id=data['id'],
                                title=data['title'],
                                message=message,
                                errormessage=errormessage))

        # return render_template("error.html", message="Posted")

@app.route('/member_classes', methods=["GET","POST"])
def member_classes():
    if request.method == "GET":
        result = get_registrations_members(db_path)
        return render_template('member_classes.html', member_classes=result)
    elif request.method == "POST":
        sql="delete from registration"
        result = run_commit_query(sql, (), db_path)
        print(result)
        f=request.form
        for x in f:
            c = f.getlist(x)
            for row in c:
                sql = """insert into registration(member_id, class_id,registration_date, attendance)
                values(
                (select member_id from member where member_name = ?),
                (select class_id from class where class_name = ?),
                datetime('now', 'localtime'),
                0)"""
                values_tuple = (x, row)
                result = run_commit_query(sql, values_tuple, db_path)
            #print(f.getlist(x))
        return redirect(url_for('member_classes'))



if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=80)
