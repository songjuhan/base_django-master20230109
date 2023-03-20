from collections import Counter

from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

from .models import GatheringFake
import pandas as pd
import numpy as np
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,LabelBinarizer,StandardScaler,MinMaxScaler
import plotly.express as px
from sklearn.cluster import DBSCAN
import itables.options as opt

import plotly.graph_objects as go
from django.core.paginator import Paginator

from itables import show
from itables.sample_dfs import get_population


attributeid = None

missing_values = None
my_dashboard = None
filename = None
uploaded_file = None


def main(request):
    return render(request, 'main.html')

def upload(request):
    return render(request, 'upload.html')



def index(request):
    datas = GatheringFake.objects.values()
    nameList = []
    valueList = []

    all_fields = GatheringFake._meta.get_fields()
    print(all_fields)

    for fi in all_fields:
        nameList.append(str(fi).split(".")[-1])

    for j in range(len(datas)):
        valueList.append(list(datas[j].values()))
    context = {'datas': valueList, 'fields_name': nameList}
    print("")
    return render(request, template_name='index.html', context={'context': context})


def mon(request):
    global attributeid, col, product_list, b, rows20,page,describe_col, describe_list

    if request.method == "POST":
        uploaded_file = request.FILES['document']

        # print(uploaded_file)

        if uploaded_file.name.endswith('.csv'):
            # save the file in media folder
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file)  # this is the name of the file

            # know where to save file
            d = os.getcwd()  # current directory of the project
            file_directory = d + '\media\\' + name
            readfile(file_directory)

            # readfile(file_directory)
            my_file = pd.read_csv(file_directory, sep=',', engine='python')

            data = pd.DataFrame(data=my_file, index=None)
            # rows and columns
            rows = len(data.axes[0])
            columns = len(data.axes[1])
            print(rows)
            rows20 = (rows//20)+1

            print(rows20)
            list=[]
            for i in range (rows20) :
                list.append(1)
            np.array_split(my_file, rows20)
            print(np)

            # pandas 데이터 프레임을 리스트로
            col = my_file.columns.tolist()
            products_list = my_file.values.tolist()
            context2 = {'columns': col, "value": products_list}

            print("key:", col)

            # describ 데이터 프레임
            describe_col = my_file.describe().columns.tolist()
            describe_list = my_file.describe().values.tolist()

            # find missing data
            missingsings = ['?', '0', '--']
            null_data = data[data.isnull().any(axis=1)]  # find the missing data

            # print(data[i])
            missing_values = len(null_data)

            print(missing_values)

            paginator = Paginator(data, 20)
            curr_page_num = request.GET.get('page')
            if curr_page_num is None:
                curr_page_num = 1
            page = paginator.page(curr_page_num)

            # csv 데이터 보내기
            message = 'Null' + ' ' + 'data :' + str(missing_values)
            context = {'messages': message, 'cols': col, 'products_list': products_list, 'describe_cols': describe_col,
                       'describe_list': describe_list, 'list': list,'page' : page, }

            messages.success(request, '성공')




            return render(request,"mon.html",context)
        else:
            messages.warning(request, ' File was not uploaded. Please use csv file extension !')

    return render(request, 'mon.html')

    # project.csv



def attribute(request):
    context = {'cols': col, 'products_list': products_list, 'describe_cols': describe_col,
               'describe_list': describe_list, 'list': list, 'page': page, }
    return render(request, 'attribute.html', context)


def readfile(filename):
    global rows, columns, data, my_file, missing_values, col, products_list
    my_file = pd.read_csv(filename, sep=',', engine='python')

    data = pd.DataFrame(data=my_file, index=None)

    # pandas 데이터 프레임을 리스트로
    col = my_file.columns.tolist()
    products_list = my_file.values.tolist()

    # rows and columns
    rows = len(data.axes[0])
    columns = len(data.axes[1])
    print(rows)
    print(columns)
    for i in range(10):
        print(products_list[i])

    # find missing data
    missingsings = ['?', '0', '--']
    null_data = data[data.isnull().any(axis=1)]  # find the missing data

    missing_values = len(null_data)


def show(request):
    global rows, columns, data, my_file, missing_values, col, products_list

    col = my_file.columns.tolist()
    products_list = my_file.values.tolist()
    context = {'cols': col, 'products_list': products_list}

    return render(request, 'show.html', context)


def results(request):
    message = 'Null' + ' ' + 'data :' + str(missing_values)

    messages.warning(request, message)
    # split into keys and values based on the attribute input
    dashboard = []

    for x in data[attributeid]:
        dashboard.append(x)

    my_dashboard = dict(Counter(dashboard))
    # print("my dashboard",my_dashboard)

    keys = my_dashboard.keys()
    values = my_dashboard.values()

    listkeys = []
    listvalues = []

    for x in keys:
        listkeys.append(x)

    for y in values:
        listvalues.append(y)
    context = {
        'listkeys': keys,
        'listvalues': values,
    }
    return render(request, 'results.html', context)

# DESCRIBE() 메서드 + 상관관계 매서드
def describe(request):
    # describ 데이터 프레임

    describe_col = my_file.describe().columns.tolist()
    describe_list = my_file.describe().values.tolist()
    describe_col.insert(0, '')
    for i in range(len(describe_list)):
        describe_list[i].insert(0, my_file.describe().index[i])
    describe_list

    # 상관관계

    corr_matrix = my_file.corr(numeric_only=True)
    # print(corr_matrix)
    corr_matrix.index.name = "columns"
    # print(corr_matrix)
    corr_col = corr_matrix.columns.tolist()
    corr_list = corr_matrix.values.tolist()
    corr_col.insert(0, '')
    for i in range(len(corr_list)):
        corr_list[i].insert(0, corr_matrix.index[i])
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
    fff = fig.to_html()

    context = {'describe_cols': describe_col, 'describe_list': describe_list, "corr_cols": corr_col,
               "corr_list": corr_list,"fff":fff}

    return render(request, "describe.html", context)

# COLUMN 별 NULL  정보
def data_null(request):
    global col, rows, columns

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    information = "columns :" + str(columns) + "," + "rows :" + str(rows)
    # columns별 null 값 출력
    b = []
    for i in col:
        b.append(data[i].isnull().sum())
    context = {
        'b': b,
        'col': col,
        'information': information,
    }

    return render(request, "null.html", context)

# NULL 값 처림 함수
def data2(request):
    global col, my_file, data,rows, columns, information
    information = "columns :" + str(columns) + "," + "rows :" + str(rows)
    b = []
    for i in col:
        b.append(data[i].isnull().sum())
    context = {
        'b': b,
        'col': col,
        'information': information,
    }
    print(col)
    # selected=[]
    # for i in col :
    #     selected.append(i)
    # del_list = [x.split("_")[0] for x in selected if x.split("_")[-1] == "d"]
    # replace_list = [x.split("_")[0] for x in selected if x.split("_")[-1] == "r"]

    if request.method == "POST":
        selected = request.POST.getlist('selected')
        print(selected)
        del_list = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "d"]
        replace_list = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "r"]
        del_list2 = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "c"]
        print("del_list", del_list)
        print("replace_list", replace_list)
        print("del_list2", del_list2)
        if (len(replace_list) > 0):
            median = my_file[replace_list].median()
            median = median.values.tolist()
            print(median)
            print(type(median))
            for i, z in zip(replace_list, median):
                my_file[i].fillna(z, inplace=True)
        if (len(del_list) > 0):
            my_file = my_file.drop(del_list, axis=1)

        if(len(del_list2)>0):
            my_file = my_file.dropna(subset=del_list2)
            print("rows :", rows)
    print("rows :", rows)
    data = pd.DataFrame(data=my_file, index=None)
    col = list(data.columns)

    return render(request, "delete.html", context)

