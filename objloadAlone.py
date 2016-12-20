#!/usr/bin/env python
# -⁻- coding: UTF-8 -*-

#Tutorial by Ian Mallett

#All tutorials will have the following functions:

#init() -> sets up the scene and any necessary variables
#quit() -> called at exit; cleans up
#GetInput() -> handle's the user's input
#Draw(Window) -> draws the scene


#The main file (Tutorial.py) runs all tutorials like:

#init()
#while True:
#    GetInput()
#    Draw(Window)
#quit()


#Each tutorial builds upon the last.  New or different
#lines will be commented.  Lines described in earlier
#tutorials will not.  Comments go directly above the
#lines they describe.  It is recommended that the
#tutorials be read in order.

#Every tutorial will also have a controls list.

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate spaceship

#Every tutorial will also have a theory section.

#Theory:
#glLibObject(...) loads a .obj file, which stores
#geometric data, returning an object.  The object can
#then be drawn via object.draw_arrays(...).  Calling
#object.build_list() and/or object.build_vbo() allows
#the object to be drawn with a display list or a vertex
#buffer object.



#Allow access to OpenGL Library
import sys,os
sys.path.append(os.path.split(sys.path[0])[0])




#Import GUI tool
import math
import Tkinter as tk, tkFileDialog
from Tkinter import *
import ttk

#Import OpenGL Library
from glLib import *
multisample = False
benchmark = False

root = tk.Tk()
embed = tk.Frame(root, width = 800, height = 600) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT, fill=BOTH, expand=1) #packs window to the left


os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

##Initial values

fieldOf = 45

notebook = ttk.Notebook(root)

lidScene = ttk.Frame(notebook, width = 75, height = 500)
notebook.add(lidScene, text = "Escena")
lidLight = ttk.Frame(notebook, width = 75, height = 500)
notebook.add(lidLight, text = "Luz")
lidCamera = ttk.Frame(notebook, width = 75, height = 500)
#buttonwin.pack(side = LEFT)
notebook.add(lidCamera, text = "Camara")
lidCaptures = ttk.Frame(notebook, width = 75, height = 500)
notebook.add(lidCaptures, text = "Capturas")
lidAcquisition = ttk.Frame(notebook, width = 75, height = 500)
notebook.add(lidAcquisition, text = "Método simple")
lidSampling = ttk.Frame(notebook, width = 75, height = 500)
notebook.add(lidSampling, text = "Método muestreo")
notebook.pack(side = LEFT, fill=BOTH, expand=1) #packs window to the left

framecose = ttk.Frame(lidAcquisition,width = 70, height = 100)
framecose.grid(row= 15, column = 0, sticky= W)


def changeParameters():
    global fieldOf, capturing
    if len(entryCameraPosX.get()) != 0:
        camerapos[0] = float(entryCameraPosX.get())
    if len(entryCameraPosY.get()) != 0:
        camerapos[1] = float(entryCameraPosY.get())
    if len(entryCameraPosZ.get()) != 0:
        camerapos[2] = float(entryCameraPosZ.get())

    if len(entryCameraLookAtX.get()) != 0:
        cameraLookAt[0] = float(entryCameraLookAtX.get())
    if len(entryCameraLookAtY.get()) != 0:
        cameraLookAt[1] = float(entryCameraLookAtY.get())
    if len(entryCameraLookAtZ.get()) != 0:
        cameraLookAt[2] = float(entryCameraLookAtZ.get())
    quit()
    capturing = True
    if len(entryCameraFieldOfView.get()) != 0:
        fieldOf = float(entryCameraFieldOfView.get())
        glScalef(2,3,4)
    init(8)


def changeParametersCaptures():
    #global camWindowX, camWindowY, stepsX, stepsY
    if len(entryCameraIncX.get()) != 0:
        camWindowX = float(entryCameraIncX.get())
    if len(entryCameraIncY.get()) != 0:
        camWindowY = float(entryCameraIncY.get())
    if len(entryCameraStepsX.get()) != 0:
        stepsX = float(entryCameraStepsX.get())
    if len(entryCameraStepsY.get()) != 0:
        stepsY = float(entryCameraStepsY.get())

def changeParametersLight():
    global light, lightsPos, lightsDir, lightsCol
    current = options.index(currentSource.get())


    quit()

    if len(entryLightPosX.get()) != 0:
        lightsPos[current][0]= float(entryLightPosX.get())
    if len(entryLightPosY.get()) != 0:
        lightsPos[current][1]= float(entryLightPosY.get())
    if len(entryLightPosZ.get()) != 0:
        lightsPos[current][2]= float(entryLightPosZ.get())

    if len(entryLightDirX.get()) != 0:
        lightsDir[current][0]= float(entryLightDirX.get())
    if len(entryLightDirY.get()) != 0:
        lightsDir[current][1]= float(entryLightDirY.get())
    if len(entryLightDirZ.get()) != 0:
        lightsDir[current][2]= float(entryLightDirZ.get())

    if len(entryLightColR.get()) != 0:
        lightsCol[current][0]= float(entryLightColR.get())
    if len(entryLightColG.get()) != 0:
        lightsCol[current][1]= float(entryLightColG.get())
    if len(entryLightColB.get()) != 0:
        lightsCol[current][2]= float(entryLightColB.get())

    lightsActive[current] = activeLight.get()

    if sourceType.get() == "Spotlight":
        lightsType[current] = 1
    else:
        lightsType[current] = 0

    init(8)

def updateParametersLight(currentS):
    current = options.index(currentS)
    entryLightPosX.delete(0, END)
    entryLightPosX.insert(0, lightsPos[current][0])
    entryLightPosY.delete(0, END)
    entryLightPosY.insert(0, lightsPos[current][1])
    entryLightPosZ.delete(0, END)
    entryLightPosZ.insert(0, lightsPos[current][2])

    entryLightDirX.delete(0, END)
    entryLightDirX.insert(0, lightsDir[current][0])
    entryLightDirY.delete(0, END)
    entryLightDirY.insert(0, lightsDir[current][1])
    entryLightDirZ.delete(0, END)
    entryLightDirZ.insert(0, lightsDir[current][2])

    entryLightColR.delete(0, END)
    entryLightColR.insert(0, lightsCol[current][0])
    entryLightColG.delete(0, END)
    entryLightColG.insert(0, lightsCol[current][1])
    entryLightColB.delete(0, END)
    entryLightColB.insert(0, lightsCol[current][1])

    activeLight.set(lightsActive[current])
    print lightsType[current]

def changeParametersScene():
    global objectPos, objectRot, objectSca, sceneWindowSize

    if len(entrySceneOBJPosX.get()) != 0:
        objectPos[0]= float(entrySceneOBJPosX.get())
    if len(entrySceneOBJPosY.get()) != 0:
        objectPos[1]= float(entrySceneOBJPosY.get())
    if len(entrySceneOBJPosZ.get()) != 0:
        objectPos[2]= float(entrySceneOBJPosZ.get())

    if len(entrySceneOBJRotX.get()) != 0:
        objectRot[0]= float(entrySceneOBJRotX.get())
    if len(entrySceneOBJRotY.get()) != 0:
        objectRot[1]= float(entrySceneOBJRotY.get())
    if len(entrySceneOBJRotZ.get()) != 0:
        objectRot[2]= float(entrySceneOBJRotZ.get())

    if len(entrySceneOBJScaX.get()) != 0:
        objectSca[0]= float(entrySceneOBJScaX.get())
    if len(entrySceneOBJScaY.get()) != 0:
        objectSca[1]= float(entrySceneOBJScaY.get())
    if len(entrySceneOBJScaZ.get()) != 0:
        objectSca[2]= float(entrySceneOBJScaZ.get())

    if len(entrySceneWindowSizeX.get()) != 0:
        sceneWindowSize[0] = float(entrySceneWindowSizeX.get())
    if len(entrySceneWindowSizeY.get()) != 0:
        sceneWindowSize[1] = float(entrySceneWindowSizeY.get())

    updateParametersScene()

