
from queue import Empty
from flask import redirect, render_template, request, session, url_for,flash
from app.auth import auth as auth_blueprint
from app.models import User, Socialmidias
from app import db
from app.forms import Socialmidias_url, DeleteSocialMidias,EmailToResetPassword, UpdateSocialMidias
from app import mail
from flask_mail import Message
from werkzeug.security import generate_password_hash
from flask_login import login_required


           


def init_app(app):
    app.register_blueprint(auth_blueprint)
 
    
    @app.route('/')
    def index():
        return render_template('index.html')    

    @app.route('/main')
    @login_required
    def main():
        name = session['name']
        userid = session['id']
        socialmidias = Socialmidias.query.filter_by(user_id=userid).first()

        return render_template("main.html",name=name, socialmidias=socialmidias)

    @app.route('/addsocialmidias', methods=['GET','POST'])
    @login_required
    def addsocialmidias():
        userid = session['id']
        user_username = session['username']
        form = Socialmidias_url()
        socialmidias = Socialmidias.query.filter_by(user_id=userid).first()
        if form.validate_on_submit():
            if form.facebook_url.data == form.linkedin_url.data:
                flash("Facebook url and Linkedin url cannot be the same", "danger")
                return redirect(url_for('addsocialmidias'))
            elif socialmidias is not None:
                socialmidias.facebook = form.facebook_url.data or socialmidias.facebook
                socialmidias.username_socialmidias = user_username
                socialmidias.linkedin = form.linkedin_url.data or socialmidias.linkedin
            else:
                socialmidias = Socialmidias(
                        facebook=form.facebook_url.data,linkedin=form.linkedin_url.data, username_socialmidias=user_username,user_id=userid)
            db.session.add(socialmidias)
            db.session.commit()
            return redirect(url_for('socialmidias'))
        return render_template('addsocialmidia.html',form=form)


    @app.route('/socialmidias')
    @login_required
    def socialmidias():
        userid = session["id"]
        socialmidias =  Socialmidias.query.filter_by(user_id = userid).first()
        return render_template('socialmidias.html', userid=userid, socialmidias=socialmidias)

    @app.route('/shareprofile', methods=["GET", "POST"])
    @login_required
    def shareprofile():
        userid = session['id']
        username = session['username']
        user = db.session.query(User).filter_by(id = userid).first()
        return render_template('qrcode.html',user=user,username=username)


    @app.route('/sharedprofile/<string:username>', methods=["GET", "POST"])
    def sharedprofile(username):
        socialmidias =  Socialmidias.query.filter_by(username_socialmidias = username).first()
        name = username
        return render_template('sharedprofile.html', socialmidias=socialmidias, name=name)

    @app.route('/customizesharedprofile', methods=["GET", "POST"])
    @login_required
    def customizesharedprofile():

        if request.method == "POST":
            facebook_url_customization = request.form.get('facebook_url')
            linkedin_url_customization = request.form.get('linkedin_url')
            session.modified = True
            session['facebookcustomization'] = facebook_url_customization
            session['linkedincustomization'] = linkedin_url_customization
            return redirect(url_for('main'))

        return render_template('customizesharedprofile.html')        


    @app.route('/deletefacebook', methods=["GET", "POST"])
    @login_required
    def deletefacebook():
        userid = session["id"]
        socialmidias =  Socialmidias.query.filter_by(user_id = userid).first()
        form = DeleteSocialMidias()
        
        if form.validate_on_submit() and request.method == "POST":
            facebookurl = form.url.data
            if facebookurl == socialmidias.facebook:
                socialmidias.facebook = ''
                db.session.commit()
                return redirect(url_for('socialmidias'))     
            elif facebookurl != None or Empty and facebookurl != socialmidias.facebook:
                flash('The Facebook url doesnt match', 'danger')      
               

                  
        return render_template('deletefacebook.html',form=form)

    @app.route('/deletelinkedin', methods=["GET", "POST"])
    @login_required
    def deletelinkedin():
        userid = session["id"]
        socialmidias =  Socialmidias.query.filter_by(user_id = userid).first()
        form = DeleteSocialMidias()

        if form.validate_on_submit() and request.method == "POST":
            linkedinurl = form.url.data
            if linkedinurl == socialmidias.linkedin:
                socialmidias.linkedin = ''
                db.session.commit()
                return redirect(url_for('socialmidias'))  
            elif linkedinurl != None or Empty and linkedinurl != socialmidias.linkedin:
                flash('The Linkedin url doesnt match', 'danger') 
                    

        return render_template('deletelinkedin.html', form=form)   


    @app.route('/updatefacebook', methods=["GET", "POST"])
    @login_required
    def updatefacebook():
        userid = session["id"]
        socialmidias =  Socialmidias.query.filter_by(user_id = userid).first()
        form = UpdateSocialMidias()

        if form.validate_on_submit() and request.method == "POST":
            new = form.new.data
            if new == '':
                flash('The new value is Empty', 'danger')
                return redirect(url_for('updatefacebook'))
            socialmidias.facebook = new
            db.session.commit()
            return redirect(url_for('socialmidias'))
        

        return render_template('updatefacebook.html', form=form)

    @app.route('/updatelinkedin', methods=["GET", "POST"])
    @login_required
    def updatelinkedin():
        userid = session["id"]
        socialmidias =  Socialmidias.query.filter_by(user_id = userid).first()
        form = UpdateSocialMidias()

        if form.validate_on_submit() and request.method == "POST":
            new = form.new.data
            if new == '':
                flash('The new value is Empty', 'danger')
                return redirect(url_for('updatelinkedin'))   
            socialmidias.linkedin = new
            db.session.commit()
            return redirect(url_for('socialmidias'))
        

        return render_template('updatelinkedin.html', form=form)            



    @app.route('/resetpassword', methods=["GET", "POST"])
    @login_required
    def resetpassword():
        form = EmailToResetPassword()
        
        if form.validate_on_submit():
            userid = session['id']
            user = User.query.filter_by(id = userid).first()
            email = form.emailresetpassword.data
            if user.email == email:
                subject = 'Reset Password'
                name = session['name']

                msg = Message(subject,sender="vitorcontacamp@gmail.com", recipients=[email], html=render_template('linkPage.html',name=name))

                mail.send(msg)

                if mail.send:
                    flash('Email Sent!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Email not sent', 'danger')
                    return redirect(url_for('resetpassword'))    
            else:
                flash('Email not exist', 'danger')
                return redirect(url_for('resetpassword'))    
            

        return render_template('resetpassword.html',form=form)  

    @app.route('/newpassword', methods=["GET", "POST"])
    @login_required
    def newpassword():
        if request.method == "POST":

            password1 = request.form['password1']
            password2 = request.form['password2']

            if password1 == password2:
                userid = session['id']
                user = User.query.filter_by(id = userid).first()
                user.password = generate_password_hash(password2)
                db.session.commit()
                flash('Password Successfully changed', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('The passwords are differents', 'danger')
                return redirect(url_for('newpassword'))     
        return render_template('newpassword.html')        