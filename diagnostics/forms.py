from django import forms

from diagnostics.models import Education, GeneralInfo, Service, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser

class GeneralInfoForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'мужской'),
        ('F', 'женский'),
    )

    gender = forms.CharField(widget=forms.RadioSelect(attrs={
        'class': "input-field", 'name': "gender", 'onclick':"showIsPregnancy()"
    }, choices=GENDER_CHOICES))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "input-field", 'name': "age", 'min':"1", 'oninput': "showIsPregnancy()"
    }))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': "input-field", 'name': "weight", 'min':"1"
    }))
    height = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': "input-field", 'name': "height", 'min':"1"
    }))
    pregnancy = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "input-field", 'min':"1"
    }), required=False)

    class Meta:
        model = GeneralInfo
        fields = ('gender', 'age', 'weight', 'height', 'pregnancy')


class BloodInfoForm(forms.Form):
    erythrocytes = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Эритроциты (RBC)', help_text='10^12 клеток/л, 10^6 клеток/мкл, клеток/мкл')
    hemoglobin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Гемоглобин (HGB)', help_text='г/л, г/дл')
    leukocytes = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Лейкоциты (WBC)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    platelets = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Тромбоциты (PLT)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    
    
    hematocrit = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Гематокрит (HCT)', help_text='%, л/л')
    soe = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='СОЭ (ESR)', help_text='мм/ч')
    color_indicator = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Цветовой показатель')
    mean_erytr_volume = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Средний объем эритроцита (MCV)', help_text='фл')
    # distr_erytr_size = forms.FloatField(widget=forms.NumberInput(attrs={
    #     'min': "0", 'class': "input-field", 'placeholder': "Введите результат"
    # }), required=False, label='Распределение эритроцитов по величине (RDW)', help_text='%', max_value=100)
    distr_erytr_volume_variation = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Распределение эритроцитов по объему, коэффициент вариации (RDW-CV), %', help_text='%', max_value=100)
    distr_ertyr_volume_standart_devi = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Распределение эритроцитов по объему, стандартное отклонение (RDW-SD), фл', help_text='фл')
    distr_platelets_volume = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Распределение тромбоцитов по объему (PDW)')
    mean_platelets_volume = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Средний объем тромбоцита (MPV)', help_text='фл')
    big_eryrt_coeff = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Коэффициент больших тромбоцитов (P-LCR)', help_text='%', max_value=100)
    mean_hemoglobin_in_erytr = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Среднее содержание гемоглобина в эритроците (МСН)', help_text='пг')
    mean_concentration_hemoglobin_in_eryrts = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Средняя концентрация гемоглобина в эритроците (MCHC)', help_text='г/л, г/дл')
    basophils = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Базофилы (BA, BAS)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    basophils_procent = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Базофилы (BA, BAS), %', help_text='%', max_value=100)
    eosinophils = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Эозинофилы (EO)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    eosinophils_procent = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Эозинофилы (EO), %', help_text='%', max_value=100)
    neutrophils = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Нейтрофилы (NE, NEUT)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    neutrophils_procent = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Нейтрофилы (NE, NEUT), %', help_text='%', max_value=100)
    neutrophils_stick = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Нейтрофилы палочкоядерные', help_text='%', max_value=100)
    neutrophils_segment = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Нейтрофилы сегментоядерные', help_text='%', max_value=100)
    lymphocytes = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Лимфоциты (LY, LYM)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    lymphocytes_procent = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Лимфоциты (LY, LYM), %', help_text='%', max_value=100)
    monocytes = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Моноциты (MO, MON)', help_text='10^9 клеток/л, 10^3 клеток/мкл, клеток/мкл')
    monocytes_procent = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Моноциты (MO, MON), %', help_text='%', max_value=100)
    trombocrit = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'placeholder': "Введите результат"
    }), required=False, label='Тромбокрит (PCT)', help_text='%', max_value=100)



