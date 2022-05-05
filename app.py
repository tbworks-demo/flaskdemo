from operator import and_
from os import error, mkdir
from flask import Flask, render_template, flash, request, url_for, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FileField
from wtforms import validators
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired

from datetime import datetime, date, timedelta

from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, or_ , and_
from forms import Login, Str_case_approval, Str_conversations, Str_case_update, Str_import_entry, Str_export_entry, Str_case_update_export, Str_case_update_mentor_hawb, Str_s4s_entry, Str_s4s_conversations, Str_s4s_update

import pandas
import numpy

from io import BytesIO #Converts data from Database into bytes

import os #File operations

import boto3
import os
import json
from spaces import Client

#New 18.02.2022
from io import BytesIO
import paramiko, sys
import time


#FOR E-MAIL SENDING
import os
import smtplib
import imghdr
from email.message import EmailMessage

#İlerleyen safhalarda Jane'ın akıbetini sorduğu dosyaların süreç çalışmasına bakalım. Yani Mentor ekibi açık kalmış olan dosyaları nasıl görüntüleyebilir? Bunlarla ilgili hatırlatma tetikleyicisi ne olmalı? 15.02.2022
#Ana ekrana See All Records her iki status durumunu da ekleyelim. 16.02.2022 - Burada kaldık!!

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tansubaktiran:secret@secret/tansubaktiran"


#Secret key
app.config['SECRET_KEY'] = "secret"
#Initialize the adatabase
db = SQLAlchemy(app)

#Setting up user login parts
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'


#USER LOGIN FUNCTION
@login_manager.user_loader
def load_user(id):
    return str_staff_db.query.get(int(id)) 

#TIME NOW - TO BE USED IN TIME CALCULATIONS
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")



