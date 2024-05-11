from django import forms
from django.forms import widgets
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import uuid
from django_ckeditor_5.fields import CKEditor5Field


from phonenumber_field.formfields import PhoneNumberField

class RICForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    ROLE = (
        ('Student', 'Student'),
        ('Academician', 'Academician'),
        ('Industrial Expert', 'Industrial Expert/Scientist/Project Staffs/Research Associates/Post Doctorates'),
        ('Other', 'Other')
    )
    event = forms.ModelChoiceField(
        queryset=Event1.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Events You Want to Participate"
    )
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Theme"
        )
    iitg_student = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Are you IIT Guwahati Student", initial='', required=True)
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    role = forms.ChoiceField(choices=ROLE, label="Mention your Role")

    default_abstract = '''<div>
                        <div style="clear:both;">
                            <p class="NoSpacing" style="line-height:normal;margin-bottom:0pt;">
                                <img src="data:image/png;base64,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" alt="" width="734" height="97">
                            </p>
                        </div>
                        <p style="font-size:14pt;line-height:normal;margin:0.55pt 120.4pt 0.55pt 96.4pt;orphans:0;text-align:center;widows:0;">
                            <a id="_Hlk133139167"><span style="font-family:'Times New Roman';"><strong>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit</strong></span></a>
                        </p>
                        <p style="font-size:10pt;line-height:normal;margin-bottom:0.35pt;margin-left:179.85pt;margin-right:204.35pt;orphans:0;text-align:center;widows:0;">
                            <span style="font-family:'Times New Roman';">Lorem Ipsum</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">1</span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:-0.6pt;">&nbsp;</span><span style="font-family:'Times New Roman';letter-spacing:-0.7pt;">Doerm</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">2</span><span style="font-family:'Times New Roman';letter-spacing:-0.3pt;">, Sitssn</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">3</span><span style="font-family:'Times New Roman';letter-spacing:-0.3pt;">&nbsp;and Muhttgbd</span><span style="font-family:'Times New Roman';font-size:7pt;vertical-align:3.5pt;">4</span>
                        </p>
                        <p style="font-size:10pt;line-height:normal;margin-bottom:0pt;margin-left:88.45pt;margin-right:112.45pt;orphans:0;text-align:center;widows:0;">
                            <span style="font-family:'Times New Roman';">Department of</span><span style="font-family:'Times New Roman';letter-spacing:-0.4pt;">&nbsp;</span><span style="font-family:'Times New Roman';">XYZ</span><span style="font-family:'Times New Roman';letter-spacing:-0.05pt;">&nbsp;</span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:-0.65pt;">&nbsp;Institute of ABC </span><span style="font-family:'Times New Roman';">,</span><span style="font-family:'Times New Roman';letter-spacing:0.05pt;">&nbsp;</span><span style="font-family:'Times New Roman';">India (Country)</span>
                        </p>
                        <p style="font-size:10pt;line-height:115%;margin-bottom:10.45pt;text-align:center;">
                            <span style="font-family:'Times New Roman';" >E-mail:&nbsp;</span><i><span style="font-family:'Times New Roman';">loremipum@abc.de.fg, loremipum@abc.de.fg,</span></i>
                        </p>
                        <p style="line-height:11.8pt;margin-bottom:0pt;margin-left:7.1pt;margin-right:29.6pt;orphans:0;text-align:center;text-indent:28.9pt;widows:0;">
                            <span style="font-family:'Times New Roman';font-size:12pt;vertical-align:2pt;"><strong>Abstract</strong></span>
                        </p>
                        <p style="font-size:10pt;line-height:104%;margin-bottom:0pt;margin-left:5.5pt;margin-right:27.8pt;orphans:0;text-align:justify;text-indent:30.5pt;widows:0;">
                            <span style="font-family:'Times New Roman';">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</span><br>
                            <span style="font-family:'Times New Roman';">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</span>
                        </p>
                        <p style="font-size:10pt;line-height:104%;margin-bottom:0pt;margin-left:5.5pt;margin-right:27.8pt;orphans:0;text-align:justify;text-indent:30.5pt;widows:0;">
                            <span style="font-family:'Times New Roman';"><strong>Keywords:&nbsp;</strong>Neque porro, quisquam est, qui dolorem ipsum, quia dolor sit amet, consectetur, adipisci velit</span>
                        </p>
                    </div>'''

    abstract = CKEditor5Field(default=default_abstract, config_name='extends')

    class Meta:
        model = RICEvent
        fields = ("institute", "dept","title", "iitg_student", "theme", "role", "abstract", "event", "number")
        labels = {
            "institute": "Please Enter your institute (Note: Please Enter Your institute name in Block Letters) *",
            "dept": "Please Select your related Department *",
            "abstract": "Please submit your Abstract file in following format (sample abstract is given below) *",
        }



class ICForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
    )
    ROLE = (
        ('Student','Student'),
        ('Academician','Academician'),
        ('Industrial Expert','Industrial Expert'),
        ('Other','Other')
    )

    event = forms.ModelChoiceField(
            queryset=ICEvent.objects.all(),
            widget=forms.RadioSelect,
            required=True,
            label="Events You Want to Participate"
            )
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Theme"
        )
    iitg_student = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Are you IIT Guwahati Student", initial='', widget=forms.Select(), required=True)
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    role = forms.ChoiceField(choices=ROLE,label="Mention your Role")
    class Meta:
        model = IC
        fields = ("institute","theme","title","iitg_student","role","event","number","remarks")
        labels = {
            "institute": "Please Enter your Institute/Organization (Note: Please Enter Your institute/organization name in Block Letters) *",
            "Remarks": "Any Remarks",

        }


class AccommodationForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    state_choices = (
        ("Andhra Pradesh","Andhra Pradesh"),
        ("Arunachal Pradesh","Arunachal Pradesh"),
        ("Assam","Assam"),
        ("Bihar","Bihar"),
        ("Chhattisgarh","Chhattisgarh"),
        ("Goa","Goa"),
        ("Gujarat","Gujarat"),
        ("Haryana","Haryana"),
        ("Himachal Pradesh","Himachal Pradesh"),
        ("Jammu and Kashmir","Jammu and Kashmir"),
        ("Jharkhand","Jharkhand"),
        ("Karnataka","Karnataka"),
        ("Kerala","Kerala"),
        ("Madhya Pradesh","Madhya Pradesh"),
        ("Maharashtra","Maharashtra"),
        ("Manipur","Manipur"),
        ("Meghalaya","Meghalaya"),
        ("Mizoram","Mizoram"),
        ("Nagaland","Nagaland"),
        ("Odisha","Odisha"),
        ("Punjab","Punjab"),
        ("Rajasthan","Rajasthan"),
        ("Sikkim","Sikkim"),
        ("Tamil Nadu","Tamil Nadu"),
        ("Telangana","Telangana"),
        ("Tripura","Tripura"),
        ("Uttar Pradesh","Uttar Pradesh"),
        ("Uttarakhand","Uttarakhand"),
        ("West Bengal","West Bengal"),
        ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
        ("Chandigarh","Chandigarh"),
        ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
        ("Daman and Diu","Daman and Diu"),
        ("Lakshadweep","Lakshadweep"),
        ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
        ("Puducherry","Puducherry"),
        ("Other", "Other")
    )
    ROLE = (
        ('Student','Student'),
        ('Academician','Academician'),
        ('Industrial Expert','Industrial Expert/Scientist/Project Staffs/Research Associates/Post Doctorates'),
        ('Attendee','Attendee'),
        ('Other','Other')
    )
    role = forms.ChoiceField(choices=ROLE,label="Mention your Role")
    college = forms.CharField(max_length=300, label="School/ College/ Company/ Organisation Name *" )
    address_line_1 = forms.CharField(max_length=100, label="School / Company/ Organisation Address Line 1 *")
    address_line_2 = forms.CharField(max_length=100, label="School / Company/ Organisation  Address Line 2 *")
    pincode = forms.CharField(max_length=6, label="Pincode *")
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    state = forms.ChoiceField(choices=state_choices, label="State *")
    within_radius = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Are you within a 50km radius of IITG?", widget=forms.Select(), required=True)
    entry_date = forms.DateField(label="Entry Date *", widget=forms.DateInput(attrs={'type':'date'}))
    # exit_date = forms.DateField( label="Exit Date *", widget=forms.HiddenInput())
    # no_of_days = forms.ChoiceField(choices=no_of_days_choices, label="No of Days *")

    class Meta:
        model = Accommodation
        fields = ("name","role", "college",  "address_line_1", "address_line_2", "pincode", "number", "state", "within_radius","entry_date")
        labels = {
            "college": "College *",
            "address_line_1": "Address Line 1 *",
            "address_line_2": "Address Line 2 *",
            "pincode": "Pincode *",
            "number":"Phone Number *",
            "state": "State *",
            "within_radius": "Is your college / organisation within a 50km radius of IITG? *",
            "entry_date": "Entry Date *",
        }



class AbstractForm(forms.ModelForm):
    class Meta:
        model = RICEvent
        fields = ("abstract",)



class AbstractICForm(forms.ModelForm):
    class Meta:
        model = IC
        fields = ("icSubmission",)


class AbstractRICForm(forms.ModelForm):
    class Meta:
        model = RICEvent
        fields = ("abstract",)



