from flask import render_template, request, make_response, session
from . import app, db
from .models import Subject, Trial
import datetime


# Views


@app.route('/', methods=['GET', 'POST'])
def experiment():
    n_trls = 48
    if request.method == 'GET':
        return render_template('templates/experiment.html')
    if request.method == 'POST':
        d = request.get_json(force=True)[0]
        if d['trial_type'] == 'survey-text':
            session['prolificID'] = d['response']['prolificID']
            session['exp_trial'] = 0
        #elif 'In this experiment' in d['stimulus']:
            print('found a new subject:' + d['subjectID'])
            subj = Subject(jspsychID=d['subjectID'], prolificID=session.get('prolificID'), date=datetime.datetime.now())
            db.session.add(subj)
            db.session.commit()
        elif d['trial_type'] == 'video-slider-response':
            print('new trial data received')
            t = session.get('exp_trial')+1
            session['exp_trial'] = t
            subj = Subject.query.filter_by(jspsychID=d['subjectID']).first()
            trial_dat = Trial(trial_num=t,
                              jspsychID=d['subjectID'],
                              stimulus=d['stimulus'][0].split('/')[2],
                              block=d['trial_type'],
                              time_elapse=d['time_elapsed'],
                              cause_resp=d['response_1'],
                              anim_resp=d['response_2'],
                              cause_rt=d['rt_1'],
                              anim_rt=d['rt_2'],
                              trial_rt=d['rt'],
                              subject_id=subj.id)
            if t == n_trls:
                subj.completion = True
                db.session.add(subj)
            db.session.add(trial_dat)
            db.session.commit()
        '''
        elif d['trial_type'] == 'video-slider-response_CF':
            print('new trial data received')
            t = session.get('exp_trial')+1
            session['exp_trial'] = t
            subj = Subject.query.filter_by(jspsychID=d['subjectID']).first()
            #trial_dat = Trial.query.filter_by(jspsychID=d['subjectID'], stimulus=d['stimulus'][0].split('/')[2])
            #if trial_dat :
            #    trial_dat.cf_resp = d['cf_response']
            #    trial_dat.cf_rt = d['cf_rt']


            trial_dat = Trial(trial_num=t,
                              jspsychID=d['subjectID'],
                              stimulus=d['stimulus'][0].split('/')[2],
                              block=d['trial_type'],
                              time_elapse=d['time_elapsed'],
                              cf_resp=d['cf_response'],
                              cf_rt=d['cf_rt'],
                              trial_rt=d['rt'],
                              subject_id=subj.id)
            if t == n_trls:
                subj.completion = True
                db.session.add(subj)
            db.session.add(trial_dat)
            db.session.commit()
            '''
        return make_response("", 200)

