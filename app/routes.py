from app import app
from flask import render_template, flash, redirect, url_for, request, send_from_directory, session, jsonify
from werkzeug import secure_filename
from app.utils import make_gif, read_img, save_nii
import os
import re
from app.DBConnection import  Db
import numpy as np

app.secret_key="dfsdfsdfsdfsdfc"

@app.route('/index')
def index():
    files = [file for file in os.listdir(app.config['UPLOAD_FOLDER'])
             if file.endswith('.mmri')]
    return render_template('indexaa.html', title='Home', files=files)


@app.route('/upload')
def upload_file():
    return render_template('upload.html', title='Upload the MRI files')


@app.route('/uploader', methods=['POST'])
def upload_file_():
    cause = ''  # For catching specific cause of error
    modalities = ['t1', 't2w', 't1ce', 'flair']
    pat = re.compile(r'[^\.]*\.(.*)')
    formats = {m: pat.findall(request.files[m].filename)[0] for m in modalities}
    if request.method == 'POST':
        try:
            cause = 'while uploading the files. Ensure that the files'
            ' are accessible and try again. '
            for m in modalities:
                f = request.files[m]
                f.save(
                 os.path.join(
                   app.config['UPLOAD_FOLDER'],
                   secure_filename(f"{request.form['name']}_{m}.{formats[m]}")
                   )
                )
            flash('Files were uploaded succesfully.')

            cause = 'while exporting the files into a single multimodal-MRI'
            ' (.mmri) file. Make sure the uploaded files are valid MRI files'
            ' and try again.'
            img = np.array(
             [
               read_img(
                 os.path.join(
                   app.config['UPLOAD_FOLDER'],
                   secure_filename(f"{request.form['name']}_{m}.{formats[m]}")
                 )
               )
               for m in modalities
             ]
            )

            np.save(os.path.join(
              app.config['UPLOAD_FOLDER'],
              secure_filename(f"{request.form['name']}")
            ), img)

            os.rename(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    secure_filename(f"{request.form['name']}.npy")
                    ),
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    secure_filename(f"{request.form['name']}.mmri")
                    )
                )
            cause = 'while cleaning up the temporary files. Make sure this '
            f'path is accessible and try again:{app.config["UPLOAD_FOLDER"]}'
            [os.remove(
              os.path.join(
                app.config['UPLOAD_FOLDER'],
                f'{request.form["name"]}_{m}.{formats[m]}'
                )
            ) for m in modalities]

            cause = None

        except Exception as e:
            flash(
                f'An error occured {cause}' if cause is not None else
                'An unknown error occured.')
            return f"""<div class="w3-container">
              <h1 class="w3-xxxlarge w3-text-black"><b>Sorry Something Went Wrong.</b></h1>
              <hr style="width:50px;border:5px solid red" class="w3-round">
              <p>An error occured while uploading the MRI files. See below for more info.</p>
              <br />
              <h3 class="w3-xlarge w3-text-black"><b>Error Text:</b></h3>
              <hr>
              <p> {e} </p>
              <a href='/upload'><h3 class="w3-xlarge w3-text-black">
                <b>&lt; Go back and try again.</b></h3></a>
            </div>"""
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        file = request.form.get('files_dropdown')
        print(file)
        print(app.config["UPLOAD_FOLDER"])
        # try:
        out_file = make_gif(file)
        success = True
        error = None
        # except Exception as e:
        #     success = False
        #     error = str(e)

        return render_template('analyze.html', title='Results', success=success,
                               file=out_file, error=error, folder=app.config["UPLOAD_FOLDER"])
    elif request.method == 'GET':
        if app.config['TESTING_ANALYZE']:
            return render_template('analyze.html', title='Testing Analyze', success=True,
                                   file='Test', error='error', folder=app.config["UPLOAD_FOLDER"])
        else:
            flash('Select a MMRI file from the list or add your own to get the prediction result.')
            return redirect(url_for('index'))


@app.route('/download-mask/<file>/<mod>', methods=['GET'])
def download(file, mod):
    if request.method == 'GET':
        mods = {'t1': 0, 't2': 1, 't1ce': 2, 'flair':3}

        img = np.load(f'{app.config["UPLOAD_FOLDER"]}/{file}.npy')
        save = img[mods[mod]]
        name = f'{file[:-5]}_{mod}.nii.gz'
        save_nii(save, name)
        return redirect(url_for('static', filename=app.config['EXPORT_FOLDER_REL']+name), code=301)