class WorkshopForm(forms.ModelForm):
    workshop = forms.ModelMultipleChoiceField(
            queryset=Workshop.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            label="Events You Want to Participate"
            )
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    class Meta:
        model = WorkshopBio
        fields = ("dept","workshop","number")


class WorkshopPaymentDetailForm(forms.ModelForm):
    class Meta:
        model = WorkshopBio
        fields = ("razorpay_payment_id",)


class IntegrationBeeForm(forms.ModelForm):


    CLASS_CHOICES = (
        ('B1','B1'),
        ('B2','B2'),
        ('B3','B3'),
        ('B4','B4'),
    )

    class_name = forms.ChoiceField(choices=CLASS_CHOICES,label="Class (Here B1-> Bachelors Year 1 etc)")
    id_card = forms.FileField(label="Upload your proof of studentship as ID Card/Bonafide Certificate (PDF format only)")
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))

    def save(self, commit=True):
        instance = super(IntegrationBeeForm, self).save(commit=False)

        # generate a unique ID using uuid
        instance.uuid = 'RIC2023-intBee-' + str(uuid.uuid4().int)[0:6]

        if commit:
            instance.save()
        return instance

    class Meta:
        model = IntegrationBee
        fields = ("name", "school_college_name", "school_college_address", "class_name",  "id_card", "number")
        labels = {
            "name": "Name of student",
            "school_college_name": "School/College Name",
            "school_college_address": "School/College Address",
            "class_name": "Class",
            "number": "Phone Number"
        }


class DifferentiaChallengeForm(forms.ModelForm):


    CLASS_CHOICES = (
        ('XI','XI'),
        ('XII','XII'),

    )

    # level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.RadioSelect, label="Level of Integration Bee")
    class_name = forms.ChoiceField(choices=CLASS_CHOICES,label="Class")
    id_card = forms.FileField(label="Upload your proof of studentship as ID Card/Bonafide Certificate (PDF format only)")
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))

    def save(self, commit=True):
        instance = super(DifferentiaChallengeForm, self).save(commit=False)

        # generate a unique ID using uuid
        instance.uuid = 'RIC2023-dsino-' + str(uuid.uuid4().int)[0:6]

        if commit:
            instance.save()
        return instance

    class Meta:
        model = DifferentiaChallenge
        fields = ("name", "school_college_name", "school_college_address",  "class_name", "id_card", "number")
        labels = {
            "name": "Name of student",
            "school_college_name": "School/College Name",
            "school_college_address": "School/College Address",
            "class_name": "Class",
            "number": "Phone Number"
        }


class IDForm(forms.ModelForm):
    class Meta:
        model = IntegrationBee
        fields = ("id_card",)

class StudDetailForm(forms.ModelForm):
    class Meta:
        model = MathEvent
        fields = ("student_list",)


class MathEventForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    school_contact = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    student_list = forms.FileField(label='Upload Excel File with student details', required=True)
    teacher_list = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='List of Teachers Coming to Attend', required=True)
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))

    def save(self, commit=True):
        instance = super(MathEventForm, self).save(commit=False)

        # generate a unique ID using uuid
        instance.uuid = 'RIC2023-mathOly-' + str(uuid.uuid4().int)[0:6]

        if commit:
            instance.save()
        return instance

    class Meta:
        model = MathEvent
        fields = ('school_name', 'school_address', 'school_contact', 'point_of_contact', 'student_list', 'teacher_list')
        labels = {
            'school_name': 'School/College Name *',
            'school_address': 'School/College Address *',
            'school_contact': 'School/College Contact Number *',
            'point_of_contact': 'Point of Contact *',

        }

class MathEventIndividualForm(forms.ModelForm):
    CLASS_CHOICES = (
        ('VI','VI'),
        ('VII','VII'),
        ('VIII','VIII'),
        ('IX','IX'),
        ('X','X'),

    )
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    school_contact = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    id_card = forms.FileField(label="Upload ID Card", required=True)
    class_name = forms.ChoiceField(choices=CLASS_CHOICES,label="Class")

    def save(self, commit=True):
        instance = super(MathEventIndividualForm, self).save(commit=False)

        # generate a unique ID using uuid
        instance.uuid = 'RIC2023-mathOlympics-' + str(uuid.uuid4().int)[0:6]

        if commit:
            instance.save()
        return instance

    class Meta:
        model = MathEventIndividual
        fields = ('name','id_card',  "class_name", "number", 'school_name', 'school_address', 'school_contact')
        labels = {
            'name': 'Name *',
            'school_name': 'School/College Name *',
            'school_address': 'School/College Address *',
            'school_contact': 'School/College Contact Number *',

        }