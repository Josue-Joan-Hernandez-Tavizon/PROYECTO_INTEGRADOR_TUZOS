import tkinter as tk
import pywinstyles
class PanelR(tk.Canvas):
    def __init__(self,cont,w,h,bord_w,n_rad,bord_col,in_col):
        tk.Canvas.__init__(self,cont,width=w,height=h,highlightthickness=0,bg=cont["bg"])
        self.cont=cont 
        self.crear_panel([w-bord_w,bord_w,bord_w,w-bord_w],[bord_w,bord_w,h-bord_w,h-bord_w],n_rad,width=bord_w,outline=bord_col,fill=in_col)
        self.configure(width=w,height=h,bg="white")
        pywinstyles.set_opacity(self,color="white")
    def crear_panel(self,x,y,nit,**kwargs):
        if nit<2:
            nit=2
        mult_r=nit-1
        div_r=nit
        puntos=[]
        for i in range(len(x)):
            puntos.append(x[i])
            puntos.append(y[i])
            if i != (len(x)-1):
                puntos.append((mult_r*x[i]+x[i+1])/div_r)
                puntos.append((mult_r*y[i]+y[i+1])/div_r)
                puntos.append((mult_r*x[i+1]+x[i])/div_r)
                puntos.append((mult_r*y[i+1]+y[i])/div_r)
            else:
                puntos.append((mult_r*x[i]+x[0])/div_r)
                puntos.append((mult_r*y[i]+y[0])/div_r)
                puntos.append((mult_r*x[0]+x[i])/div_r)
                puntos.append((mult_r*y[0]+y[i])/div_r)
                puntos.append(x[0])
                puntos.append(y[0])
        return self.create_polygon(puntos,**kwargs,smooth=tk.TRUE)
