from . import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    prolificID = db.Column(db.String)
    jspsychID = db.Column(db.String)
    completion = db.Column(db.Boolean)
    compelete_time = db.Column(db.DateTime)
    exp_cond = db.Column(db.String)
    trials = db.relationship('Trial', backref='subject', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Subject %r>' % self.id


class Trial(db.Model):
    __tablename__ = 'trials'
    id = db.Column(db.Integer, primary_key=True)
    prolificID = db.Column(db.String)
    jspsychID = db.Column(db.String)
    time_elapse = db.Column(db.Float)
    cause_agent = db.Column(db.VARCHAR(20))
    cause_patient = db.Column(db.VARCHAR(20))
    cause_agent_rt = db.Column(db.VARCHAR(50))
    cause_patient_rt = db.Column(db.VARCHAR(50))
    anim_check = db.Column(db.Boolean)
    tower_check = db.Column(db.Boolean)
    agent_check = db.Column(db.Boolean)
    sub_feedback1 = db.Column(db.VARCHAR(50))
    sub_feedback2 = db.Column(db.VARCHAR(50))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def __repr__(self):
        return '<Subject %r>' % self.id