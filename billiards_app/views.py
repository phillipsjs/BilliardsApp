from flask import render_template, request, make_response, session
from . import app, db
from .models import Subject, Trial
import datetime


# Views


@app.route('/', methods=['GET', 'POST'])
def experiment():
    n_trls = 4
    if request.method == 'GET':
        return render_template('experiment.html')
    if request.method == 'POST':
        d = request.get_json(force=True)[0]
        if d['trial_type'] == 'survey-text':
            session['prolificID'] = d['response']['prolificID']
            session['exp_trial'] = 0
        elif 'In this experiment' in d['stimulus']:
            print('found a new subject:' + d['subjectID'])
            subj = Subject(jspsychID=d['subjectID'], prolificID=session.get('prolificID'), date=datetime.datetime.now())
            db.session.add(subj)
            db.session.commit()
        else: #d['trial_type'] == 'video-slider-response':
            print('new trial data received')
            t = session.get('exp_trial')+1
            session['exp_trial'] = t
            subj = Subject.query.filter_by(jspsychID=d['subjectID']).first()
            trial_dat = Trial(trial_num=t,
                              jspsychID=d['subjectID'],
                              stimulus=d['stimulus'][0].split('/')[2],
                              time_elapse=d['time_elapsed'],
                              cause_resp=d['response_1'],
                              cf_resp=d['response_2'],
                              agent_resp=d['response_3'],
                              rt_1=d['rt_1'],
                              rt_2=d['rt_2'],
                              rt_3=d['rt_3'],
                              trial_rt=d['rt'],
                              subject_id=subj.id)
            if t == n_trls:
                subj.completion = True
                db.session.add(subj)
            db.session.add(trial_dat)
            db.session.commit()


        return make_response("", 200)

