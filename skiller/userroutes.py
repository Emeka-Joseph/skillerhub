import os, random, string,json
from flask import render_template, redirect, flash, session, request, url_for,jsonify
from sqlalchemy import desc,asc,or_,func

#from flask import flask_mysql

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email



#3rd party importations
from skiller.models import State,Users, Album,Skill,DisplayPictures #import the required tables from the database
from skiller.forms import JoinForm
from skiller import app, db,CSRFProtect

def generate_name(): 
    filename = random.sample(string.ascii_lowercase,10) 
    return ''.join(filename) 

class JoinForm(FlaskForm):
    fullname = StringField('fullname:',validators=[DataRequired(), Regexp("^[A-Za-z]*",0,"Your Fullname must not contain anyother character except string")], render_kw={'placeholder':"Enter your fullname"})

    gender = SelectField('gender:',validators=[DataRequired('Kindly select your gender to proceed')])

    email = StringField('Your Email:',validators=[Email(message="Hello, please enter a valid email"), DataRequired(message="your email address is needed in order to join")])
    
    password = PasswordField('password:', validators=[DataRequired(length(min=6,message='your passowrod must be at least 6 digits'))])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Re-enter password to match')])
    
    submit = SubmitField('Join')



@app.route('/') 
def home():
    id = session.get('user')
    deets = db.session.query(Users).get(id)
    allskill = Skill.query.all()
    allstates = State.query.all()
    return render_template('user/index.html',deets=deets,allskill=allskill,allstates=allstates) 


    
@app.route('/search',methods=['POST','GET'])
def search():
    allstates = State.query.all()
    skill = Skill.query.all()
    allskill = Skill.query.all()
     
    if request.method=='POST':
        deets = db.session.query(Users).all()
        beta = db.session.query(Users).first()
        searchdpone = beta.user_dpone
        skill_in_need = request.form.get('skill')
        search_state = request.form.get('statename')
        skillset = db.session.query(Users).filter(Users.user_skill==skill_in_need)
        if skill_in_need=='' or skill_in_need==None:
             return redirect('/')
        else:
            return render_template('user/search.html',deets=deets,skill=skill,skillset=skillset, skill_in_need=skill_in_need,random=random, beta=beta,searchdpone=searchdpone,search_state=search_state,allstates=allstates,allskill=allskill)
    


@app.route('/searchbyloc',methods=['POST','GET'])
def searchbyloc():
    #displays = DisplayPictures.query.all() 
    #for t in propics
    allstates = State.query.all()
    skill = Skill.query.all() 
    allskill = Skill.query.all()
  
    if request.method=='POST':
        deets = db.session.query(Users).all()
        beta = db.session.query(Users).first()
        searchdpone = beta.user_dpone
        skill_in_need = request.form.get('skill')
        search_state = request.form.get('statename')
        skillset = db.session.query(Users).filter(Users.user_skill==skill_in_need)
        if skill_in_need=='' or skill_in_need==None:
             return redirect('/')
        else:
            return render_template('user/search_location.html',deets=deets,skill=skill,skillset=skillset, skill_in_need=skill_in_need,random=random, beta=beta,searchdpone=searchdpone,search_state=search_state,allstates=allstates, allskill=allskill)



@app.route('/client/<int:cid>,<st>')
def client_search(cid,st):
    clients = db.session.query(Users).filter(Users.user_id==cid).first()
    st_state = db.session.query(Users).filter(Users.user_state==st).first()
    deets = db.session.query(Users).get(cid)
    username=deets.user_fullname
    propic = Album.query.order_by(Album.album_id.desc()).all()
    disp = DisplayPictures.query.order_by(DisplayPictures.dp_id.desc()).all()
    #db.session.query(Album).all()
    album_userid = db.session.query(Users).get(cid)
    dp_userid = db.session.query(Users).get(cid)
    return render_template('user/clientSearchResult.html',deets=deets,username=username,propic=propic,disp=disp,clients=clients,st_state=st_state)


