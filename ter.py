# -*- coding: utf-8 -*
import random
import math


class univexp:
	fichier="univexp01"
	tecr=0.0
	tsor=0.0
	n=10000
	
	
	def __init__(self):
		self.init()
		self.fi=open(self.fichier,"w")
		self.wbande()
		self.tecr=self.tecr+self.dti
		self.tsor=self.tecr+self.dtsor
		
		while(abs(self.tecr-self.tstop)>self.dtsor/2.0):
			print("abs(self.tecr-self.tstop)>self.dtsor/2.0: {}-{}={}>{}/2.0".format(self.tecr,self.tstop,self.tecr-self.tstop,self.dtsor))
			while(abs(self.tecr-self.tsor)>self.dti/2.0):
				self.avance()
				self.ordonne()
				self.tecr=self.tecr+self.dti
			self.wbande()
			self.tsor=self.tsor+self.dtsor
		
		self.fi.close()	
		print("\nfin du programme.\n")
		
		

	def avance(self):
		r2=-(math.sqrt(2.0))
		tier=1.0/3.0
		AA=0
		BB=0
		E=0
		
		#calcul de l'accélération
		a=[0]*self.m
		self.eav=self.epolar+0.5*self.n
		
		for i in range(self.ifirst, self.ilast+1):
			self.eap=self.eav-1
			a[i]=0.5*(self.eav+self.eap)
			self.eav=self.eap
		
		#les particules avancent de dti
		
		for i in range(self.ifirst, self.ilast+1):
			E=a[i]
			AA=(self.x[i]+E-r2*self.v[i])*math.exp(r2*self.dti)
			BB=2.0*(self.x[i]+E-self.v[i]/r2)*math.exp(-self.dti/r2)
			self.x[i]=((AA+BB)*tier)-E
			self.v[i]=(AA*r2-BB/r2)*tier
			if(self.x[i]>self.x[self.m-1]):
				self.epolar+=1
				self.x[i]=self.x[1]+self.x[i]-self.x[self.m-1]
		
	def ordonne(self):
		j=0
		xp=0.0
		vp=0.0
		mip=0.0
		map1=0.0
		for i in range(self.ifirst+1, self.ilast+1):
			j=i
			xp=self.x[i]
			vp=self.v[i]
			np=self.name[i]
			while(j!=1 and self.x[i]<self.x[j-1]):
				j-=1
			for k in range(i,j+2,-1):
				self.x[k]=self.x[k-1]
				self.v[k]=self.v[k-1]
				self.name[k]=self.name[k-1]
			
			self.x[j]=xp
			self.v[j]=vp
			self.name[j]=np
	
	def wbande(self):
		print("enregistrement a tecr={:7.3f}").format(self.tecr)
		
		self.fi.write(("#{:5d} {:5d} {:5d} {:5d} {:7.3f}\n").format(self.m, self.n, self.ifirst, self.ilast, self.tecr))
		for i in range(self.ifirst, self.ilast+1):
			self.fi.write(("{} {} {}\n").format(self.x[i],self.v[i],self.name[i]))
		
		self.fi.write("\n")
		
	def init(self):
		self.m=self.n+2
		self.ifirst=1
		self.ilast=self.n
		self.dti=0.001
		self.dtsor=1.0
		self.tstop=15.0
		self.gravplas=1.0
		self.pvit=100.0
		
		self.x=[0.0]*self.m
		self.v=[0.0]*self.m
		self.mi=[0.0]*self.m
		self.ma=[0.0]*self.m
		self.name=[0]*self.m
		
		print("simulation : "+self.fichier)
		print(("{:19.15f} : pas de temps \n").format(self.dti))
		print(("n = {:8d} pvit = {:7.1f}").format(self.n, self.pvit))
		print(("tstop = {:7.1f} dtsor = {:7.1f}").format(self.tstop, self.dtsor))

		#initialisation des "particules-mur"

		self.x[0]=-0.5*float(self.n)
		"""self.v[0]=0.0
		self.mi[0]=0.0
		self.ma[0]=0.0
		self.name[0]=0"""
		self.x[self.m-1]=0.5*float(self.n)
		"""self.v[self.m-1]=0.0
		self.mi[self.m-1]=0.0
		self.ma[self.m-1]=0.0
		self.name[self.m-1]=0"""
			
		#initialisation des particules
        
		for i in range(self.ifirst, self.ilast+1):
			self.name[i]=i-1
			self.x[i]=self.x[1]+0.5+i-(self.ifirst+1)
			self.v[i]=2.0*self.pvit*(0.5-random.random())
			self.mi[i]=1.0
			self.ma[i]=1.0
		self.epolar=0
		
		#calage du barycentre à zéro avec une vitesse moyenne  nulle
		
		vmoy=sum(self.v[self.ifirst:self.ilast])
		vmoy=vmoy/float(self.n)
		
		#self.v[self.ifirst:self.ilast]=self.v[self.ifirst:self.ilast]-vmoy
		for i in range(self.ifirst,self.ilast+1):
			self.v[i]=self.v[i]-vmoy
			
		vmoy=sum(self.v[self.ifirst:self.ilast])
		print(("vmoyen = {:7.3f}").format(vmoy))
		
def main():
	u=univexp()		
	
main()