def updateParametersScene():
    entrySceneOBJPosX.delete(0, END)
    entrySceneOBJPosX.insert(0, objectPos[0])
    entrySceneOBJPosY.delete(0, END)
    entrySceneOBJPosY.insert(0, objectPos[1])
    entrySceneOBJPosZ.delete(0, END)
    entrySceneOBJPosZ.insert(0, objectPos[2])

    entrySceneOBJRotX.delete(0, END)
    entrySceneOBJRotX.insert(0, objectRot[0])
    entrySceneOBJRotY.delete(0, END)
    entrySceneOBJRotY.insert(0, objectRot[1])
    entrySceneOBJRotZ.delete(0, END)
    entrySceneOBJRotZ.insert(0, objectRot[2])

    entrySceneOBJScaX.delete(0, END)
    entrySceneOBJScaX.insert(0, objectSca[0])
    entrySceneOBJScaY.delete(0, END)
    entrySceneOBJScaY.insert(0, objectSca[1])
    entrySceneOBJScaZ.delete(0, END)
    entrySceneOBJScaZ.insert(0, objectSca[2])

    entrySceneWindowSizeX.delete(0, END)
    entrySceneWindowSizeX.insert(0, sceneWindowSize[0])
    entrySceneWindowSizeY.delete(0, END)
    entrySceneWindowSizeY.insert(0, sceneWindowSize[1])

def simpleCaptures():
    aux = camPointingForward.get()
    aux1 = camerapos[2]
    aux2 = camerapos[0]
    aux3 = camerapos[1]
    camPointingForward.set(1)
    camerapos[2] = 0.0000000001
    if labelRightToLeft.get() == 1:
        camerapos[0] = sceneWindowSize[0]
    else:
        camerapos[0] = sceneWindowSize[0]*-1
    if labelUpwards.get() == 1:
        camerapos[1] = sceneWindowSize[1] * -1
    else:
        camerapos[1] = sceneWindowSize[1]
    captures()
    camPointingForward.set(aux)
    camerapos[2] = aux1
    camerapos[0] = aux2
    camerapos[1] = aux3
    #glTranslatef(-2.0, -1.5, -5)

def changeParametersAcquisition():
    global imageResolution, holoDimensions, capturesNumber, fieldOf

    if len(entryAcquisitionResolutionX.get()) != 0:
        imageResolution[0]= int(entryAcquisitionResolutionX.get())
    if len(entryAcquisitionResolutionY.get()) != 0:
        imageResolution[1]= int(entryAcquisitionResolutionY.get())

    if len(entryAcquisitionHologramDimensionsX.get()) != 0:
        holoDimensions[0]= float(entryAcquisitionHologramDimensionsX.get())
        sceneWindowSize[0] = holoDimensions[0]/2.0
    if len(entryAcquisitionHologramDimensionsY.get()) != 0:
        holoDimensions[1]= float(entryAcquisitionHologramDimensionsY.get())
        sceneWindowSize[1] = holoDimensions[1]/2.0

    if len(entryAcquisitionCapturesNumberX.get()) != 0:
        capturesNumber[0]= int(entryAcquisitionCapturesNumberX.get())
    if len(entryAcquisitionCapturesNumberY.get()) != 0:
        capturesNumber[1]= int(entryAcquisitionCapturesNumberY.get())
    quit()
    capturing = True
    if len(entryCameraFieldOfView.get()) != 0:
        fieldOf = float(entryCameraFieldOfView.get())
    init(8)
    updateParametersAcquisition()

def updateParametersAcquisition():
    #computeCameraPlaneDimensions()
    entryAcquisitionResolutionX.delete(0, END)
    entryAcquisitionResolutionX.insert(0, imageResolution[0])
    entryAcquisitionResolutionY.delete(0, END)
    entryAcquisitionResolutionY.insert(0, imageResolution[1])

    entryAcquisitionHologramDimensionsX.delete(0, END)
    entryAcquisitionHologramDimensionsX.insert(0, holoDimensions[0])
    entryAcquisitionHologramDimensionsY.delete(0, END)
    entryAcquisitionHologramDimensionsY.insert(0, holoDimensions[1])

    entryAcquisitionCapturesNumberX.delete(0, END)
    entryAcquisitionCapturesNumberX.insert(0, capturesNumber[0])
    entryAcquisitionCapturesNumberY.delete(0, END)
    entryAcquisitionCapturesNumberY.insert(0, capturesNumber[1])

    entryCameraFieldOfView.delete(0, END)
    entryCameraFieldOfView.insert(0, fieldOf)

def changeParametersSampling():
    global holoPlaneDimensions, camPlaneDimensions, holoCamPlaneDistance, samplingCaptures, writingFOV

    if len(entrySamplingHoloPlaneDx.get()) != 0:
        holoPlaneDimensions[0]= float(entrySamplingHoloPlaneDx.get())
    if len(entrySamplingHoloPlaneDy.get()) != 0:
        holoPlaneDimensions[1]= float(entrySamplingHoloPlaneDy.get())

    if len(entrySamplingCameraPlaneDimensionsX.get()) != 0:
        camPlaneDimensions[0]= float(entrySamplingCameraPlaneDimensionsX.get())
    if len(entrySamplingCameraPlaneDimensionsY.get()) != 0:
        camPlaneDimensions[1]= float(entrySamplingCameraPlaneDimensionsY.get())

    if len(entrySamplingHoloPlaneD.get()) != 0:
        holoCamPlaneDistance= float(entrySamplingHoloPlaneD.get())

    if len(entrySamplingCapturesNumberK.get()) != 0:
        samplingCapturesNumber[0] = int(entrySamplingCapturesNumberK.get())
    if len(entrySamplingCapturesNumberL.get()) != 0:
        samplingCapturesNumber[1] = int(entrySamplingCapturesNumberL.get())

    if len(entrySamplingFOVx.get()) != 0:
        writingFOV[0]= float(entrySamplingFOVx.get())
    if len(entrySamplingFOVy.get()) != 0:
        writingFOV[1]= float(entrySamplingFOVy.get())

    updateParametersSampling()

def updateParametersSampling():
    entrySamplingHoloPlaneDx.delete(0, END)
    entrySamplingHoloPlaneDx.insert(0, holoPlaneDimensions[0])
    entrySamplingHoloPlaneDy.delete(0, END)
    entrySamplingHoloPlaneDy.insert(0, holoPlaneDimensions[1])

    entrySamplingHoloPlaneD.delete(0, END)
    entrySamplingHoloPlaneD.insert(0, holoCamPlaneDistance)

    entrySamplingCapturesNumberK.delete(0, END)
    entrySamplingCapturesNumberK.insert(0, samplingCapturesNumber[0])
    entrySamplingCapturesNumberL.delete(0, END)
    entrySamplingCapturesNumberL.insert(0, samplingCapturesNumber[1])

    entrySamplingCameraPlaneDimensionsX.delete(0, END)
    entrySamplingCameraPlaneDimensionsX.insert(0, camPlaneDimensions[0])
    entrySamplingCameraPlaneDimensionsY.delete(0, END)
    entrySamplingCameraPlaneDimensionsY.insert(0, camPlaneDimensions[1])

    entrySamplingFOVx.delete(0, END)
    entrySamplingFOVx.insert(0, writingFOV[0])
    entrySamplingFOVy.delete(0, END)
    entrySamplingFOVy.insert(0, writingFOV[1])

def startCaptures():
    captures()


def loadObject():
    global fileName
    fileName = tkFileDialog.askopenfilename()
    quit()
    init(8)
    entrySceneOBJPath.delete(0, END)
    entrySceneOBJPath.insert(0, fileName)


def changeImagesPath():
    global imagesPath
    imagesPath = tkFileDialog.askdirectory() + "/"
    entryAcquisitionPath.delete(0, END)
    entryAcquisitionPath.insert(0, imagesPath)
    entrySamplingPath.delete(0, END)
    entrySamplingPath.insert(0, imagesPath)

    quit()
    init(8)


changy = 0.1
def changeBackColor():
    global backColor
    global changy
    print backColor
    if backColor[0] < 1:
       print "coli"
       backColor[0] += changy
       backColor[1] += changy
       backColor[2] += changy
       if backColor[0] > 0.9:
           changy = -0.1
       if backColor[0] < 0.2:
           changy = 0.1

labelCamera = Label(lidCamera, text="Cámara")
labelCameraPos = Label(lidCamera, text="Posición inicial")
labelCameraPosX = Label(lidCamera, text="X")
labelCameraPosY = Label(lidCamera, text="Y")
labelCameraPosZ = Label(lidCamera, text="Z")
labelCameraLookAt = Label(lidCamera, text="Mirar a")
labelCameraLookAtX = Label(lidCamera, text="X")
labelCameraLookAtY = Label(lidCamera, text="Y")
labelCameraLookAtZ = Label(lidCamera, text="Z")
labelCameraStepsX = Label(lidCaptures, text="Número de pasos X")
labelCameraStepsY = Label(lidCaptures, text="Número de pasos Y")
labelIncX = Label(lidCaptures, text="Tam. ventana X")
labelIncY = Label(lidCaptures, text="Tam. ventana Y")