class ChemInfoForm(forms.Form):
    protein = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "protein", 'placeholder': "Введите результат"
    }), required=False, label='Белок общий', help_text='г/л')
    billirubin_general = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "billirubin_general", 'placeholder': "Введите результат"
    }), required=False, help_text='мкмоль/л', label='Билирубин общий')
    billirubin_direct = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "billirubin_direct", 'placeholder': "Введите результат"
    }), required=False, label='Билирубин прямой', help_text='мкмоль/л')
    sugar = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "sugar", 'placeholder': "Введите результат"
    }), required=False, label='Глюкоза', help_text='ммоль/л')
    urea = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "urea", 'placeholder': "Введите результат"
    }), required=False, label='Мочевина', help_text='ммоль/л')
    amylase = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "amylase", 'placeholder': "Введите результат"
    }), required=False, label='Амилаза панкреатическая', help_text='ед/л')


    ALT = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "ALT", 'placeholder': "Введите результат"
    }), required=False, label='АлАТ (АЛТ)', help_text='ед/л')
    ALB = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "ALB", 'placeholder': "Введите результат"
    }), required=False, label='Альбумин (ALB)', help_text='г/л')
    alpha_amylase = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "alpha_amylase", 'placeholder': "Введите результат"
    }), required=False, label='Амилаза общая (альфа-амилаза, амилаза, диастаза)', help_text='ед/л')
    ACT = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "ACT", 'placeholder': "Введите результат"
    }), required=False, label='АсАТ (АСТ)', help_text='ед/л')
    beta_globulin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "beta_globulin", 'placeholder': "Введите результат"
    }), required=False, label='Бета-глобулин', help_text='г/л')
    vitamin_b12 = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "vitamin_b12", 'placeholder': "Введите результат"
    }), required=False, label='Витамин B12', help_text='пг/мл')
    gamma_globulin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "gamma_globulin", 'placeholder': "Введите результат"
    }), required=False, label='Гамма-глобулин', help_text='г/л')
    gamma_gpt = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "gamma_gpt", 'placeholder': "Введите результат"
    }), required=False, label='Гамма-ГТП (гамма-глутамилтранспептидаза, ГГТП, гамма-глутамилтрансфераза, Гамма-ГТ)', help_text='ед/л')
    hemoglobin_glik = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "hemoglobin_glik", 'placeholder': "Введите результат"
    }), required=False, label='Гликированный гемоглобин', help_text='%', max_value=100)
    homocistein = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "homocistein", 'placeholder': "Введите результат"
    }), required=False, label='Гомоцистеин', help_text='мкмоль/л')
    ferum = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "amylferumase", 'placeholder': "Введите результат"
    }), required=False, label='Железо', help_text='мкмоль/л')
    zhel_acid = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "zhel_acid", 'placeholder': "Введите результат"
    }), required=False, label='Желчные кислоты', help_text='мкмоль/л')
    calium = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "calium", 'placeholder': "Введите результат"
    }), required=False, label='Калий', help_text='ммоль/л')
    calcium_general = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "calcium_general", 'placeholder': "Введите результат"
    }), required=False, label='Кальций общий', help_text='ммоль/л')
    coeff_atereg = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "coeff_atereg", 'placeholder': "Введите результат"
    }), required=False, label='Коэффициент атерогенности (Ка)')
    kreatinin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "kreatinin", 'placeholder': "Введите результат"
    }), required=False, label='Креатинин', help_text='мкмоль/л')
    kreatinkinaza = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "kreatinkinaza", 'placeholder': "Введите результат"
    }), required=False, label='Креатинкиназа (креатинфосфокиназа, КФК)', help_text='ед/л')
    laktat = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "laktat", 'placeholder': "Введите результат"
    }), required=False, label='Лактат', help_text='ммоль/л')
    laktatdegidroginaza = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "laktatdegidroginaza", 'placeholder': "Введите результат"
    }), required=False, label='Лактатдегидрогеназа (ЛДГ)', help_text='ед/л')
    ferum_ability = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "ferum_ability", 'placeholder': "Введите результат"
    }), required=False, label='Латентная железосвязывающая способность сыворотки крови', help_text='мкмоль/л')
    lipaza = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "lipaza", 'placeholder': "Введите результат"
    }), required=False, label='Липаза', help_text='МЕ/л')
    magniy = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "magniy", 'placeholder': "Введите результат"
    }), required=False, label='Магний', help_text='ммоль/л')
    mnoglobin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "mnoglobin", 'placeholder': "Введите результат"
    }), required=False, label='Миоглобин', help_text='мкг/л, нг/мл')
    moch_acid = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "moch_acid", 'placeholder': "Введите результат"
    }), required=False, label='Мочевая кислота', help_text='мкмоль/л')
    natriy = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "natriy", 'placeholder': "Введите результат"
    }), required=False, label='Натрий', help_text='ммоль/л')
    reakt_protein = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "reakt_protein", 'placeholder': "Введите результат"
    }), required=False, label='С-реактивный белок (СРБ, C-реактивный белок)', help_text='мг/л')
    transferin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "transferin", 'placeholder': "Введите результат"
    }), required=False, label='Трансферрин', help_text='г/л')
    trigleceridy = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "trigleceridy", 'placeholder': "Введите результат"
    }), required=False, label='Триглицериды', help_text='ммоль/л')
    ferritin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "ferritin", 'placeholder': "Введите результат"
    }), required=False, label='Ферритин', help_text='мкг/л, нг/мл')
    folievay_acid = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "folievay_acid", 'placeholder': "Введите результат"
    }), required=False, label='Фолиевая кислота', help_text='нг/мл')
    phosphor = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "phosphor", 'placeholder': "Введите результат"
    }), required=False, label='Фосфор', help_text='ммоль/л')
    fruktozamin = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "fruktozamin", 'placeholder': "Введите результат"
    }), required=False, label='Фруктозамин', help_text='мкмоль/л')
    chlor = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "chlor", 'placeholder': "Введите результат"
    }), required=False, label='Хлор', help_text='ммоль/л')
    cholesterin_general = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "cholesterin_general", 'placeholder': "Введите результат"
    }), required=False, label='Холестерин общий (холестерол общий, H)', help_text='ммоль/л')
    cholesterin_lpvp = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "cholesterin_lpvp", 'placeholder': "Введите результат"
    }), required=False, label="Холестерин-ЛПВП (липопротеины высокой плотности, HDL, 'хороший холестерол', 'хороший холестерин')", help_text='ммоль/л')
    cholesterin_lpnp = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "cholesterin_lpnp", 'placeholder': "Введите результат"
    }), required=False, label="Холестерин-ЛПНП (липопротеины низкой плотности, LDL, 'плохой холестерол', 'плохой холестерин')", help_text='ммоль/л')
    choliensteraza = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "choliensteraza", 'placeholder': "Введите результат"
    }), required=False, label='Холинэстераза', help_text='ед/л')
    acid_fosfataza = forms.FloatField(widget=forms.NumberInput(attrs={
        'min': "0", 'class': "input-field-blood", 'name': "acid_fosfataza", 'placeholder': "Введите результат"
    }), required=False, label='Щелочная фосфатаза', help_text='ед/л')


