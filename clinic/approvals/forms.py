from django import forms

from clinic.approvals.choices import JoinRequestStatusChoices
from clinic.approvals.models import JoinRequest


class JoinRequestForm(forms.ModelForm):
    class Meta:
        model = JoinRequest
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.status != JoinRequestStatusChoices.PENDING:
            self.fields["status"].widget.attrs["readonly"] = True
            self.fields["status"].disabled = True  # Disables the field to prevent editing