labelSceneOBJPath = Label(lidScene, text="Ruta")
labelSceneOBJPos = Label(lidScene, text="Posición del objeto")
labelSceneOBJPosX = Label(lidScene, text="X")
labelSceneOBJPosY = Label(lidScene, text="Y")
labelSceneOBJPosZ = Label(lidScene, text="Z")
labelSceneOBJRot = Label(lidScene, text="Rotación")
labelSceneOBJRotX = Label(lidScene, text="X")
labelSceneOBJRotY = Label(lidScene, text="Y")
labelSceneOBJRotZ = Label(lidScene, text="Z")
labelSceneOBJSca = Label(lidScene, text="Escalamiento")
labelSceneOBJScaX = Label(lidScene, text="X")
labelSceneOBJScaY = Label(lidScene, text="Y")
labelSceneOBJScaZ = Label(lidScene, text="Z")
labelSceneWindow = Label(lidScene, text="Ventana")
labelSceneWindowSizeX = Label(lidScene, text="X")
labelSceneWindowSizeY = Label(lidScene, text="Y")

labelLightPos = Label(lidLight, text="Posicin")
labelLightX = Label(lidLight, text="X")
labelLightY = Label(lidLight, text="Y")
labelLightZ = Label(lidLight, text="Z")
labelLightDir = Label(lidLight, text="Dirección")
labelLightDirX = Label(lidLight, text="X")
labelLightDirY = Label(lidLight, text="Y")
labelLightDirZ = Label(lidLight, text="Z")
labelLightCol = Label(lidLight, text="Color")
labelLightR = Label(lidLight, text="R")
labelLightG = Label(lidLight, text="G")
labelLightB = Label(lidLight, text="B")

labelResolution= Label(lidAcquisition, text="Resolución imagen")
labelResolutionX= Label(lidAcquisition, text="X")
labelResolutionY= Label(lidAcquisition, text="Y")
labelSaveImages= Label(lidAcquisition, text= "Guardar imágenes")
labelSaveImagesPath= Label(lidAcquisition, text="Ruta")
labelHologramDimensions= Label(lidAcquisition, text="Dimensiones holograma")
labelHologramDimensionsX= Label(lidAcquisition, text="X")
labelHologramDimensionsY= Label(lidAcquisition, text="Y")
labelCapturesNumber= Label(lidAcquisition, text="Número de capturas")
labelCapturesNumberX= Label(lidAcquisition, text="X")
labelCapturesNumberY= Label(lidAcquisition, text="Y")
labelCameraParameters= Label(lidAcquisition, text="Parámetros de cámara")
labelCameraFieldOfView = Label(lidAcquisition, text="Campo visual")

labelSamplingFindFOV= Label(lidSampling, text="Hallar FOV-Cámara")
labelSamplingHoloPlaneDimensions= Label(lidSampling, text="Dimensiones plano Holograma")
labelSamplingHoloPlaneDx= Label(lidSampling, text="Dx:")
labelSamplingHoloPlaneDy= Label(lidSampling, text="Dy:")
labelSamplingHoloCameraPlaneDistance= Label(lidSampling, text="Distancia Holograma-Plano Cámara")
labelSamplingHoloCameraPlaneD= Label(lidSampling, text="d:")
labelSamplingFOVCamHor= Label(lidSampling, text="FOV-Cam hor.(°):")
labelSamplingFOVCamVer= Label(lidSampling, text="FOV-Cam ver.(°):")
labelSamplingSaveImages= Label(lidSampling, text= "Guardar imágenes")
labelSamplingSaveImagesPath= Label(lidSampling, text="Ruta")
labelSamplingCapturesNumber= Label(lidSampling, text="Número de capturas")
labelSamplingCapturesNumberK= Label(lidSampling, text="K:")
labelSamplingCapturesNumberL= Label(lidSampling, text="L:")
labelSamplingCameraPlaneDimensions = Label(lidSampling, text="Dimensiones plano cámara")
labelSamplingCameraPlaneDimensionsX = Label(lidSampling, text="X:")
labelSamplingCameraPlaneDimensionsY = Label(lidSampling, text="Y:")
labelSamplingWritingFOVx= Label(lidSampling, text="FOV Escritura                            FOVx(°):")
labelSamplingWritingFOVy= Label(lidSampling, text="                             FOVy(°):")
labelSamplingCapturesDirection= Label(lidSampling, text="Sentido de captura")

#Captures Direction and camera look at Sampling Method
camPointingForward = IntVar()
checkCamPointing = Checkbutton(lidSampling, text="Cámara simple", variable=camPointingForward)
checkCamPointing.grid(row=24, column = 0, sticky=W)
labelSamplingRightToLeft = IntVar()
checkSamplingRightToLeft = Checkbutton(lidSampling, text="Derecha a izquierda", variable=labelSamplingRightToLeft)
checkSamplingRightToLeft.grid(row=24, column = 1, sticky=W)
labelSamplingUpwards = IntVar()
checkSamplingUpwards = Checkbutton(lidSampling, text="Abajo hacia arriba", variable=labelSamplingUpwards)
checkSamplingUpwards.grid(row=25, column = 0, sticky=W)
labelSamplingVerPivot = IntVar()
checkSamplingPivot = Checkbutton(lidSampling, text="Pivoteo Vertical", variable=labelSamplingVerPivot)
checkSamplingPivot.grid(row=25, column = 1, sticky=W)

#Display camera and holo planes
labelSamplingCamPlane = IntVar()
checkSamplingCamPlane = Checkbutton(lidSampling, text="Mostrar plano cámara", variable=labelSamplingCamPlane)
checkSamplingCamPlane.grid(row=21, column = 0, sticky=W)
labelSamplingHoloPlane = IntVar()
checkSamplingHoloPlane = Checkbutton(lidSampling, text="Mostrar plano holograma", variable=labelSamplingHoloPlane)
checkSamplingHoloPlane.grid(row=21, column = 1, sticky=W)


#Captures Direction Simple Method
labelRightToLeft = IntVar()
checkRightToLeft = Checkbutton(lidAcquisition, text="Derecha a izquierda", variable=labelRightToLeft)
checkRightToLeft.grid(row=17, sticky=W)
labelUpwards = IntVar()
checkUpwards = Checkbutton(lidAcquisition, text="Abajo hacia arriba", variable=labelUpwards)
checkUpwards.grid(row=18, sticky=W)
labelVerPivot = IntVar()
checkPivot = Checkbutton(lidAcquisition, text="Pivoteo Vertical", variable=labelVerPivot)
checkPivot.grid(row=19, sticky=W)



options = ["Fuente 1", "Fuente 2", "Fuente 3", "Fuente 4", "Fuente 5",
           "Fuente 6", "Fuente 7", "Fuente 8"]

currentSource = StringVar(lidLight)
currentSource.set(options[0]) # initial value

lightSourcesMenu = OptionMenu(lidLight, currentSource, *options, command=updateParametersLight)
lightSourcesMenu.grid(row=0, column=0, sticky=W)

sourceType = StringVar(lidLight)
sourceType.set("Puntual") # initial value

lightSourcesTypeMenu = OptionMenu(lidLight, sourceType,  "Puntual", "Spotlight")
lightSourcesTypeMenu.grid(row=0, column=1, sticky=W)

entrySceneOBJPath = Entry(lidScene)
entrySceneOBJPosX = Entry(lidScene)
entrySceneOBJPosY = Entry(lidScene)
entrySceneOBJPosZ = Entry(lidScene)
entrySceneOBJRotX = Entry(lidScene)
entrySceneOBJRotY = Entry(lidScene)
entrySceneOBJRotZ = Entry(lidScene)
entrySceneOBJScaX = Entry(lidScene)
entrySceneOBJScaY = Entry(lidScene)
entrySceneOBJScaZ = Entry(lidScene)
entrySceneWindowSizeX = Entry(lidScene)
entrySceneWindowSizeY = Entry(lidScene)

entryCameraPosX =  Entry(lidCamera)
entryCameraPosY =  Entry(lidCamera)
entryCameraPosZ =  Entry(lidCamera)
entryCameraLookAtX =  Entry(lidCamera)
entryCameraLookAtY =  Entry(lidCamera)
entryCameraLookAtZ =  Entry(lidCamera)
entryCameraStepsX = Entry(lidCaptures)
entryCameraStepsY = Entry(lidCaptures)
entryCameraIncX = Entry(lidCaptures)
entryCameraIncY = Entry(lidCaptures)

