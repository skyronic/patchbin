from django import forms

class PatchForm(forms.Form):
    patchFile = forms.FileField(required = False, label = r'Upload Patch', help_text = r'Only unified diff with .patch extension')
    #patchText = forms.Textarea(required = False, label = r'Insert Patch text', help_text = r'Paste Unified diff here')
    #patchType = forms.ChoiceField(['Unified', 'Something Else'], required = False, label = r'Type of patch')
    
    