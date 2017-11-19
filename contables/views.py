# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion,estadoComprobacion,estadoResulta
from myauth.models import  MyUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count
# Create your views here.
@login_required
def index(request):
	userId=request.user.is_admin
	return render(request, 'contables/index.html', {'user':userId})

@login_required
def periodoConta(request):
	periodo = PeriodoContable.objects.all()
	cantidad= int(0)
	print(cantidad)
	for periodos in periodo:
		if periodos.estadoPeriodo == True:
			cantidad= int(cantidad)+1
			print(cantidad)

	if request.method == 'POST':
		periodoParcial = PeriodoContable.objects.get(id_periodoContable=request.POST['idperiodo'])
		periodoParcial.estadoPeriodo = False
		periodoParcial.save()
	
	periodo = PeriodoContable.objects.all()

	return render(request, 'contables/periodoContable.html',{'periodoCont':periodo,'cant':cantidad})

@login_required
def nuevoPeriodo(request):
		if request.method == 'POST':
			PeriodoContable.objects.create(
				fechaInicio=request.POST['fechaIni'],
				fechaFin=request.POST['fechaFin'],
				estadoPeriodo=True
			)
			bal = estadoComprobacion.objects.get(id=1)
			bal.debe=0.00
			bal.haber= 0.00
			bal.save()
			cuenta = Cuenta.objects.all()
			for cuentas in cuenta:
				cuentaParcial=Cuenta.objects.get(id=cuentas.id)
				cuentaParcial.saldoAcreedor=0.00
				cuentaParcial.saldoDeudor=0.00
				cuentaParcial.debe=0.00
				cuentaParcial.haber=0.00
				cuentaParcial.save()
			return HttpResponse('No se almacenaron los datos')
		return render(request, 'contables/nuevoPeriodo.html')

@login_required
def manejoTransaccion(request, periodoId):
	periodo=periodoId
	return render(request, 'contables/menu.html',{'periodoId':periodo})

@login_required
def consultarTransaccion(request,periodoId):
	periodo=periodoId
	transaccion=Transaccion.objects.filter(id_periodoContable=periodoId)
	return render(request, 'contables/consultarTransaccion.html',{'periodoId':periodo,'transacciones':transaccion})

@login_required
def consultaAfectado(request,periodoId,transaccionId):
	cuenta =Cuenta.objects.all()
	detalles = detalleTransaccion.objects.filter(id_Transaccion=transaccionId)
	return render (request, 'contables/detalleCuentaAfectada.html',{'detalle':detalles,'cuentas':cuenta,'periodoId':periodoId})

@login_required
def nuevaTransaccion(request,periodoId):
	periodo=periodoId
	#el periodoId sirve para validar que si esta cerrado no se puede hacer una nueva transaccion
	if request.method == 'POST':
			Transaccion.objects.create(
				descripcion=request.POST['descripcion'],
				fecha=request.POST['fechaTransaccion'],
				id_periodoContable= PeriodoContable.objects.get(id_periodoContable=request.POST['periodo']),
				is_inicial = False,
			)
			return HttpResponse('No se almacenaron los datos')
	return render(request,'contables/ingresarTransaccion.html',{'periodoId':periodo})

@login_required
def transacciones(request,periodoId):
	periodo=periodoId
	periodoCont=PeriodoContable.objects.filter(id_periodoContable=periodoId)
	transaccion=Transaccion.objects.filter(id_periodoContable=periodoId)
	return render(request, 'contables/transaccionLista.html',{'periodos':periodoCont,'periodoId':periodo,'transacciones':transaccion})

@login_required
def detallesTransaccion(request,periodoId,transaccionId):
	periodo=periodoId
	trans=transaccionId
	cuentas=Cuenta.objects.all()
	
	if request.method == 'POST':
		if request.POST['cuentaId1'] != request.POST['cuentaId2']:
			if request.POST['monto1'] == request.POST['monto2']:
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

@login_required
def generadorEstados(request,periodoId):
	periodo= periodoId
	return render(request,'contables/generadorEstados.html',{'periodoId':periodo})