class str_staff_db(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    name_db = db.Column(db.String(200))
    email_db = db.Column(db.String(200))
    password_db = db.Column(db.String(120))
    role_db = db.Column(db.String(120))
    last_login_db = db.Column(db.DateTime, default=datetime.utcnow)
    last_logout_db = db.Column(db.DateTime, default=datetime.utcnow)
        
    def __repr__(self):
        
        return '<Name %r>' % self.name_db

class str_cases_db(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    str_ref_db = db.Column(db.String(30))
    tur_ref_db = db.Column(db.String(30))
    date_added_db = db.Column(db.DateTime, default=datetime.utcnow)
    initial_status_db = db.Column(db.String(20), nullable=True)
    cancellation_status_db = db.Column(db.String(20), nullable=True)
    status_db = db.Column(db.String(20), nullable=True)
    file1_name_db = db.Column(db.String(50), nullable=True)
    file1_data_db = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)
    file2_name_db = db.Column(db.String(50), nullable=True)
    file2_data_db = db.Column(db.LargeBinary, nullable=True)
    file3_name_db = db.Column(db.String(50), nullable=True)
    file3_data_db = db.Column(db.LargeBinary, nullable=True)
    file4_name_db = db.Column(db.String(50), nullable=True)
    file4_data_db = db.Column(db.LargeBinary, nullable=True)
    file5_name_db = db.Column(db.String(50), nullable=True)
    file5_data_db = db.Column(db.LargeBinary, nullable=True)
    file6_name_db = db.Column(db.String(50), nullable=True)
    file6_data_db = db.Column(db.LargeBinary, nullable=True)
    file7_name_db = db.Column(db.String(50), nullable=True)
    file7_data_db = db.Column(db.LargeBinary, nullable=True)
    
    notes_db = db.Column(db.String(1500), nullable=True)
    operation_type_db = db.Column(db.String(50), nullable=True)
    enduser_name_surname_db = db.Column(db.String(50), nullable=True)
    enduser_company_name_db = db.Column(db.String(50), nullable=True)
    enduser_address_db = db.Column(db.String(200), nullable=True)
    enduser_tel_db = db.Column(db.String(50), nullable=True)
    enduser_email_db = db.Column(db.String(100), nullable=True)
    conversations = db.relationship('conversations_db', backref='case')
    new_file1_name_db = db.Column(db.String(50), nullable=True)
    new_file1_data_db = db.Column(db.LargeBinary, nullable=True)
    new_file2_name_db = db.Column(db.String(50), nullable=True)
    new_file2_data_db = db.Column(db.LargeBinary, nullable=True)
    new_file3_name_db = db.Column(db.String(50), nullable=True)
    new_file3_data_db = db.Column(db.LargeBinary, nullable=True)
    new_file4_name_db = db.Column(db.String(50), nullable=True)
    new_file4_data_db = db.Column(db.LargeBinary, nullable=True)
    
    export_pickup_ups_or_enduser_db = db.Column(db.String(20), nullable=True)
    export_pickup_username_db = db.Column(db.String(200), nullable=True)
    export_pickup_company_db = db.Column(db.String(200), nullable=True)
    export_pickup_address_db = db.Column(db.String(200), nullable=True)
    export_pickup_telephone_db = db.Column(db.String(200), nullable=True)
    export_pickup_email_db = db.Column(db.String(100), nullable=True)
    
    export_mentor_reference_db = db.Column(db.String(30), nullable=True)
    export_waybill_no_db = db.Column(db.String(30), nullable=True)
    export_mentor_status_db = db.Column(db.String(20), nullable=True)

class conversations_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_db = db.Column(db.String(50))
    date_of_sending_db = db.Column(db.DateTime, default=datetime.utcnow)
    text_db = db.Column(db.String(2500))
    case_id_db = db.Column(db.Integer, db.ForeignKey('str_cases_db.id'))
    str_ref_db = db.Column(db.String(50))

class str_s4s_db(db.Model): #added on 23.03.2022
    id = db.Column(db.Integer, primary_key=True)
    cm_rma_db = db.Column(db.String(50))
    juniper_part_no_db = db.Column(db.String(50), nullable=True)
    serial_no_db = db.Column(db.String(50), nullable=True)
    quantity_db = db.Column(db.Integer, nullable=True)
    country_of_origin_db = db.Column(db.String(50), nullable=True)
    rma_no = db.Column(db.String(50), nullable=True)
    sto_no_db = db.Column(db.String(50), nullable=True)
    ups_so_db = db.Column(db.String(50), nullable=True)
    export_invoice_no_db = db.Column(db.String(50), nullable=True)
    export_price_db = db.Column(db.Float, nullable=True)
    export_hawb_no_db = db.Column(db.String(50), nullable=True)
    export_cob_date_db = db.Column(db.DateTime)
    repair_cm_consignee_db = db.Column(db.String(50), nullable=True)
    export_country_db = db.Column(db.String(50), nullable=True)
    export_remarks_db = db.Column(db.String(500), nullable=True)
    cm_reference_db = db.Column(db.String(50), nullable=True) #Bundan sonrakiler inbound - ithalatta kullanılacak.
    
    reimport_invoice_no_db = db.Column(db.String(50), nullable=True)
    reimport_repair_price_db = db.Column(db.Float, nullable=True) 
    total_shipment_value_db = db.Column(db.Float, nullable=True)
    total_customs_cif_value_usd_db = db.Column(db.Float, nullable=True)
    total_customs_cif_value_idr_db = db.Column(db.Float, nullable=True)
    total_shipment_customs_duty_idr_db = db.Column(db.Float, nullable=True)
    total_shipment_customs_vat_idr_db = db.Column(db.Float, nullable=True)
    import_hawb_no_db = db.Column(db.String(50), nullable=True)
    reimport_date_db = db.Column(db.DateTime)
    reimport_consignee_db = db.Column(db.String(50), nullable=True)
    import_country_db = db.Column(db.String(50), nullable=True)
    import_remarks_db = db.Column(db.String(500), nullable=True)
    new_buy_price_db = db.Column(db.Float, nullable=True)
    hs_code_db = db.Column(db.Integer, nullable=True)
    duty_rate_on_new_buy_db = db.Column(db.Float, nullable=True)
    estimated_duty_charge_on_new_buy_db = db.Column(db.Float, nullable=True)
    estimated_vat_charge_on_new_buy_db = db.Column(db.Float, nullable=True)
    case_status_db = db.Column(db.String(40), nullable=True)
    cancellation_status_db = db.Column(db.String(50), nullable=True)
    latest_reimport_date_db = db.Column(db.DateTime)
    
class s4s_conversations_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_db = db.Column(db.String(50))
    date_of_sending_db = db.Column(db.DateTime, default=datetime.utcnow)
    text_db = db.Column(db.String(2500))
    s4s_id_db = db.Column(db.Integer, db.ForeignKey('str_s4s_db.id', ondelete="CASCADE")) 
    serial_no_db = db.Column(db.String(50))

@app.route('/')
@app.route('/index')
def index():
    name="TEST"
    number = 10
    conversation_test_filter = []
    pending_records_filter = []
    pending_records_filter_export = []
    warning_s4s_records = []
    last_logout_of_user = 0
    number_of_pending_records = 0
    number_of_pending_records_export = 0
    if current_user.is_authenticated:
        print(current_user.last_login_db)
        
        last_logout_of_user = current_user.last_logout_db
        print("Last logout of this user : ", last_logout_of_user)

        active_user = str_staff_db.query.filter_by(id=active_user_id).first()
                
        pending_records_filter = str_cases_db.query.filter(str_cases_db.initial_status_db=="Pending").all()
        pending_records_filter_export = str_cases_db.query.filter(str_cases_db.export_mentor_status_db=="Customs Clearance Continue").all()
        conversation_test_filter = conversations_db.query.filter(conversations_db.date_of_sending_db>last_logout_of_user).all()
        number_of_pending_records = len(pending_records_filter)
        number_of_pending_records_export = len(pending_records_filter_export)
        
        
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        target_date = now + timedelta(days=120)
        
        warning_s4s_records = str_s4s_db.query.filter(str_s4s_db.latest_reimport_date_db<target_date).all()

        print("//////pending_records : ",pending_records_filter)
        print("//////number_of_pending_records : ", number_of_pending_records)
        
    
    return  render_template("index.html", name=name, number=number, conversation_test_filter=conversation_test_filter, last_logout_of_user=last_logout_of_user, number_of_pending_records=number_of_pending_records, pending_records_filter=pending_records_filter, pending_records_filter_export=pending_records_filter_export, number_of_pending_records_export=number_of_pending_records_export, warning_s4s_records=warning_s4s_records)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------for s4s entry

@app.route('/new_s4s_entry', methods=["GET", "POST"])
@login_required
def new_s4s_entry():
    form = Str_s4s_entry()
    
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db

    if request.method == "POST":
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        print("S4S request method POST check")
        if form.validate_on_submit():
            
            print("S4S entry work validation step check")
            
            #file operations here
            file1 = request.files['inputFile1'] 
            file2 = request.files['inputFile2']
            file3 = request.files['inputFile3']
            file4 = request.files['inputFile4']
            file5 = request.files['inputFile5']
            file6 = request.files['inputFile6']
                                            
            data1 = file1.read()
            data2 = file2.read()
            data3 = file3.read()
            data4 = file4.read()
            data5 = file5.read()
            data6 = file6.read()

            
            new_s4s = str_s4s_db(              
                cm_rma_db = form.cm_rma_number.data,
                juniper_part_no_db = form.juniper_part_number.data,
                serial_no_db = form.part_serial_number.data,
                quantity_db = form.quantity.data,
                country_of_origin_db = form.country_of_origin.data,
                rma_no = form.rma_number.data,
                sto_no_db = form.sto_number.data,
                ups_so_db = form.ups_so_number.data,
                export_invoice_no_db = form.export_invoice_number.data,
                export_price_db = form.export_price.data,
                export_hawb_no_db = form.export_hawb_number.data,
                export_cob_date_db = form.export_date.data,
                repair_cm_consignee_db = form.repair_cm_consignee.data,
                export_country_db = form.country_of_export.data,
                export_remarks_db = form.export_remarks.data,
                cm_reference_db = form.cm_reference_number.data,
                reimport_invoice_no_db = form.reimport_invoice_number.data,
                reimport_repair_price_db = form.reimport_repair_price.data, 
                total_shipment_value_db = form.total_shipment_value.data,
                total_customs_cif_value_usd_db = form.total_customs_cif_value_usd.data,
                total_customs_cif_value_idr_db = form.total_customs_cif_value_idr.data,
                total_shipment_customs_duty_idr_db = form.total_shipment_customs_duty_idr.data,
                total_shipment_customs_vat_idr_db = form.total_shipment_customs_vat_idr.data,
                import_hawb_no_db = form.reimport_hawb_number.data,
                reimport_date_db = form.reimport_date.data,
                reimport_consignee_db = form.reimport_consignee.data,
                import_country_db = form.country_of_import.data,
                import_remarks_db = form.reimport_remarks.data,
                new_buy_price_db = form.new_buy_price.data,
                hs_code_db = form.hs_code.data,
                duty_rate_on_new_buy_db = form.duty_rate_on_new_buy.data,
                estimated_duty_charge_on_new_buy_db = form.estimated_duty_charge_on_new_buy.data,
                estimated_vat_charge_on_new_buy_db = form.estimated_vat_charge_on_new_buy.data,
                case_status_db = form.case_status.data,
                cancellation_status_db = form.cancellation_status.data
                
            )    
            db.session.add(new_s4s)         
            db.session.commit()             
            
            if form.export_date.data:
                s4s_to_update = str_s4s_db.query.order_by(str_s4s_db.id.desc()).first()
                s4s_to_update.latest_reimport_date_db = s4s_to_update.export_cob_date_db + timedelta(days=(3*365))
                db.session.commit()

           
            potential_list_of_files=[file1.filename, file2.filename, file3.filename, file4.filename, file5.filename, file6.filename]
            list_of_files = []
            for file in potential_list_of_files:
                if file:
                    list_of_files.append(file)                                
            print("List of files :", list_of_files)

            potential_list_of_data=[data1, data2, data3, data4, data5, data6]
            list_of_data = []
            for data_file in potential_list_of_data:
                if data_file:
                    list_of_data.append(data_file)

            Company_path_on_remote = "/root/s4s_tests/"
            subfolder_name = form.part_serial_number.data #Should be unique!!! 24.03.2022

            #Creating a folder/directory on remote server  - 23.02.2022
            transport = paramiko.Transport(("secret", 22))
            transport.connect(username = "root", password = "secret")
            sftp = paramiko.SFTPClient.from_transport(transport)
            try:
                sftp.chdir(Company_path_on_remote + subfolder_name)  # Test if remote_path exists
            except IOError:
                sftp.mkdir(Company_path_on_remote + subfolder_name)  # Create remote_path
                sftp.chdir(Company_path_on_remote + subfolder_name)
            sftp.close()
            transport.close()   
            

            ssh = paramiko.SSHClient()
            ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect("secret", username="root", password="secret")
            
            ftp = ssh.open_sftp()

            for file_name, file_data in zip(list_of_files, list_of_data):                
                if file_data:
                    folder_path_and_filename = Company_path_on_remote + subfolder_name + "/" + file_name
                    ftp.putfo(BytesIO(file_data), folder_path_and_filename)
            
            ftp.close()
            ssh.close()
            flash("New S4S case has been recorded successfully. Thank you!", "success")
            return render_template("index.html", user_name = user_name, user_role = user_role, form=form)
        else:
            flash("There has been a problem during saving the new S4S case. Please inform your administrator.", 'error')
                            
    return render_template("new_s4s_entry.html", form=form, user_name = user_name, user_role = user_role)

@app.route('/view_s4s_entries', methods=["GET", "POST"])
@login_required
def view_s4s_entries(): 

    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    all_s4s_cases = str_s4s_db.query.order_by(str_s4s_db.id).all()

    now = datetime.now()
    today_var = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if request.method == "GET":
        all_cases = str_cases_db.query.order_by(str_cases_db.date_added_db.desc()).all()
        return render_template("view_s4s_entries.html", all_s4s_cases=all_s4s_cases, user_name = user_name, user_role = user_role, now=now)


@app.route('/see_one_s4s/<int:id>', methods=["GET", "POST"])
@login_required
def see_one_s4s(id):
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    s4s_to_show = str_s4s_db.query.get_or_404(id)

    #For time delta calculations only. To be deleted when tdelta tests finish. 31.03.2022
    if (s4s_to_show.reimport_date_db) and (s4s_to_show.export_cob_date_db):
        time_difference_to_be_printed = (s4s_to_show.reimport_date_db) - (s4s_to_show.export_cob_date_db)
        print("Time difference is : ", time_difference_to_be_printed.days)
        print("Type of time difference is : ", type(time_difference_to_be_printed))
        latest_date_of_import = (s4s_to_show.export_cob_date_db) + timedelta(days=(3*365))
        print("Latest date for import : ", latest_date_of_import)
    else:
        print("At least one of the time fields does not exist")


    form = Str_s4s_conversations()
    
    
    conversations_to_display = s4s_conversations_db.query.filter_by(s4s_id_db=s4s_to_show.id).order_by(s4s_conversations_db.id.desc()).all()

    #DOSYA İSİMLERİNİ  DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    list_of_file_names = []
    
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("secret", username="root", password="secret")
    ftp = ssh.open_sftp()
    for i in ftp.listdir("/root/s4s_tests/" + s4s_to_show.serial_no_db):
        print("This is a file in this directory : ", i)
        list_of_file_names.append(i)
        
            
    ftp.close()
    ssh.close()

    #DOSYALARI İSİMLERİNİ DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    
    list_of_file_names.reverse()
    len_of_files_list = len(list_of_file_names)
    
    list_of_file_name_numbers = [] #23.03.2022 -start
    for file_number in range(len_of_files_list):
        list_of_file_name_numbers.append(file_number)
    print("List of file name numbers : ", list_of_file_name_numbers) #23.03.2022 -end
    
    print("Len of files list", len_of_files_list)
    print("List of file names : ", list_of_file_names)
    
    download_text="download_attachment"
    list_of_links = []
    for num_of_file in range(len_of_files_list):
        list_of_links.append(download_text + str(num_of_file+1))

    #IMPORTANT - FOR ZIPPING TWO LISTS IN JINJA2 - IN THIS CASE FOR ZIPPING 
    app.jinja_env.filters['zip'] = zip

    sender_to_be_recorded = current_user.name_db
    s4s_id_to_be_recorded = s4s_to_show.id
    if request.method == "POST":
        if form.validate_on_submit(): # Recording Conversations
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            print("Case S4S NOTE/Conversation entry validation step check")
            conversation_to_be_recorded = s4s_conversations_db(

                sender_db = sender_to_be_recorded,
                text_db = form.text.data,
                s4s_id_db = s4s_id_to_be_recorded,
                date_of_sending_db = dt_string,
                serial_no_db = s4s_to_show.serial_no_db
            )
            if form.text.data:
                db.session.add(conversation_to_be_recorded)
                db.session.commit()
            
            conversations_to_display = s4s_conversations_db.query.filter_by(s4s_id_db=s4s_to_show.id).order_by(s4s_conversations_db.id.desc()).all()
            
        return render_template("see_one_s4s.html", s4s_to_show=s4s_to_show, user_name = user_name, user_role = user_role, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, list_of_file_name_numbers=list_of_file_name_numbers)


    #HOW TO RECORD A FILE IN A FILE SYSTEM RATHER THAN IN THE MYSQL. resolved on 1st March 2022 both reading and writing
    

    return render_template("see_one_s4s.html", user_name = user_name, user_role = user_role, s4s_to_show=s4s_to_show, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, list_of_file_name_numbers=list_of_file_name_numbers)



@app.route('/update_one_s4s/<int:id>', methods=["GET", "POST"])
@login_required
def update_one_s4s(id):

    form = Str_s4s_update()
    s4s_to_update = str_s4s_db.query.get_or_404(id)

    
    if request.method == "GET":

        form = Str_s4s_update() 
        
        form.cm_rma_number.data=s4s_to_update.cm_rma_db
        form.juniper_part_number.data=s4s_to_update.juniper_part_no_db
        form.part_serial_number.data=s4s_to_update.serial_no_db
        form.quantity.data=s4s_to_update.quantity_db
        form.country_of_origin.data=s4s_to_update.country_of_origin_db
        form.rma_number.data=s4s_to_update.rma_no
        form.sto_number.data=s4s_to_update.sto_no_db
        form.ups_so_number.data=s4s_to_update.ups_so_db
        form.export_invoice_number.data=s4s_to_update.export_invoice_no_db
        form.export_price.data=s4s_to_update.export_price_db
        form.export_hawb_number.data=s4s_to_update.export_hawb_no_db
        form.export_date.data=s4s_to_update.export_cob_date_db
        form.repair_cm_consignee.data=s4s_to_update.repair_cm_consignee_db
        form.country_of_export.data=s4s_to_update.export_country_db
        form.export_remarks.data=s4s_to_update.export_remarks_db
        form.cm_reference_number.data=s4s_to_update.cm_reference_db 
        
        form.reimport_invoice_number.data=s4s_to_update.reimport_invoice_no_db
        form.reimport_repair_price.data=s4s_to_update.reimport_repair_price_db 
        form.total_shipment_value.data=s4s_to_update.total_shipment_value_db
        form.total_customs_cif_value_usd.data=s4s_to_update.total_customs_cif_value_usd_db
        form.total_customs_cif_value_idr.data=s4s_to_update.total_customs_cif_value_idr_db
        form.total_shipment_customs_duty_idr.data=s4s_to_update.total_shipment_customs_duty_idr_db
        form.total_shipment_customs_vat_idr.data=s4s_to_update.total_shipment_customs_vat_idr_db
        form.reimport_hawb_number.data=s4s_to_update.import_hawb_no_db
        form.reimport_date.data=s4s_to_update.reimport_date_db
        form.reimport_consignee.data=s4s_to_update.reimport_consignee_db
        form.country_of_import.data=s4s_to_update.import_country_db
        form.reimport_remarks.data=s4s_to_update.import_remarks_db
        form.new_buy_price.data=s4s_to_update.new_buy_price_db
        form.hs_code.data=s4s_to_update.hs_code_db
        form.duty_rate_on_new_buy.data=s4s_to_update.duty_rate_on_new_buy_db
        form.estimated_duty_charge_on_new_buy.data=s4s_to_update.estimated_duty_charge_on_new_buy_db
        form.estimated_vat_charge_on_new_buy.data=s4s_to_update.estimated_vat_charge_on_new_buy_db
        form.case_status.data=s4s_to_update.case_status_db
        form.cancellation_status.data=s4s_to_update.cancellation_status_db
        
        return render_template("update_one_s4s.html", form=form, s4s_to_update=s4s_to_update, id=id)
   

    if request.method == "POST":
        
        #File operations here
        file1 = request.files['inputFile1'] 
        file2 = request.files['inputFile2']
        file3 = request.files['inputFile3']
        file4 = request.files['inputFile4']
        file5 = request.files['inputFile5']
        file6 = request.files['inputFile6']

        data1 = file1.read()
        data2 = file2.read()
        data3 = file3.read()
        data4 = file4.read()
        data5 = file5.read()
        data6 = file6.read()
        

        potential_list_of_files=[file1.filename, file2.filename, file3.filename, file4.filename, file5.filename, file6.filename]
        list_of_files = []
        for file in potential_list_of_files:
            if file:
                list_of_files.append(file)                                
        print("List of files :", list_of_files)

        potential_list_of_data=[data1, data2, data3, data4, data5, data6]
        list_of_data = []
        for data_file in potential_list_of_data:
            if data_file:
                list_of_data.append(data_file)

        Company_path_on_remote = "/root/s4s_tests/"
        subfolder_name = form.part_serial_number.data

        

        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect("secret", username="root", password="secret")
        
        ftp = ssh.open_sftp()

        for file_name, file_data in zip(list_of_files, list_of_data):                
            if file_data:
                folder_path_and_filename = Company_path_on_remote + subfolder_name + "/" + file_name
                ftp.putfo(BytesIO(file_data), folder_path_and_filename)        
            
        ftp.close()
        ssh.close()
        
        
        #S4S POST Record - 28.03.2022
        s4s_to_update.cm_rma_db = form.cm_rma_number.data,
        s4s_to_update.juniper_part_no_db = form.juniper_part_number.data,
        s4s_to_update.serial_no_db = form.part_serial_number.data,
        s4s_to_update.quantity_db = form.quantity.data,
        s4s_to_update.country_of_origin_db = form.country_of_origin.data,
        s4s_to_update.rma_no = form.rma_number.data,
        s4s_to_update.sto_no_db = form.sto_number.data,
        s4s_to_update.ups_so_db = form.ups_so_number.data,
        s4s_to_update.export_invoice_no_db = form.export_invoice_number.data,
        s4s_to_update.export_price_db = form.export_price.data,
        s4s_to_update.export_hawb_no_db = form.export_hawb_number.data,
        s4s_to_update.export_cob_date_db = form.export_date.data,
        s4s_to_update.repair_cm_consignee_db = form.repair_cm_consignee.data,
        s4s_to_update.export_country_db = form.country_of_export.data,
        s4s_to_update.export_remarks_db = form.export_remarks.data,
        s4s_to_update.cm_reference_db = form.cm_reference_number.data, 
        s4s_to_update.reimport_invoice_no_db = form.reimport_invoice_number.data,
        s4s_to_update.reimport_repair_price_db = form.reimport_repair_price.data, 
        s4s_to_update.total_shipment_value_db = form.total_shipment_value.data,
        s4s_to_update.total_customs_cif_value_usd_db = form.total_customs_cif_value_usd.data,
        s4s_to_update.total_customs_cif_value_idr_db = form.total_customs_cif_value_idr.data,
        s4s_to_update.total_shipment_customs_duty_idr_db = form.total_shipment_customs_duty_idr.data,
        s4s_to_update.total_shipment_customs_vat_idr_db = form.total_shipment_customs_vat_idr.data,
        s4s_to_update.import_hawb_no_db = form.reimport_hawb_number.data,
        s4s_to_update.reimport_date_db = form.reimport_date.data,
        s4s_to_update.reimport_consignee_db = form.reimport_consignee.data,
        s4s_to_update.import_country_db = form.country_of_import.data,
        s4s_to_update.import_remarks_db = form.reimport_remarks.data,
        s4s_to_update.new_buy_price_db = form.new_buy_price.data,
        s4s_to_update.hs_code_db = form.hs_code.data,
        s4s_to_update.duty_rate_on_new_buy_db = form.duty_rate_on_new_buy.data,
        s4s_to_update.estimated_duty_charge_on_new_buy_db = form.estimated_duty_charge_on_new_buy.data,
        s4s_to_update.estimated_vat_charge_on_new_buy_db = form.estimated_vat_charge_on_new_buy.data,
        s4s_to_update.case_status_db = form.case_status.data,
        s4s_to_update.cancellation_status_db = form.cancellation_status.data


        try:
            db.session.commit()
            flash("S4S case has been succesfully updated.", "success")
            
            s4s_to_update = str_s4s_db.query.get_or_404(id)
            if s4s_to_update.export_cob_date_db:
                print("time delta from update function",  s4s_to_update.export_cob_date_db + timedelta(days=(3*365)))
                s4s_to_update.latest_reimport_date_db = s4s_to_update.export_cob_date_db + timedelta(days=(3*365))
                db.session.commit()

            return render_template("update_one_s4s.html", form=form, s4s_to_update=s4s_to_update, id=id)
            
        except:
            db.session.commit()
            flash("There has been a problem during updating process. Please inform your IT Administrator.", "success")
            return render_template("update_one_s4s.html", form=form, s4s_to_update=s4s_to_update, id=id)



@app.route('/new_import_entry', methods=["GET", "POST"])
@login_required
def new_import_entry(): 
        
    form = Str_import_entry()

    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    
    if user_role == "user1":
            
        if request.method == "POST":
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            if form.validate_on_submit():
                print("Case entry work validation step check")
                
                
                file1 = request.files['inputFile1'] 
                file2 = request.files['inputFile2']
                file3 = request.files['inputFile3']
                file4 = request.files['inputFile4']
                file5 = request.files['inputFile5']
                file6 = request.files['inputFile6']
                                               
                data1 = file1.read()
                data2 = file2.read()
                data3 = file3.read()
                data4 = file4.read()
                data5 = file5.read()
                data6 = file6.read()

                
                new_case = str_cases_db(  
                    
                    str_ref_db = form.str_ref.data,
                    tur_ref_db = form.tur_ref.data,
                    date_added_db = dt_string,
                    initial_status_db = "Pending",
                    cancellation_status_db = form.cancellation_status.data,
                    status_db = "Approval Phase",
                    file1_name_db = file1.filename,
                    file1_data_db = None, #file1_data_db = data1,
                    file2_name_db = file2.filename,
                    file2_data_db = None,
                    file3_name_db = file3.filename,
                    file3_data_db = None,
                    file4_name_db = file4.filename,
                    file4_data_db = None,
                    file5_name_db = file5.filename,
                    file5_data_db = None,
                    file6_name_db = file6.filename,
                    file6_data_db = None,
                    
                    
                    notes_db = form.note.data,
                    operation_type_db = "Import to Country",
                    enduser_name_surname_db = form.enduser_name.data,
                    enduser_company_name_db = form.enduser_company.data,
                    enduser_address_db = form.enduser_address.data,
                    enduser_tel_db = form.enduser_telephone.data,
                    enduser_email_db = form.enduser_email.data )
                
                db.session.add(new_case)  
                db.session.commit()

                potential_list_of_files=[file1.filename, file2.filename, file3.filename, file4.filename, file5.filename, file6.filename]
                list_of_files = []
                for file in potential_list_of_files:
                    if file:
                        list_of_files.append(file)                                
                print("List of files :", list_of_files)

                potential_list_of_data=[data1, data2, data3, data4, data5, data6]
                list_of_data = []
                for data_file in potential_list_of_data:
                    if data_file:
                        list_of_data.append(data_file)

                Company_path_on_remote = "/root/Company_tests/"
                subfolder_name = form.str_ref.data

                #Creating a folder/directory on remote server under Company_tests directory - 23.02.2022
                transport = paramiko.Transport(("secret", 22))
                transport.connect(username = "root", password = "secret")
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.chdir(Company_path_on_remote + subfolder_name)  # Test if remote_path exists
                except IOError:
                    sftp.mkdir(Company_path_on_remote + subfolder_name)  # Create remote_path
                    sftp.chdir(Company_path_on_remote + subfolder_name)
                sftp.close()
                transport.close()   
                #Creating a folder/directory on remote server under Company_tests directory - 23.02.2022

                ssh = paramiko.SSHClient()
                ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                ssh.connect("Secret", username="root", password="secret")
                
                ftp = ssh.open_sftp()

                for file_name, file_data in zip(list_of_files, list_of_data):                
                    if file_data:
                        folder_path_and_filename = Company_path_on_remote + subfolder_name + "/" + file_name
                        ftp.putfo(BytesIO(file_data), folder_path_and_filename)
                


                ftp.close()
                ssh.close()

                #FOR E-MAIL SENDING AS A NOTIFICATION  07.03.2022
                EMAIL_ADDRESS = "secret"
                EMAIL_PASSWORD = "secret"
                text="Test subject"

                msg = EmailMessage()
                msg['Subject'] = 'You have a new approval request. Reference is ' + (form.str_ref.data)
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = "secretemail"

                msg.set_content('You have a new approval request. Reference is ' + (form.str_ref.data))

                msg.add_alternative("""\<!DOCTYPE html>
                <html>
                    <body>
                        <h1 style="color:SlateGray;">You have a new approval request</h1>
                        <p style="color:orangered;">Please visit your Company Global online system account. </p>
                    </body>
                </html>
                """, subtype="html")

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                    smtp.send_message(msg)
                #FOR E-MAIL SENDING AS A NOTIFICATION 07.03.2022
                
                #Passing pending records information to index after new case entry
                pending_records_filter = str_cases_db.query.filter(str_cases_db.initial_status_db=="Pending").all()
                number_of_pending_records = len(pending_records_filter)
                last_logout_of_user = current_user.last_logout_db
                conversation_test_filter = conversations_db.query.filter(conversations_db.date_of_sending_db>last_logout_of_user).all()


                flash("New case has been recorded successfully. Thank you!", "success")
                return render_template("index.html", user_name = user_name, user_role = user_role, pending_records_filter=pending_records_filter, number_of_pending_records=number_of_pending_records,  conversation_test_filter=conversation_test_filter)
            else:
                flash("There has been a problem during saving the new case. Please inform your administrator.", 'error')
    else:   
        flash("New case entry screen is only available for authorized staff. Please inform your administrator in case of a mistake.", 'error')
        return render_template("index.html")
    
    return render_template("new_import_entry.html", form=form, user_name = user_name, user_role = user_role)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------for export entry
@app.route('/new_export_entry', methods=["GET", "POST"])
@login_required
def new_export_entry(): #Adding a new work to database by sales team
        
    form = Str_export_entry()

    # active_user_id tespiti ile login olmuş kullanıcıyı buluyoruz. Oradan da e-mailine de ulaşarak kaydı kimin yaptığını otomatik olarak sisteme atıyoruz.
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    
    #print(user_email, user_name, user_role, "Just passed from new_work_entry... beginning")
    
    if user_role == "user1":
            
        if request.method == "POST":
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            if form.validate_on_submit():
                print("Case entry work validation step check")
                
                #file operations here
                file1 = request.files['inputFile1'] #HTML form üzerindeki isim. Oradan gelecek.
                file2 = request.files['inputFile2']
                file3 = request.files['inputFile3']
                file4 = request.files['inputFile4']
                file5 = request.files['inputFile5']
                file6 = request.files['inputFile6']
                                               
                data1 = file1.read()
                data2 = file2.read()
                data3 = file3.read()
                data4 = file4.read()
                data5 = file5.read()
                data6 = file6.read()

                #Sonrasında aynı isimle aramak için database üzerine dosya ismini yazmamız gerekebilir. 23.02.2022
                #Dosyaları ayrı bir yerde tutacak isek database üzerindeki data fieldlere dummy veri kaydetmemiz gerekebilir.
                new_case = str_cases_db(  
                    
                    str_ref_db = form.str_ref.data,
                    tur_ref_db = form.tur_ref.data,
                    date_added_db = dt_string,
                    initial_status_db = "Auto Approved",
                    cancellation_status_db = form.cancellation_status.data,
                    status_db = "Pickup and Customs Clearance",
                    file1_name_db = file1.filename,
                    file1_data_db = None, #file1_data_db = data1,
                    file2_name_db = file2.filename,
                    file2_data_db = None,
                    file3_name_db = file3.filename,
                    file3_data_db = None,
                    file4_name_db = file4.filename,
                    file4_data_db = None,
                    file5_name_db = file5.filename,
                    file5_data_db = None,
                    file6_name_db = file6.filename,
                    file6_data_db = None,
                    
                    notes_db = form.note.data,
                    operation_type_db = "Export from Country",
                    
                    #Export related fields below - Heather fills in
                    export_pickup_ups_or_enduser_db = form.export_pickup_ups_or_enduser.data,
                    export_pickup_username_db = form.enduser_name.data,
                    export_pickup_company_db = form.enduser_company.data,
                    
                    export_pickup_address_db = form.enduser_address.data,
                    export_pickup_telephone_db = form.enduser_telephone.data,
                    export_pickup_email_db = form.enduser_email.data,
                    export_mentor_status_db = "Customs Clearance Continue"
                    
                    
                    )
                
                db.session.add(new_case)  
                db.session.commit()           

                potential_list_of_files=[file1.filename, file2.filename, file3.filename, file4.filename, file5.filename, file6.filename]
                list_of_files = []
                for file in potential_list_of_files:
                    if file:
                        list_of_files.append(file)                                
                print("List of files :", list_of_files)

                potential_list_of_data=[data1, data2, data3, data4, data5, data6]
                list_of_data = []
                for data_file in potential_list_of_data:
                    if data_file:
                        list_of_data.append(data_file)

                Company_path_on_remote = "/root/company_tests/"
                subfolder_name = form.str_ref.data

                #Creating a dolfer/directory on remote server under Company_tests directory - 23.02.2022
                transport = paramiko.Transport(("secret", 22))
                transport.connect(username = "root", password = "secret")
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.chdir(Company_path_on_remote + subfolder_name)  # Test if remote_path exists
                except IOError:
                    sftp.mkdir(Company_path_on_remote + subfolder_name)  # Create remote_path
                    sftp.chdir(Company_path_on_remote + subfolder_name)
                sftp.close()
                transport.close()   
                #Creating a dolfer/directory on remote server under Company_tests directory - 23.02.2022

                ssh = paramiko.SSHClient()
                ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                ssh.connect("secret", username="root", password="secret")
                
                ftp = ssh.open_sftp()

                for file_name, file_data in zip(list_of_files, list_of_data):                
                    if file_data:
                        folder_path_and_filename = Company_path_on_remote + subfolder_name + "/" + file_name
                        ftp.putfo(BytesIO(file_data), folder_path_and_filename)
                
            

                ftp.close()
                ssh.close()

                #FOR E-MAIL SENDING AS A NOTIFICATION  07.03.2022
                EMAIL_ADDRESS = "Secret"
                EMAIL_PASSWORD = "Secret"
                text="Test subject"

                msg = EmailMessage()
                msg['Subject'] = 'You have a new approval request. Reference is ' + (form.str_ref.data)
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = "Secret"

                msg.set_content('You have a new approval request. Reference is ' + (form.str_ref.data))

                msg.add_alternative("""\<!DOCTYPE html>
                <html>
                    <body>
                        <h1 style="color:SlateGray;">You have a new approval request</h1>
                        <p style="color:orangered;">Please visit your Company Global online system account. </p>
                    </body>
                </html>
                """, subtype="html")

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                    smtp.send_message(msg)
           


                #Passing pending records information to index after new case entry
                pending_records_filter = str_cases_db.query.filter(str_cases_db.initial_status_db=="Pending").all()
                number_of_pending_records = len(pending_records_filter)
                last_logout_of_user = current_user.last_logout_db
                conversation_test_filter = conversations_db.query.filter(conversations_db.date_of_sending_db>last_logout_of_user).all()


                flash("New EXPORT case has been recorded successfully. Thank you!", "success")
                return render_template("index.html", user_name = user_name, user_role = user_role, pending_records_filter=pending_records_filter, number_of_pending_records=number_of_pending_records,  conversation_test_filter=conversation_test_filter)
            else:
                flash("There has been a problem during saving the new EXPORT case. Please inform your administrator.", 'error')
    else:   
        flash("New EXPORT case entry screen is only available for authorized staff. Please inform your administrator in case of a mistake.", 'error')
        return render_template("index.html")
    
    return render_template("new_export_entry.html", form=form, user_name = user_name, user_role = user_role)



@app.route('/see_all_records', methods=["GET", "POST"])
@login_required
def see_all_records(): #Adding a new work to database by sales team

    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    #all_cases = str_cases_db.query.order_by(str_cases_db.date_added_db).all()
    if request.method == "GET":
        if (user_role == "user1"):
            all_cases = str_cases_db.query.order_by(str_cases_db.date_added_db.desc()).all()
            return render_template("see_all_cases.html", all_cases=all_cases, user_name = user_name, user_role = user_role)
        
        elif user_role == "user3":
            all_cases = str_cases_db.query.filter(str_cases_db.operation_type_db=="Import to Country").order_by(str_cases_db.id.desc()).all()
            return render_template("see_all_cases.html", all_cases=all_cases, user_name = user_name, user_role = user_role)
        
        elif user_role == "user4":
            all_cases = str_cases_db.query.filter(str_cases_db.operation_type_db=="Export from Country").order_by(str_cases_db.id.desc()).all()
            print("Printing from Agent's account... exports")
            return render_template("see_all_cases.html", all_cases=all_cases, user_name = user_name, user_role = user_role)

        else:
            flash("This screen is only available for authorized staff. Please inform your administrator in case of a mistake.", 'error')
            return render_template("index.html")


@app.route('/update_one_case/<int:id>', methods=["GET", "POST"])
@login_required
def update_one_case(id):

    form = Str_case_update()
    case_to_update = str_cases_db.query.get_or_404(id)

    
    if request.method == "GET":

        if case_to_update.operation_type_db=="Import to Country":
            form = Str_case_update()
            form.str_ref.data = case_to_update.str_ref_db
            form.tur_ref.data = case_to_update.tur_ref_db
            form.note.data = case_to_update.notes_db
            form.enduser_name.data = case_to_update.enduser_name_surname_db
            form.enduser_company.data = case_to_update.enduser_company_name_db
            form.enduser_address.data = case_to_update.enduser_address_db
            form.enduser_telephone.data = case_to_update.enduser_tel_db
            form.enduser_email.data = case_to_update.enduser_email_db
            form.cancellation_status.data = case_to_update.cancellation_status_db
            return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)
   
        if case_to_update.operation_type_db=="Export from Country":
            form = Str_case_update_export()
            form.str_ref.data = case_to_update.str_ref_db
            form.tur_ref.data = case_to_update.tur_ref_db
            form.note.data = case_to_update.notes_db
            form.export_pickup_ups_or_enduser.data = case_to_update.export_pickup_ups_or_enduser_db
            
            form.enduser_name.data = case_to_update.export_pickup_username_db
            form.enduser_company.data = case_to_update.export_pickup_company_db
            form.enduser_address.data = case_to_update.export_pickup_address_db
            form.enduser_telephone.data = case_to_update.export_pickup_telephone_db
            form.enduser_email.data = case_to_update.export_pickup_email_db
            form.cancellation_status.data = case_to_update.cancellation_status_db
            
            return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)
    
    
    #HERE WE WILL ADD IMPORT OR EXPORT IF -TO BE ABLE TO FORWARD RELEVANT INFORMATION TO IMPORT/EXPORT  // RECORDING IS REMAINING 18.03.2022
    #ALSO DISABLE OTHER USERS FROM REACHING TO THIS END POINT!!! 18.03.2022
    
    if request.method == "POST":
        if case_to_update.operation_type_db=="Import to Country":
            #File operations here
            file1 = request.files['inputFile1'] #HTML form üzerindeki isim. Oradan gelecek.
            file2 = request.files['inputFile2']
            file3 = request.files['inputFile3']
            file4 = request.files['inputFile4']

            data1 = file1.read()
            data2 = file2.read()
            data3 = file3.read()
            data4 = file4.read()
            

            potential_list_of_files=[file1.filename, file2.filename, file3.filename, file4.filename]
            list_of_files = []
            for file in potential_list_of_files:
                if file:
                    list_of_files.append(file)                                
            print("List of files :", list_of_files)

            potential_list_of_data=[data1, data2, data3, data4]
            list_of_data = []
            for data_file in potential_list_of_data:
                if data_file:
                    list_of_data.append(data_file)

            Company_path_on_remote = "/root/company_tests/"
            subfolder_name = form.str_ref.data

            

            ssh = paramiko.SSHClient()
            ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect("Secret", username="root", password="Secret")
            
            ftp = ssh.open_sftp()

            for file_name, file_data in zip(list_of_files, list_of_data):                
                if file_data:
                    folder_path_and_filename = Company_path_on_remote + subfolder_name + "/" + file_name
                    ftp.putfo(BytesIO(file_data), folder_path_and_filename)        
                
            ftp.close()
            ssh.close()
            
            
            case_to_update.str_ref_db = form.str_ref.data
            case_to_update.tur_ref_db = form.tur_ref.data
            case_to_update.notes_db = form.note.data
            case_to_update.enduser_name_surname_db = form.enduser_name.data
            case_to_update.enduser_company_name_db = form.enduser_company.data
            case_to_update.enduser_address_db = form.enduser_address.data
            case_to_update.enduser_tel_db = form.enduser_telephone.data
            case_to_update.enduser_email_db = form.enduser_email.data
            case_to_update.cancellation_status_db = form.cancellation_status.data

            try:
                db.session.commit()
                flash("Case has been succesfully updated.", "success")
                return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)
                
            except:
                db.session.commit()
                flash("There has been a problem during updating process. Please inform your IT Administrator.", "success")
                return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)

        if case_to_update.operation_type_db=="Export from Country":
            form = Str_case_update_export()
            case_to_update.str_ref_db = form.str_ref.data
            case_to_update.tur_ref_db = form.tur_ref.data 
            case_to_update.notes_db = form.note.data 
            case_to_update.export_pickup_ups_or_enduser_db = form.export_pickup_ups_or_enduser.data 
            
            case_to_update.export_pickup_username_db = form.enduser_name.data 
            case_to_update.export_pickup_company_db = form.enduser_company.data 
            case_to_update.export_pickup_address_db = form.enduser_address.data 
            case_to_update.export_pickup_telephone_db = form.enduser_telephone.data
            case_to_update.export_pickup_email_db = form.enduser_email.data
            case_to_update.cancellation_status_db = form.cancellation_status.data
            try:
                db.session.commit()
                flash("Case has been succesfully updated.", "success")
                return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)
                
            except:
                db.session.commit()
                flash("There has been a problem during updating process. Please inform your IT Administrator.", "success")
                return render_template("update_one_case.html", form=form, case_to_update=case_to_update, id=id)

