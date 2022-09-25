from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
                  path('', index),
                  path('login/', login_view, name='login'),
                  path('register/', register_view, name='register'),
                  path('activate/', activate_view, name='activate'),
                  path('donate/', donate_view, name='donate'),
                  path('history/', history_view, name='history'),
                  path('receipt/<int:pk>/', receipt_view, name='receipt'),
                  path('receipt/pdf/<int:pk>/', receipt_pdf_view, name='receipt-pdf'),
                  path('transfer/', transfer_view, name='transfer'),
                  path('form_pay/', form_pay_view, name='form-pay'),
                  path('qr/', qr_reader, name='qr'),
                  path('pseudo_auth/', pseudo_auth_view, name='pseudo_auth'),
                  path('token-transfer/', token_view, name='token-tranfer'),
                  path('make_card/',make_card,name='make_card')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