################################
@app.route('/')
def login():
    return render_template('index.html')
@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login` WHERE `username`='"+username+"' AND `password`='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['loginid']
        if res['type']=="admin":
            return redirect('/admin_home')
        elif res['type']=="doctor":
            return redirect('/dr_home')
        elif res['type']=="patient":
            return redirect('/pt_home')
        else:
            return'''<script>alert('Invalid Username or Password');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid Username or Password');window.location='/'</script>'''



# @app.route("/index")
# def index():
#     return  render_template("patient/index.html")

#admin////////////////////////////////////////////////

@app.route('/add_disease')
def add_disease():
    return render_template('admin/add_disease.html')
@app.route('/add_disease_post',methods=['post'])
def add_disease_post():
    disease_name=request.form['textfield']
    description=request.form['textarea']
    db=Db()
    qry="INSERT INTO `disease`(`disease_name`,`description`) VALUES('"+disease_name+"','"+description+"')"
    res=db.insert(qry)
    return redirect('/disease_mgmt')

@app.route('/admin_home')
def admin_home():
    return render_template('admin/admin_index.html')

@app.route('/add_symptoms')
def add_symptoms():
    db=Db()
    qry="SELECT * FROM `disease`"
    res=db.select(qry)
    return render_template('admin/add_symptoms.html',data=res)

@app.route('/add_symptoms_post',methods=['post'])
def add_symptoms_post():
    symptom=request.form['textarea']
    disease=request.form['select']
    db=Db()
    qry="INSERT INTO `symptoms`(`diseaseid`,`symptom`) VALUES ('"+disease+"','"+symptom+"')"
    res=db.insert(qry)
    return redirect('/symptom_mgmt')



#change Password
@app.route('/change_password')
def change_password():
    return render_template('admin/change_pass.html')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    current_password=request.form['textfield2']
    new_password=request.form['textfield3']
    confirm_password=request.form['textfield4']
    db=Db()
    qry="SELECT * FROM `login` WHERE `password`='"+current_password+"' AND `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if new_password==confirm_password:
            qry2="UPDATE `login` SET `password`='"+confirm_password+"' WHERE `loginid`='"+str(session['lid'])+"'"
            res2=db.update(qry2)
            return '''<script>alert('Password Change Successfull');window.location='/'</script>'''
        else:
            return '''<script>alert('Invalid Username or Password');window.location='/change_password'</script>'''
    else:
         return '''<script>alert('Invalid Username or Password');window.location='/change_password'</script>'''



@app.route('/disease_mgmt')
def disease_mgmnt():
    db=Db()
    qry="SELECT * FROM `disease`"
    res=db.select(qry)
    return render_template('admin/disease_mgmt.html',data=res)

@app.route('/disease_mgmt_post',methods=['post'])
def disease_mgmt_post():
     search=request.form['textfield']
     db=Db()
     qry="SELECT * FROM `disease`WHERE `disease_name`LIKE '"+search+"'"
     res=db.select(qry)
     return render_template('admin/disease_mgmt.html',data=res)
#to delete after clicking delete
@app.route('/delete_disease/<id>')
def delete_disease(id):
    db=Db()
    qry="DELETE FROM`disease` WHERE `diseaseid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/disease_mgmt')

#edit diesease get
@app.route('/edit_disease/<id>')
def edit_disease(id):
    db=Db()
    qry="SELECT * FROM `disease` WHERE `diseaseid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('admin/edit_disease.html',data=res)
#edit disease post
@app.route('/edit_disease_post',methods=['post'])
def edit_disease_post():
    id=request.form['id']
    disease_name = request.form['textfield']
    description = request.form['textarea']
    db=Db()
    qry="UPDATE `disease` SET `disease_name`='"+disease_name+"',`description`='"+description+"' WHERE `diseaseid`='"+id+"'"
    res=db.update(qry)
    return redirect('/disease_mgmt')

@app.route('/send_reply/<id>')
def send_reply(id):
    return render_template('admin/Send_reply.html',id=id)
@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    id=request.form['id']
    reply=request.form['textarea']
    db=Db()
    qry="UPDATE `complaints` SET `reply`='"+reply+"' , `cmpstatus` ='replied' WHERE `complaintid`='"+id+"'"
    res=db.update(qry)
    return  '''<script>alert('Reply successfully Sent');window.location='/view_complaint'</script>'''


