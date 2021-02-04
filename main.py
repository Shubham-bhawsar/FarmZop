from flask import Flask,render_template,request,session,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_mail import Mail
import json
import math
import pickle
import numpy as np
import pandas as pd
from check import classname
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json
app=Flask(__name__)
  

local_server=True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app.config.update(MAIL_SERVER = 'smtp.gmail.com',
                MAIL_PORT ='465',
                MAIL_USE_SSL = True,
                MAIL_USERNAME = 'abc@gmail.com',
                MAIL_PASSWORD = 'password@123123123')

mail=Mail(app)

app.secret_key = "super123secret123key"
app.config['UPLOAD_FOLDER']='media\\shubham\\New Volume\\Project\\digital farming\\web\\static\\uploads'

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

db = SQLAlchemy(app)

class Contacts(db.Model):
    Email = db.Column(db.String(20), primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Message = db.Column(db.String(120), unique=False, nullable=False)
    Subject = db.Column(db.String(120), unique=False, nullable=False)

class Blog(db.Model):
    Title = db.Column(db.String(20), unique=False,nullable=False)
    Content = db.Column(db.String(1000), unique=False, nullable=False)
    Date = db.Column(db.String(120), unique=False, nullable=True)
    SNo = db.Column(db.Integer,primary_key=True)
    Slug = db.Column(db.String(120), unique=False, nullable=False)
    Image = db.Column(db.String(12), nullable=True)
@app.route('/')
def home():
    return render_template('index.html',params=params)

@app.route('/test')
def test():
    return render_template('test.html',params=params)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/detectdis',methods=['GET','POST'])
def trainers():
    result="After Uploading Here will be Your Results"
    if request.method=='POST':
        
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_file.filename) ))
        #return redirect(url_for('trainers'))
        
        json_file = open('modelcolor.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
# load weights into new model
        loaded_model.load_weights("modelcolor.h5")
#print("Loaded model from disk")
        img=image.load_img(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_file.filename) ))
        img = image.img_to_array(img)
        img = img/255 
        X = np.array(img)
        X=np.reshape(X,(1,300,300,3))
        res=loaded_model.predict(X)
        classes=classname
        result=classes[np.argmax(res)]


    return render_template('detectdis.html',params=params,Result=result)


@app.route('/cropassess')
def elements():
    result="After Uploading Here will be Your Results"
    if request.method=='POST':
        
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_file.filename) ))
        #return redirect(url_for('trainers'))
    return render_template('cropassess.html',params=params,Result=result)

@app.route('/yield',methods=['GET','POST'])
def yieldf():
    result="After Uploading Here will be Your Results"
    if request.method=='POST': 
        Crop=request.form.get('Crop')
        MnTr=(request.form.get('MnTR'))
        MnTK=(request.form.get('MnTK'))
        MnTW =(request.form.get('MxTW'))
        MxTr=(request.form.get('MxTR'))
        MxTK=(request.form.get('MxTK'))
        MxTW =(request.form.get('MxTW'))
        PPR=(request.form.get('PPR'))
        PPK=(request.form.get('PPK'))
        PPW =(request.form.get('PPW'))
        VPR=(request.form.get('VPR'))
        VPK=(request.form.get('VPK'))
        VPW =(request.form.get('VPW'))
        WDR=(request.form.get('WDR'))
        WDK=(request.form.get('WDK'))
        WDW =(request.form.get('WDW'))
        RCER=(request.form.get('RCER'))
        RCEK=(request.form.get('RCEK'))
        RCEW =(request.form.get('RCEW'))
        area=(request.form.get('area'))
        loaded_model = pickle.load(open('modifyEY.sav', 'rb'))
        label=pickle.load(open('labelencoder.sav','rb'))
        onehot=pickle.load(open('onehot.sav','rb'))
        arr=[Crop,float(area),float(MnTr),float(MnTK),float(MnTW),float(MxTr),float(MxTK),float(MxTW),float(VPR),float(VPK),float(VPW),float(RCER),float(RCEK),float(RCEW),float(PPR),float(PPK),float(PPW),float(WDR),float(WDK),float(WDW)]
        
        laben=label.transform([Crop])
        arr[0]=laben[0]
        arr=np.array(arr)
        arr=np.reshape(arr,(1,20))
        arr=onehot.transform(arr)
        
        #arr=[326.0,13.546667,25.046333,19.296500,	28.879000,	36.329667,	32.604333,	8.790833,	22.593000,	15.691917,	3.990000,	5.751667,	4.870833,	5.053667,	42.508500,	23.781083,	6.3200,	19.1520,	25.472]
        #arr=np.reshape(arr,(1,-1))
        resu = loaded_model.predict(arr)
        result='Hii farmer!!! your predicted yield would be '+str(resu[0])
        #return render_template('about.html',params=params)
    return render_template('yield.html',params=params,result=str(result))

