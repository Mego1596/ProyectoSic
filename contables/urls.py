from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^periodoConta/$', views.periodoConta),
    url(r'^periodoConta/nuevoPeriodo/$',views.nuevoPeriodo),
    url(r'^catalogo/$',views.catalogoCuenta),
    url(r'^menu/(?P<periodoId>\d+)/$', views.manejoTransaccion),
    url(r'^consulta/(?P<periodoId>\d+)/$', views.consultarTransaccion),
    url(r'^nuevaTrans/(?P<periodoId>\d+)/$', views.nuevaTransaccion),
    url(r'^transaccion/(?P<periodoId>\d+)/$',views.transacciones),
    url(r'^detalleTrans/(?P<periodoId>\d+)/(?P<transaccionId>\d+)/$',views.detallesTransaccion),
    url(r'^detalleAfectado/(?P<periodoId>\d+)/(?P<transaccionId>\d+)/$',views.consultaAfectado),
    url(r'^generador/(?P<periodoId>\d+)/$', views.generadorEstados),
    url(r'^historial/(?P<periodoId>\d+)/$', views.historialCuenta),
    url(r'^balanceComprobacion/(?P<periodoId>\d+)/$', views.balancesComprobacion),
    url(r'^agregarCuenta/$', views.agregarCuentaPadre),
    url(r'^agregarCuentaHija/(?P<cuentaId>\d+)/$', views.agregarCuentaHija),
    url(r'^modificarCuenta/(?P<cuentaId>\d+)/$', views.modificarCuenta),
    url(r'^contabilidadGeneral/(?P<periodoId>\d+)/$', views.contabilidadGeneral),
    url(r'^estadoResultado/(?P<periodoId>\d+)/$', views.estadosResultado),
    url(r'^estadoCapital/(?P<periodoId>\d+)/$', views.estadoCapita),
]