entryLightPosX =  Entry(lidLight)
entryLightPosY =  Entry(lidLight)
entryLightPosZ =  Entry(lidLight)
entryLightDirX =  Entry(lidLight)
entryLightDirY =  Entry(lidLight)
entryLightDirZ =  Entry(lidLight)
entryLightColR =  Entry(lidLight)
entryLightColG =  Entry(lidLight)
entryLightColB =  Entry(lidLight)

entryAcquisitionResolutionX = Entry(lidAcquisition)
entryAcquisitionResolutionY = Entry(lidAcquisition)
entryAcquisitionPath = Entry(lidAcquisition)
entryAcquisitionHologramDimensionsX = Entry(lidAcquisition)
entryAcquisitionHologramDimensionsY = Entry(lidAcquisition)
entryAcquisitionCapturesNumberX = Entry(lidAcquisition)
entryAcquisitionCapturesNumberY = Entry(lidAcquisition)
entryCameraFieldOfView =  Entry(lidAcquisition)

entrySamplingHoloPlaneDx = Entry(lidSampling)
entrySamplingHoloPlaneDy = Entry(lidSampling)
entrySamplingHoloPlaneD = Entry(lidSampling)
entrySamplingFOVCamHor = Entry(lidSampling)
entrySamplingFOVCamVer = Entry(lidSampling)
entrySamplingPath = Entry(lidSampling)
entrySamplingCapturesNumberK = Entry(lidSampling)
entrySamplingCapturesNumberL = Entry(lidSampling)
entrySamplingCameraPlaneDimensionsX = Entry(lidSampling)
entrySamplingCameraPlaneDimensionsY = Entry(lidSampling)
entrySamplingFOVx = Entry(lidSampling)
entrySamplingFOVy = Entry(lidSampling)

labelSceneOBJPath.grid(row=1, column=0, sticky=W)
labelSceneOBJPos.grid(row=3, column=0, sticky=W)
labelSceneOBJPosX.grid(row=4, column=0, sticky=E)
labelSceneOBJPosY.grid(row=5, column=0, sticky=E)
labelSceneOBJPosZ.grid(row=6, column=0, sticky=E)
labelSceneOBJRot.grid(row=7, column=0, sticky=W)
labelSceneOBJRotX.grid(row=8, column=0, sticky=E)
labelSceneOBJRotY.grid(row=9, column=0, sticky=E)
labelSceneOBJRotZ.grid(row=10, column=0, sticky=E)
labelSceneOBJSca.grid(row=11, column=0, sticky=W)
labelSceneOBJScaX.grid(row=12, column=0, sticky=E)
labelSceneOBJScaY.grid(row=13, column=0, sticky=E)
labelSceneOBJScaZ.grid(row=14, column=0, sticky=E)
labelSceneWindow.grid(row=15, column=0, sticky=W)
labelSceneWindowSizeX.grid(row=16, column=0, sticky=E)
labelSceneWindowSizeY.grid(row=17, column=0, sticky=E)

labelResolution.grid(row=0, column=0, sticky=W)
labelResolutionX.grid(row=1, column=0, sticky=E)
labelResolutionY.grid(row=2, column=0, sticky=E)
ttk.Label(lidAcquisition, text= "").grid(row=3, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=3, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=3, column = 1, columnspan=5, sticky= "ew")
labelSaveImages.grid(row=4, column=0, sticky=W)
labelSaveImagesPath.grid(row=5, column=0, sticky=E)
ttk.Label(lidAcquisition, text= "").grid(row=6, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=6, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=6, column = 1, columnspan=5, sticky= "ew")
labelHologramDimensions.grid(row=7, column=0, sticky=W)
labelHologramDimensionsX.grid(row=8, column=0, sticky=E)
labelHologramDimensionsY.grid(row=9, column=0, sticky=E)
ttk.Label(lidAcquisition, text= "").grid(row=10, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=10, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=10, column = 1, columnspan=5, sticky= "ew")
labelCapturesNumber.grid(row=11, column=0, sticky=W)
labelCapturesNumberX.grid(row=12, column=0, sticky=E)
labelCapturesNumberY.grid(row=13, column=0, sticky=E)
ttk.Label(lidAcquisition, text= "").grid(row=14, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=14, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidAcquisition,orient=HORIZONTAL).grid(row=14, column = 1, columnspan=5, sticky= "ew")
labelCameraParameters.grid(row=15, column=0, sticky="nw")
labelCameraFieldOfView.grid(row=16, column=0, sticky="nw")

labelSamplingFindFOV.grid(row=0, column=0, sticky=W)
labelSamplingHoloPlaneDimensions.grid(row=1, column=0, sticky=W)
labelSamplingHoloPlaneDx.grid(row=2, column=0, sticky=E)
labelSamplingHoloPlaneDy.grid(row=3, column=0, sticky=E)
labelSamplingHoloCameraPlaneDistance.grid(row=4, column=0, sticky=W)
labelSamplingHoloCameraPlaneD.grid(row=5, column=0, sticky=E)
labelSamplingFOVCamHor.grid(row=7, column=0, sticky=E)
labelSamplingFOVCamVer.grid(row=8, column=0, sticky=E)
ttk.Label(lidSampling, text= "").grid(row=9, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=9, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=9, column = 1, columnspan=5, sticky= "ew")
labelSamplingSaveImages.grid(row=10, column=0, sticky=W)
labelSamplingSaveImagesPath.grid(row=11, column=0, sticky=E)
ttk.Label(lidSampling, text= "").grid(row=12, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=12, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=12, column = 1, columnspan=5, sticky= "ew")
labelSamplingCapturesNumber.grid(row=13, column=0, sticky=W)
labelSamplingCapturesNumberK.grid(row=14, column=0, sticky=E)
labelSamplingCapturesNumberL.grid(row=15, column=0, sticky=E)
labelSamplingCameraPlaneDimensions.grid(row=16, column=0, sticky=W)
labelSamplingCameraPlaneDimensionsX.grid(row=17, column=0, sticky=E)
labelSamplingCameraPlaneDimensionsY.grid(row=18, column=0, sticky=E)
labelSamplingWritingFOVx.grid(row=19, column=0, sticky=W)
labelSamplingWritingFOVy.grid(row=20, column=0, sticky=E)
ttk.Label(lidSampling, text= "").grid(row=22, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=22, column = 0, columnspan=5, sticky= "ew")
ttk.Separator(lidSampling,orient=HORIZONTAL).grid(row=22, column = 1, columnspan=5, sticky= "ew")
labelSamplingCapturesDirection.grid(row=23, column=0, sticky=W)

labelCamera.grid(row=0, column=0, sticky=W)
labelCameraPos.grid(row=1, column=0, sticky=E)
labelCameraPosX.grid(row=2, column=0, sticky=E)
labelCameraPosY.grid(row=3, column=0, sticky=E)
labelCameraPosZ.grid(row=4, column=0, sticky=E)
labelCameraLookAt.grid(row=5, column=0, sticky=W)
labelCameraLookAtX.grid(row=6, column=0, sticky=E)
labelCameraLookAtY.grid(row=7, column=0, sticky=E)
labelCameraLookAtZ.grid(row=8, column=0, sticky=E)
labelCameraStepsX.grid(row=0, column=0, sticky=W)
labelCameraStepsY.grid(row=1, column=0, sticky=W)
labelIncX.grid(row=2, column=0, sticky=W)
labelIncY.grid(row=3, column=0, sticky=W)

labelLightPos.grid(row=1, column=0, sticky=W)
labelLightX.grid(row=2, column=0, sticky=E)
labelLightY.grid(row=3, column=0, sticky=E)
labelLightZ.grid(row=4, column=0, sticky=E)
labelLightDir.grid(row=5, column=0, sticky=W)
labelLightDirX.grid(row=6, column=0, sticky=E)
labelLightDirY.grid(row=7, column=0, sticky=E)
labelLightDirZ.grid(row=8, column=0, sticky=E)
labelLightCol.grid(row=9, column=0, sticky=W)
labelLightR.grid(row=10, column=0, sticky=E)
labelLightG.grid(row=11, column=0, sticky=E)
labelLightB.grid(row=12, column=0, sticky=E)

