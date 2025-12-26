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
  conn= psycopg2.connect(host='localhost',database='vedant',user='dhaval',password='test@123',port=6432)
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
            return render_template('dashboard.html',user=session['user'],data=data)
        else:
            return redirect('/dashboard')
    else:
        return "test"

@app.route('/login',methods=['post'])
def login():
    email = request.form.get('email')
    password= request.form.get('password')
    query = f"select uname,pwd from users where uname='{email}'and pwd='{password}'"
    data=db_userbase(query)
    if data:
        session['user']=email
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
        type= 'select'
        data = dbconn(query,type)
        return render_template('dashboard.html',user=user,data=data)
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


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=500)