# 원 핫 인코딩 함수
def onehot_encoder(request):
    global domino,domino_1hot,my_file
    context = {'col': col}
    if request.method == "POST":
        selected5 = request.POST.getlist('selected5')
        print(selected5)
        for do in data.columns:
            if data[do].dtype == "object":
                r = data[do].nunique()
                domino = data[do]
                domino_encoder = LabelBinarizer()
                domino_reshaped = domino.values.reshape(-1, 1)
                domino_1hot = domino_encoder.fit_transform(domino_reshaped)
                for i in range(rows):
                    for j in range(r):
                        if domino_1hot[i][j] == 1:
                            data[do][i] = j

    return render(request,"onehot.html",context)


# 시각화  VIEW 함수
def plot(request):
    global my_file, col, products_list, rows,data
    colss = []
    if request.method == "POST":
        selected2 = request.POST.getlist('selected2')
        print(selected2)
        fig = px.histogram(data, x=selected2[0], title="logtitud by value")
        chart = fig.to_html()
        context = {"chart": chart, "col": col}
        return render(request, 'plot.html', context)

    else :
        # fig = go.Figure()
        # for cccc in data.columns:
        #     if data[cccc].dtype != "object":
        #         fig.add_trace(go.Scatter(y=data[cccc], x=data.index, mode='lines', name=cccc))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['confirmed'],
        # #                          mode='lines+markers', name='confirmed'))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['deceased'],
        # #                          mode='lines+markers', name='deceased'))
        #
        # chart = fig.to_html()
        # context = {"chart": chart, "col": col}
        context = {"col": col}
        return render(request, 'plot.html',context)
