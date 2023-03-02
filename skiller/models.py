from datetime import datetime
from skiller import db


class Users(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fullname = db.Column(db.String(100),nullable=False)
    gender= db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120)) 
    user_skill = db.Column(db.String(100),nullable=False)
    user_phone=db.Column(db.String(120),nullable=True) 
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)
    user_state=db.Column(db.String(100), nullable=True)
    #user_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))
    user_address = db.Column(db.String(255),nullable=False)
    user_pwd=db.Column(db.String(120),nullable=False)
    #set relationships
    #skiller_user=db.relationship('Skiller',back_populates='user_skiller')
    #project_users=db.relationship('Project', back_populates='users_project')
    #state_users = db.relationship('State', back_populates='users_state')
    #lga_users = db.relationship('Lga', back_populates='users_lga')


class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_fullname = db.Column(db.String(100),nullable=False)
    admin_email = db.Column(db.String(120)) 
    admin_password=db.Column(db.String(120),nullable=True)

"""class Category(db.Model):
    cat_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    cat_name=db.Column(db.String(100),nullable=False)"""

class Skill(db.Model):
    skill_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    skill_name=db.Column(db.String(100),nullable=False)
    #skiller_skill=db.relationship("Skiller", back_populates="skill_skiller")
    
class Album(db.Model):
    album_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    album_name=db.Column(db.String(100),nullable=True)
    Album_userid=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #relationship
    catalogue=db.relationship('Users',backref='user_album')


"""class Skiller(db.Model):
    skiller_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    #ForeignKey
    skiller_userid=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    skiller_skillid=db.Column(db.Integer, db.ForeignKey('skill.skill_id'))
    #set relationship
    skill_skiller=db.relationship("Skill", back_populates="skiller_skill")
    user_skiller = db.relationship("Users", back_populates="skiller_user")
    project_skiller=db.relationship('Project', back_populates='skiller_project')"""

"""class Project(db.Model):
    proj_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    proj_title=db.Column(db.String(255),nullable=False)
    #ForeignKey
    proj_skilleridid=db.Column(db.Integer, db.ForeignKey('skiller.skiller_id'))
    proj_useridid=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    project_details=db.Column(db.Text,nullable=False)
    #relationships
    users_project=db.relationship('Users', back_populates='project_users')
    skiller_project=db.relationship('Skiller', back_populates='project_skiller')"""



class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name = db.Column(db.String(100),nullable=False) 
    #set relationship
    #lga_state = db.relationship("Lga", back_populates="state_lga")
    #users_state = db.relationship('Users', back_populates='state_users')

"""class Lga(db.Model):
    lga_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    lga_name = db.Column(db.String(100),nullable=False)
    lga_stateid = db.Column(db.Integer, db.ForeignKey('state.state_id'))    
    #set relationships
    state_lga = db.relationship("State", back_populates="lga_state")
    #users_lga = db.relationship('Users', back_populates='lga_users')
    """

class Payment(db.Model):
    pay_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    #pay_donid = db.Column(db.Integer, db.ForeignKey('donation.don_id'),nullable=True)
    pay_date = db.Column(db.DateTime(),default=datetime.utcnow)
    pay_amount_deducted = db.Column(db.Float)
    pay_status = db.Column(db.Enum('pending','failed','paid'), nullable=False, server_default=('pending'))
    pay_ref = db.Column(db.String(20),nullable=False)
    pay_others = db.Column(db.Text(),nullable=True)
    #relationship
    #donation_deets = db.relationship('Donation',backref='paydeets')