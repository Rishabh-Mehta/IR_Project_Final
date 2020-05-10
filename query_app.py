import numpy as np
import pandas as pd
import re
import pickle
import scipy.sparse
import sys
import time
from nltk.corpus import stopwords
np.seterr(divide='ignore', invalid='ignore')
np.set_printoptions(threshold=sys.maxsize)
from nltk.stem import WordNetLemmatizer

#start = time.time()

#query = sys.argv[1]
lemma = WordNetLemmatizer()

def get_doc_list(q,data_vector):
    doc = []
    for i in q.nonzero()[1]:
        doc=np.append(doc,data_vector[:,i].nonzero()[0])
    return list(set(doc))

def retrive(q,flag,data,data_vector,vectorizer,page_rank):
    print("Starting Reterival...")
    start = time.time()
    Query = set(q.split())
    if flag == 0:
        q =q.lower()
        q=' '.join(lemma.lemmatize(w) for w in q.split() if not w in stopwords.words('english'))    
    q=vectorizer.transform([q])
    q_dict = {i:vectorizer.get_feature_names()[i] for i in q.nonzero()[1]} 
    print("query transformed",time.time()-start)
    doc_list = get_doc_list(q,data_vector)
    print("Found doc list",time.time()-start)
    retrival = []
    count =0
    for i in doc_list:# range(data_vector.shape[0]):
        #if(np.any(np.logical_and(q.toarray(),data_vector[i].toarray()))):
            count+=1
            match = (set(q.nonzero()[1]) & set(data_vector[i].nonzero()[1]))
            #mismatch = set(q.nonzero()[1]) - match
            term_match = list(match)
            match = set([q_dict[i] for i in list(match)])
            mismatch = Query - match
            
            cos_sim = [data_vector[i,term]*q[0,term] for term in term_match]
            sim=(np.sum(cos_sim)/ scipy.sparse.linalg.norm(data_vector[i]))
            pagerank = page_rank[data.page_url[i]]
            netscore = sim +pagerank
            retrival.append([data.page_url[i],netscore,match,mismatch,sim,pagerank,i])
    print("Retrival Complete",time.time()-start)
    if retrival == []:
        print("Query does not match any documents")
        return retrival,'',count
    else:
        retrival.sort(key=lambda x:x[1],reverse=True)
        if flag == 0:
            query_expansion = pseudo_relevance(retrival,10,q,data_vector,vectorizer)
            print("Query expansion complete",time.time()-start)
            print(time.time()-start)
            return retrival[0:30],query_expansion,count
        else :
            return retrival[0:30],count

def pseudo_relevance(result,k,q,data_vector,vectorizer):
    print("Running Pseudo Relevance...")
    result = result[:k]
    result.sort(key=lambda x:x[4],reverse=True)
    rel_index=[item[6] for item in result]
    relevant_vector=np.zeros(data_vector.shape[1])
    non_relevant_vector=(scipy.sparse.csr_matrix.sum(data_vector.T,axis=1)).T
    for i in rel_index:
        relevant_vector +=data_vector[i]
    relevant_vector = 0.75*(relevant_vector / k)
    non_relevant_vector -=relevant_vector
    non_relevant_vector = 0.15*(non_relevant_vector / (data_vector.shape[0]-k))
    q_new = q + relevant_vector + non_relevant_vector
    q_opt = (np.argsort(-q_new)).T[:5]
    print("Query Expansion")
    query_exp = query_expansion(q_opt,vectorizer)
    return query_exp
     
def query_expansion(q,vectorizer):

    query=''
    for i in list(q):
        query += ' '+vectorizer.get_feature_names()[int(i)]
    query  = query.split()
    query = list(dict.fromkeys(query))
    query = ' '.join(ch for ch in query)
    return query 

def matched_words(Result,k,vectorizer):
    for R in Result:
        match =list(R[k])
        
        for i in range(len(match)):
            match[i] = vectorizer.get_feature_names()[match[i]]
        R[k] = match
    return Result


    