@app.route('/client/<int:cid>,<st>')
def searchResult(cid,st):
    clients = db.session.query(Users).filter(Users.user_id==cid).first()
    st_state = db.session.query(Users).filter(Users.user_state==st).first()
    deets = db.session.query(Users).get(cid)
    username=deets.user_fullname
    propic = Album.query.order_by(Album.album_id.desc()).all()
    disp = DisplayPictures.query.order_by(DisplayPictures.dp_id.desc()).all()
    #db.session.query(Album).all()
    album_userid = db.session.query(Users).get(cid)
    dp_userid = db.session.query(Users).get(cid)
    return render_template('user/clientSearchResult.html',deets=deets,username=username,propic=propic,disp=disp,clients=clients,st_state=st_state)



@app.route('/clientstate/<int:cid>')
def searchBySkill(cid):
    allskill = db.session.query.all()
    clients = db.session.query(Users).filter(Users.user_id==cid).first()
    deets = db.session.query(Users).get(cid)
    username=deets.user_fullname
    propic = Album.query.order_by(Album.album_id.desc()).all()
    disp = DisplayPictures.query.order_by(DisplayPictures.dp_id.desc()).all()
    album_userid = db.session.query(Users).get(cid)
    dp_userid = db.session.query(Users).get(cid)
    return render_template('user/search_location.html',deets=deets,username=username,propic=propic,disp=disp,clients=clients,allskill=allskill)        
   
@app.route('/join')
def join():
    states = State.query.all()
    #lg = db.session.query(Lga).all()
    return render_template('user/join.html',states=states)  



@app.route('/register', methods=['GET','POST']) 
def register():
    if request.method=='GET':
        deets = db.session.query(Users)
        states = State.query.all()
        return render_template('user/join.html',deets=deets)
    else:
        fullname = request.form.get('fullname')
        #userstate = db.session.query(State)
        #state = userstate.state_name
        gender = request.form.get('gender')
        email=request.form.get('email')
        phone = request.form.get('phone')
        #state = request.form.get('stateid')
        #state = request.form.get('stateid')
        #address = request.form.get('address')
        pwd=request.form.get('password')
        con_pwd = request.form.get('conpwd')
        hashed_pwd = generate_password_hash(pwd)
        if fullname !='' and email !='' and pwd !='' and gender!='' and pwd == con_pwd :

            #insert into database using ORM method
            u=Users(user_fullname=fullname,user_email=email,user_pwd=hashed_pwd, user_phone =phone, user_pix='',user_skill='', user_address='', gender=gender, user_state='')
            #add to session
            db.session.add(u)
            db.session.commit()
            #to get the id of the record that has just been inserted
            """userid=u.user_id     
            session['user']=userid"""
            flash('Thank you for joining the community, login to continue')
            return redirect(url_for('user_login'))
        else:
            flash('You must complete all the fields to signup OR check that your password match is correct')
            return redirect(url_for('join'))

@app.route('/howItWorks')
def howItWorks():
    deets = db.session.query(Users).all()
    return render_template('user/how_it_works.html',deets=deets)


@app.route('/aboutus')
def aboutus():
    deets = db.session.query(Users).all()
    return render_template('user/about_us.html',deets=deets)


@app.route('/contact', methods=['GET','POST'])
def contact():
    id = session.get('user')
    if id==None:
        return redirect(url_for('user_login'))
    else:
        if request.method=='GET': 
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            allstates = State.query.all()
            return render_template('user/contact.html',deets=deets,allstates=allstates)
        else:
            phone = request.form.get('phone')
            state = request.form.get('statename')
            address = request.form.get('address')
            userobj = db.session.query(Users).get(id)
            userobj.user_phone=phone
            userobj.user_state=state
            userobj.user_address=address
            """c=Users(user_phone=phone,user_state=state,user_address=address)
            db.session.add(c)"""
            db.session.commit() 
            flash('contact details successfully updated')
            return redirect(url_for('user_dashboard'))
        
