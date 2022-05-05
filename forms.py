from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, ValidationError, PasswordField, FileField, FloatField
from wtforms.validators import DataRequired, Email, InputRequired, Optional
from wtforms.fields.core import DateField, RadioField

class Login(FlaskForm):
    name = StringField("Please enter your username", validators=[DataRequired()])
    password = PasswordField("Please enter your password", validators=[DataRequired()])
    submit = SubmitField("Enter System")

class Str_import_entry(FlaskForm): #For imports
    
    str_ref = StringField("Main Ref. Number", validators=[DataRequired()])
    tur_ref = StringField("Country Ref. Number", validators=[DataRequired()])
    note = TextAreaField("Notes or explanations about the case")
    enduser_name = StringField("End User Contact Name-Surname ")
    enduser_company = StringField("End User Company")
    enduser_address = StringField("End User Address")
    enduser_telephone = StringField("End User Telephone")
    enduser_email = StringField("End User Email")
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    file1_field = FileField()
    file2_field = FileField()
    file3_field = FileField()
    file4_field = FileField()
    file5_field = FileField()
    file6_field = FileField()

    submit = SubmitField("Save case details and send")

class Str_export_entry(FlaskForm): 
    
    str_ref = StringField("Main Ref. Number", validators=[DataRequired()])
    tur_ref = StringField("Country Ref. Number", validators=[DataRequired()])
    note = TextAreaField("Notes or explanations about the case")
    export_pickup_ups_or_enduser = SelectField(label='Where to pick up the goods', choices=[("UPS", "UPS"), ("From End User", "From End User")])
    enduser_name = StringField("End User Contact Name-Surname")
    enduser_company = StringField("End User Company")
    enduser_address = StringField("End User Address")
    enduser_telephone = StringField("End User Telephone")
    enduser_email = StringField("End User Email")
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    file1_field = FileField()
    file2_field = FileField()
    file3_field = FileField()
    file4_field = FileField()
    file5_field = FileField()
    file6_field = FileField()

    submit = SubmitField("Save case details and send")


class Str_case_update(FlaskForm):
    
    str_ref = StringField("Main Ref. Number", validators=[DataRequired()])
    tur_ref = StringField("Country Ref. Number", validators=[DataRequired()])
    note = TextAreaField("Notes or explanations about the case")
    type_of_operation = SelectField(label='Import or Export', choices=[("Import to Country", "Import to Country"), ("Export from Country", "Export from Country")])
    enduser_name = StringField("End User Contact Name-Surname ")
    enduser_company = StringField("End User Company")
    enduser_address = StringField("End User Address")
    enduser_telephone = StringField("End User Telephone")
    enduser_email = StringField("End User Email")
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    new_file1_field = FileField()
    new_file2_field = FileField()
    new_file3_field = FileField()
    new_file4_field = FileField()

    submit = SubmitField("Save case details and send")

class Str_case_update_export(FlaskForm):
    
    str_ref = StringField("Main Ref. Number", validators=[DataRequired()])
    tur_ref = StringField("Country Ref. Number", validators=[DataRequired()])
    note = TextAreaField("Notes or explanations about the case")
    export_pickup_ups_or_enduser = SelectField(label='Where to pick up the goods', choices=[("UPS", "UPS"), ("From End User", "From End User")])
    enduser_name = StringField("End User Contact Name-Surname ")
    enduser_company = StringField("End User Company")
    enduser_address = StringField("End User Address")
    enduser_telephone = StringField("End User Telephone")
    enduser_email = StringField("End User Email")
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    
    submit = SubmitField("Save case details and send")

class Str_case_update_mentor_hawb(FlaskForm):
    
    mentor_ref = StringField("Agency Ref. Number")
    hawb_number = StringField("HAWB Number (konşimento no)")
    export_mentor_status = SelectField(label='Export Agency Status', choices=[("Customs Clearance Continue", "Customs Clearance Continue"), ("Customs Clearance Completed", "Customs Clearance Completed")])

    submit = SubmitField("Save import information")

class Str_case_approval(FlaskForm):
    reply_note = TextAreaField("Notes or explanations about the case")
    reply_result = SelectField(label='Decision of Approval or Disapproval about this case/file', choices=[("Approve", "Approve"), ("Disapprove", "Disapprove"), ("Conditional Approve", "Conditional Approve")])
    submit = SubmitField("Save reply and send")

class Str_conversations(FlaskForm):
            
    text = TextAreaField("Notes to be added to conversation - questions or answers")
    submit = SubmitField("Send message to this case...")