@app.route('/see_one_case/<int:id>', methods=["GET", "POST"])
@login_required
def see_one_case(id):
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    case_to_show = str_cases_db.query.get_or_404(id)
    
    form = Str_conversations()
    form2 = Str_case_update_mentor_hawb()
    
    conversations_to_display = conversations_db.query.filter_by(case_id_db=case_to_show.id).order_by(conversations_db.id.desc()).all()
    

    #DOSYA İSİMLERİNİ  DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    list_of_file_names = []
    
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("Secret", username="root", password="Secret")
    ftp = ssh.open_sftp()
    for i in ftp.listdir("/root/company_tests/" + case_to_show.str_ref_db):
        print("This is a file in this directory : ", i)
        list_of_file_names.append(i)
        #lstatout=str(ftp.lstat(i)).split()[0]
            
    ftp.close()
    ssh.close()


    #DOSYALARI İSİMLERİNİ DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    list_of_file_names.reverse()
    len_of_files_list = len(list_of_file_names)
    
    list_of_file_name_numbers = [] #23.03.2022 -start
    for file_number in range(len_of_files_list):
        list_of_file_name_numbers.append(file_number)
    print("List of file name numbers : ", list_of_file_name_numbers) #23.03.2022 -end
    
    print("Len of files list", len_of_files_list)
    print("List of file names : ", list_of_file_names)
    


    download_text="download_attachment"
    list_of_links = []
    for num_of_file in range(len_of_files_list):
        list_of_links.append(download_text + str(num_of_file+1))

    #IMPORTANT - FOR ZIPPING TWO LISTS IN JINJA2 - IN THIS CASE FOR ZIPPING 
    app.jinja_env.filters['zip'] = zip
    
    sender_to_be_recorded = current_user.name_db
    case_id_to_be_recorded = case_to_show.id
    if request.method == "POST":
        if form.validate_on_submit(): # Recording Conversations
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            print("Case NOTE/Conversation entry validation step check")
            conversation_to_be_recorded = conversations_db(

                sender_db = sender_to_be_recorded,
                text_db = form.text.data,
                case_id_db = case_id_to_be_recorded,
                date_of_sending_db = dt_string,
                str_ref_db = case_to_show.str_ref_db
            )
            if form.text.data:
                db.session.add(conversation_to_be_recorded)
                db.session.commit()
            
            conversations_to_display = conversations_db.query.filter_by(case_id_db=case_to_show.id).order_by(conversations_db.id.desc()).all()
            
            if current_user.role_db=="user4": 
                
                if (form2.mentor_ref.data) or (form2.hawb_number.data):
                    case_to_show.export_mentor_reference_db = form2.mentor_ref.data
                    case_to_show.export_waybill_no_db = form2.hawb_number.data
                    case_to_show.export_mentor_status_db = form2.export_mentor_status.data          
                    try:
                        db.session.commit()
                        flash("Import additional information has been succesfully updated.", "success")
                        return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, form2=form2)
                    except:
                        db.session.commit()
                        flash("There has been a problem during updating process. Please inform your IT Administrator.", "success")
                        return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, form2=form2)
        
                            
        return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, form2=form2, list_of_file_name_numbers=list_of_file_name_numbers)


    if request.method == "GET":
        form2 = Str_case_update_mentor_hawb()
        form2.mentor_ref.data = case_to_show.export_mentor_reference_db
        form2.hawb_number.data = case_to_show.export_waybill_no_db
        form2.export_mentor_status.data = case_to_show.export_mentor_status_db
        

        print(case_to_show)
        print("Conversations : ", conversations_to_display)


        return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, form2=form2, list_of_file_name_numbers=list_of_file_name_numbers)
    #else:
    return render_template("see_one_case.html", user_name = user_name, user_role = user_role, case_to_show=case_to_show, list_of_file_names=list_of_file_names, len_of_files_list=len_of_files_list, list_of_links=list_of_links, form=form, conversations_to_display=conversations_to_display, id=id, form2=form2, list_of_file_name_numbers=list_of_file_name_numbers)
    

