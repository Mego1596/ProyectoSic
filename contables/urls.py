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
    url(r'^balanceGeneral/(?P<periodoId>\d+)/$', views.balanceGral),
    url(r'^contabilidadCostos/(?P<periodoId>\d+)/$', views.contabilidadCost),
    url(r'^compraMP/(?P<periodoId>\d+)/$', views.compraMateriaPrima),
    url(r'^manejoOrdenes/(?P<periodoId>\d+)/$', views.manejoOrden),
    url(r'^contratacion/(?P<periodoId>\d+)/$', views.contratacionEmpleado),
    url(r'^planillaGeneral/(?P<periodoId>\d+)/$', views.planilla),
    url(r'^kardex/(?P<periodoId>\d+)/$', views.manejoKardex),
    url(r'^crearOrden/(?P<periodoId>\d+)/$', views.crearOrd),
    url(r'^modificarCIF/(?P<periodoId>\d+)/$', views.modificarCif),
    url(r'^gestionarOrden/(?P<ordenId>\d+)/$', views.gestionOrden),
    url(r'^asignarMP/(?P<ordenId>\d+)/$', views.asignarMP),
    url(r'^asignarMOD/(?P<ordenId>\d+)/$', views.asignarMOD),
    url(r'^detallesKardex/(?P<materiaId>\d+)/$', views.detalleKardex),
    url(r'^productoTerminado/(?P<ordenId>\d+)/(?P<periodoId>\d+)/$', views.prodTerminado),
    url(r'^planillaGral/(?P<empleadoId>\d+)/$', views.asignarPlanilla),
]