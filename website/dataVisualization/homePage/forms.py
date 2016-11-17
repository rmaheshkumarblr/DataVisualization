from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()

class CreateUserForm(forms.Form):
    email_address = forms.EmailField(label='Email Address', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password_repeat = forms.CharField(
        label='Confirm Password',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

class LoginForm(forms.Form):
    email_address = forms.EmailField(label='Email Address', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


USETYPE = ((1, 'Ambient Monitoring'),
           (2, 'Indoor'),
           (3, 'Mobile'),
           (4, 'Experiment'))

POLLUTANTOFINTEREST = ((1, 'VOC1'),
                       (2, 'VOC2'),
                       (3, 'O3'),
                       (4, 'CO2'))

class DocumentForm(forms.Form):
    # docfile = forms.FileField(label='Select a file',widget=forms.ClearableFileInput(attrs={'class' : 'btn btn-info btn-lg'}))
    podId = forms.CharField(label='Pod ID', max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    projectName = forms.CharField(label='Project Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = forms.CharField(label='Name of your School', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mentorName = forms.CharField(label='Name of your Mentor', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Location', max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    startDate = forms.DateField(label='Start Date',widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
    endDate = forms.DateField(label='End Date',widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
    podUseType = forms.MultipleChoiceField(label='POD Usage type', choices=USETYPE,widget=forms.CheckboxSelectMultiple())
    pollutantOfInterest = forms.MultipleChoiceField(label='Pollutants of Interest', choices=POLLUTANTOFINTEREST,widget=forms.CheckboxSelectMultiple())
    podUseReason = forms.CharField(label='POD Usage Reason',widget=forms.Textarea(attrs={'class': 'form-control'}))

    docfile = forms.FileField(label='Select a file',label_suffix="") 




