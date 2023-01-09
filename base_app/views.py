from collections import Counter

from django.shortcuts import render, redirect
from .models import GatheringFake
import pandas as pd
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
# Create your views here.
# Functions or Class Based Views for rendering html templates





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
    context = {'datas' : valueList, 'fields_name' : nameList}
    return render(request, template_name='index.html', context={'context':context})




def mon(request):

    global attributeid, col, product_list
    context={}

    if request.method == "POST":
        uploaded_file = request.FILES['document']
        attributeid = request.POST.get('attributeid')


        print(attributeid)
        #print(uploaded_file)

        if uploaded_file.name.endswith('.csv'):
            # save the file in media folder
            savefile = FileSystemStorage()

            name =savefile.save(uploaded_file.name, uploaded_file) # this is the name of the file

            # know where to save file
            d = os.getcwd() # current directory of the project
            file_directory = d+'\media\\'+name
            readfile(file_directory)

            # readfile(file_directory)
            my_file = pd.read_csv(file_directory, sep=',', engine='python')

            data = pd.DataFrame(data=my_file, index=None)

            # pandas 데이터 프레임을 리스트로
            col = my_file.columns.tolist()
            products_list = my_file.values.tolist()
            print(f'testtesttesttesttesttesttesttest{type(col)}')
            context2 = {'columns': col, "value": products_list}

            print("key:", col)
            # print("value :", products_list)

            # rows and columns
            rows = len(data.axes[0])
            columns = len(data.axes[1])
            print(rows)
            print(columns)

            # find missing data
            missingsings = ['?', '0', '--']
            null_data = data[data.isnull().any(axis=1)]  # find the missing data

            my_file = pd.read_csv(file_directory, sep=',', engine='python')

            data = pd.DataFrame(data=my_file, index=None)

            # pandas 데이터 프레임을 리스트로
            col = my_file.columns.tolist()
            products_list = my_file.values.tolist()

            print("key:", col)
            # print("value :", products_list)

            # rows and columns
            rows = len(data.axes[0])
            columns = len(data.axes[1])
            print(rows)
            print(columns)

            # find missing data
            missingsings = ['?', '0', '--']
            null_data = data[data.isnull().any(axis=1)]  # find the missing data

            missing_values = len(null_data)


            # csv 데이터 보내기
            context = {'messages':messages, 'cols':col, 'products_list':products_list}
            return render(request, 'results.html', context)
        else :
            messages.warning(request,' File was not uploaded. Please use csv file extension !')





    return render(request, 'mon.html')

          #project.csv
def readfile(filename):
    global rows, columns, data ,my_file, missing_values, col, products_list
    my_file = pd.read_csv(filename, sep=',' , engine='python')

    data = pd.DataFrame(data=my_file, index=None)

    # pandas 데이터 프레임을 리스트로
    col = my_file.columns.tolist()
    products_list = my_file.values.tolist()

    #print("value :", products_list)


    #rows and columns
    rows = len(data.axes[0])
    columns = len(data.axes[1])
    print(rows)
    print(columns)
    for i in range(10):
        print(products_list[i])

    #find missing data
    missingsings =['?', '0', '--']
    null_data = data[data.isnull().any(axis=1)] # find the missing data

    missing_values = len(null_data)






def results(request):

    message = 'I found' + str(rows) + 'rows and' + str(columns) +'columns. Missing data are: ' + str(missing_values)

    messages.warning(request, message)

    #split into keys and values based on the attribute input
    dashboard = []

    for x in data[attributeid]:
        dashboard.append(x)

    my_dashboard = dict(Counter(dashboard))
    #print("my dashboard",my_dashboard)

    keys = my_dashboard.keys()
    values =my_dashboard.values()

    listkeys= []
    listvalues =[]

    for x in keys :
        listkeys.append(x)

    for y in values:
        listvalues.append(y)

    context = {
        'listkeys' : listkeys,
        'listvalues' : listvalues
    }
    #print(listkeys)
    return render(request, 'results.html')