#DELETING AN S4S ENTRY WITH ITS FILES ON FILE SYSTEM VIA SSH - 29.03.2022
@app.route('/delete_one_s4s/<int:id>', methods=["GET", "POST"])
@login_required
def delete_one_s4s(id):

    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    
    s4s_to_delete = str_s4s_db.query.get_or_404(id)
    s4s_conv_to_delete = s4s_conversations_db.query.filter_by(s4s_id_db=s4s_to_delete.id).all()

    #Deleting the directory on file system
    #---------------------------------------------------------------------------
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect("Secret",username="root",password="Secret")

    Company_folder_to_be_removed = s4s_to_delete.serial_no_db
    filepath="/root/s4s_tests/" + Company_folder_to_be_removed
    cmd = "rm -rf "  + filepath

    stdin, stdout, stderr = ssh.exec_command(cmd)
    while not stdout.channel.exit_status_ready():
        time.sleep(5)

    #---------------------------------------------------------------------------
    #Deleting the directory on file system
    
    try:
        #db.session.delete(s4s_conv_to_delete)
        db.session.delete(s4s_to_delete)
        db.session.commit()
        flash("Record deleted, thank you.", "success")
        print("Entry deleted.. now should be re-routing to form2??")
        all_s4s = str_s4s_db.query.order_by(str_s4s_db.id)
        return redirect(url_for("view_s4s_entries")) #Orjinal codemy videsounda bu satır yok. 
        # Bunun yerine aşağıdaki satır yazılmış ama delete/n urlinde kalıyordu. 
        # Dolayısı ile sildikten sonra yeni giriş hata veriyordu.
        #return  render_template("form2.html", form=form, name=name, our_users=our_users)
    except:
        all_s4s = str_s4s_db.query.order_by(str_s4s_db.id)
        flash("There is a problem in deletion of the record. Please inform your administrator.", 'error')
        return  render_template("view_s4s_entries.html", all_s4s=all_s4s)