def plot2(request):
    global my_file, col, products_list, rows, data

    if request.method == "POST":
        selected3 = request.POST.getlist('selected3')
        print(selected3)
        fig = px.scatter(data, x=selected3[0], y=selected3[1],color=selected3[2])
        chart = fig.to_html()
        context = {"chart": chart, "col": col}
        return render(request, 'plot2.html', context)
    else:

        context ={"col": col}
        return render(request,'plot2.html',context)
def plot3(request):
    global my_file, col, products_list, rows, data

    if request.method == "POST":
        selected4 = request.POST.getlist('selected4')
        print(selected4)
        fig = px.box(data, y=selected4[0])
        chart = fig.to_html()
        context = {"chart": chart, "col": col}
        return render(request, 'plot3.html', context)
    else:

        context = {"col": col}
        return render(request, 'plot3.html', context)


def bar(request):
    global my_file, col, products_list, rows,data
    print(col)
    colss = []
    if request.method == "POST":
        selected2 = request.POST.getlist('selected2')
        fig = px.bar(data, x=selected2[0], title="logtitud by value")
        chart = fig.to_html()
        context = {"chart": chart, "col": col}
        return render(request, 'bar.html', context)

    else :
        # fig = go.Figure()
        # for cccc in data.columns:
        #     if data[cccc].dtype != "object":
        #         fig.add_trace(go.Scatter(y=data[cccc], x=data.index, mode='lines', name=cccc))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['confirmed'],
        # #                          mode='lines+markers', name='confirmed'))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['deceased'],
        # #                          mode='lines+markers', name='deceased'))
        #
        # chart = fig.to_html()
        # context = {"chart": chart, "col": col}
        context = {"col": col}
        return render(request, 'bar.html',context)


def pie(request):
    global my_file, col, products_list, rows,data
    print(col)
    colss = []
    if request.method == "POST":
        selected2 = request.POST.getlist('selected2')
        fig = go.pie(data, x=selected2[0], title="logtitud by value")
        chart = fig.to_html()
        context = {"chart": chart, "col": col}
        return render(request, 'pie.html', context)

    else :
        # fig = go.Figure()
        # for cccc in data.columns:
        #     if data[cccc].dtype != "object":
        #         fig.add_trace(go.Scatter(y=data[cccc], x=data.index, mode='lines', name=cccc))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['confirmed'],
        # #                          mode='lines+markers', name='confirmed'))
        # # fig.add_trace(go.Scatter(x=time['date'], y=time['deceased'],
        # #                          mode='lines+markers', name='deceased'))
        #
        # chart = fig.to_html()
        # context = {"chart": chart, "col": col}
        context = {"col": col}
        return render(request, 'pie.html',context)




# Normalization
def Normalization(request):
    global my_file, col, products_list, rows, data
    context ={"col": col}
    if request.method == "POST":
        selected6 = request.POST.getlist('selected6')
        print(selected6)
        MinMaxScaler_list = [x.split("@#$%")[0] for x in selected6 if x.split("@#$%")[-1] == "a"]
        standardScaler_list = [x.split("@#$%")[0] for x in selected6 if x.split("@#$%")[-1] == "w"]
        print("MinMaxScaler_list", MinMaxScaler_list)
        print("standardScaler_list", standardScaler_list)
        # MinMaxcaler객체 생성
        if (len(MinMaxScaler_list) > 0):
            for i in MinMaxScaler_list:
                min_scaler = MinMaxScaler()
                minmax_data = min_scaler.fit_transform(my_file[[i]])
                print(minmax_data)
                my_file[i] = minmax_data

                print(my_file)

        if(len(standardScaler_list)>0):
            for j in standardScaler_list:
                std_scaler = StandardScaler()
                std_data = std_scaler.fit_transform(my_file[[j]])
                print(std_data)
                my_file[i] = std_data
                print(my_file)
    return render(request, "standardScaler.html",context)



