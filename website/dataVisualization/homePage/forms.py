from django import forms

# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()

class DocumentForm(forms.Form):
    # docfile = forms.FileField(label='Select a file',widget=forms.ClearableFileInput(attrs={'class' : 'btn btn-info btn-lg'}))
    docfile = forms.FileField(label='Select a file',label_suffix="")