#DELETING AN S4S ENTRY WITH ITS FILES ON FILE SYSTEM VIA SSH - 29.03.2022


@app.route('/delete_one_case/<int:id>', methods=["GET", "POST"])
@login_required
def delete_one_case(id):

    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    case_to_delete = str_cases_db.query.get_or_404(id)

    #Deleting the directory on file system
    #---------------------------------------------------------------------------
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect("Secret",username="root",password="Secret")

    Company_folder_to_be_removed = case_to_delete.str_ref_db
    filepath="/root/company_tests/" + Company_folder_to_be_removed
    cmd = "rm -rf "  + filepath

    stdin, stdout, stderr = ssh.exec_command(cmd)
    while not stdout.channel.exit_status_ready():
        time.sleep(5)

    #---------------------------------------------------------------------------
    #Deleting the directory on file system
    
    try:
        db.session.delete(case_to_delete)
        db.session.commit()
        flash("Record deleted, thank you.", "success")
        print("Entry deleted.. now should be re-routing to form2??")
        all_cases = str_cases_db.query.order_by(str_cases_db.date_added_db)
        return redirect(url_for("see_all_records")) #Orjinal codemy videsounda bu satır yok. 
        # Bunun yerine aşağıdaki satır yazılmış ama delete/n urlinde kalıyordu. 
        # Dolayısı ile sildikten sonra yeni giriş hata veriyordu.
        #return  render_template("form2.html", form=form, name=name, our_users=our_users)
    except:
        flash("There is a problem in deletion of the record. Please inform your administrator.", 'error')
        return  render_template("see_all_cases.html", all_cases=all_cases)
    