#symptoms
@app.route('/symptom_mgmt')
def symptom_mgmt():
    db=Db()
    qry="SELECT * FROM `symptoms` INNER JOIN `disease`ON `symptoms`.`diseaseid`=`disease`.`diseaseid`"
    res=db.select(qry)
    return render_template('admin/Symptom_mngmnt.html',data=res)
#to delete symptoms
@app.route('/delete_symptom/<id>')
def delete_symptom(id):
    db=Db()
    qry="DELETE FROM`symptoms` WHERE `symptomid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/symptom_mgmt')
@app.route('/symptom_mgmt_post',methods=['post'])
#symptoms search
def symptom_mgmt_post():
     search=request.form['textfield']
     dbv=Db()
     qry="SELECT * FROM `symptoms`  INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid` WHERE `symptom`LIKE '"+search+"'"
     res=dbv.select(qry)
     return render_template('admin/Symptom_mngmnt.html',data=res)
#edit Symptoms get
@app.route('/edit_symptoms/<sid>')
def edit_symptoms(sid):
    db=Db()
    qry="SELECT * FROM `symptoms` INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid` WHERE`symptomid`='"+sid+"'"
    res=db.selectOne(qry)
    return render_template("admin/edit_symptoms.html",data=res)
#edit symptoms post
@app.route('/edit_symptoms_post',methods=['post'])
def edit_symptoms_post():
    sid=request.form['id']
    diseaseid=request.form['textfield']
    description=request.form['textarea']
    db=Db()
    qry="UPDATE `symptoms` SET `symptom`='"+description+"' WHERE `symptomid`='"+sid+"'"
    res=db.update(qry)
    return redirect('/symptom_mgmt')

@app.route('/view_complaint')
def view_complaint():
    db=Db()
    qry="SELECT * FROM `complaints`INNER JOIN `user`ON `user`.`user_lid`=`complaints`.`userid` JOIN `doctor` ON  `doctor`.`doctor_lid`=`complaints`.`doctorid`"
    res=db.select(qry)
    return render_template('admin/View comp_reply.html',data=res)


@app.route('/view_review')
def view_review():
    db=Db()
    qry="SELECT * FROM `review` JOIN `user`ON `user`.`user_lid`= `review`.`userid` JOIN `doctor` ON  `doctor`.`doctor_lid`= `review`.`doctorid`"
    res=db.select(qry)
    return render_template('admin/View Rev_rate.html',data=res)


# @app.route('/view_review_post',methods=['post'])
# def view_review_post():
#     search = request.form['select']
#     db=Db()
#     qry="SELECT * FROM `review` INNER JOIN `user`ON `user`.`userid`= `review`.`userid` JOIN `doctor` ON  `doctor`.`doctorid`= `review`.`doctorid` WHERE `reviewstar`='"+search+"'"
#     res=db.select(qry)
#     return render_template('admin/View Rev_rate.html',data=res)


#view user
@app.route('/view_user')
def view_user():
    db=Db()
    qry="SELECT * FROM `user`"
    res=db.select(qry)
    return render_template('admin/View User.html',data=res)
@app.route('/view_user_post',methods=['post'])
def view_user_post():
     search=request.form['textfield']
     db = Db()
     qry = "SELECT * FROM `user` where username like '%"+search+"%'"
     res = db.select(qry)
     return render_template('admin/View User.html', data=res)


#view docter
@app.route('/view_doctor')
def view_doctor():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `drstatus`='pending'"
    res=db.select(qry)
    return render_template('admin/View_appove_dr.html',data=res)
#reject docotr
@app.route('/reject_dr/<id>')
def reject_dr(id):
    db=Db()
    qry="DELETE FROM`doctor`WHERE `doctorid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_doctor')
@app.route('/approve_dr/<id>')
def approve_dr(id):
    db=Db()
    qry="UPDATE `doctor` SET `drstatus`='approved' WHERE `doctorid`='"+id+"'"
    res=db.update(qry)
    return redirect('/approved_dr')

@app.route('/approved_dr')
def approved_dr():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `drstatus`='approved'"
    res=db.select(qry)
    return render_template('admin/approved_dr.html',data=res)
@app.route('/approved_dr_post',methods=['post'])
def approved_dr_post():
    search = request.form['textfield']
    db = Db()
    qry = "SELECT * FROM `doctor`WHERE `doctorname`LIKE '" + search + "'"
    res = db.select(qry)
    return render_template("admin/approved_dr.html",data=res)

@app.route('/view_doctor_post',methods=['post'])
def view_doctor_post():
     search=request.form['textfield']
     db=Db()
     qry="SELECT * FROM `doctor`WHERE `doctorname`LIKE '"+search+"'"
     res=db.select(qry)
     return render_template('admin/View_appove_dr.html',data=res)

