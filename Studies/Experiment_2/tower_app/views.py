from flask import render_template, request, make_response, redirect
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
        return render_template('/consent.html')
    if request.method == 'POST':
        dd = request.get_json(force=True)[0]
        if dd['experiment_section'] == 'consent':  # After consent
            subj = Subject(date=datetime.datetime.now(),
                           prolificID=dd['prolificID'],
                           exp_cond='animate_rational')
            db.session.add(subj)
            db.session.commit()
        return redirect('/experiment', 200)#make_response(200)


@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.method == 'GET':
        return render_template('experiment.html')

    if request.method == 'POST':
        dd = request.get_json(force=True)[0]
        sid = Subject.query.filter_by(prolificID=dd['prolificID']).first()
        if dd['experiment_section'] == 'test_video':
            tdat = Trial(prolificID=dd['prolificID'],
                         time_elapse=dd['time_elapsed'],
                         cause_agent=str(dd['response_1']),
                         cause_patient=str(dd['response_2']),
                         cause_agent_rt=str(dd['rt_1']),
                         cause_patient_rt=str(dd['rt_2']),
                         subject_id=sid.id,
                         anim_check=False,
                         tower_check=False,
                         agent_check=False
                         )
            db.session.add(tdat, sid)
            db.session.commit()
        if dd['experiment_section'] == 'anim_check':
            subdat = Trial.query.filter_by(prolificID=dd['prolificID']).first()
            subdat.anim_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'tower_check':
            subdat = Trial.query.filter_by(prolificID=dd['prolificID']).first()
            subdat.tower_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'agent_check':
            subdat = Trial.query.filter_by(prolificID=dd['prolificID']).first()
            subdat.agent_check = True
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'feedback':
            subdat = Trial.query.filter_by(prolificID=dd['prolificID']).first()
            subdat.sub_feedback1 = dd['response']['Q0']
            subdat.sub_feedback2 = dd['response']['Q1']
            db.session.add(subdat)
            db.session.commit()
        if dd['experiment_section'] == 'debrief':
            sid.complete_time = datetime.datetime.now()
            sid.completion = True
            db.session.add(sid)
            db.session.commit()
        return make_response("", 200)

