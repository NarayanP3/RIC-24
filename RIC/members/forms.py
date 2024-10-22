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
        fields = ("institute", "dept","title", "iitg_student", "theme", "role", "abstract", "event","number")
        labels = {
            "institute": "Please Enter your institute (Note: Please Enter Your institute name in Block Letters) *",
            "dept": "Please Select your related Department *",
            "abstract": "Please submit your Abstract file in following format (sample abstract is given below) *",
        }


class FullPaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = RICEvent
        fields = ['full_paper_abstract']
        widgets = {
            'full_paper_abstract': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(FullPaperSubmissionForm, self).__init__(*args, **kwargs)
        # Remove the "Clear" checkbox
        self.fields['full_paper_abstract'].widget.clear_checkbox_label = ''
        self.fields['full_paper_abstract'].widget.template_name = 'django/forms/widgets/clearable_file_input.html'
        self.fields['full_paper_abstract'].widget.initial_text = ''
        self.fields['full_paper_abstract'].widget.input_text = 'Change'

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