@app.route('/view_fb')
def view_fb():
    db=Db()
    qry="SELECT * FROM `feedback` INNER JOIN  `user`ON `user`.`user_lid`= `feedback`.`userid` JOIN `doctor` ON  `doctor`.`doctor_lid`= `feedback`.`doctorid`"
    res=db.select(qry)
    return render_template('admin/view_fb.html',data=res)
@app.route('/view_fb_post',methods=['post'])
def view_fb_post():
    date1=request.form['textfield']
    date2=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `feedback` INNER JOIN  `user`ON `user`.`userid`= `feedback`.`userid` JOIN `doctor` ON  `doctor`.`doctorid`= `feedback`.`doctorid` WHERE `date` BETWEEN '"+date1+"' AND '"+date2+"'"
    res=db.select(qry)
    return render_template('admin/view_fb.html',data=res)

#doctor/////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/dr_home')
def dr_home():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `doctor_lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("doctor/dr_home.html",data=res)


@app.route('/chat_patient')
def chat_patient():
    return render_template('doctor/Chat_patnts.html')
@app.route('/chat_patient_post',methods=['post'])
def chat_patient_post():
    fromdate=request.form['texfield']
    todate=request.form['textfield2']
    return "ok"

#precription
@app.route('/load_prescription/<id>')
def load_prescription(id):
    db=Db()
    qry="SELECT * FROM `prescription` JOIN `appointment` ON `appointment`.`appointmentid`=`prescription`.`appointmentid` JOIN `user` ON `appointment`.`userid` = `user`.`user_lid` WHERE `appointment`.`appointmentid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('doctor/Load_prescription.html',data=res)
@app.route('/add_prescription/<id>')
def add_prescription(id):
    db=Db()
    qry="SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid`   WHERE `appointmentid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('doctor/add_prescription.html',data=res)

@app.route('/upload_prescription',methods=['post'])
def upload_prescription():
    db=Db()
    appointmentid=request.form['id']
    prescription=request.form['textarea']
    findings=request.form['textarea1']
    qry="INSERT INTO `prescription` (`appointmentid`,`Findings`,`prescription`) VALUES ('"+appointmentid+"','"+prescription+"','"+findings+"') "
    res=db.insert(qry)
    return ''' <script>alert("Successfully Prescribed"); window.location='/view_appointment'</script>'''



#schedule
@app.route('/schedule_mgmt')
def schedule_mgmt():
    db=Db()
    qry="SELECT * FROM `schedule` WHERE `doctorid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template('doctor/Schedule_mngmt.html',data=res)
@app.route('/delete_schedule/<id>')
def delete_schedule(id):
    db=Db()
    qry="DELETE FROM `schedule` WHERE `scheduleid`='"+id+"'"
    res=db.delete(qry)
    return ''' <script>confirm("Are you Sure"); window.location='/schedule_mgmt'</script>'''

#add schedule
@app.route('/add_schedule')
def add_schedule():
    return render_template('doctor/add_schedule.html')
@app.route('/add_schedule_post',methods=['post'])
def add_schedule_post():
    starttime=request.form['textfield2']
    endtime=request.form['textfield3']
    date=request.form['textfield']
    db=Db()
    qry="INSERT INTO `schedule` (`doctorid`,`date`,`starttime`,`endtime`) VALUES ('"+str(session['lid'])+"','"+date+"','"+starttime+"','"+endtime+"')"
    res=db.insert(qry)
    return ''' <script>alert("Successfullly scheduled");window.location='/add_schedule'</script>'''
#edit_schedule
@app.route('/edit_schedule/<id>')
def edit_schedule(id):
    db=Db()
    qry="SELECT * FROM `schedule` WHERE `scheduleid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('doctor/edit_schedule.html',data=res)
@app.route('/edit_schedule_post',methods=['post'])
def edit_schedule_post():
    scheduleid=request.form['hidden']
    starttime = request.form['textfield2']
    endtime = request.form['textfield3']
    date = request.form['textfield']
    db=Db()
    qry="UPDATE `schedule` SET `date`='"+date+"',`starttime`='"+starttime+"',`endtime`='"+endtime+"' WHERE `scheduleid`='"+scheduleid+"'"
    res=db.update(qry)
    return ''' <script>alert("Successfully Edited");window.location='/schedule_mgmt'</script>'''


