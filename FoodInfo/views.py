from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import *
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect





# Create your views here.
@login_required(login_url='User:login')
## service page는 오늘 데이터들을 처리
def service(request):

    authuser = User.objects.get(username=request.user)
    # 차트
    # today-> baseDate 변수명 변경

    baseDate = datetime.date.today()
    todayTable = (UserTable.objects.all()).filter(
            date=baseDate, authuser_id=authuser)

    weekTable = (UserTable.objects.all()).filter(
           date__range=[baseDate + datetime.timedelta(days=-6), baseDate + datetime.timedelta(days=0)], authuser_id=authuser)

    if request.method == 'POST':
        #체크박스로 여러개 찍어온 데이터 객체들을 리스트 안에 저장
        authuser = User.objects.get(username=request.user)
        get_list = request.POST.getlist('val_id')
        context = []
        # 두 번 이상 검색하려면 baseDate를 datetime에서 str로 변환해줘야 함
        baseDate = str(baseDate)
        # baseDate2 = request.POST.get('baseDate')
        for id in get_list:
            obj = Table.objects.get(id=id)
            context.append(obj)
        #넘어온 데이터와 유저 정보를 DB에 저장
            usertable = UserTable(authuser=authuser, table=obj, name=obj, serving_wt=obj.serving_wt,
                                  kcal=obj.kcal,carbo=obj.carbo, protein=obj.protein, fat=obj.fat, company=obj.company,
                                  date = baseDate) # baseDate2 to baseDate
            usertable.save()
        context = get_list_or_404(UserTable, authuser=authuser)
        return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable,
                                                     'weekTable': weekTable, 'baseDate':baseDate})

    else:
        #오늘 값을 넘겨줘야 페이지 이동 처리가 가능
        baseDate = datetime.date.today()
        baseDate = str(baseDate)

        # UserTable에 값이 있을 때
        try :
            authuser = User.objects.get(username=request.user)
            context = get_list_or_404(UserTable, authuser=authuser)
            return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable,
                                                         'weekTable': weekTable, 'baseDate': baseDate})
        # UserTable에 값이 없을 때
        except:
            return render(request, 'service_test.html', {'todayTable': todayTable, 'weekTable': weekTable,
                                                         'baseDate': baseDate})


def search(request):
    if request.method == 'GET':
        q = request.GET.get('q', "")
    else:
        q = request.POST.get('q', "")
        # 오늘 날짜 값
        baseDate = request.POST.get('baseDate')
    tables = (Table.objects.all()).filter(name__icontains=q)

    if q:
        # tables = tables.filter(name__icontains=q)
        paginator = Paginator(tables, 10)
        page = request.GET.get('page')
        table_pages = paginator.get_page(page)
        return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages,
                                               'baseDate': baseDate})
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



def getDate(request):
    authuser = User.objects.get(username=request.user)

    if request.method == 'POST':
        getDate = request.POST.get('getDate')  ###
        get_list = request.POST.getlist('val_id')  ###

        getDate = request.POST.get('getDate')
        DateforChart = getDate

        # 그래프의 날짜 처리를 위해 형식변환
        DateforTable = datetime.datetime.strptime(getDate, "%Y-%m-%d").date()
        ThatDayTable = (UserTable.objects.all()).filter(date=DateforTable, authuser_id=authuser)
        weekTable = (UserTable.objects.all()).filter(date__range=[DateforTable + datetime.timedelta(days=-6),
                                                                  DateforTable + datetime.timedelta(days=0)],
                                                     authuser_id=authuser)

        # get_list에 값이 있으면 -> 검색해서 불러온 값이 있다는 의미
        # 따라서 여기서 불러온 값을 db 저장
        if len(get_list) >= 1 :
            context = []

            for id in get_list:
                obj = Table.objects.get(id=id)
                context.append(obj)
                # 넘어온 데이터와 유저 정보를 DB에 저장
                usertable = UserTable(authuser=authuser, table=obj, name=obj, serving_wt=obj.serving_wt,
                                      kcal=obj.kcal, carbo=obj.carbo, protein=obj.protein, fat=obj.fat,
                                      company=obj.company,
                                      date=getDate)  # baseDate2 to baseDate
                usertable.save()
            context = get_list_or_404(UserTable, authuser=authuser)
            return render(request, 'serviceByDate.html', {'weekTable': weekTable, 'ThatDayTable': ThatDayTable,
                                                          'getDate': getDate,'DateforChart': DateforChart})

        else :
            return render(request, 'serviceByDate.html', {'weekTable': weekTable,'ThatDayTable': ThatDayTable,
                                                          'getDate': getDate, 'DateforChart': DateforChart})

    else :
        next = request.POST.get('next', '/FoodInfo/service/')
        return  HttpResponseRedirect(next)

