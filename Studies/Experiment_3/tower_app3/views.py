from flask import render_template, request, make_response, redirect, session, url_for
from . import app, db
from .models import Subject, Trial
import datetime


@app.route('/', methods=['GET'])
def choose():
    if request.method == 'GET':
        return render_template('chooseuradventure.html')


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'GET':
        '''
        for condition in ['animate_rational', 'animate_moral', 'inanimate_rational', 'inanimate_moral']:
            if condition.split('_')[0] == 'inanimate':
                n_condition = 1
            else:
                n_condition = 2
            if len(Subject.query.filter_by(exp_cond=condition, completion=1).all()) < n_condition:
                session['cond'] = condition.split('_')[0]
                session['norm'] = condition.split('_')[1]
                break
            else:
                continue
        '''
        return render_template('/consent.html', cond='animate', norm='rational')


    if request.method == 'POST':
        print('New Subject!')
        dd = request.get_json(force=True)[0]
        session['prolificID'] = dd['prolificID']
        session['jspsychID'] = dd['jspsychID']
        if dd['experiment_section'] == 'consent':  # After consent
            subj = Subject(date=datetime.datetime.now(),
                           prolificID=dd['prolificID'],
                           jspsychID=dd['jspsychID'],
                           exp_cond=dd['experiment_condition'])
            db.session.add(subj)
            db.session.commit()
        return redirect(url_for('experiment'))#make_response(200)


@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.method == 'GET':
        return render_template('experiment.html', jsID=session['jspsychID'], proID=session['prolificID'],
                               cond='animate', norm='rational')

    if request.method == 'POST':
        dd = request.get_json(force=True)[0]
        sid = Subject.query.filter_by(jspsychID=dd['jspsychID']).first()
        if dd['experiment_section'] == 'first_video':
            session['s1'] = dd['stimulus'][0]
        if dd['experiment_section'] == 'test_video':
            tdat = Trial(prolificID=dd['prolificID'],
                         jspsychID=dd['jspsychID'],
                         time_elapse=dd['time_elapsed'],
                         stim1=session['s1'],
                         stim2=dd['stimulus'][0],
                         Q0=str(dd['response_0']),
                         Q1=str(dd['response_1']),
                         Q2=str(dd['response_2']),
                         Q3=str(dd['response_3']),
                         Q0_rt=str(dd['rt_0']),
                         Q1_rt=str(dd['rt_1']),
                         Q2_rt=str(dd['rt_2']),
                         Q3_rt=str(dd['rt_3']),
                         subject_id=sid.id,
                         anim_check=False,
                         tower_check=False,
                         agent_check=False
                         )
            db.session.add(tdat, sid)
            db.session.commit()
        # For comprehension checks, the last check in DB where value is True is one that was incorrect if multiple entries for single subject
        if dd['experiment_section'] == 'anim_check':
            subdat = Trial.query.filter_by(jspsychID=dd['jspsychID']).all()[-1]
            subdat.anim_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'tower_check':
            subdat = Trial.query.filter_by(jspsychID=dd['jspsychID']).all()[-1]
            subdat.tower_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'agent_check':
            subdat = Trial.query.filter_by(jspsychID=dd['jspsychID']).all()[-1]
            subdat.agent_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'feedback':
            subdat = Trial.query.filter_by(jspsychID=dd['jspsychID']).all()[-1]
            subdat.sub_feedback1 = dd['response']['Q0']
            subdat.sub_feedback2 = dd['response']['Q1']
            sid.complete_time = datetime.datetime.now()
            sid.completion = True
            db.session.add(subdat, sid)
            db.session.commit()
        if dd['experiment_section'] == 'debrief':
            sid.complete_time = datetime.datetime.now()
            sid.completion = True
            db.session.add(sid)
            db.session.commit()
        return make_response("", 200)

