import ast
import json
import os
import re
from urllib.parse import unquote
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.translation import activate
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib import auth

from datetime import datetime

from .function import zhP_defStart, zhPvar, zhP_defCngZh, zh_vZ
from .result import *
from .document import *

from diagnostics.models import *
from diagnostics.forms import *


# Create your views here.

GENDERS = {
    'F': 'пол: женский',
    'M': 'пол: мужской',
}

def set_language(request, language):
    previous_url = request.META.get('HTTP_REFERER')
    request.session['language'] = language
    # print(111)
    return redirect(previous_url)

def index(request):
    language = request.session.get('language', 'ru')
    # print(language)
    if language == 'en':
        return render(request, 'diagnostics/1_index_en.html')
    if language == 'ru':
        return render(request, 'diagnostics/1_index.html')

def privacy(request):
    language = request.session.get('language', 'ru')
    if request.method == 'POST':
        now = datetime.now()
        formatted_date_time = now.strftime("%Y%m%d%H%M%S")
        request.session['idObs'] = f'idObs_{formatted_date_time}'

        zhP_frz, o_zhPallVar, zhP_0frz = zhP_defStart()
        request.session['zhP_frz'] = zhP_frz
        request.session['o_zhPallVar'] = o_zhPallVar
        request.session['zhP_0frz'] = zhP_0frz

        if not (request.session.get('zhP') and request.session.get('zh0P')):
            zhP = set()
            zh0P = set()
            request.session['zhP'] = list(zhP)
            request.session['zh0P'] = list(zh0P)

        return HttpResponseRedirect(reverse('general'))
    if language == 'en':
        return render(request, 'diagnostics/2_privacy_en.html')
    if language == 'ru':
        return render(request, 'diagnostics/2_privacy.html')

def generalInfo(request):
    request.session['captcha'] = []
    if request.method == 'POST':

        data=request.POST
        result={}
        if data.get('gender')=='' or data.get('age')=='' or data.get('weight')=='' or data.get('height')=='' or (data.get('ispregnancy')=='on' and data.get('pregnancy')==''):
            if data.get('ispregnancy')=='on' and data.get('pregnancy')=='':
                result['error'] = "Заполните поле беременности!"
            else:
                result['error'] = "Заполните обязательные поля!"
            
        else:
            if data['pregnancy'] != '':
                pregnancy = float(data['pregnancy'])
            else:
                pregnancy = ''
            request.session['danP'] = (GENDERS[data['gender']], int(data['age']), float(data['weight']), float(data['height']), pregnancy, request.session['idObs'])
            result['redirect'] = True

        return JsonResponse(result)
    else:
        form=GeneralInfoForm()
    language = request.session.get('language', 'ru')
    
    context={'form': form,
             'doctor': request.session.get('dopDanP')}
    if language == 'en':
        return render(request, 'diagnostics/3_general_en.html', context)
    if language == 'ru':
        return render(request, 'diagnostics/3_general.html', context)
    
def complaints(request):
    request.session['captcha'] = []
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('disease'))
    
    language = request.session.get('language', 'ru')
    context = {
        'doctor': request.session.get('dopDanP')
    }
    if language == 'en':
        return render(request, 'diagnostics/4_complaints_en.html')
    if language == 'ru':
        return render(request, 'diagnostics/4_complaints.html', context)

@csrf_exempt
def add_complaints(request):
    if request.method == "POST":
        data = json.loads(request.body)
        input_data = data.get('data', '')

        o_zhPallVar = set(request.session['o_zhPallVar'])
        if input_data:
            matched_options = zhPvar(input_data, o_zhPallVar)
        else:
            matched_options = ''
        return JsonResponse({"result": matched_options[:8]})

