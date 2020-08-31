from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import *
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url='User:login')
def service(request):

    authuser = User.objects.get(username=request.user)
    # 차트
    # today-> baseDate 변수명 변경
    baseDate = datetime.date.today()
    print("=====================baseDate in service()=====================")
    print(baseDate)
    print(type(baseDate))

    todayTable = (UserTable.objects.all()).filter(
            date=baseDate, authuser_id=authuser)

    weekTable = (UserTable.objects.all()).filter(
           date__range=[baseDate + datetime.timedelta(days=-6), baseDate + datetime.timedelta(days=0)], authuser_id=authuser)

    if request.method == 'POST':
        #체크박스로 여러개 찍어온 데이터 객체들을 리스트 안에 저장
        authuser = User.objects.get(username=request.user)
        get_list = request.POST.getlist('val_id')
        context = []

        for id in get_list:
            obj = Table.objects.get(id=id)
            context.append(obj)
        #넘어온 데이터와 유저 정보를 DB에 저장
            usertable = UserTable(authuser=authuser, table=obj, name=obj, serving_wt=obj.serving_wt,
                                  kcal=obj.kcal,carbo=obj.carbo, protein=obj.protein, fat=obj.fat, company=obj.company)
            usertable.save()

        context = get_list_or_404(UserTable, authuser=authuser)
        return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable, 'baseDate':baseDate})

    else:
        baseDate = datetime.date.today()
        try :
            authuser = User.objects.get(username=request.user)
            context = get_list_or_404(UserTable, authuser=authuser)
            return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable, 'baseDate':baseDate})
        except:
            return render(request, 'service_test.html', {'todayTable': todayTable, 'weekTable': weekTable, 'baseDate':baseDate})


def search(request):
    if request.method == 'GET':
        q = request.GET.get('q', "")
    else:
        q = request.POST.get('q', "")

    tables = (Table.objects.all()).filter(name__icontains=q)

    if q:
        # tables = tables.filter(name__icontains=q)
        paginator = Paginator(tables, 10)
        page = request.GET.get('page')
        table_pages = paginator.get_page(page)
        # return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages})
        return render(request, 'search.html', {'tables': tables, 'q': q, 'table_pages': table_pages})
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
    authuser = User.objects.get(username=request.user)
    if request.method == 'POST':
        baseDate = request.POST.get('getDate','')
        print("=======baseDate=======")
        baseDate3=datetime.datetime.strptime(baseDate, "%Y-%m-%d").date()
        print(baseDate3)
        print(type(baseDate3))

        todayTable = (UserTable.objects.all()).filter(
            date=baseDate3, authuser_id=authuser)
        weekTable = (UserTable.objects.all()).filter(
           date__range=[baseDate3 + datetime.timedelta(days=-6), baseDate3 + datetime.timedelta(days=0)], authuser_id=authuser)

        context = get_list_or_404(UserTable, authuser=authuser)
        # return render(request, 'service.html',{'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable, 'baseDate': baseDate})
        return render(request, 'service_test.html', {'select_food': context, 'todayTable': todayTable, 'weekTable': weekTable, 'baseDate':baseDate})
        # return render(request, 'service_test.html', {"baseDate":baseDate})