@app.route('/download_attachments/<int:id>', methods=["GET", "POST"])
@login_required
def download_attachments(id): #Adding a new work to database by sales team
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    case_to_show = str_cases_db.query.get_or_404(id)

     
    list_of_files=[case_to_show.file1_name_db, case_to_show.file2_name_db,case_to_show.file3_name_db, case_to_show.file4_name_db, case_to_show.file5_name_db, case_to_show.file6_name_db, ]
    list_of_file_datas=[case_to_show.file1_data_db, case_to_show.file2_data_db,case_to_show.file3_data_db, case_to_show.file4_data_db, case_to_show.file5_data_db, case_to_show.file6_data_db, ]
    
    if request.method == "GET":
        print("Case to show : ", case_to_show)
        
        for file_name, file_data in zip(list_of_files, list_of_file_datas):
            counter = 0
            print("counter : ", (counter+1),"file_name : ", file_name)
        
            return send_file(BytesIO(file_data), download_name=file_name, as_attachment=True)
      
        
    return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role, list_of_files=list_of_files)
    

#FILE DOWNLOAD NEW - VIA SSH FROM REMOTE SERVER
#id case numarasına, file_no o case içindeki dosyanın sıra numarasına işaret ediyor. Daha önceki çözümde her dosya sıra numarası için ayrı bir fonksiyon yazmıştık. Şimdi tek bir fonksiyon ile çok dosya indirebiliyoruz. 
# Test edilecek.23.03.2022