def outlier_iqr(data, column,num=0.25):
    # lower, upper 글로벌 변수 선언하기
    global lower, upper

    # 4분위수 기준 지정하기
    q25, q75 = np.quantile(data[column], num), np.quantile(data[column], 1-num)

    # IQR 계산하기
    iqr = q75 - q25

    # outlier cutoff 계산하기
    cut_off = iqr * 1.5

    # lower와 upper bound 값 구하기
    lower, upper = q25 - cut_off, q75 + cut_off

    print('IQR은', iqr, '이다.')
    print('lower bound 값은', lower, '이다.')
    print('upper bound 값은', upper, '이다.')

    # 1사 분위와 4사 분위에 속해있는 데이터 각각 저장하기
    data1 = data[data[column] > upper]
    print(data1)
    data2 = data[data[column] < lower]
    print(data2)
    sum3 = pd.concat([data1, data2])
    print(sum3)
    print("data1 :", data1)
    print("data2 :", data2)
    sum2 = data1.shape[0] + data2.shape[0]
    print("sum2 :", sum2)
    # 이상치 총 개수 구하기
    print('총 이상치 개수는', data1.shape[0] + data2.shape[0], '이다.')
    return sum3,sum2,lower,upper

def outlier(request):
    global my_file, col, products_list, rows, data
    print('='* 100)
    print(my_file)
    if request.method == "POST":
        selected7 = request.POST.get('selected7')
        print("selected7 :", selected7)
        print(type(selected7))
        sum3,sum2, lower, upper = outlier_iqr(my_file, selected7)


        mean = data[selected7].mean()
        std = data[selected7].std()
        print("mean :", mean)
        print("std :", std)
        fig = px.box(data, x=selected7, title=str(selected7)+" "+"outlier")

        fig.add_vrect(x0=lower, x1=data[selected7].min(), line_color="green", fillcolor="red", opacity=0.2)
        print(data[selected7].min())
        fig.add_vrect(x0=upper, x1=data[selected7].max(), line_color="green", fillcolor="red", opacity=0.2)
        print(data[selected7].max())
        print(3333)
        print("sum2 :", sum2)
        chart = fig.to_html()


        context = {"chart": chart, "col": col, "sum2": sum2}
        return render(request, "outlier.html", context)

    else:
        context = {"col": col}
        return render(request, 'outlier.html', context)

def outlier_results(request):
    global col, my_file, data, rows, columns
    context = {"col": col}
    if request.method == "POST":
        selected8 = request.POST.get('selected8')
        sum3, _, _, _ = outlier_iqr(my_file, selected8)
        print("selected8 :", selected8)
        print("len(selected8) :", len(selected8))
        print("rows :", rows)
        index2 = sum3.index
        print(index2)
        my_file = my_file.drop(index2)
        print(my_file.index)
        print("rows :", rows)



        print("rows :",rows)
    return render(request, "outlier_results.html", context)



def dbscan(request):
    global col, my_file, data, rows, columns

    if request.method == "POST":
        print(2123)
        selected9 = request.POST.getlist('selected9')
        print(2123)
        print(selected9)
        print(213)
        X= my_file[selected9].values
        print(X)
        dbscan = DBSCAN(eps=2.5, min_samples=13).fit(X)
        labels = dbscan.labels_
        pd.Series(labels).value_counts()
        my_file["labels"]=labels
        print(my_file)
        unique_labels = set(labels)
        for label in(unique_labels):
            sample_mask = [True if l == label else False for l in labels]
            fig = px.scatter(my_file, x=X[:, 0], y=X[:, 1], color="labels")
            chart = fig.to_html()
            context = {"col": col,"chart": chart}
        return render(request, 'dbsacn.html', context)


    else:
        context = {"col": col}
        return render(request, 'dbsacn.html', context)

def sub1(request):
        return render(request, 'sub1.html')


def sub2(request):
    return render(request, 'sub2.html')

def sub3(request):
    return render(request, 'sub3.html')
def sub4(request):
    return render(request, 'sub4.html')
def sub5(request):
    return render(request, 'sub5.html')
