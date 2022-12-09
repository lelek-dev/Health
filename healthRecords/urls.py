from django.urls import path, include

from . import views

app_name = "health"
urlpatterns = [
    path('folder', views.IndexViewFolder.as_view(), name='index'),    
    path('folder/create/<int:pk>', views.CreateViewSubFolder, name='createSub'),
    path('folder/create', views.CreateViewFolder, name='create'),
    path('folder/update/<int:pk>', views.UpdateViewFolder, name='update'),
    path('folder/delete/<int:pk>', views.DeleteViewFolder, name='delete'),

    path('record/<int:pkFolder>', views.IndexViewRecord, name='indexRecord'),
    path('record/create/<int:pkFolder>', views.CreateViewRecord, name='createRecord'),
    path('record/update/<int:pkRecord>/media/delete/<int:pkMedia>', views.DeleteViewMedia, name='deleteMedia'),
    path('record/update/<int:pkRecord>', views.UpdateViewRecord, name='updateRecord'),
    path('record/delete/<int:pkRecord>', views.DeleteViewRecord, name='deleteRecord'),

    path('record/share/<int:pkRecord>', views.ShareViewRecord, name='shareRecord'),


    path('patient/<int:pkUser>', views.IndexViewPatient, name='indexPatient'),
    path('patient/<int:pkUser>/record/<int:pkRecord>', views.IndexViewPatientRecord, name='indexPatientRecord'),  
    path('patient/<int:pkUser>/record/create', views.CreateViewPatientRecord, name='createPatientRecord'),


    # path('wishlist/share/<uuid:uuidWishlist>', views.ShareViewWishlist, name='share'),

    # path('shared', views.IndexViewShared, name='indexShare'),
    # path('shared/<int:pkWishlist>', views.DetailViewSharedWishlist, name='detailShareWishlist'),
    # path('shared/wish/<int:pkWish>', views.DetailViewSharedWish, name='detailShareWish'),
    # path('shared/wish/mark/<int:pkWish>', views.MarkViewSharedWish, name='markShareWish'),
    # path('shared/wish/removemark/<int:pkWish>', views.UnmarkViewSharedWish, name='unmarkShareWish'),
]