@app.route('/download_attachment/<int:id>/<int:file_no>', methods=["GET", "POST"])
@login_required
def download_attachment(id, file_no):
    
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_name = active_user.name_db
    user_role = active_user.role_db
    case_to_show = str_cases_db.query.get_or_404(id)
    
    #DOSYA İSİMLERİNİ  DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    list_of_file_names = []
    
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("Secret", username="root", password="Secret")
    ftp = ssh.open_sftp()
    for i in ftp.listdir("/root/Company_tests/" + case_to_show.str_ref_db):
        print("This is afile in this directory : ", i)
        list_of_file_names.append(i)
        #lstatout=str(ftp.lstat(i)).split()[0]
            
    ftp.close()
    ssh.close()

    list_of_file_names.reverse()


    #DOSYALARI İSİMLERİNİ DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    
    file_name_to_download = list_of_file_names[file_no]
    
    Company_directory_to_download = case_to_show.str_ref_db
    file_path_to_download_on_remote = "/root/Company_tests/" + Company_directory_to_download + "/" + file_name_to_download
    
    
    if request.method == "GET":

        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect("Secret", username="root", password="Secret")        
        ftp = ssh.open_sftp()
        
        download_file = ftp.open(file_path_to_download_on_remote, mode='r', bufsize=-1)
        
        return send_file(download_file, download_name=file_name_to_download, as_attachment=True) #May we need this approach if number of files in the file system will not be displayed on HTML?

    return render_template("see_one_case.html", case_to_show=case_to_show, user_name = user_name, user_role = user_role)

