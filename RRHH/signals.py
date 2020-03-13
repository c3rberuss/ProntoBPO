from django.dispatch import Signal

count_view = Signal(providing_args=['applicant'])
