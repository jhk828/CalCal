from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import *
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat
from dateutil.parser import parse


# Create your views here.
@login_required(login_url='User:login')
def service(request):

    authuser = AuthUser.objects.get(username=request.user)
    # 차트
    # today-> baseDate 변수명 변경
    baseDate = datetime.date.today()
    todayTable = (UserTable.objects.all()).filter(
            date=baseDate, authuser_id=authuser)

    weekTable = (UserTable.objects.all()).filter(
           date__range=[baseDate + datetime.timedelta(days=-6), baseDate + datetime.timedelta(days=0)], authuser_id=authuser)
    if request.method == 'POST':
        #체크박스로 여러개 찍어온 데이터 객체들을 리스트 안에 저장
        authuser = AuthUser.objects.get(username=request.user)
        get_list = request.POST.getlist('val_id')
        context = []
        # 두 번 이상 검색하려면 baseDate를 변환해줘야 함
        baseDate = str(baseDate)
        baseDate2 = request.POST.get('baseDate')
        print(type(baseDate2))
        for id in get_list:
            obj = Table.objects.get(id=id)
            context.append(obj)
        #넘어온 데이터와 유저 정보를 DB에 저장
            usertable = UserTable(authuser=authuser, table=obj, name=obj, serving_wt=obj.serving_wt,
                                  kcal=obj.kcal,carbo=obj.carbo, protein=obj.protein, fat=obj.fat, company=obj.company,
                                  date = baseDate2)
            usertable.save()
        context = get_list_or_404(UserTable, authuser=authuser)
        return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable, 'baseDate':baseDate})

    else:
        baseDate = datetime.date.today()
        baseDate = str(baseDate)
        try :
            authuser = AuthUser.objects.get(username=request.user)
            context = get_list_or_404(UserTable, authuser=authuser)
            return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable,
                                                         'weekTable': weekTable, 'baseDate': baseDate})
        except:
            return render(request, 'service_test.html', {'todayTable': todayTable, 'weekTable': weekTable,
                                                         'baseDate': baseDate})


def search(request):
    # baseDate = datetime.date.today()
    if request.method == 'GET':
        q = request.GET.get('q', "")
    else:
        q = request.POST.get('q', "")
        baseDate = request.POST.get('baseDate')
        print(baseDate)
        urlDate = baseDate.replace('-', '')
        urlDate = int(urlDate)
    tables = (Table.objects.all()).filter(name__icontains=q)

    if q:
        # tables = tables.filter(name__icontains=q)
        paginator = Paginator(tables, 10)
        page = request.GET.get('page')
        table_pages = paginator.get_page(page)
        # return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages})
        return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages, 'baseDate': baseDate, 'urlDate': urlDate})
    else:
        return render(request, 'search.html')


def delete(request, food_id):
    #UserTable의 id값을 이용해 해당 레코드를 DB에서 제거
    delete_record = UserTable.objects.get(id=food_id)
    delete_record.delete()
    return redirect('FoodInfo:service')

def update(request, food_id):
    food_count = request.POST.get('count')
    usertable = UserTable.objects.get(id=food_id)
    if usertable.amount == 1.0 :
        if len(food_count) == 0 :
            food_count = 1.0
        else :
            food_count = float(food_count)
        usertable = UserTable(id=food_id, authuser_id=request.user,
                              name = usertable.name,
                              table_id = usertable.table_id,
                              serving_wt=round(usertable.serving_wt * food_count,2),
                              kcal=round(usertable.kcal * food_count,2),
                              carbo=round(usertable.carbo * food_count,2),
                              protein=round(usertable.protein * food_count,2),
                              fat=round(usertable.fat * food_count,2),
                              company = usertable.company,
                              amount = food_count)
        usertable.save()
    else :
        if len(food_count) == 0 :
            food_count = 1.0
        else :
            food_count = float(food_count)

        table = Table.objects.get(id=usertable.table_id)
        usertable = UserTable(id=food_id, authuser_id=request.user,
                              name=usertable.name,
                              table_id=usertable.table_id,
                              serving_wt=round(table.serving_wt * food_count, 2),
                              kcal=round(table.kcal * food_count, 2),
                              carbo=round(table.carbo * food_count, 2),
                              protein=round(table.protein * food_count, 2),
                              fat=round(table.fat * food_count, 2),
                              company=usertable.company,
                              amount=food_count)
        usertable.save()

    return redirect('FoodInfo:service')

def getDate(request, inputDate):
    authuser = AuthUser.objects.get(username=request.user)
    if request.method == 'POST':
        baseDate = request.POST.get('getDate','')
        print("=======baseDate=======")
        #url 구하기 위해서 변환
        urlDate = baseDate.replace('-', '')
        urlDate = int(urlDate)
        baseDate3=datetime.datetime.strptime(baseDate, "%Y-%m-%d").date()
        todayTable = (UserTable.objects.all()).filter(
            date=baseDate3, authuser_id=authuser)
        weekTable = (UserTable.objects.all()).filter(
           date__range=[baseDate3 + datetime.timedelta(days=-6), baseDate3 + datetime.timedelta(days=0)], authuser_id=authuser)
        context = get_list_or_404(UserTable, authuser=authuser)
        ThatDayTable = (UserTable.objects.all()).filter(
            date=baseDate3, authuser_id=authuser)
        specificDate = str(urlDate)[:4]+'-'+str(urlDate)[4:6]+'-'+str(urlDate)[6:]
        return render(request, 'service_test1.html', {'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable,
                                                      'baseDate': baseDate, 'ThatDayTable': ThatDayTable, 'urlDate': urlDate,
                                                      'specificDate': specificDate})