#singup
@app.route('/dr_signup')
def dr_signup():
    return render_template('doctor/register_index.html')

@app.route('/dr_signup_post',methods=['post'])
def dr_signup_post():
    name=request.form['textfield']
    dob=request.form['textfield1']
    pin = request.form['textfield2']
    post = request.form['textfield3']
    place = request.form['textfield4']
    house = request.form['textfield5']
    phone = request.form['textfield6']
#==================save phot0==============
    photo=request.files['fileField']
    from datetime import datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"D:\\Brainy-master\\app\\static\\doctor\\"+ date +".jpg")
    path="/static/doctor/"+ date +".jpg"
    gender=request.form['RadioGroup1']
    state=request.form['select']
    district=request.form['select2']
    email = request.form['textfield7']
    qualification = request.form['textarea']
    experience = request.form['textfield8']
    username = request.form['textfield9']
    password=request.form['textfield10']
    confirm_pass = request.form['textfield11']
    db=Db()
    qry2="INSERT INTO `login` (`username`,`password`,`type`) VALUES ('"+username+"','"+confirm_pass+"','doctor')"
    res1 = db.insert(qry2)
    qry="INSERT INTO `doctor` (`doctor_lid`,`doctorname`,`dob`,`gender`,`photo`,`state`,`district`,`pin`,`post`,`place`,`house`,`phone`,`email`,`qualification`,`experience`,`drstatus`) VALUES ('"+str(res1)+"','"+name+"','"+dob+"','"+gender+"','"+str(path)+"','"+state+"','"+district+"','"+pin+"','"+post+"','"+place+"','"+house+"','"+phone+"','"+email+"','"+qualification+"','"+experience+"','pending')"
    res=db.insert(qry)
    return redirect('/')

#change pass
@app.route('/dr_change_pass')
def dr_change_pass():
    return render_template('doctor/dr_change_pass.html')


#view  dr symptoms
@app.route('/view_dr_symptoms')
def view_dr_symptoms():
    db=Db()
    qry="SELECT * FROM `symptoms` INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid` "
    res=db.select(qry)
    return render_template('doctor/view Symptoms.html',data=res)
@app.route('/view_dr_symptoms_post',methods=['post'])
def view_dr_symptoms_post():
     search=request.form['textfield']
     db = Db()
     qry = "SELECT * FROM `symptoms`  INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid` WHERE `symptom`LIKE '" + search + "'"
     res = db.select(qry)
     return render_template('doctor/view Symptoms.html',data=res)

#view dr disease
@app.route('/view_dr_disease')
def view_dr_disease():
    db=Db()
    qry="SELECT * FROM `disease`"
    res=db.select(qry)
    return render_template('doctor/view_diseases.html',data=res)
@app.route('/view_dr disease_post',methods=['post'])
def view_dr_disease_post():
     search=request.form['textfield']
     db=Db()
     qry="SELECT * FROM `disease` WHERE `disease_name`='"+search+"'"
     res=db.select(qry)
     return render_template('doctor/view_diseases.html',data=res)

#view docotr profile
@app.route('/view_dr_profile')
def view_dr_profile():
    db=Db()
    qry="SELECT * FROM `doctor` INNER JOIN `login` ON `login`.`loginid`=`doctor`.`doctor_lid` WHERE `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('doctor/View_profile.html',data=res)
@app.route('/view_dr_profile_post',methods=['post'])
def view_dr_profile_post():
    return redirect('/edit_dr_profile')

#edit Dr Profile
@app.route('/edit_dr_profile')
def edit_dr_profile():
    db=Db()
    qry="SELECT * FROM `doctor` INNER JOIN `login` ON `login`.`loginid`=`doctor`.`doctor_lid` WHERE `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('doctor/edit _dr_profile.html',data=res)
