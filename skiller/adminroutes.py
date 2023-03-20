from flask import render_template, redirect, flash, session, request, url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from skiller.models import Skill,Admin,Users


from skiller import app, db

@app.route('/admin') 
def homepage():
    return "This is Admin Page for Skiller Platform "
    #return render_template('user/index.html') 


@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='GET':
        return render_template('admin/admin_login.html')
    else:
        email=request.form.get('email')
        pwd=request.form.get('password')
        #run a query to know if the admin email exists on the database 
        deets = db.session.query(Admin).filter(Admin.admin_email==email).first() 
        if deets !=None:
            pwd_indb = deets.admin_password
            if pwd_indb==pwd:
                id = deets.admin_id
                session['admin'] = id
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('admin')!=None:
        id = session['admin']
        deets = db.session.query(Admin).get(id) 
        admin_name=deets.admin_fullname
        return render_template('admin/admin_dashboard.html',deets=deets,admin_name=admin_name)
    else: 
        return redirect(url_for('admin_login'))


@app.route('/admin/skills', methods=['POST','GET'])
def skills():
    if session.get('admin')==None:
        return render_template('admin/admin_login.html')
    else:
        if request.method=='GET':
            return render_template('/admin/add_skill.html')
        else:
            skill=request.form.get('skill')
            skills = Skill(skill_name=skill)
            db.session.add(skills)
            db.session.commit()
            flash('Skill added successfully')
            return redirect(url_for('admin_dashboard'))


@app.route('/manage_users')
def usermanager():
    if session.get('admin')==None:
        return render_template('admin/admin_login.html')
    else:
        allusers = Users.query.all()
        return render_template('admin/all_users.html',allusers=allusers)


@app.route('/admin/delete/<id>')
def delete_user(id):
    userobj = Users.query.get_or_404(id)
    db.session.delete(userobj)
    db.session.commit()
    flash('Succesfully Deleted')
    return redirect(url_for('usermanager')) 

@app.route('/admin/logout')
def admin_logout():
    #pop the session redirect to home page
    if session.get('admin')!=None:
        session.pop('admin',None)
    return redirect(url_for('admin_login'))