class Str_s4s_entry(FlaskForm):


    cm_rma_number = StringField("CM RMA number", validators=[DataRequired()]) #main group number per s4s shipment
    juniper_part_number = StringField("Customer part number", validators=[DataRequired()]) #part number of the unit to be sent under s4s
    part_serial_number = StringField("Part serial number", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    country_of_origin = StringField("Country of Origin")
    rma_number = StringField("RMA number starting with R")
    sto_number = StringField("STO number")
    ups_so_number = StringField("UPS SO number")
    export_invoice_number = StringField("Export invoice number")
    export_price = FloatField("Export price", validators=[Optional()])
    export_hawb_number = StringField("Export HAWB number")
    export_date = DateField('Export date', format='%Y-%m-%d', validators=[Optional()])
    repair_cm_consignee = StringField("Repair CM consignee")
    country_of_export = StringField("Country of export")
    export_remarks = TextAreaField("Export remarks")
    cm_reference_number = StringField("CM reference number")
    reimport_invoice_number = StringField("Import invoice number")
    reimport_repair_price = FloatField("Reimport repair price", validators=[Optional()])
    total_shipment_value = FloatField("Total shipment value", validators=[Optional()])
    total_customs_cif_value_usd = FloatField("Total customs CIF value (USD)", validators=[Optional()])
    total_customs_cif_value_idr = FloatField("Total customs CIF value (IDR)", validators=[Optional()])
    
    total_shipment_customs_duty_idr = FloatField("Total shipment customs duty (IDR)", validators=[Optional()])
    total_shipment_customs_vat_idr = FloatField("Total shipment customs VAT (IDR)", validators=[Optional()])
    
    reimport_hawb_number = StringField("Import HAWB number")
    reimport_date = DateField('Import date', format='%Y-%m-%d', validators=[Optional()])
    reimport_consignee = StringField("Reimport consignee")
    country_of_import = StringField("Country of import")
    
    reimport_remarks = TextAreaField("Reimport remarks")
    new_buy_price = FloatField("New buy price", validators=[Optional()])
    hs_code = IntegerField("HS Code", validators=[Optional()])
    duty_rate_on_new_buy = FloatField("Duty rate on new buy", validators=[Optional()])
    
    estimated_duty_charge_on_new_buy = FloatField("Estimated duty charge on new buy", validators=[Optional()])
    estimated_vat_charge_on_new_buy = FloatField("Estimated VAT charge on new buy", validators=[Optional()])
    case_status = SelectField(label='S4S Status', choices=[("Exported", "Exported"), ("Imported and Closed", "Imported and Closed")])
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    

    file1_field = FileField()
    file2_field = FileField()
    file3_field = FileField()
    file4_field = FileField()
    file5_field = FileField()
    file6_field = FileField()

    submit = SubmitField("Save S4S case details and send")

class Str_s4s_conversations(FlaskForm):
            
    text = TextAreaField("Notes to be added to S4S conversation - questions or answers")
    submit = SubmitField("Send message to this S4S case...")


class Str_s4s_update(FlaskForm):

    cm_rma_number = StringField("CM RMA number") #main group number per s4s shipment
    juniper_part_number = StringField("Customer part number") #part number of the unit to be sent under s4s
    part_serial_number = StringField("Part serial number")
    quantity = IntegerField("Quantity", validators=[Optional()])
    country_of_origin = StringField("Country of Origin")
    rma_number = StringField("RMA number starting with R")
    sto_number = StringField("STO number")
    ups_so_number = StringField("UPS SO number")
    export_invoice_number = StringField("Export invoice number")
    export_price = FloatField("Export price", validators=[Optional()])
    export_hawb_number = StringField("Export HAWB number")
    export_date = DateField('Export date', format='%Y-%m-%d', validators=[Optional()])
    repair_cm_consignee = StringField("Repair CM consignee")
    country_of_export = StringField("Country of export")
    export_remarks = TextAreaField("Export remarks")
    cm_reference_number = StringField("CM reference number")
    reimport_invoice_number = StringField("Import invoice number")
    reimport_repair_price = FloatField("Reimport repair price", validators=[Optional()])
    total_shipment_value = FloatField("Total shipment value", validators=[Optional()])
    total_customs_cif_value_usd = FloatField("Total customs CIF value (USD)", validators=[Optional()])
    total_customs_cif_value_idr = FloatField("Total customs CIF value (IDR)", validators=[Optional()])
    
    total_shipment_customs_duty_idr = FloatField("Total shipment customs duty (IDR)", validators=[Optional()])
    total_shipment_customs_vat_idr = FloatField("Total shipment customs VAT (IDR)", validators=[Optional()])
    
    reimport_hawb_number = StringField("Import HAWB number")
    reimport_date = DateField('Import date', format='%Y-%m-%d', validators=[Optional()])
    reimport_consignee = StringField("Reimport consignee")
    country_of_import = StringField("Country of import")
    
    reimport_remarks = TextAreaField("Reimport remarks")
    new_buy_price = FloatField("New buy price", validators=[Optional()])
    hs_code = IntegerField("HS Code", validators=[Optional()])
    duty_rate_on_new_buy = FloatField("Duty rate on new buy", validators=[Optional()])
    
    estimated_duty_charge_on_new_buy = FloatField("Estimated duty charge on new buy", validators=[Optional()])
    estimated_vat_charge_on_new_buy = FloatField("Estimated VAT charge on new buy", validators=[Optional()])
    case_status = SelectField(label='S4S Status', choices=[("Exported", "Exported"), ("Imported and Closed", "Imported and Closed")])
    cancellation_status = SelectField(label='Cancelled or Active', choices=[("Active", "Active"), ("Cancelled", "Cancelled")])
    

    file1_field = FileField()
    file2_field = FileField()
    file3_field = FileField()
    file4_field = FileField()

    submit = SubmitField("Save S4S case details and send")
