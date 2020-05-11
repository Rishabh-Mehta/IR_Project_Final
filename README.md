# UIC Web Search Engine 

## Deployment 
The web app is deployed on heroku [https://irwebapp-heroku.herokuapp.com/] 
Use this link to view deployed search engine ,or run the code locally using the following Instructions
Source code for web app can be found at [https://github.com/rishabh2605/IR_Project_Final]


### Instructions 

#### Pre requisites 
Before you continue, ensure you have met the following requirements:

1. Django==2.2.12
2. nltk==3.4.5
3. numpy==1.18.1
4. pandas==1.0.3
5. pip==20.0.2
6. py==1.8.1
7. pyparsing==2.4.6
8. pytest==5.4.1
9. python-dateutil==2.8.1
10. scikit-learn==0.22.1
11. scipy==1.4.1

these can be installed using
 > pip install -r requirements.txt

#### Requirements
Make sure the files
1. crawler.pk1
2. data_vector.npz
3. page_rank
4. vectorizer 
are present before execution 

#### Execution 

Navigate to ..\IR_Web App\IR_Project_Final\IR_Project_Final and run the following command 

> python manage.py runserver

then open 127.0.0.1:8000 (or) the url displayed in console after running the above command 

### Usage 

Once the program is executed , a web page is displayed with a search bar.User can input a query and click search , the results will be displayed.
The page will also display a query expansion result which can be searched by clicking on it , it also shows total number of matched documents along with top 30 results.

### Additional Resources console app

The project only contains code for web app. To check the console app which also has the code for crawler , pre processing and pagerank code is available at  
[https://github.com/rishabh2605/Information_Retrival]. 
The same requirements are applicable for console app .
The execution for crawler , pre processing and pagerank will consume almost 2 hrs , hence it is recommended to have 
1. crawler.pk1
2. data_vector.npz
3. page_rank
4. vectorizer 
files before and then the application can be run in console with query as command line argument
> python query.py "Query"

[https://irwebapp-heroku.herokuapp.com/]


