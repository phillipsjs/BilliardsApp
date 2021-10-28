from flask import render_template, request, make_response, session
from . import app, db
from .models import Subject, Trial
import datetime


@app.route('/', methods=['GET'])
def choose():
    if request.method == 'GET':
        return render_template('chooseuradventure.html')


@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.method == 'GET':
        return render_template('experiment.html')

    if request.method == 'POST':
        dd = request.get_json(force=True)[0]
        if dd['trial_type'] == 'html-keyboard-response': # After instruction screen
            subj = Subject(date=datetime.datetime.now(),
                           jspsychID=dd['subjectID'],
                           prolificID=dd['prolificID'],
                           anim_cond='inanimate_rational')
            db.session.add(subj)
            db.session.commit()
        if dd['trial_type'] == 'video-slider-response':
            print(dd)
            sid = Subject.query.filter_by(jspsychID=dd['subjectID']).first()
            sid.complete_time = datetime.datetime.now()
            sid.completion = True

            tdat = Trial(jspsychID=dd['subjectID'],
                         time_elapse=dd['time_elapsed'],
                         cause_agent=str(dd['response_1']),
                         cause_patient=str(dd['response_2']),
                         cause_agent_rt=str(dd['rt_1']),
                         cause_patient_rt=str(dd['rt_2']),
                         subject_id=sid.id)
            db.session.add(tdat, sid)
            db.session.commit()
        if dd['trial_type'] == 'survey-text':
            sid = Subject.query.filter_by(jspsychID=dd['subjectID']).first()
            sid.feedback = str(dd['response'])
            db.session.add(sid)
            db.session.commit()

        return make_response("", 200)