@app.route('/login', methods=['GET','POST'])
def user_login():
    if request.method=='GET':
        return render_template('user/user_login.html')
    else:
        #retrieve the form data
        email=request.form.get('email')
        pwd=request.form.get('password')
        #run a query to know if the username exists on the database 
        deets = db.session.query(Users).filter(Users.user_email==email).first() 
        if deets !=None:
            pwd_indb = deets.user_pwd
            #compare the paswword coming from the form with the hashed password in the db
            chk = check_password_hash(pwd_indb, pwd)
            if chk:
                #log in the person
                id = deets.user_id
                session['user'] = id
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('user_login'))
        else:
            return redirect(url_for('user_login'))


@app.route('/logout')
def user_logout():
    #pop the session redirect to home page
    if session.get('user')!=None:
        session.pop('user',None)
    return redirect(url_for('user_login'))


@app.route('/dashboard')
def user_dashboard():
    if session.get('user')!=None:
        id = session['user']
        deets = db.session.query(Users).get(id)
        username=deets.user_fullname
        propic = Album.query.order_by(Album.album_id.desc()).all()
        disp = DisplayPictures.query.order_by(DisplayPictures.dp_id.desc()).all()
        #db.session.query(Album).all()
        album_userid = db.session.query(Users).get(id)
        dp_userid = db.session.query(Users).get(id)
        return render_template('user/user_dashboard.html',deets=deets,username=username,propic=propic,disp=disp)
        
    else: 
        return redirect(url_for('user_login'))

@app.route('/projects')
def projects():
    if session.get('user')==None:
        return redirect('user/user_login.html')
    else:
        if request.method.get=='GET':
            return render_template('user/project.html')

@app.route('/skill', methods=['POST','GET'])
def skill():
    id = session.get('user')
    if id ==None:
        return render_template('user/user_login.html')
    else:
        if request.method=='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            chose = Skill.query.all() 
            return render_template('user/skill.html',chose=chose,deets=deets)
        else:
            skill = request.form.get('skill')
            skilldit = request.form.get('hint')
            userobj = db.session.query(Users).get(id)
            userobj.user_skill=skill 
            db.session.commit()
            flash('Skill successfully updated')
            return redirect(url_for('user_dashboard',skilldit=skilldit))


@app.route('/delete/<int:id>')
def delete(id): 
    pic_to_del=Album.query.get_or_404(id)
    try:
        db.session.delete(pic_to_del)
        db.session.commit()
        flash('Picture deleted successfully')
        my_pics = Album.query.order_by(Album.Album_userid) 
        return redirect(url_for('user_dashboard'))
        
    except:
        flash('whoops, there was a problem deleting the picutre')
        return redirect(url_for('user_dashboard'))



@app.route('/profile', methods=['POST', 'GET'])
def user_profile():
    id = session.get('user')
    if id ==None:
        return render_template('user/user_login.html')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            return render_template('user/profile.html',deets=deets)
        else:
            file = request.files['pix'] 
            filename = file.filename #original filename
            filetype = file.mimetype
            allowed = ['.png', '.jpg','.jpeg']
            if filename !='':
                #upload
                name,ext = os.path.splitext(filename) 
                #import os on line 1
                if ext.lower() in allowed:
                    newname = generate_name()+ext
                    file.save("skiller/static/uploads/"+newname)
                    userobj = db.session.query(Users).get(session['user'])

                    userobj.user_pix=newname
                    db.session.commit()
                    flash('Picture uploaded')
                    return redirect(url_for('user_dashboard'))
                    return 'File uploaded'
                else:
                    return 'File extension not allowed '
            else:
                flash('Please chose a file')
                return 'Please chose a file'

@app.route('/bet')
def bet():
    return render_template('user/catalogue.html')


