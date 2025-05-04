from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import EmailMessage

import environ
env = environ.Env()
environ.Env.read_env()

import pandas as pd
import json
import io

# Create your views here.
def fileUploadIndex(request):
    return render(request, "mann_interface/index.html")

def fileUpload(request):
    if request.method == 'POST':
        myfile = request.FILES.get('myfile')
        my_df_file = pd.read_csv(myfile)
        print(my_df_file)

        request.session['mydffile_as_json'] = my_df_file.to_json()

        return HttpResponse(my_df_file.to_html())
    return HttpResponseBadRequest("this is bad request")
    
def sendMailWithSummary(request):

    if request.method == 'POST' and request.session['mydffile_as_json']:
        print("TRIGGERED")
        my_df = pd.DataFrame(json.loads(request.session['mydffile_as_json']))
        my_df['Order Date'] = pd.to_datetime(my_df['Order Date'], errors = 'coerce') #ye wo jo faulty data hai usko 'NaT' se replace kar dega
        my_df['Date'] = my_df['Order Date'].dt.date

        aggrigated_df = my_df.groupby('Date').agg({'Order Total': 'sum',
                                                   'Net Bill Value': 'sum',
                                                   'Total Container Charge': 'sum',
                                                   'Total GST': 'sum',
                                                   'GF Platform Fee': 'sum',
                                                   'GST on GF Platform Fee': 'sum',
                                                   'Total Payable to Merchant': 'sum'})
        
        recipient_mail = request.POST.get('recipient_mail')
        subject = 'Date wise summary of sales'
        message = 'please find the attached summary of sales date wise'
        file_name = 'date_wise_report.csv'

        file = io.StringIO()
        aggrigated_df.to_csv(file)
        csv_string = file.getvalue()

        mail = EmailMessage(
            subject = subject,
            body = message,
            from_email = env('SENDER_MAIL'),
            to = [recipient_mail]
        )

        mail.attach('date_wise_report.csv', csv_string, 'text/csv')
        mail.send()
        print("MIAL SENT")
        file.close()

        return HttpResponse()

    return HttpResponseBadRequest()