#------------download s4s attachment
@app.route('/download_attachment_s4s/<int:id>/<int:file_no>', methods=["GET", "POST"])
@login_required
def download_attachment_s4s(id, file_no): #For importing attachments of s4s cases only.
    
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_name = active_user.name_db
    user_role = active_user.role_db
    s4s_to_show = str_s4s_db.query.get_or_404(id)
    
    #DOSYA İSİMLERİNİ  DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    list_of_file_names = []
    
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("Secret", username="root", password="Secret")
    ftp = ssh.open_sftp()
    for i in ftp.listdir("/root/s4s_tests/" + s4s_to_show.serial_no_db):
        print("This is afile in this directory : ", i)
        list_of_file_names.append(i)
            
    ftp.close()
    ssh.close()

    list_of_file_names.reverse()


    #DOSYALARI İSİMLERİNİ DOĞRUDAN REMOTE SERVER ÜZERİNDEKİ DIRECTORY ÜZERİNDEN ALMAK.
    
    file_name_to_download = list_of_file_names[file_no]
    #file_name_to_download = list_of_file_names[1]
    
    Company_directory_to_download = s4s_to_show.serial_no_db
    file_path_to_download_on_remote = "/root/s4s_tests/" + Company_directory_to_download + "/" + file_name_to_download
    
    
    if request.method == "GET":

        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect("Secret", username="root", password="Secret")        
        ftp = ssh.open_sftp()
        
        download_file = ftp.open(file_path_to_download_on_remote, mode='r', bufsize=-1)
        #file_to_download =   case_to_show.file2_name_db
        return send_file(download_file, download_name=file_name_to_download, as_attachment=True) #May we need this approach if number of files in the file system will not be displayed on HTML?

    return render_template("see_one_case.html", s4s_to_show=s4s_to_show, user_name = user_name, user_role = user_role)


#------------download s4s attachment

#Agency Approval Part below


@app.route('/import_approval_step/<int:id>', methods=["GET", "POST"])
@login_required
def import_approval_step(id): #Approving a new import request or not (mainly by Agency staff or automatic)
    
    form = Str_case_approval()

    test_for_current_user = current_user.name_db
    print("Test for current user : ", test_for_current_user)
    
    active_user = str_staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    case_to_approve = str_cases_db.query.get_or_404(id)

    if request.method== "POST":
        
        print("check point for POST")
        if user_role=="user3":
            print("check point for user3 POST")
            if form.validate_on_submit():
                
                print("check point for user3 POST and validate")
                
                case_to_approve.initial_status_db = form.reply_result.data

                                             
                db.session.commit() #Unutma
                                                               
                user_name = active_user.name_db
                user_role = active_user.role_db                   
                flash("Your reply is recorded successfully.", 'error')
                return render_template("approval_entry.html", form=form, case_to_approve=case_to_approve, user_name = user_name, user_role = user_role)
                
            else:
                flash("There was an error during recording your reply. Please inform your administrator.", 'error')
                return render_template("index.html", form=form, case_to_approve=case_to_approve, user_name = user_name, user_role = user_role)
        else:
            flash("This screen is only available for staff authorized to approve import requests. Please inform your administrator if you think there is a mistake.", 'error')
            return render_template("index.html", user_name = user_name, user_role = user_role)

    if request.method == "GET":
        work_to_show = str_cases_db.query.get_or_404(id)
        
        if user_role=="user3":
            print("check point GET user3")
            form = Str_case_approval()
            return render_template("approval_entry.html", form=form, case_to_approve=case_to_approve, active_user=active_user, user_role = user_role, user_name = user_name)
        else:
            flash("This screen is only available for staff authorized to approve import requests. Please inform your administrator if you think there is a mistake.", 'error')
            return render_template("index.html", form=form,  active_user=active_user, user_role = user_role, user_name = user_name)

    return render_template("index.html", form=form, case_to_approve=case_to_approve, user_name = user_name, user_role = user_role)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------Agency Approval Part above


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    name=None
    
    global active_user_id
    active_user_id = None

    if current_user.is_authenticated:
        print("User is ALREADY LOGGED IN")
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        
        print("Form validated")
        user = str_staff_db.query.filter_by(email_db=form.name.data).first()
        
        if user:
            password = user.password_db
            print("passcheck hashed", password)
            
            password_check = bcrypt.check_password_hash(password, form.password.data)
            print(password_check)
        
        if user and password_check:
            print("///Found this user and his password is correct!!!/// hashing technique is used..")
            login_user(user)
            
            #For recording last login time
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            user.last_login_db = dt_string
            db.session.commit()
            
            
            flash('You have successfully logged in. Have a nice day.', 'success')
            active_user_id = int(user.id)
            print("////////////",active_user_id, type(active_user_id))
            print(current_user, "Current user name : ", current_user.name_db, "Current user role : ", current_user.role_db )
            
            return redirect(url_for('index'))
            
        else:
            flash('There has been a problem during logging in. Please check your username and password', 'error')
    return render_template('login.html', title='Login', form=form, name=name)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        
        user_to_be_updated = str_staff_db.query.filter_by(id=current_user.id).first()
    
        #For recording last logout time
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        user_to_be_updated.last_logout_db = dt_string
        db.session.commit()
        

    logout_user()
    print("The user should have been LOGGED OUT NOW!!!")
    flash('You have successfully logged out. Have a nice day.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False)
