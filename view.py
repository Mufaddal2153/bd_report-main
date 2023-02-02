import requests
import json
from flask import render_template, redirect, url_for, request, session, jsonify
# from sqlalchemy import extract
# from model import Project, Designation, Task, User, TimeSheet
# from forms import AddProject, ViewProject, ViewUser, ViewWork, AskDesignation, AddUser, AddWork
from config import bd_report, mysql
from datetime import datetime

#################### UPDATED TO CHECK PULL PUSH GIT ###############
############ Second Check ############
######### VIEW FUNCTIONS ##########

to_reload = False

@bd_report.route('/',methods=['GET','POST'])
def index():
    return render_template('trello_login.html')

@bd_report.route('/admin/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        userN = request.form['username']
        passW = request.form['password']

        cur.execute("Select username, password from admin where username=%s and password=%s", (userN, passW))
        mysql.connection.commit()
        res = cur.fetchall()
        if res:
            session['uName'] = userN
            return render_template('welcome.html', uName = userN) 
        else:
            print('not here')
            return render_template('login.html')
    return render_template('login.html')

@bd_report.route('/home')
def home():
    return render_template("home.html")

@bd_report.route('/token_post',methods=["GET",'POST'])
def token_post():
    res = {}
    if request.method == "POST" or request.method == "GET":
        token = request.form['token']
        base_url = 'https://trello.com/1/'
        mem_url = base_url + 'members/me'
        params_key_and_token = {'key': key, 'token': token}
        response = requests.get(mem_url, params=params_key_and_token)
        response = response.json()
        trello_id = response['id']
        user = response['username']
        session['token'] = token
        if trello_id == None:
            res['error'] = "/index"
        elif trello_id:
            get_user = User.query.filter_by(trello_id=trello_id).first()
            if get_user:
                res['success']='/add_project'
                token=token
                db.session.commit()
            else:
                res['trello_id']=trello_id
                res['user']=user
                token=token
                res['token']=token
                res['success'] ='/ask_designation'+'?'+'trello_id='+res['trello_id']+'&'+'user='+res['user']+'&'+'token='+res['token']

        res = json.dumps(res)
        return res


    return render_template('trello_login.html')

@bd_report.route('/admin/add_designation',methods=['POST'])
def add_designation():
    # form = AskDesignation()
    print("here")
    if request.method == 'POST':
        # desi = request.form.get('designation')
        desi = request.get_json()['designation'].lower()
        print(desi)
        cur = mysql.connection.cursor()
        cur.execute("select p.designation from designation p where p.designation=%s", (desi,))
        mysql.connection.commit()
        res = cur.fetchall()
        msg = {}
        if res:
            msg['error'] = "Designation Exists"
        else:
            cur.execute("insert into designation (designation) values (%s)", (desi,))
            mysql.connection.commit()
            msg['success'] = 'Desgination Added'
            cur.execute("select p.designation from designation p where p.designation=%s", (desi,))
            mysql.connection.commit()
            ret = cur.fetchall()[0]
            msg['designation_id'] = ret
            
            
        return json.dumps(msg)
    return ""


@bd_report.route('/admin/add_project',methods=['GET','POST'])
def add_project():
    # form = AddProject()

    if session['uName']:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            res_dict = {}
            get_data = request.get_json()
            if get_data['project']:
                data = get_data['project'].lower()
                cur.execute("select * from project where project_name=%s", (data, ))
                mysql.connection.commit()
                ret = cur.fetchall()
                if ret:
                    res_dict['msg'] = "Project Already Exists"
                else:
                    cur.execute("insert into project (project_name) values (%s)", (data,))
                    mysql.connection.commit()
                    res_dict['msg'] = "Project Updated"

                return jsonify(res_dict)

        cur.execute("select * from project")
        mysql.connection.commit()
        res = cur.fetchall()
        return render_template('add/add_project.html', uName = session['uName'], projects=res)
    else:
        return render_template('login.html')

@bd_report.route('/admin/add_user',methods=['GET','POST'])
def add_user():
    if session['uName']:
        cur = mysql.connection.cursor()
        msg = {}
        if request.method == 'POST':
            res_dict = {}
            get_data = request.get_json()
            for i in get_data:
                if i['value']:
                    res_dict[i['name']] = i['value']
            
            cur.execute('select username, password from user where username = %s', (res_dict['new_user'], ))
            mysql.connection.commit()
            user = cur.fetchall()
            if user:
                msg['msg'] = "Username Already Exists"
                return jsonify(msg)
            
            cur.execute("insert into user (username, password, designation_id) values (%s, %s, %s)", (res_dict['new_user'], res_dict['new_user_pass'], res_dict['designation']))
            mysql.connection.commit()
            msg['msg'] = f"{res_dict['new_user']} User Added Successfully"
            print(msg)
            return jsonify(msg)

        cur.execute('select * from designation')
        mysql.connection.commit()
        desi = cur.fetchall()
        return render_template('add/add_user.html', uName = session['uName'], designation = desi)
    else:
        return render_template('login.html')


@bd_report.route('/data_list',methods=['GET','POST'])
def data_list():
    board_id = request.form['board_id']
    token = session.get('token')

    base_url = 'https://trello.com/1/'
    list_url = base_url+"boards/{}/lists".format(board_id)

    params_key_and_token = {'key': key, 'token': token}
    response_list = requests.get(list_url,params=params_key_and_token)

    data = response_list.json()
    data_list = {j['id']: j['name'] for j in data}
    data_list = json.dumps(data_list)

    return data_list

@bd_report.route('/hello',methods=['GET','POST'])
def add_work():
    form = AddWork()
    if form.validate_on_submit():
        work = form.work.data
        designation = form.designation.data
        designation_id = designation.id
        add_work = Task(work,designation_id)
        db.session.add(add_work)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add/add_work.html',form=form)

@bd_report.route('/data_card',methods=['GET','POST'])
def data_card():
    list_id = request.form['list_id']
    token = session.get('token')


    base_url = 'https://trello.com/1/'
    card_url = base_url+"lists/{}/cards".format(list_id)

    params_key_and_token = {'key': key, 'token': token}
    response_card = requests.get(card_url, params=params_key_and_token)

    data = response_card.json()
    data_card = {j['id']: j['name'] for j in data}
    data_card = json.dumps(data_card)
    return data_card

@bd_report.route('/view_report',methods=['GET','POST'])
def view_project():
    pass

# @bd_report.route('/view_report',methods=['GET','POST'])
# def view_project():
#     form = ViewProject()
#     if form.validate_on_submit():
#         project_name = form.project_name.data
#         date = request.form.get("date")
#         date = datetime.strptime(date,'%Y-%m-%d')
#         month = date.month
#         user = session.get('user')
#         data = TimeSheet.query.filter((extract('month',TimeSheet.date)==month),TimeSheet.project==project_name).all()
#         work_view = Task.query.all()
#         arr = {}
#         for i in work_view:
#             arr[i.id] = [j for j in data if j.work.designation_id == i.designation_id and j.task_id == i.id]
#         return render_template("view/view_report.html",work_view=work_view,arr=arr)
#     return render_template('view/view_project.html',form=form)


@bd_report.route('/view_user',methods=['GET','POST'])
def view_user():
    pass


# @bd_report.route('/view_user',methods=['GET','POST'])
# def view_user():
#     form = ViewUser()
#     if form.validate_on_submit():
#         user = form.user.data
#         date = request.form.get("date")
#         date = datetime.strptime (date,'%Y-%m-%d')
#         month = date.month
#         data = TimeSheet.query.filter(extract("month",TimeSheet.date)==month,TimeSheet.user==user).all()
#         return render_template("view/view_report_user.html",data=data)
#     return render_template('view/view_user.html', form=form)


@bd_report.route('/view_work',methods=['GET','POST'])
def view_work():
    pass


# @bd_report.route('/view_work',methods=['GET','POST'])
# def view_work():
#     form = ViewWork()
#     if form.validate_on_submit():
#         work = form.work.data
#         date = request.form.get("date")
#         date = datetime.strptime(date,'%Y-%m-%d')
#         month = date.month
#         data = TimeSheet.query.filter(extract("month",TimeSheet.date)==month,TimeSheet.work==work).all()
#         return render_template("view/view_report_work.html",data=data)
#     return render_template("view/view_work.html",form=form)

if __name__ == '__main__':
    bd_report.run(debug=True)
