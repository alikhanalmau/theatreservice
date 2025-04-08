from django.urls import path
from .views import (
    EventListAPIView,
    ExcursionSlotListAPIView,
    MyExcursionCancelAPIView,
    MyExcursionOrdersAPIView,
    ReviewCreateAPIView,
    ExcursionOrderAPIView,
    TicketOrderListCreateAPIView,
    UserRegisterAPIView
)

urlpatterns = [
    path('events/', EventListAPIView.as_view()),
    path('reviews/', ReviewCreateAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('tickets/', TicketOrderListCreateAPIView.as_view()),
    path('excursion-slots/', ExcursionSlotListAPIView.as_view()),
    path('excursions/', ExcursionOrderAPIView.as_view()),
    path('my-excursions/', MyExcursionOrdersAPIView.as_view()),
    path('reviews/', ReviewCreateAPIView.as_view(), name='review-list-create'),
    path('my-excursions/<int:pk>/cancel/', MyExcursionCancelAPIView.as_view(), name='cancel_excursion'),

]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