entrySceneOBJPath.grid(row=1, column=1, sticky=W)
entrySceneOBJPosX.grid(row=4, column=1, sticky=W)
entrySceneOBJPosY.grid(row=5, column=1, sticky=W)
entrySceneOBJPosZ.grid(row=6, column=1, sticky=W)
entrySceneOBJRotX.grid(row=8, column=1, sticky=W)
entrySceneOBJRotY.grid(row=9, column=1, sticky=W)
entrySceneOBJRotZ.grid(row=10, column=1, sticky=W)
entrySceneOBJScaX.grid(row=12, column=1, sticky=W)
entrySceneOBJScaY.grid(row=13, column=1, sticky=W)
entrySceneOBJScaZ.grid(row=14, column=1, sticky=W)
entrySceneWindowSizeX.grid(row=16, column=1, sticky=W)
entrySceneWindowSizeY.grid(row=17, column=1, sticky=W)

entryAcquisitionResolutionX.grid(row=1, column=1, sticky=W)
entryAcquisitionResolutionY.grid(row=2, column=1, sticky=W)
entryAcquisitionPath.grid(row=5, column=1, sticky=W)
entryAcquisitionHologramDimensionsX.grid(row=8, column=1, sticky=W)
entryAcquisitionHologramDimensionsY.grid(row=9, column=1, sticky=W)
entryAcquisitionCapturesNumberX.grid(row=12, column=1, sticky=W)
entryAcquisitionCapturesNumberY.grid(row=13, column=1, sticky=W)
entryCameraFieldOfView.grid(row=16, column=1, sticky="nw")

entrySamplingHoloPlaneDx.grid(row=2, column=1, sticky=W)
entrySamplingHoloPlaneDy.grid(row=3, column=1, sticky=W)
entrySamplingHoloPlaneD.grid(row=5, column=1, sticky=W)
entrySamplingFOVCamHor.grid(row=7, column=1, sticky=W)
entrySamplingFOVCamVer.grid(row=8, column=1, sticky=W)
entrySamplingPath.grid(row=11, column=1, sticky=W)
entrySamplingCapturesNumberK.grid(row=14, column=1, sticky=W)
entrySamplingCapturesNumberL.grid(row=15, column=1, sticky=W)
entrySamplingCameraPlaneDimensionsX.grid(row=17, column=1, sticky=W)
entrySamplingCameraPlaneDimensionsY.grid(row=18, column=1, sticky=W)
entrySamplingFOVx.grid(row=19, column=1, sticky=W)
entrySamplingFOVy.grid(row=20, column=1, sticky=W)

entryCameraPosX.grid(row=2, column=1, sticky=W)
entryCameraPosY.grid(row=3, column=1, sticky=W)
entryCameraPosZ.grid(row=4, column=1, sticky=W)
entryCameraLookAtX.grid(row=6, column=1, sticky=W)
entryCameraLookAtY.grid(row=7, column=1, sticky=W)
entryCameraLookAtZ.grid(row=8, column=1, sticky=W)
entryCameraStepsX.grid(row=0, column=1, sticky=W)
entryCameraStepsY.grid(row=1, column=1, sticky=W)
entryCameraIncX.grid(row=2, column=1, sticky=W)
entryCameraIncY.grid(row=3, column=1, sticky=W)

entryLightPosX.grid(row=2, column=1, sticky=W)
entryLightPosY.grid(row=3, column=1, sticky=W)
entryLightPosZ.grid(row=4, column=1, sticky=W)
entryLightDirX.grid(row=6, column=1, sticky=W)
entryLightDirY.grid(row=7, column=1, sticky=W)
entryLightDirZ.grid(row=8, column=1, sticky=W)
entryLightColR.grid(row=10, column=1, sticky=W)
entryLightColG.grid(row=11, column=1, sticky=W)
entryLightColB.grid(row=12, column=1, sticky=W)


activeLight = IntVar()
checkActiveLight = Checkbutton(lidLight, text="Activar", variable=activeLight)
checkActiveLight.grid(row=19, sticky=W)
dWindow = IntVar()
checkWindow = Checkbutton(lidScene, text="Ventana", variable=dWindow)
checkWindow.grid(row=18, sticky=W)
dGrid = IntVar()
checkGrid = Checkbutton(lidScene, text="Malla", variable=dGrid)
checkGrid.grid(row=19, sticky=W)


buttonLidlight = Button(lidLight,text = 'Actualizar fuente actual', command = changeParametersLight)
buttonLidlight.grid(row=20, sticky=W)

buttonLidCaptures = Button(lidCaptures,text = 'Actualizar', command = changeParametersCaptures)
buttonLidCaptures.grid(row=10, sticky=W)

buttonLidCamera = Button(lidCamera,text = 'Actualizar', command = changeParameters)
buttonLidCamera.grid(row=10, sticky=W)
buttonLidCameraCap = Button(lidCamera,text = 'Realizar capturas', command = startCaptures)
buttonLidCameraCap.grid(row=13, sticky=W)

buttonLidScene = Button(lidScene,text = 'Fondo', command = changeBackColor)
buttonLidScene.grid(row=20, sticky=W)
buttonLidScene = Button(lidScene,text = 'Actualizar', command = changeParametersScene)
buttonLidScene.grid(row=21, sticky=W)
buttonLidSceneLoadObject = Button(lidScene,text = 'Cargar objeto', command = loadObject)
buttonLidSceneLoadObject.grid(row=0, sticky=W)

buttonLidAcquisitionChangePath = Button(lidAcquisition,text = 'Cambiar ruta', command = changeImagesPath)
buttonLidAcquisitionChangePath.grid(row=5, sticky=W)
buttonLidAcquisitionCapture = Button(lidAcquisition,text = 'Realizar capturas', command = simpleCaptures)
buttonLidAcquisitionCapture.grid(row=20, column = 0, sticky=W)
buttonLidAcquisitionUpdate = Button(lidAcquisition,text = 'Actualizar', command = changeParametersAcquisition)
buttonLidAcquisitionUpdate.grid(row=20, column = 1, sticky=W)

def FOVCameraOpt():
    h = holoCamPlaneDistance
    Dx = holoPlaneDimensions[0]
    Dy = holoPlaneDimensions[1]

    fovHor = math.degrees(2*math.atan((8*h*Dx)/(16*(h**2)-Dx**2)))

    betaFactorNum = 2*(6**(1.0/3.0)*h**2) - ( (81*Dx**2*h**4 + 48*h**6)**(1.0/2.0) - 9*Dx*h**2)**(2.0/3.0)
    betaFactorDen = 6**(2.0/3.0)*( (81*Dx**2*h**4 + 48*h**6)**(1.0/2.0) - 9*Dx*h**2)**(1.0/3.0)
    betaFactor = betaFactorNum/betaFactorDen

    fovVer = math.degrees(2*math.atan((Dy*(h**2 + betaFactor**2)**(1.0/2.0) ) / (2*(h**2 + betaFactor**2 - (betaFactor*Dx)/2)) ))

    print "dx: ", Dx
    print "dy: ", Dy
    print "distancia(h): ", h
    print "fovHor: ", fovHor
    print "fovVer: ", fovVer

def computeCameraPlaneDimensions():
    global camPlaneDimensions

    camPlaneDimensions[0] = computeCameraPlaneSide(holoPlaneDimensions[0], writingFOV[0])
    camPlaneDimensions[1] = computeCameraPlaneSide(holoPlaneDimensions[1], writingFOV[1])
    camWindowSize[0] = camPlaneDimensions[0]/2.0
    camWindowSize[1] = camPlaneDimensions[1]/2.0
    print camPlaneDimensions

def computeCameraPlaneSide(dx,writingFOV):
    l = dx/(2*math.tan(math.radians(writingFOV/2.0)))
    print "l: ", l
    x = holoCamPlaneDistance - l
    print "x: ", x
    return 2*x*math.tan(math.radians(writingFOV/2.0))



def samplingPreview():
    x=0
def samplingCaptures():
    aux1 = camerapos[2]
    aux2 = camerapos[0]
    aux3 = camerapos[1]
    camerapos[2] = holoCamPlaneDistance
    if labelSamplingRightToLeft.get() == 1:
        camerapos[0] = camWindowSize[0]
    else:
        camerapos[0] = camWindowSize[0]*-1
    if labelSamplingUpwards.get() == 1:
        camerapos[1] = camWindowSize[1] * -1
    else:
        camerapos[1] = camWindowSize[1]
    print camerapos
    captures(True)
    camerapos[2] = aux1
    camerapos[0] = aux2
    camerapos[1] = aux3