# class CaptchaForm(forms.Form):
#     captcha = ReCaptchaField(
#         error_messages={
#             'required': 'Пожалуйста, заполните капчу.',  # Сообщение об ошибке, если капча не заполнена
#         }
#     )


class ExtraInfoForm(forms.Form):
    LANGUAGES_CHOICES = (
        ('Английский', 'Английский'),
        ("Арабский", "Арабский"),
        ("Испанский", "Испанский"),
        ("Итальянский", "Итальянский"),
        ('Казахский', 'Казахский'),
        ("Киргизский", "Киргизский"),
        ("Китайский", "Китайский"),
        ("Корейский", "Корейский"),
        ("Немецкий", "Немецкий"),
        ("Персидский", "Персидский"),
        ("Португальский", "Португальский"),
        ('Русский', 'Русский'),
        ("Турецкий", "Турецкий"),
        ("Французский", "Французкий"),
        ("Хинди", "Хинди"),
        ("Японский", "Японский")
    )

    input = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "text-input", 'name': "extraInfo"
    }), required=False)
    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGES_CHOICES)


class AdditionalInfoForm(forms.Form):
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "last-name", 'name': "last-name"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "first-name", 'name': "first-name"
    }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "middle-name", 'name': "middle-name"
    }), required=False)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={
        'class': "form-input", 'type': "date", 'id': "birthdate", 'name': "birthdate"
    }))
    profession = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "profession", 'name': "profession"
    }), required=False)
    iin = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-input", 'type': "number", 'min': "0", 'id': "iin", 'name': "iin"
    }), required=False)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-input", 'type': "number", 'id': "phone", 'name': "phone"
    }))


class TextInfoForm(forms.Form):
    input = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "analyzeInput", 'name': "analyzeInput"
    }), required=False)


class ContactInfoForm(forms.Form):
    whatsApp = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-input", 'type': "number", 'id': "whatsApp", 'name': "whatsApp"
    }), required=False, label="WhatsApp")
    telegram = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-input", 'type': "number", 'id': "telegram", 'name': "telegram"
    }), required=False, label="Telegram")
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-input", 'type': "number", 'id': "phone", 'name': "phone"
    }), required=False, label="Телефон")
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input", 'type': "text", 'id': "email", 'name': "email"
    }), required=True, label="Email")

