from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('adminlog',views.adminlog,name='adminlog'),
    path('login',views.login_request,name='login'),
    path('register',views.register_request,name='register'),
    path('adlogout',views.adlogout,name='adlogout'),
    path('index',views.index,name='index'),
    path('storeinput',views.storeinput,name='storeinput'),
    path('coursemarks',views.course_marks,name='coursemarks')
]