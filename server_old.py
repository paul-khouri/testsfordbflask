from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sgdjkdgjdfgkdjfgk"
db_path = 'data_netball/netball.sqlite'


@app.route('/')
def index():
    sql = """select game_id, strftime('%Y-%m-%d ', game_date) as "Date", strftime('%H:%M', game_date) as "Time", team_1, team_2 from game"""
    draw = run_search_query_tuples(sql,(),db_path, True)
    return render_template("draw.html", games=draw)


@app.route('/results')
def results():
    sql = """select strftime('%Y-%m-%d ', game_date) as "Date", team_1,score_1, team_2, score_2 from game"""
    scores = run_search_query_tuples(sql,(),db_path, True)
    return render_template("results.html", scores=scores)



@app.route('/addscore' , methods=['GET', 'POST'])
def addscore():
    data = request.args
    print(data)
    if request.method == 'GET':
        sql="""select team_1, score_1, team_2, score_2 from game where game_id=? """
        value_tuple=(data['id'])
        team_data = run_search_query_tuples(sql, value_tuple, db_path, True)
        print(team_data[0])
        return render_template("netball_U_score.html", team_data=team_data[0], id=data['id'])
    elif request.method == 'POST':
        f = request.form
        print(f)
        sql="update game set score_1=?,score_2=? where game_id=?"
        values_tuple = (f['score_1'],f['score_2'],data['id'])
        result = run_commit_query(sql, values_tuple,db_path)
        return redirect(url_for('index'))


@app.route('/allscores' , methods=['GET', 'POST'])
def allscores():
    data = request.args
    complete = False
    if 'complete' in data.keys():
        complete = True
    sql = """select game_id,game_date, team_1, score_1, team_2, score_2 from game """
    value_tuple = ()
    team_data = run_search_query_tuples(sql, value_tuple, db_path, True)
    if request.method == 'GET':
        return render_template("netball_manage_scores.html", team_data=team_data, complete=complete)
    elif request.method == 'POST':
        data = request.args
        f = request.form
        print(f)
        for k in f.keys():
            x=k.split(",")
            print(x)

        sql = "update game set score_1=?,score_2=? where game_id=?"
        values_tuple = (f['score_1'], f['score_2'], data['id'])
        result = run_commit_query(sql, values_tuple, db_path)
        return redirect(url_for('allscores', complete="True"))



if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=80)