@app.route('/single-blog')
def single_blog():
    return render_template('single-blog.html',params=params)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if (('user' in session) and session['user']=='abc@gmail.com'):
        blog=Blog.query.order_by(Blog.SNo).all()
        return render_template('dashboard.html',params=params,blogs=blog)
    if request.method=='POST':
        username=request.form.get('uname')
        userpass=request.form.get('pass')
        if (username=='abc@gmail.com' and userpass=='abc@123123123'):
            session['user'] =username
            blog=Blog.query.order_by(Blog.SNo).all()
            return render_template('dashboard.html',params=params,blogs=blog)
    return render_template('login.html',params=params )

@app.route('/courses')
def courses():
    return render_template('cources.html',params=params)

@app.route('/blog')
def blog():
    blogs=Blog.query.filter_by().all()
    last=math.ceil(len(blogs)/int(params['no_of_posts']))
    page=request.args.get('page')
    if(not str(page).isnumeric()):
        page=1
    blog=blogs[(int(page)-1)*int(params["no_of_posts"]):(((int(page)-1)*int(params["no_of_posts"]))+int(params["no_of_posts"]))]
    if(int(page)==1):
        prev="/blog"
        nexta="/blog?page="+str(int(page)+1)
    elif(int(page)==last):
        prev="/blog?page="+str(int(page)-1)
        nexta="/blog?page="+str(last)
    else:
        prev="/blog?page="+str(int(page)-1)
        nexta="/blog?page="+str(int(page)+1)
    curr_page=int(page)
    nex_page=int(page)+1  
    return render_template('blog.html',params=params,blogs=blog,prev=prev,next=nexta,curr_page=curr_page,nex_page=nex_page)

@app.route('/blog/<string:blog_slug>',methods=['GET'])
def blogslug(blog_slug):
    blog=Blog.query.filter_by(Slug=blog_slug).first()
    return render_template('blogslug.html',params=params,blog=blog)

@app.route('/edit/<string:sno>',methods=['GET','POST'])
def edit(sno):
    if (('user' in session) and session['user']=="abc@gmail.com"):
        if request.method=='POST':
             box_title=request.form.get('title')
             slug=request.form.get('slug')
             content=request.form.get('content')
             SNo=request.form.get('sNo')
             img=request.form.get('img')
             date=datetime.now()
             if sno=='0':
                 blog=Blog(Title=box_title,Slug=slug,Content=content,SNo=SNo,Image=img,Date=date)
                 db.session.add(blog)
                 db.session.commit()
                 return redirect('/dashboard')
             else:
                 blog=Blog.query.filter_by(SNo=sno).first()
                 blog.Title=box_title
                 blog.Slug=slug
                 blog.Content=content
                 blog.SNo=SNo
                 blog.Image=img
                 blog.Date=date
                 db.session.commit()
                 return redirect('/dashboard')
        return render_template('edit.html',params=params,sno=sno)
    return redirect('/dashboard')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if (('user' in session) and session['user']==params['admin_user']):
        if (request.method=='POST'):
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return redirect('/dashboard')
        return redirect('/dashboard')
    return redirect('/dashboard')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        Name=request.form.get('name')
        Email=request.form.get('email')
        Subject =request.form.get('subject')
        Message=request.form.get('message')
        entry=Contacts(Name=Name,Email=Email,Subject=Subject,Message=Message)
        db.session.add(entry)
        db.session.commit()  
        mail.send_message('New Message from',
                            sender='abc@gmail.com',
                            recipients=['bhawsarshubham741@gmail.com'],
                            body=Message)  
    return render_template('contact.html',params=params)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route('/delete/<string:sno>')
def delete(sno):
    blog=Blog.query.filter_by(SNo=sno).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect('/dashboard')



 

app.run(debug=True) 