@app.route('/edit_dr_profile_post',methods=['post'])
def edit_dr_profile_post():
    name = request.form['textfield']
    dob = request.form['textfield1']
    pin = request.form['textfield2']
    post = request.form['textfield3']
    place = request.form['textfield4']
    house = request.form['textfield5']
    phone = request.form['textfield6']
    photo = request.files['fileField']
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"D:\\Brainy-master\\app\\static\\doctor\\" + date + ".jpg")
    path = "/static/doctor/" + date + ".jpg"
    gender = request.form['RadioGroup1']
    state = request.form['select']
    district = request.form['select2']
    email = request.form['textfield7']
    qualification = request.form['textarea']
    experience = request.form['textfield8']
    username = request.form['textfield9']
    db=Db()
    qry1="UPDATE `doctor` SET `doctorname`='"+name+"',`dob`='"+dob+"',`gender`='"+gender+"',photo='"+path+"',`state`='"+state+"',`district`='"+district+"',`pin`='"+pin+"',`post`='"+post+"',`place`='"+place+"',`house`='"+house+"',`phone`='"+phone+"',`email`='"+email+"',`qualification`='"+qualification+"',`experience`='"+experience+"' WHERE `doctor_lid`='"+str(session['lid'])+"'"
    res1=db.update(qry1)
    qry2="UPDATE `login` INNER JOIN`doctor`ON `doctor`.`doctor_lid`=`login`.`loginid` SET `username`='"+username+"' WHERE `doctor_lid`='"+str(session['lid'])+"'"
    res2=db.update(qry2)
    return redirect('/view_dr_profile')


@app.route('/view_dr_review')
def view_dr_review():
    return render_template('doctor/view_review.html')

#appointment----------
@app.route('/view_appointment')
def view_appointmnt():
    db=Db()
    qry="SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid` JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `schedule`.`doctorid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template('doctor/view_appointment.html',data=res)
@app.route('/reject_appointment/<id>')
def reject_appointment(id):
    db=Db()
    qry="DELETE FROM `appointment` WHERE `appointmentid`='"+id+"'"
    res=db.delete(qry)
    return ''' <script>confirm("are you sure?");window.location='/view_appointment'</script>'''
@app.route('/view_pending')
def view_pending():
    db=Db()
    qry="SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid` JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `schedule`.`doctorid`='"+str(session['lid'])+"'AND `status`='Pending'"
    res=db.select(qry)
    return render_template('doctor/view_appointment.html',data=res)


@app.route('/update_status/<id>')
def update_status(id):
    db=Db()
    qry="UPDATE `appointment` SET `status`='Consulted' WHERE `appointmentid`='"+id+"'"
    res=db.update(qry)
    return ''' <script>window.location='/view_appointment'</script>'''


#patient/////////////////////////////////////////////////////////

@app.route('/pt_home')
def pt_home():
    db=Db()
    qry="SELECT * FROM `user` WHERE `user_lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("patient/pt_home.html",data=res)

#change pass
@app.route('/pt_change_pass')
def pt_change_pass():
    return render_template('patient/pt_change_pass.html')

#appointments
@app.route('/make_appointment/<id>')
def make_appointment(id):
    db=Db()
    qry="INSERT INTO `appointment` (`userid`,`scheduleid`,date,`status`) VALUES ('"+str(session['lid'])+"','"+id+"',curdate(),'Pending')"
    res=db.insert(qry)
    return "<script>alert('Appointment Scheduled');window.location='/pt_appointment'</script>"

@app.route('/cancel_appointment/<id>')
def cancel_appointments(id):
    db=Db()
    qry="DELETE FROM `appointment` WHERE `appointmentid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/pt_appointment')

@app.route('/pt_appointment')
def pt_appointmnet():
    db=Db()
    qry="SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid` JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `appointment`.`userid`='"+str(session['lid'])+"' AND `status`='Pending'"
    res=db.select(qry)
    return render_template('patient/view_pt_appointment.html',data=res)

@app.route('/appointment_history')
def appointment_history():
    db=Db()
    qry="SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid` JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `appointment`.`userid`='"+str(session['lid'])+"' AND `appointment`.`status`='Consulted'"
    res=db.select(qry)
    print(qry)
    return render_template('patient/appointment_history.html',data=res)

@app.route('/pt_rating_review/<id>')
def pt_rating_review(id):
    return render_template('patient/Rating_review.html',id=id)


@app.route('/pt_rating_review_post', methods=['POST'])
def pt_rating_review_post():
    id=request.form['id']
    r=request.form['CheckboxGroup1']
    v=request.form['textarea']
    db=Db()
    qry="INSERT INTO `review`(`userid`,`doctorid`,`reviewstar`,`review`,`date`)VALUES('"+str(session['lid'])+"','"+str(id)+"','"+str(r)+"','"+v+"',curdate())"
    res=db.insert(qry)
    return redirect('/pt_view_doctor')

@app.route('/send_complaint/<id>')
def send_complaint(id):
    return render_template('patient/Send_complaimt.html',id=id)
