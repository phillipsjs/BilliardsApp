from . import db


class Subject(db.Model):
    __tablename__ = 'subjects'
    prolific_id = db.Column(db.String(64), unique=True, primary_key=True, index=True)
    session_id = db.Column(db.VARCHAR(300))
    participation_date = db.Column(db.DateTime)
    browser = db.Column(db.VARCHAR(80))
    browser_version = db.Column(db.VARCHAR(80))
    operating_sys = db.Column(db.VARCHAR(80))
    operating_sys_lang = db.Column(db.VARCHAR(80))
    GMT_timestamp = db.Column(db.DateTime)
    stim1 = db.Column(db.VARCHAR(200))
    stim2 = db.Column(db.VARCHAR(2000))
    Q1 = db.Column(db.VARCHAR(100))
    Q2 = db.Column(db.VARCHAR(100))
    Q3 = db.Column(db.VARCHAR(100))
    Q4 = db.Column(db.VARCHAR(100))
    Q1_rt = db.Column(db.Interval)
    Q2_rt = db.Column(db.Interval)
    Q3_rt = db.Column(db.Interval)
    Q4_rt = db.Column(db.Interval)
    anim_check = db.Column(db.Boolean)
    tower_check = db.Column(db.Boolean)
    sub_feedback = db.Column(db.VARCHAR(500))
    complete = db.Column(db.Boolean)
    cohort = db.Column(db.VARCHAR(200))
    question_order = db.Column(db.VARCHAR(200))



