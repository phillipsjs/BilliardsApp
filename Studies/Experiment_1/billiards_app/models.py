from . import db


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    jspsychID = db.Column(db.String, unique=True)
    prolificID = db.Column(db.String)
    completion = db.Column(db.Boolean)
    condition = db.Column(db.String)

    def __repr__(self):
        return '<Subject %r>' % self.id


class Trial(db.Model):
    __tablename__ = 'trials'
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.Integer)
    trial_num = db.Column(db.Integer)
    jspsychID = db.Column(db.String)
    stimulus = db.Column(db.String)
    time_elapse = db.Column(db.Float)
    cause_resp = db.Column(db.Integer)
    cf_resp = db.Column(db.Integer)
    anim_resp = db.Column(db.Integer)
    cause_rt = db.Column(db.Float)
    anim_rt = db.Column(db.Float)
    cf_rt = db.Column(db.Float)
    trial_rt = db.Column(db.Float)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def __repr__(self):
        return '<Subject %r>' % self.id

