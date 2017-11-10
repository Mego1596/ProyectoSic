from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^index/nuevoPeriodo/$',views.nuevoPeriodo),
    url(r'^menu/(?P<periodoId>\d+)/$', views.manejoTransaccion),
    url(r'^consulta/(?P<periodoId>\d+)/$', views.consultarTransaccion),
    url(r'^nuevaTrans/(?P<periodoId>\d+)/$', views.nuevaTransaccion),
    url(r'^transaccion/(?P<periodoId>\d+)/$',views.transacciones),
    url(r'^detalleTrans/(?P<periodoId>\d+)/(?P<transaccionId>\d+)/$',views.detallesTransaccion),
    url(r'^generador/(?P<periodoId>\d+)/$', views.generadorEstados),
    url(r'^historial/(?P<periodoId>\d+)/$', views.historialCuenta),
]