@app.route('/send_complaint_post',methods=['post'])
def send_complaint_post():
    complaint=request.form['textarea']
    id=request.form['id']
    db=Db()
    qry="INSERT INTO `complaints`(`userid`,`doctorid`,`complaint`,`reply`,`date`,`cmpstatus`)VALUES('"+str(session['lid'])+"','"+id+"','"+complaint+"','pending',CURDATE(),'pending')"
    res=db.insert(qry)
    return redirect('/appointment_history')

@app.route('/send_fb/<id>')
def send_fb(id):
    db = Db()
    qry = "SELECT * FROM `appointment` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `user` ON `appointment`.`userid`= `user`.`user_lid` JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `appointmentid`='"+id+"'"
    res = db.selectOne(qry)
    return render_template('patient/Send_fb.html',data=res)

@app.route('/send_fb_post',methods=['post'])
def send_fb_post():
    feedback=request.form['textarea']
    id=request.form['ide']
    appointmentid=request.form['appid']
    db=Db()
    qry2="INSERT INTO `feedback` (`doctorid`,`userid`,`feedback`,`date`,`appointmentid`) VALUE ('"+id+"','"+str(session['lid'])+"','"+feedback+"',curdate(),'"+appointmentid+"')"
    res2=db.insert(qry2)
    return '''<script>alert('Feedback Successfully sent');window.location='/appointment_history'</script>'''

#pt signup
@app.route('/pt_signup')
def patient_signup():
    return render_template('patient/register_index.html')
@app.route('/pt_signup_post',methods=['post'])
def pt_signup_post():
    username=request.form['textfield']
    dob=request.form['textfield2']
    gender=request.form['RadioGroup1']
    photo = request.files['fileField']
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"D:\\Brainy-master\\app\\static\\patient\\" + date + ".jpg")
    path = "/static/patient/" + date + ".jpg"
    state=request.form['select']
    district=request.form['select2']
    pin = request.form['textfield3']
    post = request.form['textfield4']
    place = request.form['textfield5']
    house = request.form['textfield6']
    phone = request.form['textfield7']
    email = request.form['textfield8']
    password=request.form['textfield9']
    confirm_pass = request.form['textfield10']
    db=Db()
    qry2 = "INSERT INTO `login` (`username`,`password`,`type`) VALUES ('" + username + "','" + confirm_pass + "','patient')"
    res1 = db.insert(qry2)
    qry="INSERT INTO `user` (`user_lid`,`username`,`dob`,`gender`,`photo`,`state`,`district`,`pin`,`post`,`place`,`house`,`phone`,`email`) VALUES ('"+str(res1)+"','"+username+"','"+dob+"','"+gender+"','"+path+"','"+state+"','"+district+"','"+pin+"','"+post+"','"+place+"','"+house+"','"+phone+"','"+email+"')"
    res=db.insert(qry)
    return redirect('/')

@app.route('/edit_pt_profile')
def edit_pt_profile():
    db=Db()
    qry="SELECT * FROM `user` INNER JOIN `login` ON `login`.`loginid`=`user`.`user_lid` WHERE `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('patient/edit_pt_profile.html',data=res)

@app.route('/edit_pt_profile_post', methods=['POST'])
def edit_pt_profile_post():
    username = request.form['textfield']
    dob = request.form['textfield2']
    gender = request.form['RadioGroup1']
    photo = request.files['fileField']

    state = request.form['select']
    district = request.form['select2']
    pin = request.form['textfield3']
    post = request.form['textfield4']
    place = request.form['textfield5']
    house = request.form['textfield6']
    phone = request.form['textfield7']
    email = request.form['textfield8']
    if photo!='':
        from datetime import datetime
        date = datetime.now().strftime("%Y%m%d-%H%M%S")
        photo.save(r"D:\\Brainy-master\\app\\static\\patient\\" + date + ".jpg")
        path = "/static/patient/" + date + ".jpg"
        db = Db()
        qry="UPDATE `user` SET `username`='"+username+"',`dob`='"+dob+"',`gender`='"+gender+"',`photo`='"+path+"',`house`='"+house+"',`place`='"+place+"',`post`='"+post+"',`pin`='"+pin+"',`district`='"+district+"',`state`='"+state+"',`phone`='"+phone+"',`email`='"+email+"' WHERE `user_lid`='"+str(session['lid'])+"'"
        res=db.update(qry)
        return redirect('/view_pt_profile')
    else:
        db = Db()
        qry = "UPDATE `user` SET `username`='" + username + "',`dob`='" + dob + "',`gender`='" + gender + "',`house`='" + house + "',`place`='" + place + "',`post`='" + post + "',`pin`='" + pin + "',`district`='" + district + "',`state`='" + state + "',`phone`='" + phone + "',`email`='" + email + "' WHERE `user_lid`='" + str(
            session['lid']) + "'"
        res = db.update(qry)
        return redirect('/view_pt_profile')