def searchByDate(request, urlDate):
    # baseDate = datetime.date.today()
    if request.method == 'GET':
        q = request.GET.get('q', "")
    else:
        q = request.POST.get('q', "")
        specificDate = request.POST.get('specificDate')
    tables = (Table.objects.all()).filter(name__icontains=q)

    if q:
        # tables = tables.filter(name__icontains=q)
        paginator = Paginator(tables, 10)
        page = request.GET.get('page')
        table_pages = paginator.get_page(page)
        # return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages})
        return render(request, 'search1.html', {'tables': tables, 'q': q, 'table_pages': table_pages, 'specificDate': specificDate, 'urlDate': urlDate})
    else:
        return render(request, 'search1.html')


def serviceByDate(request, urlDate):
    authuser = AuthUser.objects.get(username=request.user)
    # 차트
    # today-> baseDate 변수명 변경
    baseDate = datetime.datetime.strptime(str(urlDate), '%Y%m%d')
    print(baseDate)
    todayTable = (UserTable.objects.all()).filter(
        date=baseDate, authuser_id=authuser)
    weekTable = (UserTable.objects.all()).filter(
        date__range=[baseDate + datetime.timedelta(days=-6), baseDate + datetime.timedelta(days=0)],
        authuser_id=authuser)

    if request.method == 'POST':
        # 체크박스로 여러개 찍어온 데이터 객체들을 리스트 안에 저장
        authuser = AuthUser.objects.get(username=request.user)
        get_list = request.POST.getlist('val_id')
        context = []
        # 두 번 이상 검색하려면 baseDate를 변환해줘야 함
        baseDate = str(baseDate)
        baseDate2 = request.POST.get('specificDate')
        print(type(baseDate2))
        for id in get_list:
            obj = Table.objects.get(id=id)
            context.append(obj)
            # 넘어온 데이터와 유저 정보를 DB에 저장
            usertable = UserTable(authuser=authuser, table=obj, name=obj, serving_wt=obj.serving_wt,
                                  kcal=obj.kcal, carbo=obj.carbo, protein=obj.protein, fat=obj.fat, company=obj.company,
                                  date=baseDate2)
            usertable.save()
        context = get_list_or_404(UserTable, authuser=authuser)
        ThatDayTable = (UserTable.objects.all()).filter(
            date=baseDate2, authuser_id=authuser)
        specificDate = str(urlDate)[:4] + '-' + str(urlDate)[4:6] + '-' + str(urlDate)[6:]

        return render(request, 'service_test1.html', {'select_food': context, 'todayTable': todayTable,
                                                     'weekTable': weekTable, 'baseDate': baseDate,
                                                     'ThatDayTable': ThatDayTable, 'urlDate': urlDate,
                                                      'specificDate': specificDate})

    else:
        baseDate = datetime.date.today()
        baseDate = str(baseDate)

        try:
            authuser = AuthUser.objects.get(username=request.user)
            context = get_list_or_404(UserTable, authuser=authuser)
            return render(request, 'service_test1.html', {'select_food': context, 'todayTable': todayTable,
                                                         'weekTable': weekTable, 'baseDate': baseDate,
                                                         'urlDate': urlDate})
        except:
            return render(request, 'service_test1.html', {'todayTable': todayTable, 'weekTable': weekTable,
                                                         'baseDate': baseDate, 'urlDate': urlDate})

def deleteByDate(request, urlDate, food_id):
    #UserTable의 id값을 이용해 해당 레코드를 DB에서 제거
    delete_record = UserTable.objects.get(id=food_id)
    delete_record.delete()
    url = '/FoodInfo/'+str(urlDate)+'/service/'
    return redirect(url)

def updateByDate(request, urlDate, food_id):
    food_count = request.POST.get('count')
    usertable = UserTable.objects.get(id=food_id)
    if usertable.amount == 1.0 :
        if len(food_count) == 0 :
            food_count = 1.0
        else :
            food_count = float(food_count)
        usertable = UserTable(id=food_id, authuser_id=request.user,
                              name = usertable.name,
                              table_id = usertable.table_id,
                              serving_wt=round(usertable.serving_wt * food_count,2),
                              kcal=round(usertable.kcal * food_count,2),
                              carbo=round(usertable.carbo * food_count,2),
                              protein=round(usertable.protein * food_count,2),
                              fat=round(usertable.fat * food_count,2),
                              company = usertable.company,
                              amount = food_count)
        usertable.save()
    else :
        if len(food_count) == 0 :
            food_count = 1.0
        else :
            food_count = float(food_count)

        table = Table.objects.get(id=usertable.table_id)
        usertable = UserTable(id=food_id, authuser_id=request.user,
                              name=usertable.name,
                              table_id=usertable.table_id,
                              serving_wt=round(table.serving_wt * food_count, 2),
                              kcal=round(table.kcal * food_count, 2),
                              carbo=round(table.carbo * food_count, 2),
                              protein=round(table.protein * food_count, 2),
                              fat=round(table.fat * food_count, 2),
                              company=usertable.company,
                              amount=food_count)
        usertable.save()

    return redirect('FoodInfo:serviceByDate')