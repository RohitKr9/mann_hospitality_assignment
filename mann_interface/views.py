from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

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