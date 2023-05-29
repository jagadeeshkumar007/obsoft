from django.db import models
from django.apps import apps
from django.contrib import admin
from dynamic_models.models import ModelSchema, FieldSchema
from django.shortcuts import render, redirect
# from .forms import AdminForm
# from django.contrib.auth.models import dynamic_models_book
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login, authenticate, logout
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
#admin.site.register(ModelSchema)
#admin.site.register(FieldSchema)
import pandas as pd
import math

print(datetime.now)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
# Create your views here.


def home(request):
    return render(request, 'obapp/home.html')


@login_required(login_url='/adminlog')
def index(request):
    city = "Tadepalligudem"+" weather"
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    
    context = {
        'loc': location, 'info': info, 'weat': weather
    }
    return render(request, 'obapp/index.html', {'con':context,'user_name': request.session['user_name']})


def adminlog(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == "POST":
        uname = request.POST['uname']
        pswd = request.POST['pswd']
        user = authenticate(request, username=uname, password=pswd)
        if user and user.is_superuser:
            auth_login(request, user)
            request.session['user_name'] = uname
            return redirect(index)
        else:
            return render(request, 'Adminlogin.html', {'error': True})
    return render(request, 'obapp/Adminlogin.html',)


def adlogout(request):
    auth_logout(request)
    return redirect(adminlog)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            print("Registration successful.")
            return redirect(adminlog)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        print("Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    placeholder = ["Username", "Email", "Designation",
                   "Date Of Joinning", "Biometric Id", "Password"]
    # placeholder = {"username":"Username", "email":"Email","Designation":"Designation","DateofJoinning":"Date Of Joinning","Biometricid":"Biometric Id","password":"Password"}
    return render(request=request, template_name="obapp/Userregister.html", context={"sample": zip(form, placeholder)})


def login_request(request):
    global us
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # us=username
                request.session['us'] = username
                messages.info(request, "You are now logged in as"+username+".")
                print("You are now logged in as"+username+".")
                return redirect(home)

            else:
                print("valid")
                messages.error(request, "Invalid username or password.")
                print("Invalid username or password.")
        else:
            print("invalid")
            messages.error(request, "Invalid username or password.")
            print("Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="obapp/Userlogin.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(login_request)

#admin.site.register(ModelSchema)
#admin.site.register(FieldSchema)
# # create a new model schema
def mid1(reg):
    l1 = ['branch','coursecode','acyear','sem']
    book_schema = ModelSchema.objects.create(name=str(reg)+'mid1')
    c=0
    for i in range(4):
        l1[i] = FieldSchema.objects.create(
        name=l1[i],
        data_type='character',
        model_schema=book_schema,
        max_length=255,
        )
    exp=['a'+str(i) for i in range(27)]
    c=0
    for i in range(1,4):
        for k in ['a','b','c']:
            for j in ['atn','atmp','per']:
                #a = 'co'+i+k+'_'+j
                exp[c] = FieldSchema.objects.create(
                name='co'+str(i)+k+'_'+j,
                data_type='integer' if j!='per' else 'float',
                model_schema=book_schema,
                max_length=255,
                )
                c+=1
    exp2=['a'+str(i) for i in range(6)]  
    c1=0       
    for i in ['co1','co2','co3']:
        for j in ['atnper','atnlvl']:
            #b = i+'_'+j 
            exp2[c1] = FieldSchema.objects.create(
                name=i+'_'+j,
                data_type='integer' if j!='atnper' else 'float',
                model_schema=book_schema,
                max_length=255,
                )
            c1+=1
            
            
    Book = book_schema.as_model()
def mid2(reg):
    l1 = ['branch','coursecode','acyear','sem']
    book_schema = ModelSchema.objects.create(name=str(reg)+'mid2')
    c=0
    for i in range(4):
        l1[i] = FieldSchema.objects.create(
        name=l1[i],
        data_type='character',
        model_schema=book_schema,
        max_length=255,
        )
    exp=['a'+str(i) for i in range(27)]
    c=0
    for i in range(3,6):
        for k in ['a','b','c']:
            for j in ['atn','atmp','per']:
                #a = 'co'+i+k+'_'+j
                exp[c] = FieldSchema.objects.create(
                name='co'+str(i)+k+'_'+j,
                data_type='integer' if j!='per' else 'float',
                model_schema=book_schema,
                max_length=255,
                )
                c+=1
    exp2=['a'+str(i) for i in range(6)]  
    c1=0       
    for i in ['co3','co4','co5']:
        for j in ['atnper','atnlvl']:
            #b = i+'_'+j 
            exp2[c1] = FieldSchema.objects.create(
                name=i+'_'+j,
                data_type='integer' if j!='atnper' else 'float',
                model_schema=book_schema,
                max_length=255,
                )
            c1+=1     
    Book = book_schema.as_model()
def mid1marks(reg):
    book_schema = ModelSchema.objects.create(name=str(reg)+'mid1_marks')
    q='co'
    alp=['a','b','c']

# # add fields to the schema
    lst=['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','a12','a13','a14','a15','a16','a17','a18','a19','a20','a21','a22','a23','a24','a25','a26','a27','a28','a28','a30']
    c=0
    rno = FieldSchema.objects.create(
                name='Roll_no',
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )
    for i in range(3):
        for j in alp:
            lst[c] = FieldSchema.objects.create(
                name=q+str(i+1)+'_'+j,
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )
            c+=1
    alpp = ['proflvl','max']
    for i in range(3):
        for k in alp:
            for j in alpp:
                lst[c] = FieldSchema.objects.create(
                    name=q+str(i+1)+'_'+k+'_'+j,
                    data_type='integer' if j=='max' else 'float',
                    model_schema=book_schema,
                    max_length=255,
                )
                c+=1
    Total = FieldSchema.objects.create(
                name='Total',
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )       
    lst1=['branch','course_code','academic_year','sem']
    lst2=['branch','course_code','academic_year','sem']
    for i in range(4):
        lst1[i] = FieldSchema.objects.create(
                name=lst2[i],
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )

    Book = book_schema.as_model()
def mid_data_insert(name):
    book_schema = ModelSchema.objects.get(name='v20mid1_marks')
    Book=book_schema.as_model()
    df1 = pd.read_excel(name)
    print(df1)
    df2 = df1.drop(['Total Marks'],axis=1)
    print(df2)
    m = list(df2.iloc[3])
    l= list(df2.iloc[2])
    print(l[2],m)
    df=pd.read_excel(name,skiprows=[0,1,2,3,4])
    df.columns=['sn','rno','q1','q2','q3','q4','q5','q6','q7','q8','q9','total']
    #df['q2']=df['q2'].replace({'NaN':-1})
    df=df.fillna(-1)
    df=df.replace('A',-2)
    branch='EEE'
    course_code='V20EET02'
    academic_year='2021-22'
    sem='IV'
    for i in df.index:

        f=Book.objects.create(roll_no=df['rno'][i],co1_a=df['q1'][i],co1_b=df['q2'][i],co1_c=df['q3'][i],co2_a=df['q4'][i],co2_b=df['q5'][i],co2_c=df['q6'][i],co3_a=df['q7'][i],co3_b=df['q8'][i],co3_c=df['q9'][i],total=df['total'][i]
                              ,branch=branch,course_code=course_code,academic_year=academic_year,sem=sem,co1_a_proflvl=l[2],co1_b_proflvl=l[3],co1_c_proflvl=l[4],co2_a_proflvl=l[5],co2_b_proflvl=l[6],co2_c_proflvl=l[7],co3_a_proflvl=l[8]
                              ,co3_b_proflvl=l[9],co3_c_proflvl=l[10],co1_a_max = m[2],co1_b_max = m[3],co1_c_max = m[4],co2_a_max = m[5],co2_b_max = m[6],co2_c_max = m[7],co3_a_max = m[8],co3_b_max = m[9],co3_c_max = m[10])
        f.save()

def cal_mid1(regname):
    book_schema = ModelSchema.objects.get(name=str(regname)+'mid1_marks')
    book = book_schema.as_model()
    Book = book.objects.all()
    attain,attem,per,attainper,attainlvl = [],[],[],[],[]
    df = pd.DataFrame(Book.values_list(),columns=Book.values()[0])
    for i in range(1,4):
        atnpr = []
        for j in ['a','b','c']:
            prflvl = df['co'+str(i)+'_'+str(j)+'_proflvl'][0]
            maxmk = df['co'+str(i)+'_'+str(j)+'_max'][0]
            df1 = df[['co'+str(i)+'_'+str(j)]]
            atn = int(df1[(df1['co'+str(i)+'_'+str(j)]>=0) & (df1['co'+str(i)+'_'+str(j)]>=maxmk*prflvl)].count(axis=0))
            atm = int(df1[df1['co'+str(i)+'_'+str(j)]>=0].count(axis=0))
            atn1 = -1 if not atn else atn 
            atm1 = -1 if not atm else atm
            attain.append(atn1)
            attem.append(atm1)
            if(atn1!=-1):
                per.append(round((atn1/atm1)*100,2))
                atnpr.append((atn1/atm1)*100)
            else:
                per.append(-1)
        attainper.append(round(sum(atnpr)/len(atnpr),3))
        if attainper[-1] > 45: #These level are taken  temporarly we should take form user
            attainlvl.append(1)
        elif attainper[-1] > 55:
            attainlvl.append(2)
        elif attainper[-1] > 65:
            attainlvl.append(3)
        else:
            attainlvl.append(0)
    print(type(attain[0]),attem,per)
    mid1_schema = ModelSchema.objects.get(name=str(regname)+'mid1')
    mid1 = mid1_schema.as_model()
    mid1.objects.create(branch=df['branch'][0],coursecode=df['course_code'][0],acyear=df['academic_year'][0],sem=df['sem'][0],
                        co1a_atn=attain[0],co1a_atmp=attem[0],co1a_per=per[0],co1b_atn=attain[1],co1b_atmp=attem[1],co1b_per=per[1],co1c_atn=attain[2],co1c_atmp=attem[2],co1c_per=per[2],
                        co2a_atn=attain[3],co2a_atmp=attem[3],co2a_per=per[3],co2b_atn=attain[4],co2b_atmp=attem[4],co2b_per=per[4],co2c_atn=attain[5],co2c_atmp=attem[5],co2c_per=per[5],
                        co3a_atn=attain[6],co3a_atmp=attem[6],co3a_per=per[6],co3b_atn=attain[7],co3b_atmp=attem[7],co3b_per=per[7],co3c_atn=attain[8],co3c_atmp=attem[8],co3c_per=per[8],
                        co1_atnper=attainper[0],co1_atnlvl=attainlvl[0],co2_atnper=attainper[1],co2_atnlvl=attainlvl[1],co3_atnper=attainper[2],co3_atnlvl=attainlvl[2])

def cal_mid2(regname):
    book_schema = ModelSchema.objects.get(name=str(regname)+'mid2_marks')
    book = book_schema.as_model()
    Book = book.objects.all()
    attain,attem,per,attainper,attainlvl = [],[],[],[],[]
    df = pd.DataFrame(Book.values_list(),columns=Book.values()[0])
    for i in range(3,6):
        atnpr = []
        for j in ['a','b','c']:
            prflvl = df['co'+str(i)+'_'+str(j)+'_proflvl'][0]
            maxmk = df['co'+str(i)+'_'+str(j)+'_max'][0]
            df1 = df[['co'+str(i)+'_'+str(j)]]
            atn = int(df1[(df1['co'+str(i)+'_'+str(j)]>=0) & (df1['co'+str(i)+'_'+str(j)]>=maxmk*prflvl)].count(axis=0))
            atm = int(df1[df1['co'+str(i)+'_'+str(j)]>=0].count(axis=0))
            atn1 = -1 if not atn else atn 
            atm1 = -1 if not atm else atm
            attain.append(atn1)
            attem.append(atm1)
            if(atn1!=-1):
                per.append(round((atn1/atm1)*100,2))
                atnpr.append((atn1/atm1)*100)
            else:
                per.append(-1)
        attainper.append(round(sum(atnpr)/len(atnpr),3))
        if attainper[-1] > 45: #These level are taken  temporarly we should take form user
            attainlvl.append(1)
        elif attainper[-1] > 55:
            attainlvl.append(2)
        elif attainper[-1] > 65:
            attainlvl.append(3)
        else:
            attainlvl.append(0)
    print(type(attain[0]),attem,per)
    mid1_schema = ModelSchema.objects.get(name=str(regname)+'mid2')
    mid1 = mid1_schema.as_model()
    mid1.objects.create(branch=df['branch'][0],coursecode=df['course_code'][0],acyear=df['academic_year'][0],sem=df['sem'][0],
                        co3a_atn=attain[0],co3a_atmp=attem[0],co3a_per=per[0],co3b_atn=attain[1],co3b_atmp=attem[1],co3b_per=per[1],co3c_atn=attain[2],co3c_atmp=attem[2],co3c_per=per[2],
                        co4a_atn=attain[3],co4a_atmp=attem[3],co4a_per=per[3],co4b_atn=attain[4],co4b_atmp=attem[4],co4b_per=per[4],co4c_atn=attain[5],co4c_atmp=attem[5],co4c_per=per[5],
                        co5a_atn=attain[6],co5a_atmp=attem[6],co5a_per=per[6],co5b_atn=attain[7],co5b_atmp=attem[7],co5b_per=per[7],co5c_atn=attain[8],co5c_atmp=attem[8],co5c_per=per[8],
                        co3_atnper=attainper[0],co3_atnlvl=attainlvl[0],co4_atnper=attainper[1],co4_atnlvl=attainlvl[1],co5_atnper=attainper[2],co5_atnlvl=attainlvl[2])


def course_marks(request):
    return render(request,'storeinput.html')

def storeinput(request):
    if request.method=='POST':
        nm=request.FILES['file']
        mid_data_insert(nm)
    else:
        return redirect('login')
    return render(request,'storeinput.html')
    
def sem_avg_att_per():
    book_schema=ModelSchema.objects.create(name='v20_sem_avg_att')
    attain = FieldSchema.objects.create(
                name='per_lvl',
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )
    lst=['co1','co2','co3','co4','co5']
    for i in range(5):
        lst[i] = FieldSchema.objects.create(
                name=lst[i],
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )
    
    lst1=['branch','course_code','academic_year','sem']
    lst2=['branch','course_code','academic_year','sem']
    for i in range(4):
        lst1[i] = FieldSchema.objects.create(
                name=lst2[i],
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )
    Book = book_schema.as_model()
def sem_mid1_attain1():
    book_schema=ModelSchema.objects.create(name='sem_v20cpl5')
    attain = FieldSchema.objects.create(
                name='at_atmp_per',
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )
    c=0
    lst=['a'+str(i) for i in range(15)]
    alp=['a','b','c']
    for i in range(5):
        for j in range(3):
            lst[c] = FieldSchema.objects.create(
                name='co'+str(i+1)+'q'+str(i+1)+alp[j],
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )
            c+=1
    lst1=['branch','course_code','academic_year','sem']
    lst2=['branch','course_code','academic_year','sem']
    for i in range(4):
        lst1[i] = FieldSchema.objects.create(
                name=lst2[i],
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )
    Book = book_schema.as_model()

def sem_call():
    book_schema = ModelSchema.objects.create(name='V20sem2')
    q='q'
    alp=['a','b','c']

# # add fields to the schema
    lst=['a'+str(i) for i in range(15)]
    c=0
    sno = FieldSchema.objects.create(
                name='Roll_no',
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )
    for i in range(5):
        for j in range(3):
            lst[c] = FieldSchema.objects.create(
                name=q+str(i+1)+alp[j],
                data_type='integer',
                model_schema=book_schema,
                max_length=255,
            )
            c+=1
          
    lst1=['branch','course_code','academic_year','sem']
    lst2=['branch','course_code','academic_year','sem']
    for i in range(4):
        lst1[i] = FieldSchema.objects.create(
                name=lst2[i],
                data_type='character',
                model_schema=book_schema,
                max_length=255,
            )

    Book = book_schema.as_model()
def sem_data_insert():
    
    book_schema = ModelSchema.objects.get(name='V20sem2')
    Book=book_schema.as_model()
    #f1=pd.read_excel(name)
    #df=pd.read_excel(name,skiprows=[0,1,2,3,4,5])
    # df1=pd.read_excel("C:/Users/Dell/OneDrive/Desktop/obexl1.xlsx")
    # df=df1[5:]
    
    # df.columns=['sn','rno','q1','q2','q3','q4','q5','q6','q7','q8','q9','total']
    # df1.columns=['sn','rno','q1','q2','q3','q4','q5','q6','q7','q8','q9','total']
    #df['q2']=df['q2'].replace({'NaN':-1})
    # df=df.fillna(-1)
    # df=df.replace('A',-2)
    df1=pd.read_excel("D:/obesem.xlsx")
    df=df1[5:]
    df2=df1[3:4]
    df=df.fillna(-1)
    df=df.replace('A',-2)
    df.columns=['sn','rno','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15']
    df2.columns=['sn','rno','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15']
    
    branch='CSE'
    course_code='V20qwer'
    academic_year='2021-22'
    sem='IV'
    val=[]
    lst=['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15']
    T3=ModelSchema.objects.get(name='V20cpl1')
    t3=T3.as_model()
    max_per=[]
    for i in range(5):
        obj=t3.objects.get(co='co'+str(i+1),branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
        max_per.append(obj.pl)
    
    for i in range(15):
        df[lst[i]]=pd.to_numeric(df[lst[i]])
        mxp=max_per[0] if(i<=2) else max_per[1] if(i<=5) else max_per[2] if(i<=8) else max_per[3] if(i<=11) else max_per[4]
        l=len(df[df[lst[i]]>=math.ceil((df2.at[3,lst[i]]*mxp)/100)])
        val.append(l)
    atmp=[]
    for i in range(15):
        df[lst[i]]=pd.to_numeric(df[lst[i]])
        l=len(df[df[lst[i]]>=0])
        atmp.append(l)
   
    for i in df.index:
        f=Book.objects.create(roll_no=df['sn'][i],q1a=df['q1'][i],q1b=df['q2'][i],q1c=df['q3'][i],q2a=df['q4'][i],q2b=df['q5'][i],q2c=df['q6'][i],q3a=df['q7'][i],q3b=df['q8'][i],q3c=df['q9'][i],q4a=df['q10'][i],q4b=df['q11'][i],q4c=df['q12'][i],q5a=df['q13'][i],q5b=df['q14'][i],q5c=df['q15'][i],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
        f.save()
    T1 = ModelSchema.objects.get(name='sem_v20cpl5')
    t1=T1.as_model()
    obj1=t1.objects.create(at_atmp_per='attained',co1q1a=val[0],co1q1b=val[1],co1q1c=val[2],co2q2a=val[3],co2q2b=val[4],co2q2c=val[5],co3q3a=val[6],co3q3b=val[7],co3q3c=val[8],co4q4a=val[9],co4q4b=val[10],co4q4c=val[11],co5q5a=val[12],co5q5b=val[13],co5q5c=val[14],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
    obj1.save();
    obj2=t1.objects.create(at_atmp_per='attempted',co1q1a=atmp[0],co1q1b=atmp[1],co1q1c=atmp[2],co2q2a=atmp[3],co2q2b=atmp[4],co2q2c=atmp[5],co3q3a=atmp[6],co3q3b=atmp[7],co3q3c=atmp[8],co4q4a=atmp[9],co4q4b=atmp[10],co4q4c=atmp[11],co5q5a=atmp[12],co5q5b=atmp[13],co5q5c=atmp[14],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
    obj2.save();
    per=[]
    for i in range(15):
        try:
            per.append(round(val[i]/atmp[i]*100,2))
        except ZeroDivisionError:
            per .append(0)
    obj3=t1.objects.create(at_atmp_per='percentage',co1q1a=per[0],co1q1b=per[1],co1q1c=per[2],co2q2a=per[3],co2q2b=per[4],co2q2c=per[5],co3q3a=per[6],co3q3b=per[7],co3q3c=per[8],co4q4a=per[9],co4q4b=per[10],co4q4c=per[11],co5q5a=per[12],co5q5b=per[13],co5q5c=per[14],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
    obj3.save();
    l=[[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14]]
    per2=[]
    for i in l:
        c=3 if(per[i[2]]!=0) else 2
        per2.append(round((per[i[0]]+per[i[1]]+per[i[2]])/c,2)) 
    T2 = ModelSchema.objects.get(name='sem_v20_avg_att')
    t2=T2.as_model()
    obj4=t2.objects.create(per_lvl='percentage',co1=per2[0],co2=per2[1],co3=per2[2],co4=per2[3],co5=per2[4],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
    obj4.save();
    pvl=[]
    for i in range(5):
        obj=t3.objects.get(co='co'+str(i+1),branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
        el=1 if(per2[i]>=obj.tpl1) else 2 if(per2[i]>=obj.tpl2) else 3 if(per2[i]>=obj.tpl3) else 0
        pvl.append(el)
    obj5=t2.objects.create(per_lvl='pvl',co1=pvl[0],co2=pvl[1],co3=pvl[2],co4=pvl[3],co5=pvl[4],branch=branch,course_code=course_code,academic_year=academic_year,sem=sem)
    obj5.save();
#mid1('v20')
#mid2('v20')
#mid1marks('v20')
#mid_data_insert("C:/Users/jagad/Downloads/obexl1.xlsx")
#cal_mid('v20')
# sem_avg_att_per()
# sem_mid1_attain1()
# sem_call()