class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': "Введите email", 'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Введите пароль", 'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(UserCreationForm):

    choices = (
        ('Специалист', 'Я регистрирую свои услуги как специалист'),
        ('Клиника', 'Я регистрирую услуги клиники как администратор')
    )
    type = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес эл. почты', 'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль', 'class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль', 'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'type')

class RegistrationForm(UserChangeForm):
    last_name_or_clinic_name = forms.CharField(max_length=100, required=True)
    first_name_or_clinic_address = forms.CharField(max_length=100, required=True)
    patronymic_or_clinic_hours = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=(('мужской', 'мужской'), ('женский', 'женский')), widget=forms.RadioSelect(), required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date',  'min': '1900-01-01', 'max': '2020-12-31'}))
    
    languages = forms.MultipleChoiceField(label='Укажите языки, на которых могут быть предоставлены услуги*', 
                                          widget=forms.CheckboxSelectMultiple, required=False,
                                          choices=(
                                              ('английский', 'английский'), ('арабский', 'арабский'), ('испанский', 'испанский'),
                                              ('итальянский', 'итальянский'), ('казахский', 'казахский'), ('китайский', 'китайский'),
                                              ('корейский', 'корейский'), ('монгольский', 'монгольский'), ('немецкий', 'немецкий'),
                                              ('персидский', 'персидский'), ('португальский', 'португальский'), ('русский', 'русский'),
                                              ('турецкий', 'турецкий'), ('французский', 'французский'), ('хинди', 'хинди'),
                                              ('японский', 'японский')
                                          ))
    
    other_language = forms.CharField(label='Добавить язык, отсутствующий в списке:', required=False)
    
    whatsapp = forms.CharField(label='WhatsApp*', max_length=20, required=True, widget=forms.NumberInput())
    telegram = forms.CharField(label='Telegram', max_length=100, required=False)
    phone = forms.CharField(label='Телефон', max_length=20, required=False, widget=forms.NumberInput())
    country = forms.CharField(label='Страна*', max_length=100, required=True)
    city_or_locality = forms.CharField(label='Город, населенный пункт*', max_length=100, required=True)
    
    computer_analysis = forms.ChoiceField(label='Компьютерный анализ симптомов пациента*', 
                                         choices=(
                                             ('хочу получать только симптомы пациента без их компьютерного анализа (бесплатно)', 'хочу получать только симптомы пациента без их компьютерного анализа (бесплатно)'),
                                             ('хочу получать симптомы пациента и три наиболее вероятных диагноза или состояния, выявленных искусственным интеллектом сайта (бесплатно)', 'хочу получать симптомы пациента и три наиболее вероятных диагноза или состояния, выявленных искусственным интеллектом сайта (бесплатно)'),
                                             ('хочу получать симптомы пациента и их подробный анализ искусственным интеллектом сайта, оплата через ежемесячную подписку', 'хочу получать симптомы пациента и их подробный анализ искусственным интеллектом сайта, оплата через ежемесячную подписку')
                                         ),
                                         widget=forms.RadioSelect(), required=True)
    
    academic_degree_or_home_call = forms.CharField(max_length=100, required=False)
    currency = forms.ChoiceField(
        label='Валюта при указании стоимости услуг*:',
        choices=(
            ('', ''),
            ('AMD (Армянский драм)', 'AMD (Армянский драм)'), 
            ('AZN (Азербайджанский манат)', 'AZN (Азербайджанский манат)'), 
            ('BYR (Белорусский рубль)', 'BYR (Белорусский рубль)'), 
            ('EUR (Евро)', 'EUR (Евро)'), 
            ('GEL (Лари)', 'GEL (Лари)'), 
            ('KGS (Сом)', 'KGS (Сом)'), 
            ('KZT (Тенге)', 'KZT (Тенге)'), 
            ('RUB (Российский рубль)', 'RUB (Российский рубль)'), 
            ('USD (Доллар США)', 'USD (Доллар США)')
        ),
        widget=forms.Select(attrs={'class': 'currency-select'}),
        required=True
    )
    # currency = forms.CharField(
    #     label='Валюта при указании стоимости услуг*:',
    #     max_length=100,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'currency-input'}),
    # )

    class Meta:
        model = User
        fields = ('last_name_or_clinic_name', 'first_name_or_clinic_address',
            'patronymic_or_clinic_hours', 'gender', 'date_of_birth', 'languages', 'other_language',
            'whatsapp', 'telegram', 'phone', 'country', 'city_or_locality',
            'computer_analysis', 'academic_degree_or_home_call', 'currency')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если есть экземпляр пользователя (например, при редактировании), устанавливаем значение даты рождения в формате isoformat
        if self.instance and self.instance.date_of_birth:
            self.initial['date_of_birth'] = self.instance.date_of_birth.isoformat()

        if 'type' in self.data:
            self.update_labels(self.data.get('type'))
        elif 'instance' in kwargs and kwargs['instance']:
            self.update_labels(kwargs['instance'].type)

    def update_labels(self, user_type):
        if user_type == 'Специалист':
            self.fields['last_name_or_clinic_name'].label = 'Фамилия*'
            self.fields['first_name_or_clinic_address'].label = 'Имя*'
            self.fields['patronymic_or_clinic_hours'].label = 'Отчество'
            self.fields['gender'].label = 'Пол*'
            self.fields['date_of_birth'].label = 'Дата рождения*'
            self.fields['academic_degree_or_home_call'].label = 'Ученая степень'
        elif user_type == 'Клиника':
            self.fields['last_name_or_clinic_name'].label = 'Название клиники*'
            self.fields['first_name_or_clinic_address'].label = 'Адрес клиники*'
            self.fields['patronymic_or_clinic_hours'].label = 'Время работы клиники*'
            self.fields['patronymic_or_clinic_hours'].required = True
            self.fields['gender'] = forms.ChoiceField(choices=(('male', 'мужской'), ('female', 'женский')), widget=forms.RadioSelect(), required=False)
            self.fields['date_of_birth'] = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date',  'min': '1900-01-01', 'max': '2020-12-31'}))
            self.fields['academic_degree_or_home_call'].label = 'Вызов на дом'
            self.fields['academic_degree_or_home_call'] = forms.ChoiceField(
                label='Вызов на дом*',
                required=True,
                widget=forms.RadioSelect,
                choices=(
                    ('возможен вызов на дом', 'возможен вызов на дом'),
                    ('вызов на дом не принимается', 'вызов на дом не принимается'),
                )
            )