@app.route('/album', methods=['POST', 'GET'])
def album():
    id = session.get('user')
    if id ==None:
        return redirect('/login')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            pics = request.files
            return render_template('user/catalogue.html',deets=deets) #check again
        else:
                #pics= request.form.get('album_name')
                pics = request.files['project_picture'] 
                filename = pics.filename #original filename
                filetype = pics.mimetype
                #note to correct the profile_picture.html and name it ppi
                allowed = ['.png', '.jpg','.jpeg','.mp4']
                if filename !='':
                    #upload
                    name,ext = os.path.splitext(filename) 
                    #import os on line 1
                    if ext.lower() in allowed:
                        newname = generate_name()+ext
                        pics.save("skiller/static/uploads/album/"+newname)
                        #albumobj = db.session.query(Users).get(session['user'])
                        albumid = db.session.query(Users).get(session['user'])
                        albumid.user_album.Album_userid=id

                        #albumid.user_id=session['user']
                        f = Album(album_name=newname,Album_userid=id) 
                        db.session.add(f)
                        db.session.commit()
                        flash('File uploaded successfully')
                        return redirect(url_for('user_dashboard'))
                        
                    else:
                        return 'File extension not allowed '
                else:
                    flash('Please chose a file')
                    

@app.route('/displaypics', methods=['POST', 'GET'])
def displaypics():
    id = session.get('user')
    if id ==None:
        return redirect('/login')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            return render_template('user/displaypics.html',deets=deets)
        else:
                pics = request.files['display_picture'] 
                filename = pics.filename #original filename
                filetype = pics.mimetype
                allowed = ['.png', '.jpg','.jpeg']
                if filename !='':
                    #upload
                    name,ext = os.path.splitext(filename) 
                    #import os on line 1
                    if ext.lower() in allowed:
                        newname = generate_name()+ext
                        pics.save("skiller/static/uploads/dp/"+newname)
                        dpid = db.session.query(Users).get(session['user'])
                        
                        #dpid.user_dp1.dp_userid=id
                        dpid.user_dpone=newname
                        db.session.commit()
                        flash('File uploaded successfully')
                        return redirect(url_for('user_dashboard'))
                    else:
                        return 'File extension not allowed '
                else:
                    flash('Please chose a file')


@app.route('/displaypics2', methods=['POST', 'GET'])
def displaypics2():
    id = session.get('user')
    if id ==None:
        return redirect('/login')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            return render_template('user/displaypics2.html',deets=deets)
        else:
                file = request.files['display_picture2'] 
                filename = file.filename #original filename
                filetype = file.mimetype
                allowed = ['.png', '.jpg','.jpeg']
                if filename !='':
                    #upload
                    name,ext = os.path.splitext(filename) 
                    #import os on line 1
                    if ext.lower() in allowed:
                        newname = generate_name()+ext
                        file.save("skiller/static/uploads/dp/"+newname)
                        dpid = db.session.query(Users).get(session['user'])

                        dpid.user_dptwo=newname
                        db.session.commit()
                        flash('File uploaded successfully')
                        return redirect(url_for('user_dashboard'))
                    else:
                        return 'File extension not allowed '
                else:
                    flash('Please chose a file')



@app.route('/displaypics3', methods=['POST', 'GET'])
def displaypics3():
    id = session.get('user')
    if id ==None:
        return redirect('/login')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            return render_template('user/displaypics3.html',deets=deets)
        else:
                pic3 = request.files['display_picture3'] 
                filename = pic3.filename #original filename
                filetype = pic3.mimetype
                allowed = ['.png', '.jpg','.jpeg']
                if filename !='':
                    #upload
                    name,ext = os.path.splitext(filename) 
                    #import os on line 1
                    if ext.lower() in allowed:
                        newname = generate_name()+ext
                        pic3.save("skiller/static/uploads/dp/"+newname)
                        dpid = db.session.query(Users).get(session['user'])
                     
                        dpid.user_dpthree=newname
                        db.session.commit()
                        flash('File uploaded successfully')
                        return redirect(url_for('user_dashboard'))
                    else:
                        return 'File extension not allowed '
                else:
                    flash('Please chose a file')
            
            