def getDateSearch(request):
    if request.method == 'GET':
        q = request.GET.get('q', "")
    else:
        q = request.POST.get('q', "")
        getDate = request.POST.get('getDate')
    tables = (Table.objects.all()).filter(name__icontains=q)

    if q:
        # tables = tables.filter(name__icontains=q)
        paginator = Paginator(tables, 10)
        page = request.GET.get('page')
        table_pages = paginator.get_page(page)
        # return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages})
        return render(request, 'searchByDate.html', {'tables': tables, 'q': q, 'table_pages': table_pages, 'getDate': getDate})
    else:
        return render(request, 'searchByDate.html')


# deleteByDate는 기존 delete처럼 redirect를 쓰면
# 해당 날짜를 받지 못하므로 이 안에서 render 처리
def deleteByDate(request, food_id):
    #UserTable의 id값을 이용해 해당 레코드를 DB에서 제거
    authuser = User.objects.get(username=request.user)
    if request.method == 'POST':
        getDate = request.POST.get('getDate')
    delete_record = UserTable.objects.get(id=food_id)
    delete_record.delete()
    DateforChart = getDate

    # 그래프의 날짜 처리를 위해 형식변환
    DateforTable = datetime.datetime.strptime(getDate, "%Y-%m-%d").date()
    ThatDayTable = (UserTable.objects.all()).filter(date=DateforTable, authuser_id=authuser)
    weekTable = (UserTable.objects.all()).filter(date__range=[DateforTable + datetime.timedelta(days=-6),
                                                              DateforTable + datetime.timedelta(days=0)],
                                                 authuser_id=authuser)

    return render(request, 'serviceByDate.html', {'weekTable': weekTable, 'ThatDayTable': ThatDayTable,
                                                  'getDate': getDate, 'DateforChart': DateforChart})


# updateByDate는 기존 update처럼 redirect를 쓰면
# 해당 날짜를 받지 못하므로 이 안에서 render 처리
def updateByDate(request, food_id):
    authuser = User.objects.get(username=request.user)

    if request.method == 'POST':
        getDate = request.POST.get('getDate')
        food_count = request.POST.get('count')
    usertable = UserTable.objects.get(id=food_id)
    if usertable.amount == 1.0:
        if len(food_count) == 0:
            food_count = 1.0
        else:
            food_count = float(food_count)
        usertable = UserTable(id=food_id, authuser_id=request.user,
                              name=usertable.name,
                              table_id=usertable.table_id,
                              serving_wt=round(usertable.serving_wt * food_count, 2),
                              kcal=round(usertable.kcal * food_count, 2),
                              carbo=round(usertable.carbo * food_count, 2),
                              protein=round(usertable.protein * food_count, 2),
                              fat=round(usertable.fat * food_count, 2),
                              company=usertable.company,
                              amount=food_count,
                              date=getDate)
        usertable.save()
    else:
        if len(food_count) == 0:
            food_count = 1.0
        else:
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
                              amount=food_count,
                              date=getDate)
        usertable.save()

    DateforChart = getDate
    # 그래프의 날짜 처리를 위해 형식변환
    DateforTable = datetime.datetime.strptime(getDate, "%Y-%m-%d").date()
    ThatDayTable = (UserTable.objects.all()).filter(date=DateforTable, authuser_id=authuser)
    weekTable = (UserTable.objects.all()).filter(date__range=[DateforTable + datetime.timedelta(days=-6),
                                                              DateforTable + datetime.timedelta(days=0)],
                                                 authuser_id=authuser)

    return render(request, 'serviceByDate.html', {'weekTable': weekTable, 'ThatDayTable': ThatDayTable,
                                                  'getDate': getDate, 'DateforChart': DateforChart})