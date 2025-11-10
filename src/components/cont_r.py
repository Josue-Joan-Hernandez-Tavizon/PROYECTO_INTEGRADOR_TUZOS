import tkinter.font as font
from tkinter import *
import tkinter as tk
import pywinstyles

class ContR(tk.Canvas):
  def __init__(self,cont,n_rad,w,h,color,text='',t_font=16,fg_font="black",command=None):
    tk.Canvas.__init__(self,cont,borderwidth=0,relief="flat",highlightthickness=0,bg=cont["bg"])
    self.command=command
    self.fg_font=fg_font
    font_size=t_font
    self.font=font.Font(size=font_size,family='Helvetica',weight="normal")
    self.id=None
    self.color=color
    height=font_size+(2*h)
    width=self.font.measure(text)+(4*w)
    width=width if width>=80 else 80
    if n_rad>0.5*width:
      print("Error: border_radius is greater than width.")
      return None
    if n_rad>0.5*height:
      print("Error: border_radius is greater than height.")
      return None
    rad = 2*n_rad
    def shape():
      self.create_arc((0,rad,rad,0),start=90,extent=90,fill=color,outline=color)
      self.create_arc((width-rad,0,width,rad),start=0,extent=90,fill=color,outline=color)
      self.create_arc((width,height-rad,width-rad,height),start=270,extent=90,fill=color,outline=color)
      self.create_arc((0,height-rad,rad,height),start=180,extent=90,fill=color,outline=color)
      return self.create_polygon((0,height-n_rad,0,n_rad,n_rad,0,width-n_rad,0,width,n_rad,width,height-n_rad,width-n_rad,height,n_rad,height),fill=color,outline=color)
    id=shape()
    (x0,y0,x1,y1)=self.bbox("all")
    width=(x1-x0)
    height=(y1-y0)
    self.configure(width=width,height=height,bg="#FDC9FF")
    self.create_text(width/2,(height/2)-2,text=text,fill=self.fg_font,font=self.font,anchor="center")
    self.bind("<ButtonPress-1>",self._on_press)
    self.bind("<ButtonRelease-1>",self._on_release)
    pywinstyles.set_opacity(self,color="#FDC9FF")
  def _on_press(self,event):
      self.configure(relief="sunken")
  def _on_release(self,event):
      self.configure(relief="raised")
      if self.command is not None:
          self.command()

class Cont_Cr(tk.Canvas):
  def __init__(self,cont,r,color_f,color_bc):
    tk.Canvas.__init__(self,cont,borderwidth=0,relief="flat",highlightthickness=0,bg=color_bc)
    self.create_oval(0,0,2*r,2*r,fill=color_f,outline=color_bc)
    pywinstyles.set_opacity(self,color=color_bc)
