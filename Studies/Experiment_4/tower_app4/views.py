from . import app, db
from .models import Subject
import numpy as np
import json
from flask import redirect, url_for, render_template, request, make_response
from datetime import datetime
from ast import literal_eval


comp_code = "XXXX"
cohort = 'combine_cohort'

@app.route('/')
def index():
    if request.args.get('PROLIFIC_PID') is not None:
        prolific_id = request.args.get('PROLIFIC_PID')
        session_id = request.args.get('SESSION_ID')
    # replace random with comments on prolific
    else:
        prolific_id = 'test'+str(np.random.random())  # request.args.get('PROLIFIC_PID')
        session_id = np.random.random()  # request.args.get('SESSION_ID')

    return redirect(url_for('welcome', PROLIFIC_PID=prolific_id, SESSION_ID=session_id))


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    msg1 = "Welcome!"
    msg2 = "Press the space bar to continue..."
    next_pg = "/consent"
    return render_template('message.html', msg1=msg1, msg2=msg2, next=next_pg)


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'GET':
        return render_template('consent.html')
    if request.method == 'POST':
        return make_response("200")


@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    if request.method == 'GET':
        s1 = np.random.choice(['phys_v1.mp4', 'anim_v1.mp4'])
        s2 = np.random.choice(['y_p_v2.mp4', 'p_y_v2.mp4'])
        t_dat = Subject(prolific_id=request.args.get('PROLIFIC_PID'), session_id=request.args.get('SESSION_ID'),
                        participation_date=datetime.now(), stim1=s1, stim2=s2, cohort=cohort)
        db.session.add(t_dat)
        db.session.commit()
    return redirect(url_for('instruct', PROLIFIC_PID=request.args.get('PROLIFIC_PID'),
                            SESSION_ID=request.args.get('SESSION_ID')))


@app.route('/instruct', methods=['GET', 'POST'])
def instruct():
    if request.method == 'GET':
        stim = ["In this task, you will observe two short video clips of different events.",
                "After the second video clip, you will be asked to make specific judgements about the events you observed.",
                "You will then be asked a few short questions about the events in the videos, so please do your best to watch carefully."]
        return render_template('instruct.html', title='Welcome', stim=stim, next="/stim1")


@app.route('/stim1', methods=['GET', 'POST'])
def stim1():
    if request.method == 'GET':
        t_dat = Subject.query.filter_by(prolific_id=request.args.get('PROLIFIC_PID')).first()
        vid = '/static/stim_vids/'+t_dat.stim1
        msg = "Please familiarize yourself with this video. You will be asked about a similar clip shortly."
        return render_template('s1.html', stim=vid, prompt=msg)


@app.route('/stim2', methods=['GET', 'POST'])
def stim2():
    if request.method == 'GET':
        t_dat = Subject.query.filter_by(prolific_id=request.args.get('PROLIFIC_PID')).first()
        vid = '/static/stim_vids/'+t_dat.stim2
        msg = "Please watch the video clip below carefully"
        if t_dat.stim2 == 'p_y_v2.mp4':
            r1 = ["The <span style='color:yellow;'>yellow</span> ball caused the tower to collapse.",
                  "The <span style='color:magenta;'>pink</span> ball caused the tower to collapse.",
                  "If the <span style='color:yellow;'>yellow</span> ball had not been there, the tower would have remained standing.",
                  "If the <span style='color:magenta;'>pink</span> ball had not been there, the tower would have remained standing."
                  ]
            r2 = ["If the <span style='color:yellow;'>yellow</span> ball had not been there, the tower would have remained standing.",
                "If the <span style='color:magenta;'>pink</span> ball had not been there, the tower would have remained standing.",
                "The <span style='color:yellow;'>yellow</span> ball caused the tower to collapse.",
                "The <span style='color:magenta;'>pink</span> ball caused the tower to collapse."]
            order = np.random.choice(['cause_first', 'CF_first'], p=[.5,.5])
            if order == 'cause_first':
                rating = r1
            else:
                rating = r2
            t_dat.question_order = order
            db.session.add(t_dat)
            db.session.commit()
        else:
            r1 = ["The <span style='color:magenta;'>pink</span> ball caused the tower to collapse.",
                  "The <span style='color:yellow;'>yellow</span> ball caused the tower to collapse.",
                  "If the <span style='color:magenta;'>pink</span> ball had not been there, the tower would have remained standing.",
                  "If the <span style='color:yellow;'>yellow</span> ball had not been there, the tower would have remained standing."
                  ]
            r2 = ["If the <span style='color:magenta;'>pink</span> ball had not been there, the tower would have remained standing.",
                  "If the <span style='color:yellow;'>yellow</span> ball had not been there, the tower would have remained standing.",
                 "The <span style='color:magenta;'>pink</span> ball caused the tower to collapse.",
                  "The <span style='color:yellow;'>yellow</span> ball caused the tower to collapse."
                  ]
            order = np.random.choice(['cause_first', 'CF_first'], p=[.5, .5])
            if order == 'cause_first':
                rating = r1
            else:
                rating = r2
            t_dat.question_order = order
            db.session.add(t_dat)
            db.session.commit()

        return render_template('s1.html', stim=vid, prompt=msg, ratings=rating)
    if request.method == 'POST':
        s_dat = request.get_json()
        t_dat = Subject.query.filter_by(prolific_id=s_dat['prolific_id']).first()
        t_dat.Q1 = str(s_dat['q_1'])
        t_dat.Q1_rt = datetime.fromtimestamp(s_dat['q_1_rt'] / 1000.0) - datetime.fromtimestamp(s_dat['q_1_onset'] / 1000.0)
        t_dat.Q2 = str(s_dat['q_2'])
        t_dat.Q2_rt = datetime.fromtimestamp(s_dat['q_2_rt'] / 1000.0) - datetime.fromtimestamp(s_dat['q_2_onset'] / 1000.0)
        t_dat.Q3 = str(s_dat['q_3'])
        t_dat.Q3_rt = datetime.fromtimestamp(s_dat['q_3_rt'] / 1000.0) - datetime.fromtimestamp(s_dat['q_3_onset'] / 1000.0)
        t_dat.Q4 = str(s_dat['q_4'])
        t_dat.Q4_rt = datetime.fromtimestamp(s_dat['q_4_rt'] / 1000.0) - datetime.fromtimestamp(s_dat['q_4_onset'] / 1000.0)
        db.session.add(t_dat)
        db.session.commit()
        return make_response('200')


@app.route('/a_check', methods=['GET', 'POST'])
def a_check():
    if request.method =='GET':
        t_dat = Subject.query.filter_by(prolific_id=request.args.get('PROLIFIC_PID')).first()
        return render_template('a_check.html', s1=t_dat.stim1, s2=t_dat.stim2)
    if request.method == 'POST':
        s_dat = request.get_json()
        subj = Subject.query.filter_by(prolific_id=s_dat['prolific_id']).first()
        subj.anim_check = True
        subj.tower_check = True
        db.session.add(subj)
        db.session.commit()
        return make_response('200')


@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
    if request.method =='GET':
        return render_template('thankyou.html', cc=comp_code)
    if request.method == 'POST':
        s_dat = request.get_json()
        subj = Subject.query.filter_by(prolific_id=s_dat['prolific_id']).first()
        subj.sub_feedback = s_dat['feedback']
        subj.complete = True
        db.session.add(subj)
        db.session.commit()
        return make_response('200')