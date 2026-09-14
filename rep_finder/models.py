"""
Models for the Forms & Submissions app.

This app extends Wagtail's built-in form builder (wagtail.contrib.forms)
to create the Complaint Form and any future submission forms.

Key design decisions:
  - AbstractEmailForm (not AbstractForm) is used because submissions should
    be both stored in the database AND emailed to student government officers.
    AbstractForm only stores; AbstractEmailForm adds email notification.
  - FormField uses AbstractFormField which gives editors the power to
    add/remove/reorder form fields entirely through the Wagtail admin.
    No code changes needed to add a "Category" dropdown or rename a field.
  - The privacy_notice field lets admins display anonymity/privacy information
    near the form, which is important for a complaint submission system.

How Wagtail's form builder works:
  1. Admin creates a ComplaintFormPage in the page tree
  2. Admin adds FormField entries (name, email, textarea, dropdown, etc.)
     via InlinePanel — each FormField becomes one HTML input
  3. When a user submits the form, Wagtail:
     a) Validates the input
     b) Stores the submission in the database (viewable in Wagtail admin)
     c) Sends an email notification (if configured)
     d) Renders the thank_you_text as a landing page
"""

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django import forms

from modelcluster.fields import ParentalKey

from branches.models import Role, MemberProfile, MemberRoleAssignment, class_choices
from wagtail.fields import RichTextField


# class RepsFormField(AbstractFormField):
#     """
#     A single field in a form (e.g., "Your Name", "Description of Complaint").

#     AbstractFormField provides:
#       - label: the field's visible label
#       - field_type: dropdown of HTML input types (text, email, textarea,
#         dropdown, checkboxes, radio buttons, date, URL, number, etc.)
#       - required: whether the field must be filled in
#       - choices: comma-separated options for dropdowns/checkboxes/radios
#       - default_value: pre-filled value
#       - help_text: hint text below the field

#     The ParentalKey links this to a specific RepsFormPage, so each
#     form page has its own independent set of fields.
#     """

#     page = ParentalKey(
#         "rep_finder.RepsFormPage",
#         on_delete=models.CASCADE,
#         related_name="form_fields",
#     )

#     help_text = RichTextField(blank=True)

class RepsFormPage(forms.Form):
    your_class = forms.ChoiceField(label="Choose Your Class Year", choices=class_choices())

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    def get_representatives(self):
        chosen_constituency = self.data["your_class"]

        role_list = Role.objects.filter(constituency=chosen_constituency)

        role_assignments_list = []
        for role in role_list:
            role_assignments_list += role.assignments.all()
        
        member_profile_list = []
        for role_assignment in role_assignments_list:
            member_profile_list += [role_assignment.member]
        
        return [
            {
                "member": member,
                "roles": [assignment.role.get_display_name() for assignment in member.assignments.all() if assignment.role.constituency==chosen_constituency]
            } for member in member_profile_list
        ]

    class Meta:
        verbose_name = "Representative Finder Form"
