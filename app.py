from flask import Flask,request,render_template,redirect,session
import psycopg2

app = Flask(__name__)

# userbase = {
#     'amit':'123',
#     'sumit':'456',
#     'vedant':'789',
#     'dhaval':'111'
# }

app.secret_key = '123456789'

def dbconn(query,type):
  conn= psycopg2.connect(host='192.168.29.215',database='vedant',user='dhaval',password='test@123',port=6432)
  cursor = conn.cursor()
  cursor.execute(query)
  if type == 'save':
     try:
        conn.commit()
        data = 'data saved Successfully'
        return data
     except Exception as e:
         data = f'there is some eeror in Query: {e}'
         return data
  else:
      data = cursor.fetchall()
      return data
     
def db_userbase(query):
    users=dbconn(query,"select")
    return users

@app.route('/')
def homepage():
    if 'user' in session:
        return redirect('/dashboard')
    else:
     return render_template('index.html')

@app.route('/search',methods=['get'])
def search():
    if 'user' in session:
        user = request.args.get('search')
        print(user)
        query= f"select * from galary where users='{user}'"
        data=dbconn(query,'select')
        if data:
            owner=data[1][1]
        else:
            owner = 'No User Found'
        if data:
            return render_template('searchboard.html',user=session['user'],data=data,owner=owner)
        else:
            return redirect('/dashboard')
    else:
        return "test"

@app.route('/login',methods=['post'])
def login():
    email = request.form.get('email')
    password= request.form.get('password')
    query = f"select uname,pwd,id from users where uname='{email}'and pwd='{password}'"
    data=db_userbase(query)
    if data:
        id = data[0][2]
        user_detail = f"select * from user_detail where user_id = {id}"
        if dbconn(user_detail,'select'):
            print("User detail exists")
            pass
        else:
            insert = f"insert into user_detail (user_id,description,dp) values('{id}','{email}','/images/system/user.jpg')"
            if dbconn(insert,'save'):
                print("User detail created")
            else:
                print("Error creating user detail")
            
        session['user']=email
        session['id'] = id
        
        return redirect('/dashboard')
    else:
        return redirect('/')
    
    ## old login logic ---------
    # if email in userbase:
    #     if userbase[email] != password:
    #         return redirect('/')
    #     else:
    #         session['user']=email
    #         return redirect('/dashboard')
    # else:
    #     return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        query= f"select * from galary where users='{user}'"
        query2= f"select * from user_detail where user_id = {session['id']}"
        type= 'select'
        data = dbconn(query,type)
        userdetail = dbconn(query2,type)
        print(userdetail)
        return render_template('dashboard.html',user=user,data=data,userdata=userdetail)
    else:
        return redirect('/')
@app.route('/logout')
def logut():
    session.clear()
    return redirect('/')

@app.route('/saveimg',methods=['post'])
def saveimg():
    file = request.files['image']
    if file.filename == '':
        return redirect('/dashboard')
    else:
        path = "static/images/"+file.filename
        imagedbpath = f"images/{file.filename}"
        user=session['user']
        query=f"insert into galary (users,image) values('{user}','{imagedbpath}')"
        type = 'save'
        dbconn(query,type)
        file.save(path)
        return redirect('/dashboard')
    
@app.route('/createacc')
def createacc():
    if 'user' in session:
        return redirect('/dashboard')
    else:
        return render_template('createacc.html')
    
@app.route('/register',methods=['post'])
def register():
    name = request.form.get('name')
    password= request.form.get('password')
    query = f"insert into users (uname,pwd) values('{name}','{password}')"
    type = 'save'
    dbconn(query,type)
    message= "Account created successfully. Please log in."
    return render_template('index.html',message=message)

@app.route('/settings')
def settings():
    if 'user' in session:
        return render_template('settings.html', user=session['user'])
    else:
        return redirect('/')
    
@app.route('/update-settings',methods=['post'])
def updatesettings():
    if 'user' in session:
        old_pass = request.form.get('old_pass')
        new_pass = request.form.get('new_pass')
        name = request.form.get('fullname')
        user = session['user']
        file = request.files['profile_photo']
        description = request.form.get('description')
        if file.filename != '':
            path = "static/profilepic/"+file.filename
            file.save(path)
            imagepath = f"images/profilepic/{file.filename}"
        else: 
            imagepath= ""
        if not new_pass:
            new_pass = old_pass
        id=session['id']
        query = f"update users set pwd = '{new_pass}' , uname = '{name}' where uname = '{user}' and pwd = '{old_pass}'"
        query1 = f"update user_detail set dp = '{imagepath}' , description = '{description}' where user_id = '{id}'"
        type = 'save'
        if dbconn(query,type):
            session['user'] = name
            if dbconn(query1,type):
                pass
        else:
            return "Error updating settings"
        return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=500)