buttonLidSamplingFOVCamera = Button(lidSampling,text = 'FOV-Cámara Opt.', command = FOVCameraOpt)
buttonLidSamplingFOVCamera.grid(row=6, column = 0, sticky=E)
buttonLidSamplingUpdate = Button(lidSampling,text = 'Actualizar', command = changeParametersSampling)
buttonLidSamplingUpdate.grid(row=26, column = 0, sticky=W)
buttonLidSamplingPreview = Button(lidSampling,text = 'Vista previa', command = samplingPreview)
buttonLidSamplingPreview.grid(row=26, column = 1, sticky=W)
buttonLidSamplingCapture = Button(lidSampling,text = 'Capturar imágenes', command = samplingCaptures)
buttonLidSamplingCapture.grid(row=27, column = 0, sticky=W)
buttonLidSamplingChangePath = Button(lidSampling,text = 'Cambiar ruta', command = changeImagesPath)
buttonLidSamplingChangePath.grid(row=11, column = 0, sticky=W)


Screen = (800,600)
Windowy = glLibWindow(Screen,caption="OpenGL Library Demo: Tutorials.py",multisample=multisample,position=GLLIB_CENTER,vsync=not benchmark)
#init() -> sets up the scene and any necessary variables

camerapos = [-1.0,1.0,3.0]
cameraLookAt = [0.0,0.0,0.0]
cameradis = [0.0,0.0,0.0]
camerarot = [0,0]
cameraradius= 2
camWindowX = 2
camWindowY = 2
stepsX = 10
stepsY = 10
capturing = False
axisView = False
referenceWindowSize = [1.0,1.0]
translationVector = 0
scaling = False

imageResolution = [800, 600]
holoDimensions = [2.0, 2.0]
capturesNumber = [5, 5]
sceneWindowSize = [holoDimensions[0]/2.0,holoDimensions[1]/2.0]

holoPlaneDimensions = [2.0, 2.0]
camPlaneDimensions = [2.0, 2.0]
holoWindowSize = [holoPlaneDimensions[0]/2.0,holoPlaneDimensions[1]/2.0]
camWindowSize = [camPlaneDimensions[0]/2.0,camPlaneDimensions[1]/2.0]
holoCamPlaneDistance = 10.0
samplingCapturesNumber = [5,5]
writingFOV = [20.0,20.0]

updateParametersAcquisition()
updateParametersSampling()

objectPos = [0,0,0]
objectRot = [0,0,0]
objectSca = [1,1,1]

lightsPos = [[-1.0,1.0,3.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],
                [0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]

lightsDir = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],
                [0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]

