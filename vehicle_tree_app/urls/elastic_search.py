from django.urls import path
from vehicle_tree_app.api.v1.elasticsearch.elastic_user import LoginByUsernameView, GetAllView, SearchWithUsernameView, \
    SearchWithFirstNameView, SearchWithCityView, SearchWithLastnameView,BulkInsertView

elastic_url = [

    path('elastic/login', LoginByUsernameView.as_view(), name='LoginByUsername'),
    path('elastic/searchall', GetAllView.as_view(), name='GetAll'),
    path('elastic/searchwithlastname', SearchWithLastnameView.as_view(), name='SearchWithLastname'),
    path('elastic/searchwithfirstname', SearchWithFirstNameView.as_view(), name='SearchWithFirstName'),
    path('elastic/searchwithcity', SearchWithCityView.as_view(), name='SearchWithCity'),
    path('elastic/searchwithusername', SearchWithUsernameView.as_view(), name='SearchWithUsername'),
    path('elastic/bulkinsert', BulkInsertView.as_view(), name='BulkInsert'),

]
