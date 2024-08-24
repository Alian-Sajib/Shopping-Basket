from django.contrib import admin
from App_login.models import User,Profile

# Register your models here.
admin.site.register(User)

admin.site.register(Profile)


'''
super user id  :
email =a@gmail.com
pass = 123

user id = test2@gmail.com
pass = asdf4321

'''