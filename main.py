# -*- coding: utf-8 -*-
import datetime
from digitalocean import Image
from digitalocean import Manager

Max_diario = 7
Max_mensual = 3*28
today = datetime.date.today()

def ultima_imagen(imagenes):
	ultimo = 0	
	if len(imagenes) > 0 and (imagenes[0].name != None):		
		img_create = imagenes[0].created_at[0:10]
		ultimo = datetime.datetime.strptime(img_create,"%Y-%m-%d").date()
		for imagen in imagenes:
			if imagen.name == None: continue
			img_create = imagen.created_at[0:10]
			imagen_date = datetime.datetime.strptime(img_create,"%Y-%m-%d").date()
			if imagen_date > ultimo:
				ultimo = imagen_date
	return ultimo

def hacer_imagen(droplet):
	if droplet.get_actions()[0].status == "completed":
		print "Backup de: ",droplet.name
		droplet.take_snapshot(droplet.name)
		return True	
	else:
		print "Acción en proceso: ",droplet.get_actions()[0]
		return False

def borrar_copias(tag, imagenes):	
	print imagenes
	imagen_date = imagen.created_at[0:10]
	fecha_creacion = datetime.datetime.strptime(imagen_date,"%Y-%m-%d").date()

	for imagen in imagenes:				
		if tag == "mensual":		
			if fecha_creacion <= (today-datetime.timedelta(days = Max_meses)):
				imagen.destroy()
		elif tag == "semanal":
			pass
		elif tag == "diario":
			pass

def imagenes_x_droplet(images,imagen_id,token):
	imagenes =list()
	for id in imagen_id:
		for imagen in images:
			if imagen.id == id: imagenes.append(imagen)
	return imagenes

token = "0f7cd82fa277169b7015eed076f720fa156ee0360a3fa5906acf1a8e0eddcb29"
manager = Manager(token =token)
my_droplets  =  manager.get_all_droplets()
images =  manager.get_my_images()

# crea imagenes
for droplet in my_droplets:
	copied = False
	tags = droplet.tags
	#saco las imagenes de este droplet de la lista images
	imagenes_droplet = imagenes_x_droplet(images,droplet.snapshot_ids, token)	
	ultima = ultima_imagen(imagenes_droplet)
	print "Droplet: ",droplet.name," Tags: ",tags," Última copia: ", ultima,"Snap_ids: ",droplet.snapshot_ids," ",imagenes_droplet
	# exit(-1)
	for tag in tags:	
		if copied : continue	
		if (tag == "diario" or tag == "semanal" or tag == "mensual") and ultima == 0:
			copied = hacer_imagen(droplet)
			continue
		if tag == "mensual":
			if ultima <= (today-datetime.timedelta(days = 28)):
				borrar_copias(tag, imagenes_droplet)
				copied = hacer_imagen(droplet)
				print "copia mensual"
		elif tag == "semanal":
			if ultima <= (today-datetime.timedelta(days = 7)):
				copied = hacer_imagen(droplet)
				print "copia semanal"
		elif tag == "diario":
			if ultima <= (today-datetime.timedelta(days = 1)):
				copied = hacer_imagen(droplet)
				print "copia diaria"	
		
print manager.get_my_images()