def sub6(request):
    return render(request, 'sub6.html')

def info(request):
    global col, rows, columns

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    information = "columns :" + str(columns) + "," + "rows :" + str(rows)
    # columns별 null 값 출력
    b = []
    for i in col:
        b.append(data[i].isnull().sum())
    describe_col = my_file.describe().columns.tolist()
    describe_list = my_file.describe().values.tolist()
    describe_col.insert(0, '')
    for i in range(len(describe_list)):
        describe_list[i].insert(0, my_file.describe().index[i])
    describe_list

    # 상관관계

    corr_matrix = my_file.corr(numeric_only=True)
    # print(corr_matrix)
    corr_matrix.index.name = "columns"
    # print(corr_matrix)
    corr_col = corr_matrix.columns.tolist()
    corr_list = corr_matrix.values.tolist()
    corr_col.insert(0, '')
    for i in range(len(corr_list)):
        corr_list[i].insert(0, corr_matrix.index[i])
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
    fff = fig.to_html()

    type1 =my_file.dtypes.values.tolist()
    print(type1)
    type_c = ["int64", "float64", "bool", "object"]

    if request.method == "POST":
        choice = request.POST.getlist('choice')
        print(choice)
        choice2 = request.POST.getlist('choice2')
        print(choice2)

        # 컬럼과 데이터 타입 변경하기
        for colss, dtype in zip(choice, choice2):
            print(col)
            print(dtype)
            my_file[colss] = my_file[colss].astype(dtype)

    context = {'col': col, 'products_list': products_list, 'describe_cols': describe_col,
               'describe_list': describe_list, 'list': list, 'page': page, 'information' : information,'describe_list': describe_list, "corr_cols": corr_col,
               "corr_list": corr_list,"fff":fff, "type1": type1,"type_c":type_c,'b': b}

    return render(request, 'info.html', context)


def attribute2(request):
    global col, my_file, data,rows, columns, information
    information = "columns :" + str(columns) + "," + "rows :" + str(rows)
    b = []
    for i in col:
        b.append(data[i].isnull().sum())
    context = {
        'b': b,
        'col': col,
        'information': information,
    }
    print(col)
    # selected=[]
    # for i in col :
    #     selected.append(i)
    # del_list = [x.split("_")[0] for x in selected if x.split("_")[-1] == "d"]
    # replace_list = [x.split("_")[0] for x in selected if x.split("_")[-1] == "r"]

    if request.method == "POST":
        selected = request.POST.getlist('selected')
        print(selected)
        del_list = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "d"]
        replace_list = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "r"]
        del_list2 = [x.split("@#$%")[0] for x in selected if x.split("@#$%")[-1] == "c"]
        print("del_list", del_list)
        print("replace_list", replace_list)
        print("del_list2", del_list2)
        if (len(replace_list) > 0):
            median = my_file[replace_list].median()
            median = median.values.tolist()
            print(median)
            print(type(median))
            for i, z in zip(replace_list, median):
                my_file[i].fillna(z, inplace=True)
        if (len(del_list) > 0):
            my_file = my_file.drop(del_list, axis=1)

        if(len(del_list2)>0):
            my_file = my_file.dropna(subset=del_list2)
            print("rows :", rows)
    print("rows :", rows)
    data = pd.DataFrame(data=my_file, index=None)
    col = list(data.columns)
    context = {'cols': col, 'products_list': products_list, 'describe_cols': describe_col,
               'describe_list': describe_list, 'list': list, 'page': page,'b': b, 'col': col,'information': information}
    return render(request, 'attribute2.html', context)



def type(request) :
    global col, my_file, data, rows, columns,type1
    type1 =my_file.dtypes.values.tolist()
    print(type1)
    context = {"col": col, "type1": type1}

    return render(request, 'type.html', context)

def type2(request):
    global col, my_file,data,rows, columns, type1
    type_c =["int64","float64","bool","object"]
    if request.method == "POST":
        choice = request.POST.getlist('choice')
        print(choice)
        choice2 = request.POST.getlist('choice2')
        print(choice2)

        # 컬럼과 데이터 타입 변경하기
        for colss, dtype in zip(choice, choice2):
            print(col)
            print(dtype)
            my_file[colss] = my_file[colss].astype(dtype)

    context= {"col": col, "type1": type1,"type_c":type_c}

    return render(request, 'type2.html', context)