lightsCol = [[1.0,1.0,1.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],
                [0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]

lightsActive= [1,0,0,0,0,0,0,0]
lightsType= [0,0,0,0,0,0,0,0]

backColor = [0.1,0.1,0.1]

dialogOptions = {}
dialogOptions['defaultextension'] = ''
dialogOptions['filetypes'] = []
dialogOptions['initialdir'] = ''
dialogOptions['parent'] = root
dialogOptions['title'] = 'This is a title'

#fileName = tkFileDialog.askopenfilename(**dialogOptions)
fileName = "data/objects/cube.obj"
imagesPath = "Screenshots/"

entrySceneOBJPath.delete(0, END)
entrySceneOBJPath.insert(0, fileName)

entryAcquisitionPath.delete(0, END)
entryAcquisitionPath.insert(0, imagesPath)
entrySamplingPath.delete(0, END)
entrySamplingPath.insert(0, imagesPath)

Light1 = 8

updateParametersScene()

def init(frame):
    global View3D, Plane, Screen, Windowy, camerapos, cameraLookAt, cameradis,camerarot, fieldOf, wind, Spaceship, SpaceshipRotation, Light1, Light2,Light3,Light4,Light5,Light6,Light7,Light8, drawWindow, backColor,colorAugment
    #Creates a view.  This is a perspective view, with a viewport as big
    #as the Screen, an angle of 45 degrees, and some clipping planes.
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),fieldOf,0.0001,800)
    wind = glLibWindow(Screen,caption="OpenGL Library Demo: Tutorials.py",multisample=multisample,position=GLLIB_CENTER,vsync=not benchmark)
    colorAugment = 1
    drawWindow = True
    #cameradis = [0.0,0.0,0.0]


    #Loads a spaceship from:
    #data/objects/Spaceship.obj
    #data/objects/Spaceship.mtl

    FloorTexture = glLibTexture2D("data/grid4.png",[0,0,540,720],GLLIB_RGBA,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    Plane = glLibPlane(5,(0,1,0),FloorTexture,10)


    Spaceship = glLibObject(fileName,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    #Spaceship = glLibObject("data/objects/cube.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    #Build a display list from the data
    Spaceship.build_list()
    #Build a vertex buffer object from the data
    if GLLIB_VBO_AVAILABLE: Spaceship.build_vbo()

    #Plane = glLibPlane(2,(0,1,0))

    #After this tutorial, it is assumed
    #Vertex Buffer Objects are available.
    #Future tutorials will crash if it is
    #NOT available.  Install both NumPy
    #and Numeric for best results.

    #Variable for the spaceship's rotation
    SpaceshipRotation = [0,0]

    #Enable lighting
    glEnable(GL_LIGHTING)
    #Instance of a light.
    Light1 = glLibLight(1)
    #Set the position to be far overhead
    Light1.set_pos(lightsPos[0])
    #Make it a point light.  This is important!
    Light1.set_type(GLLIB_POINT_LIGHT)
    #Light1.set_atten(1.0,0.0,1.0)
    Light1.set_diffuse(lightsCol[0])
    Light1.set_specular(lightsCol[0])
    #Enable the light
    if lightsActive[0] == 1:
        Light1.enable()

    #Instance of a light.
    Light2 = glLibLight(2)
    #Set the position to be far overhead
    Light2.set_pos(lightsPos[1])
    #Make it a point light.  This is important!
    Light2.set_type(GLLIB_POINT_LIGHT)
    Light2.set_diffuse(lightsCol[1])
    Light2.set_specular(lightsCol[1])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[1] == 1:
        Light2.enable()

    Light3 = glLibLight(3)
    Light3.set_pos(lightsPos[2])
    Light3.set_type(GLLIB_POINT_LIGHT)
    Light3.set_diffuse(lightsCol[2])
    Light3.set_specular(lightsCol[2])
    #Light3.set_atten(1,0.0,1)
    #Make a spotlight.  Note the light_spot(...) requirement
    #in the shader below.  First, set the direction as a
    #normalized vector.  Then, make the spotlight have an
    #angle of 10 degrees (default 180; not a spotlight).
    #Then make the exponent of the spotlight.  The result is
    #a green light that projects a cone that, because it is
    #tilted, intersects the plane in an ellipse with softened
    #edges.
    if lightsType[2] == 1:
        Light3.set_spot_dir(normalize([0-lightsDir[2][0],0-lightsDir[2][1],0-lightsDir[2][2]]))
        Light3.set_spot_angle(45.0)
        Light3.set_spot_ex(0.5)
    Light3.enable()

    #Instance of a light.
    Light4 = glLibLight(4)
    #Set the position to be far overhead
    Light4.set_pos(lightsPos[3])
    #Make it a point light.  This is important!
    Light4.set_type(GLLIB_POINT_LIGHT)
    Light4.set_diffuse(lightsCol[3])
    Light4.set_specular(lightsCol[3])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[3] == 1:
        Light4.enable()

    #Instance of a light.
    Light5 = glLibLight(5)
    #Set the position to be far overhead
    Light5.set_pos(lightsPos[4])
    #Make it a point light.  This is important!
    Light5.set_type(GLLIB_POINT_LIGHT)
    Light5.set_diffuse(lightsCol[4])
    Light5.set_specular(lightsCol[4])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[4] == 1:
        Light5.enable()

    #Instance of a light.
    Light6 = glLibLight(5)
    #Set the position to be far overhead
    Light6.set_pos(lightsPos[5])
    #Make it a point light.  This is important!
    Light6.set_type(GLLIB_POINT_LIGHT)
    Light6.set_diffuse(lightsCol[5])
    Light6.set_specular(lightsCol[5])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[5] == 1:
        Light6.enable()

    #Instance of a light.
    Light7 = glLibLight(7)
    #Set the position to be far overhead
    Light7.set_pos(lightsPos[6])
    #Make it a point light.  This is important!
    Light7.set_type(GLLIB_POINT_LIGHT)
    Light7.set_diffuse(lightsCol[6])
    Light7.set_specular(lightsCol[6])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[6] == 1:
        Light7.enable()

    #Instance of a light.
    Light8 = glLibLight(8)
    #Set the position to be far overhead
    Light8.set_pos(lightsPos[7])
    #Make it a point light.  This is important!
    Light8.set_type(GLLIB_POINT_LIGHT)
    Light8.set_diffuse(lightsCol[7])
    Light8.set_specular(lightsCol[7])
    #Light2.set_atten(1.0,0.0,1.0)
    #Enable the light
    if lightsActive[7] == 1:
        Light8.enable()


    #Call the get_rel function to set it equal to
    #0 the next time it is called in GetInput()
    pygame.mouse.get_rel()

#quit() -> called at exit; cleans up
def quit():
    global Light1, Light2,Light3,Light4,Light5,Light6,Light7,Light8, Spaceship
    #Disable lighting
    glDisable(GL_LIGHTING)
    #Delete the light
    del Light1
    del Light2
    del Light3
    del Light4
    del Light5
    del Light6
    del Light7
    del Light8
    #Delete the spaceship's vertex buffer
    #objects so no exception is thrown
    if GLLIB_VBO_AVAILABLE: del Spaceship



#GetInput() -> handle's the user's input
def GetInput():
    #Get the relative motion and button state of the mouse
    global camerarot, cameraradius, capturing, translationVector, axisView, objectPos
    global scaling


    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        #Pressing the "X" on the window exits the demo
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        #ESCAPE returns to menu
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
        if event.type == KEYDOWN and event.key == K_p:
            drawPlane = True
        if event.type == KEYDOWN and event.key == K_o:
            drawPlane = False

        if event.type == KEYDOWN and event.key == K_b:
            print "colo"
            if backColor[0] < 255:
               print "coli"
               backColor[0] += 0.1
               backColor[1] += 0.1
               backColor[2] += 0.1
        if event.type == KEYDOWN and event.key == K_v:
            if backColor[0] > 0:
               backColor[0] -= 0.1
               backColor[1] -= 0.1
               backColor[2] -= 0.1
        if event.type == KEYDOWN and event.key == K_s and (key[K_LCTRL] or key[K_RCTRL]):
            captures()
        if event.type == KEYDOWN and event.key == K_s:
            scaling = not scaling
        if event.type == KEYDOWN and event.key == K_1 and (key[K_LCTRL] or key[K_RCTRL]):
            #Top
            axisView = not axisView
            translationVector = 1
            camerapos[0] = 0
            camerapos[1] = 3
            camerapos[2] = 0
            translationVector = 0
        if event.type == KEYDOWN and event.key == K_2 and (key[K_LCTRL] or key[K_RCTRL]):
            #Right
            axisView = not axisView
            translationVector = 2
            camerapos[0] = 3
            camerapos[1] = 0
            camerapos[2] = 0
        if event.type == KEYDOWN and event.key == K_3 and (key[K_LCTRL] or key[K_RCTRL]):
            #Front
            axisView = not axisView
            translationVector = 3
            camerapos[0] = 0
            camerapos[1] = 0
            camerapos[2] = 3
        if event.type == KEYDOWN and event.key == K_UP and axisView:
            print "pluc"
            if translationVector == 1:
                print "plic"
                objectPos[2] -= 1/10
            if translationVector == 2:
                print "plac"
                objectPos[1] += 1/10
            if translationVector == 3:
                print "pl0c"
                objectPos[1] += 1/10

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                capturing = False
            if event.button == 4:
                 cameraradius -= 0.1  ##Changes camera position
            if event.button == 5:
                 cameraradius += 0.1

    #If the mouse is pressed, rotate the spaceship
    #by the amount the mouse was moved
    if mpress[0]:
        if not scaling:
            camerarot[0] = clamp(80,-15,camerarot[0]+mrel[1])
            camerarot[1] += mrel[0]
        else:
            var = float(mrel[0])/100
            objectSca[0] += var
            objectSca[2] += var
            objectSca[1] += var
            print var
    if mpress[1]:
        objectRot[0] += mrel[1]
        objectRot[1] += mrel[0]
    if mpress[2]:
        if translationVector == 1:
            objectPos[0] -= float(mrel[0])/100
            objectPos[2] -= float(mrel[1])/100
        if translationVector == 2:
            objectPos[2] -= float(mrel[0])/100
            objectPos[1] -= float(mrel[1])/100
        if translationVector == 3:
            objectPos[0] += float(mrel[0])/100
            objectPos[1] -= float(mrel[1])/100


def captures(sampling = False):
    #camerapos[0] = camerapos[0] - camerapos[0]
    #camerapos[1] = camerapos[1] - camerapos[1]
    #camerapos[2] = camerapos[2] - camerapos[2]
    global cameradis, capturing, imagesPath, holoDimensions, capturesNumber
    print "campos en captures", camerapos
    capturing = True
    Draw(Windowy, False)
    cont = 1
    aux1 = cameradis[0]
    aux2 = cameradis[1]
    displacementX = holoDimensions[0]/float(capturesNumber[0]-1)
    displacementY = holoDimensions[1]/float(capturesNumber[1]-1)
    if sampling:
        print "sampling"
        #It means sampling method will be used and, as such, the displacements depend on the camera plane
        displacementX = camPlaneDimensions[0]/float(samplingCapturesNumber[0]-1)
        displacementY = camPlaneDimensions[1]/float(samplingCapturesNumber[1]-1)

    if (labelVerPivot.get() == 1 and (not sampling)) or (labelSamplingVerPivot.get() == 1 and sampling):
        print("verPi")
        for i in range(capturesNumber[0]):
            for j in range(capturesNumber[1]):
                #print "(" + str(cameradis[0])+ "," +str(cameradis[1]) +  ")"
                drawWindow = False
                Draw(Windowy, False)
                #In glLibMisc
                cont += 1
                #glLibSaveScreenshot("Screenshot"+ str(i)+str(j)+".png")
                print imageResolution
                glLibSaveScreenshot(imagesPath+"/"+str(cont)+".png", resolution=[imageResolution[0],imageResolution[1]])
                if (labelUpwards.get() == 1 and (not sampling)) or (labelSamplingUpwards.get() == 1 and sampling):
                    cameradis[1] += displacementY
                else:
                    cameradis[1] -= displacementY
                #Ship = glLibObject("data/objects/Spaceship.obj",GLLIB_MIPMAP_BLEND,GLLIB_FILTER)
            if (labelRightToLeft.get() == 1 and (not sampling)) or (labelSamplingRightToLeft.get() == 1 and sampling):
                cameradis[0] -= displacementX
            else:
                cameradis[0] += displacementX
            if (labelUpwards.get() == 1 and (not sampling)) or (labelSamplingUpwards.get() == 1 and sampling):
                cameradis[1] -= holoDimensions[1]
            else:
                cameradis[1] += holoDimensions[1]

    else:
        for i in range(capturesNumber[1]):
            for j in range(capturesNumber[0]):
                #print "(" + str(cameradis[0])+ "," +str(cameradis[1]) +  ")"
                drawWindow = False
                Draw(Windowy, False)
                print "cameradis", cameradis
                glLibSaveScreenshot(imagesPath+"/"+str(cont)+".png", resolution=[imageResolution[0],imageResolution[1]])
                cont += 1
                #glLibSaveScreenshot("Screenshot"+ str(i)+str(j)+".png")
                if (labelRightToLeft.get() == 1 and (not sampling)) or (labelSamplingRightToLeft.get() == 1 and sampling):
                    cameradis[0] -= displacementX
                else:
                    cameradis[0] += displacementX
                #Ship = glLibObject("data/objects/Spaceship.obj",GLLIB_MIPMAP_BLEND,GLLIB_FILTER)
            if (labelUpwards.get() == 1 and (not sampling)) or (labelSamplingUpwards.get() == 1 and sampling):
                print("upwar")
                cameradis[1] += displacementY
            else:
                cameradis[1] -= displacementY
            if (labelRightToLeft.get() == 1 and (not sampling)) or (labelSamplingRightToLeft.get() == 1 and sampling):
                print("righto")
                cameradis[0] += holoDimensions[0]
            else:
                cameradis[0] -= holoDimensions[0]
    capturing = False
    cameradis[0] = aux1
    cameradis[1] = aux2


#Draw(Window) -> draws the scene
def Draw(Window,drawPlane=True, drawWindow=True):
    global Light1,Light2,Light3,Light4,Light5,Light6,Light7,Light8, sceneWindowSize
    #Set the window's clear color
    Window.set_clear_color(backColor)
    #Clear the window
    Window.clear()
    #Set the view
    View3D.set_view()



    #Set the camera to (0,3,5) looking at (0,0,0) with a "up" vector pointing up (0,1,0)
    #gluLookAt(0,3,5, 0,0,0, 0,1,0)
    #gluLookAt(1.0,1.0,3.0, 0,0,0, 0,1,0)
    if capturing or axisView:
        if camPointingForward.get() == 1:
            gluLookAt(camerapos[0]+cameradis[0],camerapos[1]+cameradis[1],camerapos[2]+cameradis[2],
                camerapos[0]+cameradis[0],camerapos[1]+cameradis[1],(camerapos[2]+cameradis[2])*-1,
                0,1,0)
        else:
            gluLookAt(camerapos[0]+cameradis[0],camerapos[1]+cameradis[1],camerapos[2]+cameradis[2],
                cameraLookAt[0],cameraLookAt[1],cameraLookAt[2],
                0,1,0)
    #If the program is not making captures, the camera must move inside a sphere
    else:
        cameraposix = [cameraradius*cos(radians(camerarot[1]+90))*cos(radians(camerarot[0])),
                     cameraradius*sin(radians(camerarot[0])),
                     cameraradius*sin(radians(camerarot[1]+90))*cos(radians(camerarot[0]))]
        if camPointingForward.get() == 1:
            gluLookAt(cameraposix[0],cameraposix[1],cameraposix[2],
                cameraposix[0],cameraposix[1],(cameraposix[2])*-1,
                0,1,0)
        else:
            gluLookAt(cameraposix[0],cameraposix[1],cameraposix[2],
                cameraLookAt[0],cameraLookAt[1],cameraLookAt[2],
                0,1,0)
    #Set the light into the scene
    Light1.set()
    Light2.set()
    Light3.set()
    Light4.set()
    Light5.set()
    Light6.set()
    Light7.set()
    Light8.set()

    #####ROTAR EN AMBOS CASOS, MODIFICAR Y VISUALIZAR PERO REGRESAR EL DE LA VISUALIZAR

    #Rotate the spaceship by our rotation amount
    if drawPlane == True:
        glRotatef(SpaceshipRotation[0],0,1,0)
        glRotatef(SpaceshipRotation[1],1,0,0)

    if drawWindow == True and dWindow.get() == 1:
       glDisable(GL_TEXTURE_2D)
       glDisable(GL_LIGHTING)
       glColor3f(1,1,1)
       glPushMatrix()
       glLineWidth(2.0)
       glBegin(GL_LINE_STRIP)
       glVertex3f(sceneWindowSize[0]*-1,sceneWindowSize[1]*-1, 0.0)
       glVertex3f(sceneWindowSize[0],sceneWindowSize[1]*-1, 0.0)
       glVertex3f(sceneWindowSize[0], sceneWindowSize[1], 0.0)
       glVertex3f(sceneWindowSize[0]*-1.0, sceneWindowSize[1], 0.0)
       glVertex3f(sceneWindowSize[0]*-1.0,sceneWindowSize[1]*-1.0, 0.0)
       glEnd();
       glPopMatrix()
       glColor3f(1,1,1)

       glEnable(GL_LIGHTING)
       glEnable(GL_TEXTURE_2D)

    if (not capturing) and labelSamplingCamPlane.get()==1:
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glColor3f(1,1,1)
        glPushMatrix()
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        glVertex3f(camWindowSize[0]*-1,camWindowSize[1]*-1, holoCamPlaneDistance)
        glVertex3f(camWindowSize[0],camWindowSize[1]*-1, holoCamPlaneDistance)
        glVertex3f(camWindowSize[0], camWindowSize[1], holoCamPlaneDistance)
        glVertex3f(camWindowSize[0]*-1.0, camWindowSize[1], holoCamPlaneDistance)
        glVertex3f(camWindowSize[0]*-1.0,camWindowSize[1]*-1.0, holoCamPlaneDistance)
        glEnd();
        glPopMatrix()
        glColor3f(1,1,1)

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

    if (not capturing) and labelSamplingHoloPlane.get()==1:
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glColor3f(1,1,1)
        glPushMatrix()
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        glVertex3f(holoWindowSize[0]*-1,holoWindowSize[1]*-1, 0.0)
        glVertex3f(holoWindowSize[0],holoWindowSize[1]*-1, 0.0)
        glVertex3f(holoWindowSize[0], holoWindowSize[1], 0.0)
        glVertex3f(holoWindowSize[0]*-1.0, holoWindowSize[1], 0.0)
        glVertex3f(holoWindowSize[0]*-1.0,holoWindowSize[1]*-1.0, 0.0)
        glEnd();
        glPopMatrix()
        glColor3f(1,1,1)

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

    if drawPlane == True and dGrid.get() == 1:
       #glDisable(GL_TEXTURE_2D)
       glDisable(GL_LIGHTING)
       Plane.draw()
       glEnable(GL_LIGHTING)
       #glEnable(GL_TEXTURE_2D)

    ###Attempts to draw Axes
    if not capturing:
        w = 0
        h = 0
        tip = 0
        turn = 0

        ORG = [0,0,0]

        XP = [0.5,0,0]
        XN = [-1,0,0]
        YP = [0,0.5,0]
        YN = [0,-1,0]
        ZP = [0,0,0.5]
        ZN = [0,0,-1]
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)

        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3fv(ORG)
        glVertex3fv([1,0,0]) # X axis is red.
        glColor3f(0, 1, 0)
        glVertex3fv(ORG)
        glVertex3fv([0,1,0])  # Y axis is green.
        glColor3f(0, 0, 1)
        glVertex3fv(ORG)
        glVertex3fv([0,0,1])    # z axis is blue.
        glColor3f(1,1,1)
        glEnd()

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(-2.0, -1.5, -5)
        if not axisView:
            glRotatef(tip+camerarot[0], 1, 0, 0)
            glRotatef(turn+camerarot[1],0,1,0)
            #glScalef(0.25, 0.25, 0.25)

        glLineWidth(2.0)

        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3fv(ORG)
        glVertex3fv(XP) # X axis is red.
        glColor3f(0, 1, 0)
        glVertex3fv(ORG)
        glVertex3fv(YP)  # Y axis is green.
        glColor3f(0, 0, 1)
        glVertex3fv(ORG)
        glVertex3fv(ZP)    # z axis is blue.
        glColor3f(1,1,1)
        glEnd()

        """glColor4ub(255, 255, 0, 255)
        glRasterPos3f(1.1f, 0.0f, 0.0f)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, 'x')
        glRasterPos3f(0.0f, 1.1f, 0.0f)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, 'y')
        glRasterPos3f(0.0f, 0.0f, 1.1f)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, 'z')"""
        glPopMatrix()

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

    Light1.draw_as_point()
    Light3.draw_as_point(10)



    glPushMatrix()
    #glLoadIdentity()
    #glTranslatef(0,0,0)
    #Apply object rotation changes
    glRotatef(objectRot[0],1,0,0)
    glRotatef(objectRot[1],0,1,0)
    glRotatef(objectRot[2],0,0,1)

    #Apply position changes
    glTranslatef(objectPos[0],objectPos[1],objectPos[2])
    #Apply scaling changes
    glScalef(objectSca[0],objectSca[1],objectSca[2])
##    Spaceship.draw_arrays() #often slowest, but requires no other functions
##    Spaceship.draw_list() #often faster, but requires .build_list() (line 43)

    #if GLLIB_VBO_AVAILABLE:
    #    Spaceship.draw_vbo() #often fastest, but requires .build_vbo() (line 45)
    #else:

    Spaceship.draw_list()

    glPopMatrix()










    #Light2.draw_as_point(7)
    #Flip the buffer to the screen so that we see it
    Window.flip()

    #red = (255,0,0)
    #plano = pygame.display.get_surface()
    #pygame.draw.rect(plano, red, [222,222,222,222])
    #print plano
"""
    llenar = pygame.display.get_surface()
    WHITM = (255,255,255)
    llenar.fill(WHITM)
    print "poli"
"""

"""def main():
    Screen = (800,600)
    init(Screen)
    #Adjusting multisampling makes most things look nicer.  Breaks some tutorials.
    Window = glLibWindow(Screen,caption="OpenGL Library Demo: Tutorials.py",multisample=multisample,position=GLLIB_CENTER,vsync=not benchmark)

    while True:
        GetInput()
        Draw(Window)
if __name__ == '__main__':
    glLibTestErrors(main)"""

root.update()
def main():
    init(root)
    Clock = pygame.time.Clock()
    if benchmark:
        glLibErrors(False)
    while True:
        GetInput()
        View3D = glLibView3D((0,0,Screen[0],Screen[1]),90,0.1,20)
        Draw(Windowy)
        root.update()
        if benchmark:
            Clock.tick()
            print("fps: %f" % round(Clock.get_fps(),2))
        else:
            Clock.tick(60)
if __name__ == '__main__':
    glLibTestErrors(main)