@app.route('/reject_pt/<id>')
def reject_pt(id):
    db=Db()
    qry="DELETE FROM `user` WHERE `userid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_user')

#pt view doctor
@app.route('/pt_view_doctor')
def pt_view_doctor():
    db = Db()
    qry = "SELECT * FROM `doctor` WHERE `drstatus`='approved'"
    res = db.select(qry)
    return render_template('patient/view_doctor.html',data=res)
#search
@app.route('/pt_view_doctor_post',methods=['post'])
def pt_view_doctor_post():
     search=request.form['textfield']
     db=Db()
     qry="SELECT * FROM `doctor`WHERE `doctorname`LIKE '"+search+"'"
     res=db.select(qry)
     return render_template('patient/view_doctor.html',data=res)

@app.route('/view_dr_sched/<id>')
def view_dr_sched(id):
    db=Db()
    qry="SELECT * FROM `schedule` INNER JOIN `doctor` ON `schedule`.`doctorid`=`doctor`.`doctor_lid` WHERE `schedule`.`doctorid`='"+id+"'"
    res=db.select(qry)
    return render_template('patient/View_drschdl.html',data=res)

#view disease & symptoms
@app.route('/view_pt_symptoms')
def view_pt_symptoms():
    db=Db()
    qry="SELECT * FROM `symptoms` INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid`"
    res=db.select(qry)
    return render_template('patient/View_ds_symp.html',data=res)
@app.route('/view_pt_symptoms_post',methods=['post'])
def pt_view_pt_symptoms_post():
     search=request.form['textfield']
     db=Db()
     qry="SELECT * FROM `symptoms` INNER JOIN `disease` ON `symptoms`.`diseaseid`=`disease`.`diseaseid` WHERE`disease_name`='"+search+"'"
     res=db.select(qry)
     return render_template('patient/View_ds_symp.html',data=res)

@app.route('/view_prescription/<id>')
def view_prescription(id):
    db=Db()
    qry="SELECT * FROM `prescription` JOIN `appointment` ON `appointment`.`appointmentid`=`prescription`.`appointmentid` JOIN `user` ON `user`.`user_lid`=`appointment`.`userid` JOIN `schedule`  ON `appointment`.`scheduleid`= `schedule`.`scheduleid` JOIN `doctor` ON `doctor`.`doctor_lid`=`schedule`.`doctorid` WHERE `appointment`.`appointmentid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('patient/View_prescription.html',data=res)

@app.route('/view_prescription_post',methods=['post'])
def pt_view_prescription_post():
     search=request.form['textfield']
     return "ok"

@app.route('/view_pt_profile')
def view_pt_profile():
    db=Db()
    qry="SELECT * FROM `user`  WHERE `user_lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('patient/View_profile.html',data=res)



@app.route('/doctorchat')
def doctorchat():
    return render_template("doctor/fur_chat.html")



@app.route('/userchat')
def userchat():
    return render_template("patient/fur_chat.html")





@app.route("/viewmsg/<senid>")        # refresh messages chatlist
def viewmsg(senid):
    uid=senid
    qry = "select from_id,message as msg,date from chat where (from_id='"+str(session['lid'])+"' and to_id='" + uid + "') or ((from_id='" + uid + "' and to_id='"+str(session['lid'])+"')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    return jsonify(data=res)


@app.route("/chatview",methods=['post'])
def chatview():
    db=Db()
    qry="select * from doctor"
    res=db.select(qry)
    return jsonify(data=res)

@app.route("/insert_chat/<senid>/<msg>")
def insert_chat(senid,msg):
    db=Db()
    qry="insert into chat (date,time,from_id,to_id,message) values (curdate(),curtime(),'"+str(session['lid'])+"','"+senid+"','"+msg+"')"
    db.insert(qry)
    return jsonify(status="ok")





@app.route("/chatview1",methods=['post'])
def chatview1():
    db=Db()
    qry="select * from user"
    res=db.select(qry)
    return jsonify(data=res)



@app.route('/pt_view_complaint')
def pt_view_complaint():
    db=Db()
    qry="SELECT * FROM `complaints` JOIN `doctor` ON  `doctor`.`doctor_lid`=`complaints`.`doctorid` where `userid` ='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template('patient/View comp_reply.html',data=res)
