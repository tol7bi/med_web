"""med_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from diagnostics.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('set_language/<str:language>', set_language, name='set_language'),
    path('privacy/', privacy, name='privacy'),
    path('general/', generalInfo, name='general'),
    path('complaints/', complaints, name='complaints'),
    path('add_button/', addButon, name='add_button'),
    path('add_complaints/', add_complaints, name='add_complaints'),
    path('remove_complaint_from_set/', remove_complaint_from_set, name='remove_complaint_from_set'),
    path('add_complaint_to_set/', add_complaint_to_set, name='add_complaint_to_set'),
    path('blood/', blood, name='blood'),
    path('chem/', chem, name='chem'),
    path('extra/', extra, name='extra'),
    path('captcha/<str:redirect_to>', captchaPage, name='captcha'),
    path('data/', data, name='data'),
    path('loading/', loading, name='loading'),
    path('result/', result, name='result'),
    path('consult/<str:doctor>/', consult, name='consult'),
    path('additional/', additional, name='additional'),
    path('disease/', disease, name='disease'),
    path('medicines/', medicines, name='medicines'),
    path('illnesses/', illnesses, name='illnesses'),
    path('operations/', operations, name='operations'),
    path('drug/', drug, name='drug'),
    path('food/', food, name='food'),
    path('habits/', habits, name='habits'),
    path('new_diagnostics/', new_diagnostics, name='new_diagnostics'),
    path('profession/', profession, name='profession'),
    path('contacts/', contacts, name='contacts'),
    path('send_message', send_message, name='send_message'),
    path('success/', success, name='success'),
    path('choose/', choose, name='choose'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('cabinet_clinic/', cabinet_clinic, name='cabinet_clinic'),
    path('cabinet/', cabinet_specialist, name='cabinet_specialist'),
    path('services/', services, name='services'),
    path('logout/', logout, name='logout'),
    path('service/<int:service_id>/', get_service, name='get_service'),
    path('delete/<int:service_id>/', delete_service, name='delete_service'),
    path('services_clinic/', services_clinic, name='services_clinic'),
    path('specialists_education/', specialists_education, name='specialists_education'),
    path('delete_specialist/<int:id>/', delete_specialist, name='delete_specialist'),
    path('delete_education/<int:id>/', delete_education, name='delete_education'),
]
