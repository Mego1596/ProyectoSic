# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class PeriodoContable(models.Model):
	id_periodoContable = models.AutoField(primary_key= True)
	fechaInicio = models.DateField('Fecha de inicio', help_text='Formato: AAAA/MM/DD', blank=False, null=False)
	fechaFin = models.DateField('Fecha de Fin', help_text='Formato: AAAA/MM/DD', blank=False, null=False)
	estadoPeriodo= models.NullBooleanField(null = True);
	def __str__(self):
		return '{}{}'.format(self.fechaInicio,' hasta el ', self. fechaFin)

class Transaccion(models.Model):
	id_Transaccion= models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length = 256)
	fecha = models.DateField('Fecha de Transaccion', help_text='Formato: AAAA/MM/DD', blank=False, null=False)
	id_periodoContable = models.ForeignKey(PeriodoContable, null=True, blank=True,on_delete= models.CASCADE)
	def __str__(self):
		return '{}{}'.format(self.id_Transaccion,self.descripcion, self.fecha,self.id_periodoContable)

		
class Cuenta(models.Model):
	id = models.AutoField(primary_key=True)
	codigo = models.IntegerField()
	nombre = models.CharField(max_length = 256)
	debe = models.DecimalField('debe', max_digits=50, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
	haber = models.DecimalField('haber', max_digits=50, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
	saldoDeudor = models.DecimalField('saldo_deudor', max_digits =50, decimal_places=2,blank=False,null=False,validators=[MinValueValidator(0)],default=0.00)
	saldoAcreedor = models.DecimalField('saldo_acreedor', max_digits =50, decimal_places=2,blank=False,null=False,validators=[MinValueValidator(0)],default=0.00)
	codigo_dependiente = models.IntegerField(null= True)
	descripcion = models.CharField(max_length= 256, null=False, blank=False, default='null')
	def __str__(self):
		return '{}{}'.format(self.nombre)

	def getHaber(self):
		return self.haber

	def getDebe(self):
		return self.debe

	def getSaldoAcreedor(self):
		return self.saldoAcreedor

	def getSaldoDeudor(self):
		return self.saldoDeudor

class detalleTransaccion(models.Model):
	id_detalle = models.AutoField(primary_key = True)
	debe = models.DecimalField('debe', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])
	haber = models.DecimalField('haber', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])  
	id_Transaccion = models.ForeignKey(Transaccion, null=True, blank=True,on_delete= models.CASCADE)
	id_cuenta = models.ForeignKey(Cuenta, null=True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return '{}{}'.format(self.id_detalle)

class estadoComprobacion(models.Model):
	id= models.AutoField(primary_key=True)
	debe =models.DecimalField('debe', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])
	haber= models.DecimalField('haber', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])

class estadoResulta(models.Model):
	id=models.AutoField(primary_key=True)
	debe =models.DecimalField('debe', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])
	haber= models.DecimalField('haber', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])
	utilidades=models.DecimalField('Utilildad', max_digits=50, decimal_places=2, blank=False, null=True, validators=[MinValueValidator(0)])