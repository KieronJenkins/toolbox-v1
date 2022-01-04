import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

class TB_Window(object):
        
    #constructor​
    def __init__(self):
            
        self.window = "TB_Window"
        self.title = "Toolbox Alpha Build"
        self.size = (400, 400)
            
        # close old window is open
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            
        #create​ new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)

        cmds.columnLayout(adjustableColumn=True)
        
        cmds.separator(height=10)
        cmds.text(self.title)
        cmds.separator(height=10)
        
        #set the linear units - cm is default
        self.sceneMeasurements = cmds.optionMenu(changeCommand=self.changeMeasurements)
        cmds.menuItem(label="Centimetres")
        cmds.menuItem(label="Millimetres")
        cmds.menuItem(label="Metres")
        
        cmds.separator(height=5, style='none')
        
        #Delete history, freeze transforms and centre pivots
        cmds.rowColumnLayout(numberOfRows=1)
        self.deleteHistory = cmds.iconTextButton(align="center", style="iconOnly", image1="cube.xpm", label="cube", imageOverlayLabel="Delete", command=self.deleteHistory )
        self.freezeTransforms = cmds.iconTextButton( style="iconOnly", image1="FreezeTransform.png", label="cube", imageOverlayLabel="Freeze", command=self.freezeTransforms )
        self.centerPivots = cmds.iconTextButton( style="iconOnly", image1="CenterPivot.png", label="cube", imageOverlayLabel="Pivots", command=self.centerPivots )
        self.mergePivots = cmds.iconTextButton( style="iconOnly", image1="polyUnite.png", label="cube", imageOverlayLabel="Merge", command=self.mergePivots )
        self.edgeLoop = cmds.iconTextButton( style="iconOnly", image1="polySplitEdgeRing.png", label="cube", imageOverlayLabel="EL Tool", command=self.edgeLoop )
        self.multiCut = cmds.iconTextButton( style="iconOnly", image1="multiCut_NEX32.png", label="cube", imageOverlayLabel="MC Tool", command=self.multiCut )
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        
        cmds.rowColumnLayout(numberOfRows=1)
        cmds.checkBox( label="Preserve UVs", onCommand=self.preserveUVOn, offCommand=self.preserveUVOff )
        cmds.checkBox( label='Preserve UVs' )
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        
        #create locator with custom name - if left blank locator given default name
        cmds.rowColumnLayout(numberOfRows=1)
        self.locatorName = cmds.textFieldGrp() 
        self.createLocatorBtn = cmds.button(label="Create Locator", command=self.createLocator, height=10)
        cmds.setParent('..')
        
        cmds.separator(height=10, style='none')
        
        #create plane based on cm measurements and scale
        cmds.rowColumnLayout(numberOfRows=1)
        self.planeSize = cmds.floatFieldGrp(numberOfFields=3, value1=1, value2=1, value3=500)
        self.createPlaneBtn = cmds.button(label="Create Plan Plane", height=10, command=self.createPlanPlane)
        cmds.setParent('..')
        
        cmds.separator(height=10, style='none')
        
        cmds.rowColumnLayout(numberOfRows=1)
        self.wallSize = cmds.floatFieldGrp(numberOfFields=2, value1=1, value2=1000)
        self.createWallBtn = cmds.button(label="Create Wall", height=10, command=self.createWall)
        cmds.setParent('..')
        
        cmds.separator(height=10, style='none')
        
        #delete uv sets and refresh materials (current WIP)
        cmds.rowColumnLayout(numberOfRows=1)
        self.createPlaneBtn = cmds.button(label="Delete Extra UV Sets", height=30, width=200, command=self.deleteUVSets)
        self.createPlaneBtn = cmds.button(label="Delete Materials", height=30, width=200, command=self.matRefresh)
        cmds.setParent('..')
        
        cmds.separator(height=3, style='none')
        
        #check naming conventions of objects and export settings
        cmds.rowColumnLayout(numberOfRows=1)
        self.createPlaneBtn = cmds.button(label="External Name Check", height=30, width=200, command=self.externalNameCheck)
        self.createPlaneBtn = cmds.button(label="Interior Name Check", height=30, width=200, command=self.internalNameCheck)
        cmds.setParent('..')
        
        cmds.separator(height=4, style='none')

        #Select house object, mirrors and creates nodes
        self.mirrorHouseBtn = cmds.button(label="Mirror House", height=30, width=400, command=self.mirrorHouse)
        
        cmds.separator(height=5, style='none')


        self.exportCheckBtn = cmds.button(label="Export Check", height=30, width=400, command=self.exportCheck)
        
        
        cmds.separator(height=180, style='none')
        
        cmds.text("Made by Kieron")
        #display​ new window
        cmds.showWindow()
        
        
    def createLocator(self, *args):
        lName = cmds.textFieldGrp(self.locatorName, query=True, text=True)
        cmds.spaceLocator(name=lName)
        om.MGlobal.displayInfo("Locator Created")
        
    def changeMeasurements(self,*args):
        sceneMV = cmds.optionMenu(self.sceneMeasurements, query=True, value=True)
        if sceneMV == "Millimetres":
            cmds.currentUnit(linear="millimeter")
            om.MGlobal.displayWarning("Scale changed to MM")
        elif sceneMV == "Centimetres":
            cmds.currentUnit(linear="centimeter")
            om.MGlobal.displayWarning("Scale changed to CM")
        elif sceneMV == "Metres":
            cmds.currentUnit(linear="in")
            om.MGlobal.displayWarning("Scale changed to M")
      
    def deleteHistory(self, *args):
            cmds.delete(constructionHistory=True)
            om.MGlobal.displayInfo("History Deleted")
            
    def centerPivots(self, *args):
        for obj in cmds.ls(selection=True):
            cmds.xform(centerPivots=True)
            om.MGlobal.displayInfo("Pivots Centred")
            
    def mergePivots(self, *args):
        cmds.polyUnite()
        cmds.polyMergeVertex(distance=0.15) #change value to merge further away
        cmds.delete(constructionHistory=True)
        
    def edgeLoop(self, *args):
        mel.eval("SplitEdgeRingTool")
        mel.eval("toolPropertyWindow")
        
    def multiCut(self, *args):  
        mel.eval("dR_multiCutTool")
        mel.eval("toolPropertyWindow")    
            
    def freezeTransforms(self, *args):
        cmds.makeIdentity(apply=True, translate=True, scale=True)
        
    def createPlanPlane(self, *args):
        cmds.currentUnit(linear="centimeter") #remove this line to not switch measurements
        pWidth = cmds.floatFieldGrp(self.planeSize, query=True, value1=True)
        pHeight = cmds.floatFieldGrp(self.planeSize, query=True, value2=True)
        pScale = cmds.floatFieldGrp(self.planeSize, query=True, value3=True)
        planPlaneHeight = pHeight * pScale
        planPlaneWidth = pWidth * pScale
        sitePlan = cmds.polyPlane(name="SitePlan01", subdivisionsX=1, subdivisionsY=1, height=planPlaneHeight, width=planPlaneWidth)
        cmds.move(0,-5,0, sitePlan)
        om.MGlobal.displayWarning("Scale changed to CM")
        
    def externalNameCheck(self, *args):
        externalNames = ["Brick","LowBrick","Brick_Flemish","Cladding","Collider","Detail_Brick","Misc","WindowBoxes","FasciaBoard","Roof",
                         "FrontDoor","WallVents","RoofVents","Glass","GlassFrosted","Render","SlateCills","Sandstone","Stone","Wood_Detail","Solar",
                         "Detail_Tile_1","Detail_Tile_2","Detail_Tile_3","LowBrick","Garage_Door","Boxes","HangingBrickTiles","Doorbell","Windows","BackDoors",
                         "PatioDoors","Drainpipe_Gutter","Drainpipe_01","Drainpipe_02","LeadFlashing","FrontDoorNode","BackDoorNode"]
        hType = ["VGBH", "VGLH"]
        
        for n in hType:
            cmds.select( all=True )
        
        mHouse = cmds.ls(sl=True, assemblies=True)
        if mHouse == externalNames:
            cmds.confirmDialog( title='Object Names Correct', message='Object names all good. GGz.', button=['Thanks!'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        else:
            cmds.confirmDialog( title='Check Object Names', message='Names do not match standards document. Please check all names match standards document or are not needed before exporting.', button=['I Promise To Check Before Exporting'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            cmds.showHelp("https://docs.google.com/document/d/1NICfpaEwLb8qY3h36M5D1p_PxkdZbMsiaewjegZwtuU/edit?usp=sharing", absolute=True) 
            om.MGlobal.displayInfo("Standards Doc Opened")   

    def internalNameCheck(*args):
    
        internalNames = ["WallPaint","FloorLino","FloorTile","Carpet","Stairs_Bannister","Stairs_Carpet","Stairs_Railing","Chrome","OvenMicrowave","OvenGlass",
                         "HobCoffeeWine","CupboardDoors","Worktop","CeramicPlastic","WallTile","Wardrobes","SkirtingBoards","InteriorDoors","DoorFrames","Ceilings"]
        hType = ["VGBH", "VGLH"]
        
        for n in hType:
            cmds.select( all=True )
        
        mHouse = cmds.ls(sl=True, assemblies=True)
        if mHouse == internalNames:
            cmds.confirmDialog( title='Object Names Correct', message='Object names all good. GGz.', button=['Thanks!'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        else:
            cmds.confirmDialog( title='Check Object Names', message='Names do not match standards document. Please check all names match standards document and/or are not needed before exporting.', button=['I Promise To Check Before Exporting'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            cmds.showHelp("https://docs.google.com/document/d/1NICfpaEwLb8qY3h36M5D1p_PxkdZbMsiaewjegZwtuU/edit?usp=sharing", absolute=True) 
            om.MGlobal.displayInfo("Standards Doc Opened")    
       
    def exportCheck(self, *args):
        cmds.currentUnit(linear="centimeter")
        cmds.delete(constructionHistory=True)
        cmds.select( all=True )
        cmds.confirmDialog( title='Export Settings Set', message='House Ready For Export ', button=['Thanks!'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        mel.eval("ExportSelection")
        
        om.MGlobal.displayInfo("Export Settings Set")

       #current WIP 
    def deleteUVSets(self, *args):
        print("Delete UVs")           
        
    def createWall(self, *args):
        cmds.currentUnit(linear="millimeter") #remove this line to not switch measurements
        brickSize = 75
        brickCourse = cmds.floatFieldGrp(self.wallSize, query=True, value1=True)
        wallWidth = cmds.floatFieldGrp(self.wallSize, query=True, value2=True)
        wallHeight = brickSize * brickCourse
        sitePlan = cmds.polyPlane(name="Wall01", subdivisionsX=1, subdivisionsY=1, height=wallHeight, width=wallWidth)
        cmds.rotate(90,0,0)
        cmds.currentUnit(linear="centimeter") #remove this line to not switch measurements
        om.MGlobal.displayWarning("Scale changed to CM")
        
    def mirrorHouse(*args):
        houseTypes = ["VGLH_", "VGBH_"]
 
        for i in houseTypes:
            cmds.select( all=True )
    
        mainHouse = cmds.ls(sl=True, assemblies=True)
        cmds.scale( -1, 1, 1 )
        cmds.makeIdentity(apply=True, translate=True, scale=True)
        cmds.spaceLocator(name="Nodes", p=(0, 0, 0) )
        cmds.spaceLocator(name="BackDoorNode", p=(1, 100, 750) )
        cmds.select( 'BackDoorNode' )
        cmds.rotate( 0, "180deg", 0, r=True )
        cmds.spaceLocator(name="FrontDoorNode", p=(1, 100, 750) )
        cmds.select( 'FrontDoorNode' )
        cmds.parent( "BackDoorNode", "Nodes" )
        cmds.parent( "FrontDoorNode", "Nodes" )
        cmds.select( "FrontDoorNode" )
        cmds.xform(centerPivots=True)
        cmds.select( "BackDoorNode" )
        cmds.xform(centerPivots=True)
        cmds.parent( "Nodes", mainHouse )      
        cmds.delete(constructionHistory=True)
        om.MGlobal.displayWarning("House Mirrored, ADD _M TO THE END")        
             
    def matRefresh( *args):
        cmds.delete (cmds.ls(type='shadingDependNode'))
        cmds.delete (cmds.ls(type='shadingEngine'))
        
    def preserveUVOn(*args):
        mel.eval("setTRSPreserveUVs true")
    def preserveUVOff(*args):
        mel.eval("setTRSPreserveUVs false")
           
                                          
myWindow = TB_Window()
