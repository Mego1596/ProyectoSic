# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion
# Create your views here.
def index(request):
	return render(request, 'contables/index.html')
def periodoConta(request):
	periodo = PeriodoContable.objects.all()
	return render(request, 'contables/periodoContable.html',{'periodoCont':periodo})

def nuevoPeriodo(request):
		if request.method == 'POST':
			PeriodoContable.objects.create(
				fechaInicio=request.POST['fechaIni'],
				fechaFin=request.POST['fechaFin'],
				estadoPeriodo=True
			)
			return HttpResponse('No se almacenaron los datos')
		return render(request, 'contables/nuevoPeriodo.html')

def manejoTransaccion(request, periodoId):
	periodo=periodoId
	return render(request, 'contables/menu.html',{'periodoId':periodo})

def consultarTransaccion(request,periodoId):
	periodo=periodoId
	transaccion=Transaccion.objects.filter(id_periodoContable=periodoId)
	return render(request, 'contables/consultarTransaccion.html',{'periodoId':periodo,'transacciones':transaccion})

def consultaAfectado(request,periodoId,transaccionId):
	cuenta =Cuenta.objects.all()
	detalles = detalleTransaccion.objects.filter(id_Transaccion=transaccionId)
	return render (request, 'contables/detalleCuentaAfectada.html',{'detalle':detalles,'cuentas':cuenta})

def nuevaTransaccion(request,periodoId):
	periodo=periodoId
	#el periodoId sirve para validar que si esta cerrado no se puede hacer una nueva transaccion
	if request.method == 'POST':
			Transaccion.objects.create(
				descripcion=request.POST['descripcion'],
				fecha=request.POST['fechaTransaccion'],
				id_periodoContable= PeriodoContable.objects.get(id_periodoContable=request.POST['periodo'])
			)
			return HttpResponse('No se almacenaron los datos')
	return render(request,'contables/ingresarTransaccion.html',{'periodoId':periodo})

def transacciones(request,periodoId):
	periodo=periodoId
	transaccion=Transaccion.objects.filter(id_periodoContable=periodoId)
	return render(request, 'contables/transaccionLista.html',{'periodoId':periodo,'transacciones':transaccion})

def detallesTransaccion(request,periodoId,transaccionId):
	periodo=periodoId
	trans=transaccionId
	cuentas=Cuenta.objects.all()
	#el periodoId sirve para validar que si esta cerrado no se puede asignar detalle
	if request.method == 'POST':
		for x in xrange(0,2):
				if x == 0:
					detalleTransaccion.objects.create(
						debe =request.POST.get('monto'+str(x+1)), 
						haber = 0.00,
						id_Transaccion =Transaccion.objects.get(id_Transaccion=request.POST['idtrans'+str(x+1)]) ,
						id_cuenta =Cuenta.objects.get(id=request.POST['cuentaId'+str(x+1)]),
						)
					cuentaActualizar = Cuenta.objects.get(id=request.POST['cuentaId'+str(x+1)])	
					debeac = cuentaActualizar.getDebe()
					cuentaActualizar.debe=float(debeac)+float(request.POST['monto'+str(x+1)])					
					cuentaActualizar.save()
				else:
					if x == 1:
						detalleTransaccion.objects.create(
						debe = 0.00,
						haber =request.POST.get('monto'+str(x+1)), 
						id_Transaccion =Transaccion.objects.get(id_Transaccion=request.POST['idtrans'+str(x+1)]) ,
						id_cuenta =Cuenta.objects.get(id=request.POST['cuentaId'+str(x+1)]),
						)
					cuentaActualizar2 = Cuenta.objects.get(id=request.POST['cuentaId'+str(x+1)])	
					haberac = cuentaActualizar2.getHaber()
					cuentaActualizar2.haber=float(haberac)+float(request.POST['monto'+str(x+1)])					
					cuentaActualizar2.save()
	return render(request, 'contables/detalleTransaccion.html',{'periodoId':periodo,'transaccionId':trans,'cuenta':cuentas})


def generadorEstados(request,periodoId):
	periodo= periodoId
	return render(request,'contables/generadorEstados.html',{'periodoId':periodo})

def balancesComprobacion(request,periodoId):
	detalles = detalleTransaccion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()
	haberParcial = float(0.00)
	debeParcial = float(0.00)
	if request.method == 'POST':
		for cuenta in cuentas:
			cuentaSet=Cuenta.objects.get(id=cuenta.id)
			cuentaSet.saldoDeudor=0.00
			cuentaSet.saldoAcreedor=0.00
	
		for cuenta in cuentas:
			cuentaParcial= Cuenta.objects.get(id=cuenta.id)
			for transacciones in transaccion:
				for detalle in detalles:
					if detalle.id_cuenta_id ==cuenta.id:
						if detalle.id_Transaccion_id==transacciones.id_Transaccion:
							haberParcial=float(haberParcial)+float(detalle.haber)
							debeParcial=float(debeParcial)+float(detalle.debe)
			print(haberParcial)
			print(debeParcial)
			if haberParcial>debeParcial:
				cuentaParcial.saldoAcreedor=float(haberParcial)-float(debeParcial)
				cuentaParcial.save()
			if haberParcial<debeParcial:
				cuentaParcial.saldoDeudor=float(debeParcial)-float(haberParcial)
				cuentaParcial.save()
			else:
				cuentaParcial.saldoDeudor=0.00
				cuentaParcial.saldoAcreedor=0.00
			haberParcial=0.00
			debeParcial=0.00
	return render(request,'contables/balanceComprobacion.html',{'cuenta':cuentas})

def historialCuenta(request,periodoId):
	cuentas = Cuenta.objects.all()
	return render(request,'contables/historialCuentas.html',{'cuenta':cuentas})

def catalogoCuenta(request):
	return render(request, 'contables/catalogoCuentas.html')