@login_required
def balancesComprobacion(request,periodoId):
	detalles = detalleTransaccion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()
	haberParcial = float(0.00)
	debeParcial = float(0.00)
	sumaHaber=float(0.00)
	sumaDebe=float(0.00)
	

	for cuenta in cuentas:
		cuentaSet=Cuenta.objects.get(id=cuenta.id)
		cuentaSet.saldoAcreedor=0.00
		cuentaSet.saldoDeudor=0.00
		cuentaSet.save()
		bal=estadoComprobacion.objects.get(id=int(1))
		bal.debe=float(0.00)
		bal.haber=float(0.00)
		bal.save()

	for cuenta in cuentas:
		bal=estadoComprobacion.objects.get(id=int(1))
		cuentaParcial=Cuenta.objects.get(id=cuenta.id)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id == cuenta.id:
					if detalle.id_Transaccion_id == transacciones.id_Transaccion:
						haberParcial=float(haberParcial) + float(detalle.haber)
						debeParcial=float(debeParcial) + float(detalle.debe)
		if haberParcial > debeParcial:
			cuentaParcial.saldoAcreedor=float(haberParcial)-float(debeParcial)
			cuentaParcial.save()
			bal.haber=float(bal.haber)+float(cuentaParcial.saldoAcreedor)
			bal.save()
		if debeParcial > haberParcial:
			cuentaParcial.saldoDeudor=float(debeParcial)-float(haberParcial)
			cuentaParcial.save()
			bal.debe=float(bal.debe)+float(cuentaParcial.saldoDeudor)
			bal.save()
		if debeParcial == haberParcial:
			cuentaParcial.saldoAcreedor=0.00
			cuentaParcial.saldoDeudor=0.00
			cuentaParcial.save()
			bal.debe=float(bal.debe)+float(cuentaParcial.saldoDeudor)
			bal.haber=float(bal.haber)+float(cuentaParcial.saldoAcreedor)
			bal.save()
		haberParcial=0.00
		debeParcial=0.00

	balanceC= estadoComprobacion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()	
	return render(request, 'contables/balanceComprobacion.html',{'cuenta':cuentas,'estados':balanceC,'periodoId':periodoId})

@login_required
def estadosResultado(request,periodoId):
	cuentasResultadoDeudor = Cuenta.objects.filter(descripcion__iexact='Costo de Venta')
	cuentasResultadoAcreedor = Cuenta.objects.filter(descripcion__iexact='Ingreso')
	cuentasResultadoDeudorAdministracion = Cuenta.objects.filter(descripcion__iexact='Gastos de Administracion')
	cuentasResultadoDeudorFinanciero = Cuenta.objects.filter(descripcion__iexact='Gastos Financieros')
	cuentasResultadoDeudorVenta = Cuenta.objects.filter(descripcion__iexact='Gasto de Venta')
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	detalles = detalleTransaccion.objects.all()
	result=estadoResulta.objects.all()
	haberParcial= float(0.00)
	debeParcial= float(0.00)
	estadoRes = estadoResulta.objects.get(id=1)
	estadoRes.debe= float(0.00)
	estadoRes.haber=float(0.00)
	estadoRes.utilidades=float(0.00)
	estadoRes.save()
	reservaLegal=Cuenta.objects.filter(descripcion__iexact='Reserva Legal')
	impuesto=Cuenta.objects.filter(nombre__iexact='Impuesto sobre Renta')

	for cuenta in cuentasResultadoDeudor:
		cuentaSet=Cuenta.objects.get(id=cuenta.id)
		cuentaSet.saldoDeudor=0.00
		cuentaSet.saldoAcreedor=0.00
		cuentaSet.save()
	for cuenta in cuentasResultadoAcreedor:
		cuentaSet=Cuenta.objects.get(id=cuenta.id)
		cuentaSet.saldoDeudor=0.00
		cuentaSet.saldoAcreedor=0.00
		cuentaSet.save()

	for cuenta in cuentasResultadoAcreedor:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						haberParcial=float(haberParcial)+float(detalle.haber)
		cuentaParcial.saldoAcreedor=float(haberParcial)
		cuentaParcial.save()
		estadoRes.haber=float(estadoRes.haber)+ float(cuentaParcial.saldoAcreedor)
		estadoRes.utilidades=float(estadoRes.utilidades)+float(cuentaParcial.saldoAcreedor)
		estadoRes.save()
		haberParcial=0.00
		

	for cuenta in cuentasResultadoDeudor:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						debeParcial=float(debeParcial)+float(detalle.debe)
		cuentaParcial.saldoDeudor=float(debeParcial)
		cuentaParcial.save()
		estadoRes.debe=float(estadoRes.debe)+ float(cuentaParcial.saldoDeudor)
		estadoRes.utilidades=float(estadoRes.utilidades)-float(cuentaParcial.saldoDeudor)
		estadoRes.save()
		debeParcial=0.00

	for cuenta in cuentasResultadoDeudorAdministracion:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						debeParcial=float(debeParcial)+float(detalle.debe)
		cuentaParcial.saldoDeudor=float(debeParcial)
		cuentaParcial.save()
		estadoRes.debe=float(estadoRes.debe)+ float(cuentaParcial.saldoDeudor)
		estadoRes.utilidades=float(estadoRes.utilidades)-float(cuentaParcial.saldoDeudor)
		estadoRes.save()
		debeParcial=0.00

	for cuenta in cuentasResultadoDeudorFinanciero:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						debeParcial=float(debeParcial)+float(detalle.debe)
		cuentaParcial.saldoDeudor=float(debeParcial)
		cuentaParcial.save()
		estadoRes.debe=float(estadoRes.debe)+ float(cuentaParcial.saldoDeudor)
		estadoRes.utilidades=float(estadoRes.utilidades)-float(cuentaParcial.saldoDeudor)
		estadoRes.save()
		debeParcial=0.00

	for cuenta in cuentasResultadoDeudorVenta:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						debeParcial=float(debeParcial)+float(detalle.debe)
		cuentaParcial.saldoDeudor=float(debeParcial)
		cuentaParcial.save()
		estadoRes.debe=float(estadoRes.debe)+ float(cuentaParcial.saldoDeudor)
		estadoRes.utilidades=float(estadoRes.utilidades)-float(cuentaParcial.saldoDeudor)
		estadoRes.save()
		debeParcial=0.00

	for cuenta in reservaLegal:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						haberParcial=float(haberParcial)+float(detalle.haber)
		cuentaParcial.saldoAcreedor=float(haberParcial)
		cuentaParcial.save()
		estadoRes.utilidadNeta=float(estadoRes.utilidades)-float(cuentaParcial.saldoAcreedor)
		estadoRes.save()

	for cuenta in impuesto:
		cuentaParcial = Cuenta.objects.get(id=cuenta.id)
		estadoRes = estadoResulta.objects.get(id=1)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id ==cuenta.id:
					if detalle.id_Transaccion_id==transacciones.id_Transaccion:
						debeParcial=float(debeParcial)+float(detalle.debe)
		cuentaParcial.saldoDeudor=float(debeParcial)
		cuentaParcial.save()
		estadoRes.utilidadNeta=float(estadoRes.utilidadNeta)-float(cuentaParcial.saldoDeudor)
		estadoRes.save()

	cuentasResultadoDeudor = Cuenta.objects.filter(descripcion__iexact='Costo de Venta')
	cuentasResultadoAcreedor = Cuenta.objects.filter(descripcion__iexact='Ingreso')
	cuentasResultadoDeudorAdministracion = Cuenta.objects.filter(descripcion__iexact='Gastos de Administracion')
	cuentasResultadoDeudorFinanciero = Cuenta.objects.filter(descripcion__iexact='Gastos Financieros')
	cuentasResultadoDeudorVenta = Cuenta.objects.filter(descripcion__iexact='Gasto de Venta')
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	detalles = detalleTransaccion.objects.all()
	estado = estadoResulta.objects.all()
 	reservaLegal=Cuenta.objects.filter(descripcion__iexact='Reserva Legal')
 	impuesto=Cuenta.objects.filter(nombre__iexact='Impuesto sobre Renta')

	return render(request, 'contables/estadoResultado.html', {'impuestoRenta':impuesto,'capital':reservaLegal,'Gasto':cuentasResultadoDeudor,'Gasto2':cuentasResultadoDeudorAdministracion,'Gasto3':cuentasResultadoDeudorFinanciero,'Gasto4':cuentasResultadoDeudorVenta,'resultado':estado,'Ingreso':cuentasResultadoAcreedor})

