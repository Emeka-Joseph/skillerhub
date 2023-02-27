import os, random, string
from flask import render_template, redirect, flash, session, request, url_for
from sqlalchemy import desc,asc,or_
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text


#3rd party importations
from skiller.models import State,Lga,Users,Skiller, Album,Skill #import the required tables from the database
from skiller.forms import JoinForm
from skiller import app, db,CSRFProtect

def generate_name(): 
    filename = random.sample(string.ascii_lowercase,10) 
    return ''.join(filename) 

@app.route('/') 
def home():
    id = session['user']
    deets = db.session.query(Users).get(id)
    return render_template('user/index.html',deets=deets) 


@app.route('/join')

def join():
    #st = State.query.all()
    st = db.session.query(State).all()
    #lg = db.session.query(Lga).all()
    return render_template('user/join.html',st=st)  



@app.route('/register', methods=['POST'])
def register():
    fullname = request.form.get('fullname')
    gender = request.form.get('gender')
    email=request.form.get('email')
    phone = request.form.get('phone')
    state = request.form.get('state')
    #state = request.form.get('stateid')
    address = request.form.get('address')
    pwd=request.form.get('password')
    con_pwd = request.form.get('conpwd')
    hashed_pwd = generate_password_hash(pwd)
    if fullname !='' and email !='' and pwd !='' and gender!='' and phone!='' and state!='' and address !='' and pwd == con_pwd :

         #insert into database using ORM method
        u=Users(user_fullname=fullname,user_email=email,user_pwd=hashed_pwd, user_phone =phone, user_pix='', user_address=address, gender=gender, user_state=state)
        #add to session
        db.session.add(u)
        db.session.commit()
        #to get the id of the record that has just been inserted
        userid=u.user_id     
        session['user']=userid
        return redirect(url_for('user_login'))
    else:
        flash('You must complete all the fields to signup')
        return redirect(url_for('join'))



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
        propic = Album.query.all()
        #db.session.query(Album).all()
        album_userid = db.session.query(Users).get(id)
        return render_template('user/user_dashboard.html',deets=deets,username=username,propic=propic)
        
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
        return redirect('user/user_login.html')
    else:
        if request.method=='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            chose = Skill.query.all() 
            return render_template('user/skill.html',chose=chose,deets=deets)
        else:
            skiller = request.form.get('skill')
            #skillobj = db.session.query(Users).get(session['user'])
            #n=Users(user_skill=skiller)  #skillobj.skill=skiller
            #userobj = db.session.query(User).get(id)
            userobj = db.session.query(Users).get(id)
            userobj.user_skill=skiller
            
            #db.session.add()
            db.session.commit()
            flash('Skill successfully updated')
            return redirect(url_for('user_dashboard'))


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
        return redirect('user/user_login.html')
    else:
        if request.method =='GET':
            deets = db.session.query(Users).filter(Users.user_id==id).first()
            return render_template('user/profile.html',deets=deets)
        else:
            file = request.files['pix'] 
            filename = file.filename #original filename
            filetype = file.mimetype
            #note to correct the profile_picture.html and name it ppi
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
                        albumid.user_album.album_userid=id

                        #albumid.user_id=session['user']
                        f = Album(album_name=newname,Album_userid=id) 
                        db.session.add(f)
                        #albumpic = db.session.query(Album).get(session['user'])
                        #albumpic.album_name=newname
                        db.session.commit()
                        flash('File uploaded successfully')
                        return redirect(url_for('user_dashboard'))
                        
                    else:
                        return 'File extension not allowed '
                else:
                    flash('Please chose a file')
                    

            
            