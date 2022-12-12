from django.db import models
from internalAuth.models import HealthUser

class Request(models.Model):
    endpoint = models.CharField(max_length=100, null=True) # The url the user requested
    user = models.ForeignKey(HealthUser, on_delete=models.SET_NULL, null=True) # User that made request, if authenticated
    response_code = models.PositiveSmallIntegerField() # Response status code
    method = models.CharField(max_length=10, null=True)  # Request method
    remote_address = models.CharField(max_length=20, null=True) # IP address of user
    exec_time = models.IntegerField(null=True) # Time taken to create the response
    date = models.DateTimeField(auto_now=True) # Date and time of request
    body_response = models.TextField() # Response data
    body_request = models.TextField() # Request data