@login_required
def historialCuenta(request,periodoId):
	cuentas = Cuenta.objects.all()
	periodo=periodoId
	return render(request,'contables/historialCuentas.html',{'cuenta':cuentas,'periodoId':periodo})

@login_required
def catalogoCuenta(request):
	cuentas = Cuenta.objects.all()
	return render(request, 'contables/catalogoCuentas.html',{'cuenta':cuentas})

@login_required
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

@login_required
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

@login_required
def modificarCuenta(request,cuentaId):
	cuentaid=cuentaId
	cuentas = Cuenta.objects.filter(id=cuentaId)
	maximo =Transaccion.objects.all().aggregate(Max('id_Transaccion'))

	if request.method == 'POST':
		periodo=PeriodoContable.objects.all()
		for  periodos in periodo:
			if periodos.estadoPeriodo == True:
				transaccion=Transaccion.objects.filter(id_periodoContable=periodos.id_periodoContable,is_inicial=False)
				tamano = len(transaccion)
				if tamano == 0:
					cuentaParcial = Cuenta.objects.get(id=request.POST['idCuenta'])
					cuentaParcial.codigo= request.POST['codigoCuenta']
					cuentaParcial.nombre= request.POST['nombreCuenta']
					cuentaParcial.descripcion= request.POST['descripcionCuenta']
					cuentaParcial.debe= request.POST['debeCuenta']
					cuentaParcial.haber= request.POST['haberCuenta']
					cuentaParcial.save()
					Transaccion.objects.create(
						descripcion='Inicio',
						fecha=periodos.fechaInicio,
						id_periodoContable=PeriodoContable.objects.get(id_periodoContable=periodos.id_periodoContable),
						is_inicial=True,
						)
					detalleTransaccion.objects.create(
						debe =request.POST['debeCuenta'],
						haber =request.POST['haberCuenta'],
						id_Transaccion =Transaccion.objects.get(id_Transaccion=request.POST['idtrans']),
						id_cuenta =Cuenta.objects.get(id=request.POST['idCuenta']),
						)
				else:
					print('ya hay transacciones solo puede modificar el nombre y descripcion')
					cuentaParcial = Cuenta.objects.get(id=request.POST['idCuenta'])
					cuentaParcial.codigo= request.POST['codigoCuenta']
					cuentaParcial.nombre= request.POST['nombreCuenta']
					cuentaParcial.descripcion= request.POST['descripcionCuenta']
					cuentaParcial.save()

	return render (request, 'contables/modificarCuenta.html',{'cuenta':cuentas,'max':maximo})


def contabilidadGeneral(request,periodoId):
	periodos= periodoId
	return render(request, 'contables/contabilidadGeneral.html', {'periodoId':periodos})