from django.forms import formset_factory

class EducationForm(UserChangeForm):
    start_date = forms.DateField(label='Начало', required=False, widget=forms.DateInput(attrs={'type': 'date',  'min': '1900-01-01', 'max': '2124-08-26'}))
    end_date = forms.DateField(label='Окончание', required=False, widget=forms.DateInput(attrs={'type': 'date',  'min': '1900-01-01', 'max': '2124-08-26'}))
    specialty = forms.CharField(label='Квалификация, специальность, тема', max_length=200, required=False)
    institution = forms.CharField(label='Учебное заведение', max_length=200, required=False)

    class Meta:
        model = Education
        fields = ('start_date', 'end_date', 'specialty', 'institution')

EducationFormSet = formset_factory(EducationForm, extra=1, can_delete=True)


class ServiceForm(forms.Form):
    SERVICE_TYPE_CHOICES = [
        ('консультация', 'консультация'),
        ('процедура (манипуляция, операция, …)', 'процедура (манипуляция, операция, …)'),
    ]

    CONSULTATION_TYPE_CHOICES = [
        ('дистанционная консультация', 'дистанционная консультация'),
        ('консультация на очном приеме', 'консультация на очном приеме'),
        ('консультация, возможна дистанционная или на очном приеме', 'консультация, возможна дистанционная или на очном приеме'),
    ]

    SERVICE_CATEGORY_CHOICES = [
        ('медицинская услуга', 'медицинская услуга'),
        ('не медицинская услуга', 'не медицинская услуга'),
    ]

    MEDICAL_TYPE_CHOICES = [
        ('врачебная услуга', 'врачебная услуга'),
        ('не врачебная услуга', 'не врачебная услуга'),
    ]

    CATEGORY_CHOICES = [
        ('высшая категория', 'высшая категория'),
        ('первая категория', 'первая категория'),
        ('вторая категория', 'вторая категория'),
        ('без категории', 'без категории'),
    ]

    HOME_SERVICE_CHOICES = [
        ('возможен вызов на дом', 'возможен вызов на дом'),
        ('вызов на дом не принимается', 'вызов на дом не принимается'),
    ]

    ONLINE_PAYMENT_CHOICES = [
        ('не предоставлять пациенту возможность оплатить услугу через сайт', 'не предоставлять пациенту возможность оплатить услугу через сайт'),
        ('предоставить пациенту возможность оплатить услугу через сайт (взимается % от стоимости услуги за транзакционные издержки)', 'предоставить пациенту возможность оплатить услугу через сайт (взимается % от стоимости услуги за транзакционные издержки)'),
    ]

    PERSONALIZATION_CHOICES = [
        ('персонализированная услуга (указываются данные специалиста)', 'персонализированная услуга (указываются данные специалиста)'),
        ('не персонализированная услуга (не указываются данные специалиста)', 'не персонализированная услуга (не указываются данные специалиста)'),
    ]

    personalization = forms.ChoiceField(choices=PERSONALIZATION_CHOICES, widget=forms.RadioSelect(), required=True, label='Персонализированность услуги*:')

    last_name = forms.CharField(max_length=100, required=False, label='Фамилия*')
    first_name = forms.CharField(max_length=100, required=False, label='Имя*')
    patronymic = forms.CharField(max_length=100, required=False, label='Отчество')
    gender = forms.ChoiceField(choices=(('мужской', 'мужской'), ('женский', 'женский')), widget=forms.RadioSelect(), required=False, label='Пол*')
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'max': '2020-12-31'}), label='Дата рождения*')
    email = forms.CharField(widget=forms.EmailInput(), label='Email услуги', required=False)

    languages = forms.MultipleChoiceField(label='Укажите языки, на которых могут быть предоставлены услуги*', 
                                          widget=forms.CheckboxSelectMultiple(attrs={'class': 'no-bold'}), required=False,
                                          choices=(
                                              ('английский', 'английский'), ('арабский', 'арабский'), ('испанский', 'испанский'),
                                              ('итальянский', 'итальянский'), ('казахский', 'казахский'), ('китайский', 'китайский'),
                                              ('корейский', 'корейский'), ('монгольский', 'монгольский'), ('немецкий', 'немецкий'),
                                              ('персидский', 'персидский'), ('португальский', 'португальский'), ('русский', 'русский'),
                                              ('турецкий', 'турецкий'), ('французский', 'французский'), ('хинди', 'хинди'),
                                              ('японский', 'японский')
                                          ))
    
    other_language = forms.CharField(label='Добавить язык, отсутствующий в списке:', required=False)


    serviceType = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES, widget=forms.RadioSelect, label='Вид услуги*')
    consultationType = forms.ChoiceField(choices=CONSULTATION_TYPE_CHOICES, widget=forms.RadioSelect, required=False, label='')
    procedureName = forms.CharField(max_length=100, required=False, label='введите название процедуры, манипуляции, операции*')
    serviceCategory = forms.ChoiceField(choices=SERVICE_CATEGORY_CHOICES, widget=forms.RadioSelect, label='Тип услуги*')
    medicalType = forms.ChoiceField(choices=MEDICAL_TYPE_CHOICES, widget=forms.RadioSelect, required=False, label='')
    doctorSpecialty = forms.CharField(max_length=100, required=False, label='введите название специальности, специализации*')
    certificateStart = forms.DateField(required=False, label='начало', widget=forms.DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'max': '2124-08-26'}))
    certificateEnd = forms.DateField(required=False, label='окончание', widget=forms.DateInput(attrs={'type': 'date',  'min': '1900-01-01', 'max': '2124-08-26'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect, required=False, label='')
    nonMedicalSpecialty = forms.CharField(max_length=100, required=False, label='введите название специальности*')
    homeService = forms.ChoiceField(choices=HOME_SERVICE_CHOICES, widget=forms.RadioSelect, label='Возможность оказать данную услугу на дому', required=False)
    ageFrom = forms.IntegerField(required=False, label='Возраст пациентов, лет, от')
    ageTo = forms.IntegerField(required=False, label='Возраст пациентов, лет, до')
    experience = forms.IntegerField(label='Стаж по предлагаемой услуге, лет*', required=False)
    cost = forms.IntegerField(label='Стоимость*:')
    onlinePayment = forms.ChoiceField(choices=ONLINE_PAYMENT_CHOICES, widget=forms.RadioSelect, label='Возможность пациента оплатить услугу через сайт*')
    keywords = forms.CharField(max_length=100, required=False, label='Ключевые поисковые слова предлагаемой услуги')
    clinicName = forms.CharField(max_length=100, required=False, label='Название клиники, где оказывается услуга')
    clinicAddress = forms.CharField(max_length=100, required=False, label='Адрес, где оказывается услуга')
    appointmentTime = forms.CharField(max_length=100, required=False, label='Время приема')
    additionalInfo = forms.CharField(widget=forms.Textarea, required=False, label='Дополнительная информация о предлагаемой услуге')


