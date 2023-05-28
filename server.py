from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from q_set import get_members
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sgdjkdgjdfgkdjfgk"
db_path = 'data_netball/netball.sqlite'


@app.route('/')
def index():
    sql = """ select d.draw_id as "game_id", 
    strftime('%Y-%m-%d ', d.draw_date) as "Date",
    strftime('%H:%M', d.draw_date) as "Time", 
    b.team_name as "team_1", 
    c.team_name as "team_2"
    from draw d
    join team b on  d.team_1 = b.team_id
    join team c on  d.team_2 = c.team_id """
    draw = run_search_query_tuples(sql, (), db_path, True)
    return render_template("netball.html", games=draw)


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
        sql = "select team_id, team_name from team"
        values_tuple=()
        result = run_search_query_tuples(sql,values_tuple,db_path, True)
        return render_template("addgame.html", teams=result)
    elif request.method == "POST":
        f = request.form
        print(f)
        draw_date = f['draw_date'].replace("T", " ")
        print(draw_date)
        sql = """ insert into draw( draw_date, team_1, team_2)
        values(?,?,?)"""
        values_tuple = (draw_date, f['team_1'], f['team_2'])
        result = run_commit_query(sql, values_tuple, db_path)
        return redirect(url_for('index'))


@app.route('/member')
def member():
    result = get_members(db_path)
    return render_template("member.html", members = result)



if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=80)
