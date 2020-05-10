"""
Definition of views.
"""
import numpy as np
import pandas as pd
import pickle
import scipy.sparse
import sys
import time
from nltk.corpus import stopwords
np.seterr(divide='ignore', invalid='ignore')
np.set_printoptions(threshold=sys.maxsize)
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import QueryForm
from django.core.paginator import Paginator

import query_app 

data_vector = scipy.sparse.load_npz('data_vector.npz')
vectorizer = pickle.load(open('vectorizer','rb'))
page_rank = pickle.load(open('page_rank','rb'))
data = pd.read_pickle('crawler.pk1')
print("Files Loaded")

def home(request):

    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    page_url=[]
    match=[]
    unmatch=[]
    score=[]
    feedback=0
    new_query=''
    list_zip=''
    
    
    if 'search_q_exp' in request.GET:
            feedback =1
            print("Feedback encountered")
            start=time.time()
            user_query = request.GET['search_q_exp']
            form_in = user_query
            result,count = query_app.retrive(user_query,feedback,data,data_vector,vectorizer,page_rank)

            
    if request.method == 'POST' or feedback ==1:
        if feedback == 0:
            user_query = request.POST['search_query']
            form_in = user_query
            start=time.time()
            result,new_query,count = query_app.retrive(user_query,feedback,data,data_vector,vectorizer,page_rank)
        
           
        
        
        if( not result):
            
            #result = "No Relevant Results Found "
            print("No Relevant Results Found")
        else:
            print("Matching words..")  
            #result = query_app.matched_words(result,2,vectorizer)
            #result = query_app.matched_words(result,3,vectorizer)
            result = pd.DataFrame(result,columns=["URL","Net Score","Matched Words","Unmatched Words","Similarity","Page Rank","Doc Id"])
            page_url = result['URL']
            match =result['Matched Words']
            unmatch=result['Unmatched Words']
            score=result['Net Score']
            list_zip = list(zip(page_url,match,unmatch,score))
            #paginator = Paginator(list_zip,10)
            #page_num = request.GET.get('page')
            #page_obj = paginator.get_page(page_num)
            print(result)
            
        end =round(time.time() - start,3)
        print("Request Complete")

    
    else :
        feedback_query=''
        form_in=''
        user_query=''
        q_exp=''
        new_query=''
        result=''
        end=0
        count=0
        list_zip=''
        
    


    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'q_exp':new_query,
            'search_result':result,
            'time':end,
            'query':str(user_query),
            'result_count':count,
            'list_zip':list_zip,
            'feedback':feedback,
            'form_in':form_in,
            
            
            
            
            
            
        }

    )