@csrf_exempt
def addButon(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data_add = data.get('data', '')
        zhP_serialized = request.session['zhP']
        zhP = set([tuple(subset_list) for subset_list in zhP_serialized])
        zhP.add((data_add, request.session['idObs']))
        request.session['zhP'] = list(zhP)
        print(zhP)
        return JsonResponse({"result": ''})
        

@csrf_exempt
def remove_complaint_from_set(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data_remove = data.get('data', '')

        zhP_serialized = request.session['zhP']
        zhP = set([tuple(subset_list) for subset_list in zhP_serialized])
        zhP.add((data_remove, request.session['idObs']))

        zh0P_serialized = request.session['zh0P']
        zh0P = set([tuple(subset_list) for subset_list in zh0P_serialized])

        zhP_frz_serialized = request.session['zhP_frz']
        zhP_frz = set([tuple(subset_list) for subset_list in zhP_frz_serialized])

        o_zhPallVar = set(request.session['o_zhPallVar'])

        zhP_0frz_serialized = request.session['zhP_0frz']
        zhP_0frz = set([tuple(subset_list) for subset_list in zhP_0frz_serialized])

        zhP, zh0P, zhP_frz, o_zhPallVar = zhP_defCngZh(zhP, zh0P, zhP_frz, zhP_0frz, o_zhPallVar)

        request.session['zhP'] = list(zhP)
        request.session['zh0P'] = list(zh0P)
        request.session['zhP_frz'] = list(zhP_frz)
        request.session['o_zhPallVar'] = list(o_zhPallVar)
        return JsonResponse({"result": ''})

@csrf_exempt
def add_complaint_to_set(request):
    data = json.loads(request.body)
    data_remove = data.get('data', '')

    zhP_serialized = request.session['zhP']
    zhP = set([tuple(subset_list) for subset_list in zhP_serialized])

    for subset in zhP:
        if data_remove in subset:
            subset_to_remove = subset
            print(subset)

    zhP.discard(subset_to_remove)
    
    zh0P_serialized = request.session['zh0P']
    zh0P = set([tuple(subset_list) for subset_list in zh0P_serialized])

    zhP_frz_serialized = request.session['zhP_frz']
    zhP_frz = set([tuple(subset_list) for subset_list in zhP_frz_serialized])

    o_zhPallVar = set(request.session['o_zhPallVar'])

    zhP_0frz_serialized = request.session['zhP_0frz']
    zhP_0frz = set([tuple(subset_list) for subset_list in zhP_0frz_serialized])

    zhP, zh0P, zhP_frz, o_zhPallVar = zhP_defCngZh(zhP, zh0P, zhP_frz, zhP_0frz, o_zhPallVar)

    request.session['zhP'] = list(zhP)
    request.session['zh0P'] = list(zh0P)
    request.session['zhP_frz'] = list(zhP_frz)
    request.session['o_zhPallVar'] = list(o_zhPallVar)

    return JsonResponse({"result": ''})

def blood(request):
    # request.session['captcha'] = []
    dictionary = {
        'erythrocytes': "эритроциты",
        'hemoglobin': "гемоглобин",
        'leukocytes': "лейкоциты",
        'platelets': "тромбоциты",
        'hematocrit': 'гематокрит',
        'soe': 'СОЭ',
        'color_indicator': 'цветовой показатель',
        'mean_erytr_volume': 'средний объем эритроцита (MCV)',
        'distr_erytr_volume_variation': 'распределение эритроцитов по объему, коэффициент вариации (RDW-CV)',
        'distr_ertyr_volume_standart_devi': 'распределение эритроцитов по объему, стандартное отклонение (RDW-SD)',
        'distr_platelets_volume': 'распределение тромбоцитов по объему (PDW)',
        'mean_platelets_volume': 'средний объем тромбоцита (MPV)',
        'big_eryrt_coeff': 'коэффициент больших тромбоцитов (P-LCR)',
        'mean_hemoglobin_in_erytr': 'среднее содержание гемоглобина в эритроците (MCH)',
        'mean_concentration_hemoglobin_in_eryrts': 'средняя концентрация гемоглобина в эритроците (MCHC)',
        'basophils': 'базофилы',
        'basophils_procent': 'базофилы, %',
        'eosinophils': 'эозинофилы',
        'eosinophils_procent': 'эозинофилы, %',
        'neutrophils': 'нейтрофилы',
        'neutrophils_procent': 'нейтрофилы, %',
        'neutrophils_stick': 'нейтрофилы палочкоядерные, %',
        'neutrophils_segment': 'нейтрофилы сегментоядерные, %',
        'lymphocytes': 'лимфоциты',
        'lymphocytes_procent': 'лимфоциты, %',
        'monocytes': 'моноциты',
        'monocytes_procent': 'моноциты, %',
        'trombocrit': 'тромбокрит',
    }

    if request.method == 'POST':
        data = request.POST
        OAKzP = []
        for d in data:
            if d in dictionary and data[d] != '':
                OAKzP.append((dictionary[d], float(data[d]), request.session['idObs']))
        request.session['OAKzP'] = OAKzP

        return HttpResponseRedirect(reverse('chem'))
    else:
        form = BloodInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    
    language = request.session.get('language', 'ru')

    if language == 'en':
        return render(request, 'diagnostics/5_blood_en.html', context)
    if language == 'ru':
        return render(request, 'diagnostics/5_blood.html', context)

def chem(request):
    dictionary = {
        'protein': "белок общий",
        'billirubin_general': "билирубин общий",
        'billirubin_direct': "билирубин прямой",
        'sugar': "глюкоза",
        'urea': "мочевина",
        'amylase': "амилаза панкреатическая",
        'ALT': 'АЛТ',
        'ALB': 'альбумин',
        'alpha_amylase': 'амилаза общая',
        'ACT': 'АСТ',
        'beta_globulin': 'бета-глобулин',
        'vitamin_b12': 'витамин B12',
        'gamma_globulin': 'гамма-глобулин',
        'gamma_gpt': 'гамма-ГТП',
        'hemoglobin_glik': 'гликированный гемоглобин',
        'homocistein': 'гомоцистеин',
        'ferum': 'железо',
        'zhel_acid': 'желчные кислоты',
        'calium': 'калий',
        'calcium_general': 'кальций общий',
        'coeff_atereg': 'коэффициент атерогенности',
        'kreatinin': 'креатинин',
        'kreatinkinaza': 'креатинкиназа',
        'laktat': 'лактат',
        'laktatdegidroginaza': 'лактатдегидрогеназа',
        'ferum_ability': 'латентная железосвязывающая способность сыворотки крови',
        'lipaza': 'липаза',
        'magniy': 'магний',
        'mnoglobin': 'миоглобин',
        'moch_acid': 'мочевая кислота',
        'natriy': 'натрий',
        'reakt_protein': 'C-реактивный белок',
        'transferin': 'трансферрин',
        'trigleceridy': 'триглицериды',
        'ferritin': 'ферритин',
        'folievay_acid': 'фолиевая кислота',
        'phosphor': 'фосфор',
        'fruktozamin': 'фруктозамин',
        'chlor': 'хлор',
        'cholesterin_general': 'холестерин общий',
        'cholesterin_lpvp': 'ЛПВП',
        'cholesterin_lpnp': 'ЛПНП',
        'choliensteraza': 'холинэстераза',
        'acid_fosfataza': 'щелочная фосфатаза'
    }

    if request.method == 'POST':
        data = request.POST
        BXzP = []
        for d in data:
            if d in dictionary and data[d] != '':
                BXzP.append((dictionary[d], float(data[d]), request.session['idObs']))
        request.session['BXzP'] = BXzP
        
        return HttpResponseRedirect(reverse('extra'))
        
    else:
        form = ChemInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}

    language = request.session.get('language', 'ru')

    if language == 'en':
        return render(request, 'diagnostics/6_chem_en.html', context)
    if language == 'ru':
        return render(request, 'diagnostics/6_chem.html', context)

def extra(request):
    if request.method == 'POST':
        data = request.POST
        print(request.POST.getlist('languages'))
        request.session['fndSp'] = (data['input'], request.POST.getlist('languages'), request.session['idObs'])
        return HttpResponseRedirect(reverse('data'))
    form = ExtraInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/extra.html', context)


def new_diagnostics(request):
    # Очищаем данные сессии
    request.session.clear()
    return HttpResponseRedirect(reverse('index'))

def captchaPage(request, redirect_to):
    
    if request.method == "POST":
        return HttpResponseRedirect(reverse(redirect_to))

    context= {
        'redirect_to': redirect_to
    }
    return render(request, 'diagnostics/captcha.html', context)

def data(request):

    if not request.session.get('OAKzP'):
        request.session['OAKzP'] = []
    OAKzP_serialized = request.session['OAKzP']
    OAKzP = set([tuple(subset_list) for subset_list in OAKzP_serialized])

    if not request.session.get('BXzP'):
        request.session['BXzP'] = []

    BXzP_serialized = request.session['BXzP']
    BXzP = set([tuple(subset_list) for subset_list in BXzP_serialized])

    patient_data_raw = request.session['danP']
    gender = patient_data_raw[0]
    age = f"Возраст, лет: {int(patient_data_raw[1])}"
    weight = f'Вес, кг: {int(patient_data_raw[2])}'
    height = f'Рост, см: {int(patient_data_raw[3])}'
    if patient_data_raw[4] == '' or patient_data_raw[4] == None: #  or patient_data_raw[4] == None
        patient_data = (gender, age, weight, height)
    else:
        pregnancy = f'беременность: {int(patient_data_raw[4])} нед.'
        patient_data = (gender, age, weight, height, pregnancy)
    
    print(OAKzP)
    complaints, general_analyze, chem_analyze = zh_vZ(request.session['danP'], request.session.get('zhP', []), OAKzP, BXzP)
    print(general_analyze)
    context = {
        'patient_data': patient_data,
        'complaints': complaints,
        'disease': request.session.get('davnZbP', [''])[0],
        'medicines': request.session.get('plsP', [''])[0],
        'illnesses': request.session.get('anDsP', [''])[0],
        'operations': request.session.get('anOperP', [''])[0],
        'drug': request.session.get('alLsP', [''])[0],
        'food': request.session.get('alOtSubP', [''])[0],
        'habits': request.session.get('vrPrP', [''])[0],
        'profession': request.session.get('prof', [''])[0],
        'general_analyzes': list(general_analyze),
        'chem_analyze': list(chem_analyze),
        'extra': request.session.get('fndSp'),
        'doctor': request.session.get('dopDanP')
    }

    return render(request, 'diagnostics/7_data.html', context)


def loading(request):
    return render(request, 'diagnostics/loading.html')

def result(request):

    if not request.session.get('OAKzP'):
        request.session['OAKzP'] = []
    OAKzP_serialized = request.session['OAKzP']
    OAKzP = set([tuple(subset_list) for subset_list in OAKzP_serialized])

    if not request.session.get('BXzP'):
        request.session['BXzP'] = []
    BXzP_serialized = request.session['BXzP']
    BXzP = set([tuple(subset_list) for subset_list in BXzP_serialized])

    if not request.session.get('davnZbP'):
        request.session['davnZbP'] = ['', request.session['idObs']]
    if not request.session.get('plsP'):
        request.session['plsP'] = ['', request.session['idObs']]
    if not request.session.get('anDsP'):
        request.session['anDsP'] = ['', request.session['idObs']]
    if not request.session.get('anOperP'):
        request.session['anOperP'] = ['', request.session['idObs']]
    if not request.session.get('alLsP'):
        request.session['alLsP'] = ['', request.session['idObs']]
    if not request.session.get('alOtSubP'):
        request.session['alOtSubP'] = ['', request.session['idObs']]
    if not request.session.get('vrPrP'):
        request.session['vrPrP'] = ['', request.session['idObs']]
    if not request.session.get('fndSp'):
        request.session['fndSp'] = ['', [], request.session['idObs']]
    if not request.session.get('prof'):
        request.session['prof'] = ['', request.session['idObs']]

    print(request.session['fndSp']  )
    warning, vivod_BMI, diag, doctors = u_ds_dr(request.session['danP'], request.session.get('zhP', []), request.session['davnZbP'], request.session['plsP'], 
                                                request.session['anDsP'], request.session['anOperP'], request.session['alLsP'], request.session['alOtSubP'], 
                                                request.session['vrPrP'], request.session['prof'], OAKzP, BXzP, request.session['fndSp'])

    print(doctors)
    # print(doctors)
    context = {
        'warning': warning,
        'vivod_BMI': vivod_BMI,
        'diag': diag,
        'doctors': doctors,
        'doctor': request.session.get('dopDanP')
    }
    # print(doctors[0])
    return render(request, 'diagnostics/8_result.html', context)

def consult(request, doctor):
    context = {'doctor': doctor}
    request.session['doctor'] = doctor
    return render(request, 'diagnostics/9_consult.html', context)

def additional(request):
    if request.method == "POST":
        data = request.POST
        if data.get('last_name') and data.get('first_name') and data.get('birthdate') and data.get('phone'): 
            request.session['required'] = True
        request.session['dopDanP'] = (data['last_name'], data['first_name'], data['middle_name'], data['birthdate'], data['profession'], data['iin'], data['phone'], request.session['idObs'])
        return JsonResponse({})
    else:
        form = AdditionalInfoForm()
    context = {'form': form}
    return render(request, 'diagnostics/10_additional.html', context)

def disease(request):

    if request.method == "POST":
        data = request.POST
        request.session['davnZbP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('medicines'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/11_disease.html', context)

def medicines(request):
    if request.method == "POST":
        data = request.POST
        request.session['plsP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('illnesses'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/12_medicines.html', context)

def illnesses(request):
    if request.method == "POST":
        data = request.POST
        request.session['anDsP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('operations'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/13_illnesses.html', context)

def operations(request):
    if request.method == "POST":
        data = request.POST
        request.session['anOperP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('drug'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/14_operations.html', context)

def drug(request):
    if request.method == "POST":
        data = request.POST
        request.session['alLsP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('food'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/15_drug_allergy.html', context)

def food(request):
    if request.method == "POST":
        data = request.POST
        request.session['alOtSubP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('habits'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/16_food_allergy.html', context)

def habits(request):
    if request.method == "POST":
        data = request.POST
        request.session['vrPrP'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('profession'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/17_bad_habits.html', context)

def profession(request):
    if request.method == "POST":
        data = request.POST
        request.session['prof'] = (data['input'], request.session['idObs'])
        return HttpResponseRedirect(reverse('blood'))
    else:
        form = TextInfoForm()
    context = {'form': form,
               'doctor': request.session.get('dopDanP')}
    return render(request, 'diagnostics/profession.html', context)

idDrInfo = [
('id8dr_1', 'врач Айболит1 Александр Николаевич', 'Врач терапевт, стаж 10 лет, 2-ая категория; онколог, стаж 8 лет, высшая категория; гастроэнтеролог, стаж 11 лет, 1-ая категория; хирург, стаж 22 года, без категории. Кандидат медицинских наук. В практике использует принципы интегративной медицины.', 7000, 'cons2', 'mymail7114@yandex.ru', 'казахский', 'УЗИ'), 
('id8dr_2', 'врач Айболит2 Александр Николаевич', 'Врач инфекционист, стаж 5 лет, 1-ая категория; врач общей практики, стаж 7 лет, без категории. Кандидат медицинских наук.', 7000, 'cons2', 'gnz@live.ru', 'русский', 'ФГДС'), 
('id8dr_3', 'врач Айболит3 Александр Николаевич', 'Врач гастроэнтеролог, стаж 5 лет, 2-ая категория.', 7000, 'cons3', 'mymail200317@rambler.ru', 'английский', 'психоанализ'), 
('id8dr_4', 'врач, диетолог Айболит4 Александр Николаевич', 'Врач онколог, стаж 5 лет, высшая категория; диетолог, стаж 3 года.', 'стоимость неизвестна', 'cons3', 'osot23@mail.ru', 'русский, казахский', 'холецистэктомия, удаление желчного пузыря'), 
('id8dr_5', 'врач невролог, психолог Айболит5 Александр Николаевич', 'Врач невролог, стаж 7 лет, высшая категория; психолог, стаж 12 лет.', 9000, 'cons2', 'sm8ds8dr@gmail.com', 'русский, английский', ''), 
('id8dr_6', 'психолог Айболит6 Александр Николаевич', 'Психолог, стаж 7 лет.', 7000, 'cons2', 'mymail160811@gmail.com', 'русский, казахский, английский', ''), 
('id8dr_7', 'шаман Айболит7 Александр Николаевич', 'Шаман, опыт 777 лет. В практике использует все прошлые и будущие знания человечества.', 'стоимость неизвестна', 'cons3', 'mymail789@mail.ru', 'японский', ''), 
]

servT = [
('id8dr_1', 'A шаман Айболит7 Александр Николаевич', 'Шаман, опыт 777 лет. В практике использует все прошлые и будущие знания человечества.', 'стоимость неизвестна', 'cons2', 'mymail789@mail.ru', 'японский', ''), 
('id8dr_2', 'B психолог Айболит6 Александр Николаевич', 'Психолог, стаж 7 лет.', 7000, 'cons2', 'mymail160811@gmail.com', 'русский, казахский, английский', ''), 
('id8dr_3', 'C врач невролог, психолог Айболит5 Александр Николаевич', 'Врач невролог, стаж 7 лет, высшая категория; психолог, стаж 12 лет.', 9000, 'cons2', 'sm8ds8dr@gmail.com', 'русский, английский', ''), 
('id8dr_4', 'D врач, диетолог Айболит4 Александр Николаевич', 'Врач онколог, стаж 5 лет, высшая категория; диетолог, стаж 3 года.', 'стоимость неизвестна', 'cons3', 'mymail789@mail.ru', 'русский, казахский', 'холецистэктомия, удаление желчного пузыря'), 
('id8dr_5', 'E врач Айболит3 Александр Николаевич', 'Врач гастроэнтеролог, стаж 5 лет, 2-ая категория.', 7000, 'cons3', 'mymail200317@rambler.ru', 'английский', 'психоанализ'), 
('id8dr_6', 'G врач Айболит2 Александр Николаевич', 'Врач инфекционист, стаж 5 лет, 1-ая категория; врач общей практики, стаж 7 лет, без категории. Кандидат медицинских наук.', 7000, 'cons2', 'gnz@live.ru', 'русский', 'ФГДС'), 
('id8dr_7', 'H врач Айболит1 Александр Николаевич', 'Врач терапевт, стаж 10 лет, 2-ая категория; онколог, стаж 8 лет, высшая категория; гастроэнтеролог, стаж 11 лет, 1-ая категория; хирург, стаж 22 года, без категории. Кандидат медицинских наук. В практике использует принципы интегративной медицины.', 7000, 'cons2', 'mymail7114@yandex.ru', 'казахский', 'УЗИ'), 
]

def choose(request):
    # print(type(ast.literal_eval(unquote(request.GET.get('doctor')))))
    id = int(request.GET.get('doctor')[-1])
    print(servT[id-1])
    request.session['drInfoP'] = servT[id-1]
    # print(request.session['drInfoP'])
    return HttpResponseRedirect(reverse('contacts'))

def contacts(request):
    if request.method == "POST":
        data = request.POST
        request.session['dopDanP'] = (data['whatsApp'], data['telegram'], data['phone'], data['email'], request.session['idObs'])
        # print(1)
        return HttpResponseRedirect(reverse('profession'))
    else:
        form = ContactInfoForm()
    
    
    context = {'form': form,
               'doctor': request.session.get('dopDanP'),
               'name': request.session.get('drInfoP')}

    return render(request, 'diagnostics/contacts.html', context)

def send_message(request):
    print(request.session['drInfoP'][5])
    OAKzP_serialized = request.session['OAKzP']
    OAKzP = set([tuple(subset_list) for subset_list in OAKzP_serialized])

    BXzP_serialized = request.session['BXzP']
    BXzP = set([tuple(subset_list) for subset_list in BXzP_serialized])
    if request.session['drInfoP'][4] == 'cons2':
        document_name = sendDrRez(request.session['danP'], request.session.get('zhP'), request.session.get('davnZbP'), request.session.get('plsP'), request.session.get('anDsP'), request.session.get('anOperP'), request.session.get('alLsP'), request.session.get('alOtSubP'), request.session.get('vrPrP'), OAKzP, BXzP, request.session.get('dopDanP'), request.session.get('prof'))
    if request.session['drInfoP'][4] == 'cons3':
        document_name = sendDrSm(request.session['danP'], request.session.get('zhP'), request.session.get('davnZbP'), request.session.get('plsP'), request.session.get('anDsP'), request.session.get('anOperP'), request.session.get('alLsP'), request.session.get('alOtSubP'), request.session.get('vrPrP'), OAKzP, BXzP, request.session.get('dopDanP'), request.session.get('prof'))
    email = EmailMessage(
        document_name,
        '',
        settings.EMAIL_HOST_USER,
        [request.session['drInfoP'][5]],
    )
    file_path = f'{document_name}.docx'
    with open(file_path, 'rb') as file:
        email.attach(f'{document_name}.docx', file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    email.send()
    os.remove(file_path)
    print(document_name)
    return HttpResponseRedirect(reverse('success'))


def success(request):
    context = {
        'doctor': request.session.get('dopDanP'),
        'name': request.session.get('drInfoP')
    }
    return render(request, 'diagnostics/success.html', context)


from django.contrib import messages
def login(request):
    if request.method == 'POST':

        form = UserLoginForm(data=request.POST)
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            if user.type == 'Специалист':
                return HttpResponseRedirect(reverse('cabinet_specialist'))
            else:
                return HttpResponseRedirect(reverse('cabinet_clinic'))
        else:
            messages.info(request, 'Неправильно введены данные!')
            return redirect('login')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'diagnostics/login.html', context)


def registration(request):
    if request.method == "POST":
        print(request.POST['email'])
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                'Welcome to calcuhealth',
                'Thank you for registering on calcuhealth.',
                settings.EMAIL_HOST_USER,
                [request.POST['email']],
                fail_silently=False,
            )
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    # User.objects.all().delete()
    context = {'form': form}
    return render(request, 'diagnostics/registration.html', context)

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def cabinet_specialist(request):
    if request.method == 'POST':
        l = []
        email = request.user.email
        surname = request.POST['last_name_or_clinic_name']
        name = request.POST['first_name_or_clinic_address']
        patronymic = request.POST['patronymic_or_clinic_hours']
        gender = request.POST['gender']
        birthdate = request.POST['date_of_birth']
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').strftime('%d.%m.%Y')
        languages = request.POST.getlist('languages')
        other_language = request.POST['other_language']
        whatsapp = request.POST['whatsapp']
        telegram = request.POST['telegram']
        phone = request.POST['phone']
        country = request.POST['country']
        city = request.POST['city_or_locality']
        symptom_analysis = request.POST['computer_analysis']
        degree = request.POST['academic_degree_or_home_call']
        education_formset = EducationFormSet(request.POST)
        if education_formset.is_valid():
            for form in education_formset:
                if form.cleaned_data:

                    # start_date = form.cleaned_data.get('start_date')
                    # end_date = form.cleaned_data.get('end_date')
                    # specialty = form.cleaned_data.get('specialty')
                    # institution = form.cleaned_data.get('institution')
                    education_instance = form.save(commit=False)
                    education_instance.user = request.user
                    education_instance.save()
                    
                    
        f_oDLK = []
        education = Education.objects.filter(user=request.user)
        for e in education:
            l.append([['Начало', e.start_date.strftime('%d.%m.%Y')], ['Окончание', e.end_date.strftime('%d.%m.%Y')], ['Квалификация, специальность, тема', e.specialty], ['Учебное заведение', e.institution]])
        if len(l) == 0:
            l = [[['Начало', ''],
                ['Окончание', ''],
                ['Квалификация, специальность, тема', ''],
                ['Учебное заведение', '']]]

        form = RegistrationForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        if phone:
            phone = int(phone)
        # data = User.objects.filter(pk=request.user.id).first()
        # print(data.last_name_or_clinic_name)
        f_oDLK.append(['IdProfile', request.user.id])
        f_oDLK.append(['Email', email])
        f_oDLK.append(['Фамилия', surname])
        f_oDLK.append(['Имя', name])
        f_oDLK.append(['Отчество', patronymic])
        f_oDLK.append(['Пол', gender])
        f_oDLK.append(['Дата рождения', birthdate])
        f_oDLK.append([['Укажите языки, на которых могут быть предоставлены услуги', languages], ['добавить язык, отсутствующий в списке', other_language]])
        f_oDLK.append(['WhatsApp', int(whatsapp)])
        f_oDLK.append(['Telegram', telegram])
        f_oDLK.append(['Телефон', phone])
        f_oDLK.append(['Страна', country])
        f_oDLK.append(['Город, населенный пункт', city])
        f_oDLK.append(['Компьютерный анализ симптомов пациента', symptom_analysis])
        f_oDLK.append(['Валюта при указании стоимости услуг', request.POST['currency']])
        f_oDLK.append(l)
        f_oDLK.append(['Ученая степень', degree])
        print(f_oDLK)
        fileName = send_oDLK(f_oDLK)
        email = EmailMessage(
            'Личный кабинет',
            '',
            settings.EMAIL_HOST_USER,
            ['clchls.reg@gmail.com'],
        )
        with open(fileName, 'rb') as file:
            email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        os.remove(fileName)
        return redirect('cabinet_specialist')

    user = request.user

    education_instances = Education.objects.filter(user=request.user)
    context = {'form': RegistrationForm(instance=user), 'user': user, 'education_formset': EducationFormSet(), 'form_edu': education_instances} # EducationFormSet(initial=initial_data)
    return render(request, 'diagnostics/cabinet_specialist.html', context)

@login_required(login_url='/login/')
def cabinet_clinic(request):
    if request.method == 'POST':
        email = request.user.email
        clinic_name = request.POST['last_name_or_clinic_name']
        clinic_address = request.POST['first_name_or_clinic_address']
        clinic_hours = request.POST['patronymic_or_clinic_hours']
        languages = request.POST.getlist('languages')
        other_language = request.POST['other_language']
        whatsapp = request.POST['whatsapp']
        telegram = request.POST['telegram']
        phone = request.POST['phone']
        country = request.POST['country']
        locality = request.POST['city_or_locality']
        symptom_analysis = request.POST['computer_analysis']
        home_call = request.POST['academic_degree_or_home_call']
        form = RegistrationForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        if phone:
            phone = int(phone)
        f_oDLK = []
        f_oDLK.append(['IdProfile', request.user.id])
        f_oDLK.append(['Email', email])
        f_oDLK.append(['Название клиники', clinic_name])
        f_oDLK.append(['Адрес клиники', clinic_address])
        f_oDLK.append(['Время работы клиники', clinic_hours])
        f_oDLK.append([['Укажите языки, на которых могут быть предоставлены услуги', languages], ['добавить язык, отсутствующий в списке', other_language]])
        f_oDLK.append(['WhatsApp', int(whatsapp)])
        f_oDLK.append(['Telegram', telegram])
        f_oDLK.append(['Телефон', phone])
        f_oDLK.append(['Страна', country])
        f_oDLK.append(['Город, населенный пункт', locality])
        f_oDLK.append(['Компьютерный анализ симптомов пациента', symptom_analysis])
        f_oDLK.append(['Валюта при указании стоимости услуг', request.POST['currency']])
        f_oDLK.append(['Вызов на дом', home_call])
        print(f_oDLK)
        fileName = send_oDLK(f_oDLK)
        email = EmailMessage(
            'Личный кабинет',
            '',
            settings.EMAIL_HOST_USER,
            ['clchls.reg@gmail.com'],
        )
        with open(fileName, 'rb') as file:
            email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        os.remove(fileName)

        return redirect('cabinet_clinic')

    user = request.user
    context = {'form': RegistrationForm(instance=user)}
    return render(request, 'diagnostics/cabinet_clinic.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

def services(request):
    if request.method == 'POST':
        data = request.POST
        form = ServiceForm(request.POST)
        if data['serviceType'] == 'консультация':
            type = ['Вид услуги', data['consultationType']]
        else:
            type = ['Вид услуги', data['serviceType'], data['procedureName']]
        
        if data['serviceCategory'] == 'медицинская услуга':
            if data['certificateStart']:
                sp = data['certificateStart'].split('-')
                startTime = f'{sp[2]}.{sp[1]}.{sp[0]}'
            else:
                startTime = ''

            if data['certificateEnd']:
                sp = data['certificateEnd'].split('-')
                endTime = f'{sp[2]}.{sp[1]}.{sp[0]}'
            else:
                endTime = ''
            
            category = ['Тип услуги', data['medicalType'], data['doctorSpecialty'], startTime, endTime, data.get('category', '')]
        else:
            category = ['Тип услуги', data['serviceCategory'], data['nonMedicalSpecialty']]
        new_service = Service()
        new_service.created_by = request.user
        new_service.email = request.user.email
        new_service.service_type = type
        new_service.service_category = category
        new_service.age_from = data.get('ageFrom', '')
        new_service.age_to = data.get('ageTo', '')
        new_service.experience = data['experience']
        new_service.cost = data['cost']
        new_service.online_payment = data['onlinePayment']
        new_service.keywords = data['keywords']
        new_service.clinic_name_or_service_email = data['clinicName']
        new_service.service_address = data['clinicAddress']
        new_service.appointment_time = data['appointmentTime']
        new_service.home_service = data['homeService']
        new_service.additional_info = data['additionalInfo']
        new_service.save()
        # services = Service.objects.filter(created_by=request.user)
        f_servLK = []
        if new_service.age_from:
            age_from = int(new_service.age_from)
        else:
            age_from = ''
        if new_service.age_to:
            age_to = int(new_service.age_to)
        else:
            age_to = ''
        f_servLK.append(['Id', new_service.id])
        f_servLK.append(['IdProfile', request.user.id])
        f_servLK.append(new_service.service_type)
        f_servLK.append(new_service.service_category)
        f_servLK.append(['Возможность оказать данную услугу на дому', new_service.home_service])
        f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
        f_servLK.append(['Стаж по предлагаемой услуге, лет', int(new_service.experience)])
        f_servLK.append(['Стоимость', int(new_service.cost)])
        f_servLK.append(['Возможность пациента оплатить услугу через сайт', new_service.online_payment])
        f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', new_service.keywords])
        f_servLK.append(['Название клиники, где оказывается услуга', new_service.clinic_name_or_service_email])
        f_servLK.append(['Адрес, где оказывается услуга', new_service.service_address])
        f_servLK.append(['Время приема', new_service.appointment_time])
        f_servLK.append(['Дополнительная информация о предлагаемой услуге', new_service.additional_info])

        print(f_servLK)
        fileName = send_servLK(f_servLK)
        email = EmailMessage(
            'Услуги',
            '',
            settings.EMAIL_HOST_USER,
            ['clchls.reg@gmail.com'],
        )
        with open(fileName, 'rb') as file:
            email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        os.remove(fileName)

        return redirect('services')
    form = ServiceForm()
    services = Service.objects.filter(email = request.user.email)

    return render(request, 'diagnostics/services.html', {'form': form, 'services': services})

def services_clinic(request):
    if request.method == 'POST':
        data = request.POST
        form = ServiceForm(request.POST)
        if data['serviceType'] == 'консультация':
            type = ['Вид услуги', data['consultationType']]
        else:
            type = ['Вид услуги', data['serviceType'], data['procedureName']]
        
        if data['serviceCategory'] == 'медицинская услуга':
            if data['certificateStart']:
                sp = data['certificateStart'].split('-')
                startTime = f'{sp[2]}.{sp[1]}.{sp[0]}'
            else:
                startTime = ''

            if data['certificateEnd']:
                sp = data['certificateEnd'].split('-')
                endTime = f'{sp[2]}.{sp[1]}.{sp[0]}'
            else:
                endTime = ''
            
            if data.get('personalization') == 'персонализированная услуга (указываются данные специалиста)':
                category = ['Тип услуги', data['medicalType'], data['doctorSpecialty'], startTime, endTime, data.get('category', '')]
            else:
                category = ['Тип услуги', data['medicalType'], data['doctorSpecialty']]
        else:
            category = ['Тип услуги', data['serviceCategory'], data['nonMedicalSpecialty']]
        new_service = Service()
        new_service.persServ = data.get('personalization')
        if new_service.persServ == 'персонализированная услуга (указываются данные специалиста)':
            new_service.last_name_or_languages = data.get('last_name')
            new_service.first_name_or_additional_language = data.get('first_name')
            new_service.middle_name = data.get('patronymic')
        else:
            new_service.last_name_or_languages = data.getlist('languages')
            new_service.first_name_or_additional_language = data['other_language']
        new_service.gender = data.get('gender')
        if data.get('date_of_birth') == '':
            new_service.birth_date = None
        else:
            new_service.birth_date = data.get('date_of_birth')
        if data['email']:
            new_service.emailS = data['email']
        new_service.email = request.user.email
        new_service.service_type = type
        new_service.service_category = category

        new_service.age_from = data['ageFrom']
        new_service.age_to = data['ageTo']
        if data['experience'] == '':
            new_service.experience = None
        else:
            new_service.experience = data['experience']
        new_service.cost = data['cost']
        new_service.online_payment = data['onlinePayment']
        new_service.keywords = data['keywords']
        new_service.appointment_time = data['appointmentTime']
        new_service.home_service = data.get('homeService', '')
        new_service.additional_info = data['additionalInfo']
        new_service.service_address = request.user.first_name_or_clinic_address
        new_service.created_by = request.user
        new_service.save()
        # services = Service.objects.filter(created_by=request.user)
        f_servLK = []
        if new_service.emailS:
            email = new_service.emailS
        else:
            email = new_service.email

        if new_service.age_from:
            age_from = int(new_service.age_from)
        else:
            age_from = ''
        if new_service.age_to:
            age_to = int(new_service.age_to)
        else:
            age_to = ''
        if new_service.persServ == 'персонализированная услуга (указываются данные специалиста)':
            birthdate = datetime.strptime(new_service.birth_date, '%Y-%m-%d')
            birthdate = birthdate.strftime('%d.%m.%Y')
            
            f_servLK.append(['Id', new_service.id])
            f_servLK.append(['IdProfile', request.user.id])
            f_servLK.append(['Персонализированность услуги', new_service.persServ])
            f_servLK.append(['Фамилия', new_service.last_name_or_languages])
            f_servLK.append(['Имя', new_service.first_name_or_additional_language])
            f_servLK.append(['Отчество', new_service.middle_name])
            f_servLK.append(['Пол', new_service.gender])
            f_servLK.append(['Дата рождения', birthdate])
            f_servLK.append(new_service.service_type)
            f_servLK.append(new_service.service_category)
            f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
            f_servLK.append(['Стаж по предлагаемой услуге, лет', int(new_service.experience)])
            f_servLK.append(['Стоимость', int(new_service.cost)])
            f_servLK.append(['Возможность пациента оплатить услугу через сайт', new_service.online_payment])
            f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', new_service.keywords])
            f_servLK.append(['Email услуги', email])
            f_servLK.append(['Время приема', new_service.appointment_time])
            f_servLK.append(['Возможность оказать данную услугу на дому', new_service.home_service])
            f_servLK.append(['Дополнительная информация о предлагаемой услуге', new_service.additional_info])      
        else:
            f_servLK.append(['Id', new_service.id])
            f_servLK.append(['IdProfile', request.user.id])
            f_servLK.append(['Персонализированность услуги', new_service.persServ])
            f_servLK.append(new_service.service_type)
            f_servLK.append(new_service.service_category)
            f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
            f_servLK.append(['Стоимость', int(new_service.cost)])
            f_servLK.append(['Возможность пациента оплатить услугу через сайт', new_service.online_payment])
            f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', new_service.keywords])
            f_servLK.append(['Email услуги', email])
            f_servLK.append([['Укажите языки, на которых может быть предоставлена данная услуга',
                                new_service.last_name_or_languages],
                                ['добавить язык, отсутствующий в списке', new_service.first_name_or_additional_language]])
            f_servLK.append(['Время приема', new_service.appointment_time])
            f_servLK.append(['Возможность оказать данную услугу на дому', new_service.home_service])
            f_servLK.append(['Дополнительная информация о предлагаемой услуге', new_service.additional_info])       
        print(f_servLK)
        fileName = send_servLK(f_servLK)
        email = EmailMessage(
            'Услуги',
            '',
            settings.EMAIL_HOST_USER,
            ['clchls.reg@gmail.com'],
        )
        with open(fileName, 'rb') as file:
            email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        os.remove(fileName)

        return redirect('services_clinic')
    form = ServiceForm()
    user = request.user
    services = Service.objects.filter(created_by=request.user)
    return render(request, 'diagnostics/services_clinic.html', {'form': form, 'user': user, 'services': services})


def get_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    data = {
        'service_type': service.service_type,
        'service_category': service.service_category,
        'home_service': service.home_service,
        'age_from': service.age_from,
        'age_to': service.age_to,
        'experience': service.experience,
        'cost': service.cost,
        'online_payment': service.online_payment,
        'clinic_name_or_service_email': service.clinic_name_or_service_email,
        'service_address': service.service_address,
        'appointment_time': service.appointment_time,
        'keywords': service.keywords,
        'additional_info': service.additional_info
    }
    return JsonResponse(data)

def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    f_servLK = []
    if request.user.type == 'Специалист':
        
        if service.age_from:
            age_from = int(service.age_from)
        else:
            age_from = ''
        if service.age_to:
            age_to = int(service.age_to)
        else:
            age_to = ''
        f_servLK.append(['Id', service.id])
        f_servLK.append(['IdProfile', request.user.id])
        f_servLK.append(service.service_type)
        f_servLK.append(service.service_category)
        f_servLK.append(['Возможность оказать данную услугу на дому', service.home_service])
        f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
        f_servLK.append(['Стаж по предлагаемой услуге, лет', int(service.experience)])
        f_servLK.append(['Стоимость', int(service.cost)])
        f_servLK.append(['Возможность пациента оплатить услугу через сайт', service.online_payment])
        f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', service.keywords])
        f_servLK.append(['Название клиники, где оказывается услуга', service.clinic_name_or_service_email])
        f_servLK.append(['Адрес, где оказывается услуга', service.service_address])
        f_servLK.append(['Время приема', service.appointment_time])
        f_servLK.append(['Дополнительная информация о предлагаемой услуге', service.additional_info])
        f_servLK.append('servDel')
    else:
        if service.emailS:
            email = service.emailS
        else:
            email = service.email

        if service.age_from:
            age_from = int(service.age_from)
        else:
            age_from = ''
        if service.age_to:
            age_to = int(service.age_to)
        else:
            age_to = ''
        if service.persServ == 'персонализированная услуга (указываются данные специалиста)':
            # birthdate = datetime.strptime(, '%Y-%m-%d')
            birthdate = service.birth_date.strftime('%d.%m.%Y')
            
            f_servLK.append(['Id', service.id])
            f_servLK.append(['IdProfile', request.user.id])
            f_servLK.append(['Персонализированность услуги', service.persServ])
            f_servLK.append(['Фамилия', service.last_name_or_languages])
            f_servLK.append(['Имя', service.first_name_or_additional_language])
            f_servLK.append(['Отчество', service.middle_name])
            f_servLK.append(['Пол', service.gender])
            f_servLK.append(['Дата рождения', birthdate])
            f_servLK.append(service.service_type)
            f_servLK.append(service.service_category)
            f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
            f_servLK.append(['Стаж по предлагаемой услуге, лет', int(service.experience)])
            f_servLK.append(['Стоимость', int(service.cost)])
            f_servLK.append(['Возможность пациента оплатить услугу через сайт', service.online_payment])
            f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', service.keywords])
            f_servLK.append(['Email услуги', email])
            f_servLK.append(['Время приема', service.appointment_time])
            f_servLK.append(['Возможность оказать данную услугу на дому', service.home_service])
            f_servLK.append(['Дополнительная информация о предлагаемой услуге', service.additional_info])
            f_servLK.append('servDel')    
        else:
            f_servLK.append(['Id', service.id])
            f_servLK.append(['IdProfile', request.user.id])
            f_servLK.append(['Персонализированность услуги', service.persServ])
            f_servLK.append(service.service_type)
            f_servLK.append(service.service_category)
            f_servLK.append(['Возраст пациентов, лет', age_from, age_to])
            f_servLK.append(['Стоимость', int(service.cost)])
            f_servLK.append(['Возможность пациента оплатить услугу через сайт', service.online_payment])
            f_servLK.append(['Ключевые поисковые слова предлагаемой услуги', service.keywords])
            f_servLK.append(['Email услуги', email])
            f_servLK.append([['Укажите языки, на которых может быть предоставлена данная услуга',
                                ast.literal_eval(service.last_name_or_languages)],
                                ['добавить язык, отсутствующий в списке', service.first_name_or_additional_language]])
            f_servLK.append(['Время приема', service.appointment_time])
            f_servLK.append(['Возможность оказать данную услугу на дому', service.home_service])
            f_servLK.append(['Дополнительная информация о предлагаемой услуге', service.additional_info])
            f_servLK.append('servDel')
    print(f_servLK)
    fileName = send_servDel(f_servLK)
    email = EmailMessage(
        'Удаление услуги',
        '',
        settings.EMAIL_HOST_USER,
        ['clchls.reg@gmail.com'],
    )
    with open(fileName, 'rb') as file:
        email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    email.send()
    os.remove(fileName)
    service.delete()
    previous_url = request.META.get('HTTP_REFERER', reverse('login'))
    return HttpResponseRedirect(previous_url)

def specialists_education(request):
    if request.method == 'POST':
        l = []
        email = request.user.email
        surname = request.POST['last_name_or_clinic_name']
        name = request.POST['first_name_or_clinic_address']
        patronymic = request.POST['patronymic_or_clinic_hours']
        gender = request.POST['gender']
        birthdate = request.POST['date_of_birth']
        languages = request.POST.getlist('languages')
        other_language = request.POST['other_language']
        degree = request.POST['academic_degree_or_home_call']
        education_formset = EducationFormSet(request.POST)

        new_user = User()
        new_user.clinic_name = request.user.last_name_or_clinic_name
        new_user.last_name_or_clinic_name = surname
        new_user.first_name_or_clinic_address = name
        new_user.patronymic_or_clinic_hours = patronymic
        new_user.gender = gender
        new_user.date_of_birth = birthdate
        new_user.languages = languages
        new_user.other_language = other_language
        new_user.academic_degree_or_home_call = degree
        new_user.save()
        if education_formset.is_valid():
            for form in education_formset:
                if form.cleaned_data:

                    # start_date = form.cleaned_data.get('start_date')
                    # end_date = form.cleaned_data.get('end_date')
                    # specialty = form.cleaned_data.get('specialty')
                    # institution = form.cleaned_data.get('institution')

                    # if form.cleaned_data.get('DELETE'):
                    #     Education.objects.filter(user=request.user, start_date=start_date, end_date=end_date, specialty=specialty, institution=institution).delete()
                    # else:
                    education_instance = form.save(commit=False)
                    education_instance.user = new_user
                    education_instance.save()
                        
        f_oDSpClLK = []
        l = []
        education = Education.objects.filter(user=new_user)
        for e in education:
            l.append([['Начало', e.start_date.strftime('%d.%m.%Y')], ['Окончание', e.end_date.strftime('%d.%m.%Y')], ['Квалификация, специальность, тема', e.specialty], ['Учебное заведение', e.institution]])
        if len(l) == 0:
            l = [
                [
                ['Начало', ''],
                ['Окончание', ''],
                ['Квалификация, специальность, тема', ''],
                ['Учебное заведение', '']
                ]
            ]
        birthdate = datetime.strptime(new_user.date_of_birth, '%Y-%m-%d')
        birthdate = birthdate.strftime('%d.%m.%Y')
        f_oDSpClLK.append(['Id', new_user.id])
        f_oDSpClLK.append(['IdProfile', request.user.id])
        f_oDSpClLK.append(['Фамилия', new_user.last_name_or_clinic_name])
        f_oDSpClLK.append(['Имя', new_user.first_name_or_clinic_address])
        f_oDSpClLK.append(['Отчество', new_user.patronymic_or_clinic_hours])
        f_oDSpClLK.append(['Пол', new_user.gender])
        f_oDSpClLK.append(['Дата рождения', birthdate])
        f_oDSpClLK.append([['Укажите языки, на которых могут быть предоставлены услуги специалиста',
                            new_user.languages],
                            ['добавить язык, отсутствующий в списке', new_user.other_language]])
        f_oDSpClLK.append(l)
        f_oDSpClLK.append(['Ученая степень', new_user.academic_degree_or_home_call])
        print(f_oDSpClLK)
        fileName = send_oDSpClLK(f_oDSpClLK)
        email = EmailMessage(
            'Языки и образование специалистов',
            '',
            settings.EMAIL_HOST_USER,
            ['clchls.reg@gmail.com'],
        )
        with open(fileName, 'rb') as file:
            email.attach(fileName, file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        os.remove(fileName)

        return redirect('specialists_education')
    
    user_education = []
    print(request.user.last_name_or_clinic_name)
    if request.user.last_name_or_clinic_name != '':
        users = User.objects.filter(clinic_name=request.user.last_name_or_clinic_name)
    
        for u in users:
            education_instances = Education.objects.filter(user_id=u.pk)
            initial_data = [{'start_date': instance.start_date.strftime('%d-%m-%Y'), 'end_date': instance.end_date.strftime('%d-%m-%Y'),
                            'specialty': instance.specialty, 'institution': instance.institution}
                            for instance in education_instances]
            user_education.append({
                'specialist': u,
                'education': initial_data
            })
    print(user_education)
    context = {'form': RegistrationForm(), 'user_education': user_education, 'education_formset': EducationFormSet()}
    return render(request, 'diagnostics/specialists_education.html', context)

def delete_specialist(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    previous_url = request.META.get('HTTP_REFERER', reverse('login'))
    return HttpResponseRedirect(previous_url)

def delete_education(request, id):
    education = get_object_or_404(Education, pk=id)
    education.delete()
    previous_url = request.META.get('HTTP_REFERER', reverse('login'))
    return HttpResponseRedirect(previous_url)