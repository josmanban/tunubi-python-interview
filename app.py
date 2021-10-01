from flask import Flask, request, json, Response
from flask import Flask, request, json, Response
from util.mongo_client_wrapper import MongoAPI
import pdb


app = Flask(__name__)
app.config['DB_NAME'] = 'polls'

@app.route('/')
def base():
    return "status:up"

@app.route('/add_answer', methods=('POST',))
def answers_post():
    data = request.json
    res = MongoAPI(app.config['DB_NAME'],"answers").write(data)
    return Response(response=json.dumps(res),status=200,mimetype='application/json')

@app.route('/add_poll', methods=('POST',))
def polls_post():
    data = request.json
    res = MongoAPI(app.config['DB_NAME'],"polls").write(data)
    return Response(response=json.dumps(res),status=200,mimetype='application/json')    

@app.route('/get_polls')
def polls_get():
    db_name=app.config['DB_NAME']
    polls = MongoAPI(db_name,"polls").read()
    answers = MongoAPI(db_name,"answers").read()
    for poll in polls:
        poll['answers'] = [answer for answer in answers if answer['poll_id'] == poll['_id']]
    return Response(response=json.dumps(polls),status=200,mimetype='application/json')


if __name__ == "__main__":
    print('up')
    app.run(host='0.0.0.0', debug=True)




