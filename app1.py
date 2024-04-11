import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import os
import base64
from flask import Flask, render_template, send_from_directory,request,redirect,url_for ,\
request ,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random
import requests






app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/userdetail'


db = SQLAlchemy(app)

RECAPTCHA_SECRET_KEY = '6Lf0FbYpAAAAALlSt-nGxTXkz6EpQkyohD5qOzSl'





class userdetail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    message = db.Column(db.Text)
        
class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(21))
    content = db.Column(db.String(1000))
    date = db.Column(db.Date)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)    
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)    
    
class Uniqueid(db.Model):
    __tablename__ = 'uniqueid'
    uniqueid = db.Column(db.Integer, primary_key=True)
  


def generate_unique_id():
    return ''.join(random.choices('0123456789', k=10))  
    
    

        
@app.route('/searchprogress')
def index():
    return render_template('searchprogress.html')

@app.route('/search', methods=['POST'])
def search():
    uniqueid = request.form['uniqueid']
    user = Uniqueid.query.filter_by(uniqueid=uniqueid).first()
    if user:
        return render_template('workprogress.html', user=user)
    else:
        return render_template('error.html')        
    
def generate_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    captcha = f"What is {num1} + {num2}?"
    session['captcha_result'] = num1 + num2
    return captcha


@app.route('/validate', methods=['POST'])
def validate():
    user_answer = request.form['answer']
    correct_answer = session.get('captcha_result')

    if user_answer.isdigit() and int(user_answer) == correct_answer:
        return "Captcha Passed! You're Human."
    else:
        return "Captcha Failed! Please try again."





@app.route('/submit_post', methods=['POST'])
def submit_post():
      title=request.form['title']
      slug=request.form['slug']
      content=request.form['content']
      date=request.form['date']

      new_post= posts(title=title, slug=slug, content=content, date=date)
      db.session.add(new_post)
      db.session.commit()
      flash('Successfully posted the article to the user panel')

      return render_template('uploadpost.html',)
          
@app.route('/submit_video', methods=['POST'])
def upload_file():
        file=request.form['vedio']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return 'File uploaded successfully'   



@app.route('/submit_form', methods=['GET','POST'])
def submit_form():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    gender = request.form['gender']
    message = request.form['message']
    recaptcha_response = request.form['g-recaptcha-response']  # Correctly retrieve reCAPTCHA response

    new_user = userdetail(firstname=firstname, lastname=lastname, email=email, phone=phone, dob=dob, gender=gender,  message=message)
    db.session.add(new_user)
    db.session.commit()
    
    new_unique_id = generate_unique_id()
    new_uniqueid = Uniqueid(uniqueid=new_unique_id)  # Assuming UniqueID is a model
    db.session.add(new_uniqueid)
    db.session.commit()
    flash('Your Aknowledge number is'+new_unique_id)
    return render_template('report.html' )
   

    
    
  
       




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first() 
        if existing_user:
            flash('User already exists!', 'error')
            return redirect(url_for('register'))
        
        # Hash the password
        passward=password
        
        # Create a new user
        new_user = User(username=username, password=password)  
        db.session.add(new_user)
        db.session.commit()
        
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_logged_in'] = True
            flash('You are now logged in!', 'success')
            return redirect(url_for('report'))
        return render_template('userlogin.html', error='Invalid username or password')
    return render_template('userlogin.html')




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))









@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('admin_register'))
        existing_admin = Admin.query.filter_by(userid=userid).first()
        if existing_admin:
            flash('User already exists!', 'error')
            return redirect(url_for('admin_register'))
        new_admin = Admin(userid=userid, password=password)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin registered successfully!', 'success')
        return redirect(url_for('admin_login'))
    return render_template('admin_register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        admin = Admin.query.filter_by(userid=userid, password=password).first()
        if admin:
            session['admin_logged_in'] = True
            flash('You are now logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        username = session.get('userid')
        return render_template('admin_dashboard.html', username=username)
    else:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))




@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('admin_login'))


@app.route('/uploadvideo')
def uploadvideo():
     return render_template('video.html')



  
@app.route('/adminpanel') 
def adminpanel():
      global userdetail
      userdetails=userdetail.query.all()
      return render_template('adminpanel.html', userdetails=userdetails)   

@app.route('/manageposts') 
def manageposts():
    all_posts = posts.query.all()
    return render_template('managepost.html', posts=all_posts)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts.query.get_or_404(post_id)
    if request.method == 'POST':
        # Update post details
        post.title = request.form['title']
        post.slug = request.form['slug']
        post.content = request.form['content']
        post.date = request.form['date']
        # Commit changes to the database
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('manageposts'))                    

    return render_template('edit_post.html', post=post)

# Define route for deleting a post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('manageposts'))


@app.route('/uploadpost')
def uploadpost():
      return render_template('uploadpost.html')      
    



@app.route("/report")
def report():
    if 'user_logged_in' in session:
        username = session.get('username')
        captcha = generate_captcha()
        session['captcha'] = captcha

        return render_template('report.html', username=username,  captcha=captcha)
    flash('YOU HAVE TO LOGIN BEFORE ENTER TO SITE')
    return redirect(url_for('login'))
        



@app.route("/aboutus")
def about():
        return render_template("aboutus.html")




@app.route("/viewmore")
def viewmore():
        return render_template("viewmore.html")
   






@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
        post=posts.query.filter_by(slug=post_slug).first()
        
        
        return render_template("viewfraud.html", post=post)





@app.route("/postnew")
def postnew():
    global posts
    postn = posts.query.all()
    return render_template("postnew.html", postn=postn)



 


@app.route("/index")
def home():
    
        # Sample data for the bar chart
        x = ['total','solved','remaining']
        y = [100,80,20]
   
        
        #color list
        c=['b','g','r']
        # Create bar graph
        plt.bar(x, y,width=0.5,color=c,edgecolor='m',alpha=1)
        plt.xlabel('Status')
        plt.ylabel('Value')
        plt.title('REPORT CASES')

        # Save the plot to a bytes object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        # Close plot to prevent from displaying in console
        plt.close()
    
        c1=['b','c','r','m','g']
        x1 = ['facebook','instagram','digital','money','whatsapp']
        y1 = [10,10,20,20,40]
        # Create pie chart
        plt.pie(y1 ,labels=x1 , autopct='%1.1f%%')
 
        plt.title('REPORT CASES')

        # Save the plot to a bytes object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot1_data = base64.b64encode(buffer.getvalue()).decode()
        # Close plot to prevent from displaying in console
        plt.close()
        
        return render_template('index.html' ,  plot_data=plot_data , plot1_data=plot1_data)

       




if __name__ == '__main__':
    app.run(debug=True)
    



