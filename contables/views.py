# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion,estadoComprobacion
# Create your views here.
def index(request):
	return render(request, 'contables/index.html')
def periodoConta(request):
	periodo = PeriodoContable.objects.all()
	cantidad= int(0)
	print(cantidad)
	for periodos in periodo:
		if periodos.estadoPeriodo == True:
			cantidad= int(cantidad)+1
			print(cantidad)
	return render(request, 'contables/periodoContable.html',{'periodoCont':periodo,'cant':cantidad})

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
	balances=estadoComprobacion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()
	haberParcial = float(0.00)
	debeParcial = float(0.00)
	sumaHaber=float(0.00)
	sumaDebe=float(0.00)
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

			sumaHaber = float(sumaHaber)+ float(cuenta.getSaldoAcreedor())
			sumaDebe =  float(sumaDebe)  + float(cuenta.getSaldoDeudor())
			print(sumaHaber)
			balance = estadoComprobacion.objects.get(id=1)
			balance.debe=float(sumaDebe)
			balance.haber=float(sumaHaber)
			balance.save()
	return render(request,'contables/balanceComprobacion.html',{'cuenta':cuentas,'estado':balances})

def historialCuenta(request,periodoId):
	cuentas = Cuenta.objects.all()
	return render(request,'contables/historialCuentas.html',{'cuenta':cuentas})

def catalogoCuenta(request):
	cuentas = Cuenta.objects.all()
	return render(request, 'contables/catalogoCuentas.html',{'cuenta':cuentas})

def agregarCuentaPadre(request):
	if request.method == 'POST':
		Cuenta.objects.create(
			codigo =request.POST['codigoCuenta'],
			nombre =request.POST['nombreCuenta'],
			debe =0.00,
			haber=0.00,
			saldoDeudor=0.00,
			saldoAcreedor=0.00,
			descripcion=request.POST['descripcionCuenta']
			)
	return render(request, 'contables/agregarCuenta.html')

def agregarCuentaHija(request,cuentaId):
	cuenta=Cuenta.objects.filter(id=cuentaId)
	cuentaid=cuentaId
	if request.method == 'POST':
		Cuenta.objects.create(
			codigo =request.POST['codigoCuenta'],
			nombre =request.POST['nombreCuenta'],
			debe =0.00,
			haber=0.00,
			saldoDeudor=0.00,
			saldoAcreedor=0.00,
			codigo_dependiente=cuentaId,
			descripcion=request.POST['descripcionCuenta']
			)
	return render(request, 'contables/agregarCuentaHija.html',{'cuentas':cuenta,'cuentaId':cuentaid})

def modificarCuenta(request,cuentaId):
	cuentaid=cuentaId
	cuentas = Cuenta.objects.filter(id=cuentaId)

	if request.method == 'POST':
		periodo=PeriodoContable.objects.all()
		for  periodos in periodo:
			if periodos.estadoPeriodo == True:
				transaccion=Transaccion.objects.filter(id_periodoContable=periodos.id_periodoContable	)
				tamano = len(transaccion)
				if tamano == 0:
					cuentaParcial = Cuenta.objects.get(id=request.POST['idCuenta'])
					cuentaParcial.codigo= request.POST['codigoCuenta']
					cuentaParcial.nombre= request.POST['nombreCuenta']
					cuentaParcial.descripcion= request.POST['descripcionCuenta']
					cuentaParcial.debe= request.POST['debeCuenta']
					cuentaParcial.haber= request.POST['haberCuenta']
					cuentaParcial.save()
				else:
					print('ya hay transacciones solo puede modificar el nombre y descripcion')
					cuentaParcial = Cuenta.objects.get(id=request.POST['idCuenta'])
					cuentaParcial.codigo= request.POST['codigoCuenta']
					cuentaParcial.nombre= request.POST['nombreCuenta']
					cuentaParcial.descripcion= request.POST['descripcionCuenta']
					cuentaParcial.save()

	return render (request, 'contables/modificarCuenta.html',{'cuenta':cuentas})