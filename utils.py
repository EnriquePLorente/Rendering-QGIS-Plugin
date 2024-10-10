from qgis.core import (
    QgsProject, 
    QgsPrintLayout, 
    QgsLayoutPoint, 
    QgsLayoutSize, 
    QgsUnitTypes, 
    QgsLayoutItemShape, 
    QgsLayoutItemMap, 
    QgsMapSettings, 
    QgsRectangle, 
    QgsLayoutItemLabel, 
    QgsLayoutItemLegend, 
    QgsLayoutItemScaleBar, 
    QgsLayoutExporter,
    QgsLegendSettings
)
from PyQt5.QtGui import QFont
from qgis.core import QgsVectorLayer
import os


class generateMapComposition():
    def __init__(self, layersList, layersListAll, outputPath, nameOutputFile, dataPath):
        self.layersListAll = layersListAll
        self.layersList = layersList
        self.outputPath = outputPath
        self.nameOutputFile = nameOutputFile
        self.indexMaxExtension = self.searchBiggestExtension()
        self.dataPath = dataPath
    
    def searchBiggestExtension(self):
       
        layer_area = []
        #Open for loop
        for layer in self.layersList:
            if isinstance(layer, QgsVectorLayer):
                layer_area.append(layer.extent().area())
            else:
                layer_area.append(0)
        #Set the maximum area
        max_value = max(layer_area)
        #Set the index
        max_index = layer_area.index(max_value)
        print(f"La capa de mayor extensión es la nº: {max_index}")
        return max_index
    
    def createLayout(self):
        project = QgsProject.instance()
        
        # Create a new layout
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()  # Initialize default settings
        
        # Get the layout manager
        layoutmanager = project.layoutManager()
        layoutname = "AutomaticLayout"
        layout_list = layoutmanager.printLayouts()
        
        for existing_layout in layout_list:
            if layoutname == existing_layout.name():
                layoutmanager.removeLayout(existing_layout)
        
        # Set the name for the new layout
        layout.setName(layoutname)
        
        # Add the new layout to the project
        layoutmanager.addLayout(layout)
    

        #MAIN MAP
        rectangle_map1 = QgsLayoutItemShape(layout)
        rectangle_map1.setShapeType(QgsLayoutItemShape.Rectangle)
        rectangle_map1.attemptMove(QgsLayoutPoint(4.5,4.5, QgsUnitTypes.LayoutMillimeters))
        rectangle_map1.attemptResize(QgsLayoutSize(203.5,200.5, QgsUnitTypes.LayoutMillimeters))  
        layout.addLayoutItem(rectangle_map1)
        
        
        map = QgsLayoutItemMap(layout)
        map.setRect(20,20,20,20)
        
 
        ms = QgsMapSettings()
        # Layers to render
        ms.setLayers(self.layersList)
        extensionLayer = self.layersList[self.indexMaxExtension].extent()
        rect = QgsRectangle(extensionLayer)
        rect.scale(1.0)
        ms.setExtent(rect)
        
        map.setExtent(ms.extent())  # Set the extent of the map item based on the map settings
        map.setLayers(ms.layers())  # Set the layers for the map item
        map.setCrs(ms.destinationCrs())  # Set the coordinate reference system (CRS) for the map item

        
        layout.addLayoutItem(map)
        
        map.attemptMove(QgsLayoutPoint(5,5.5, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(203,199, QgsUnitTypes.LayoutMillimeters))
        
        
        #BASE RECTANGLE
        rectangle_basis = QgsLayoutItemShape(layout)
        rectangle_basis.setShapeType(QgsLayoutItemShape.Rectangle)
        rectangle_basis.attemptResize(QgsLayoutSize(80, 200, QgsUnitTypes.LayoutMillimeters)) 
        rectangle_basis.attemptMove(QgsLayoutPoint(210, 5, QgsUnitTypes.LayoutMillimeters))    
        layout.addLayoutItem(rectangle_basis)
        
        
        #MAP 2
        rectangle_map2 = QgsLayoutItemShape(layout)
        rectangle_map2.setShapeType(QgsLayoutItemShape.Rectangle)
        rectangle_map2.attemptResize(QgsLayoutSize(75, 55, QgsUnitTypes.LayoutMillimeters))  
        rectangle_map2.attemptMove(QgsLayoutPoint(212.5, 7.5, QgsUnitTypes.LayoutMillimeters))    
        layout.addLayoutItem(rectangle_map2)
        
        map2 = QgsLayoutItemMap(layout)
        map2.setRect(20,20,20,20)
        
        ms2 = QgsMapSettings()

        ms2.setLayers([self.layersList[self.indexMaxExtension]])
        extensionLayer2 = self.layersList[self.indexMaxExtension].extent()
        rect2 = QgsRectangle(extensionLayer2)
        rect2.scale(1.0)
        ms2.setExtent(rect2)
        map2.setExtent(rect2)
        map2.setLayers([self.layersList[self.indexMaxExtension]])
              
        
        layout.addLayoutItem(map2)
        
        map2.attemptResize(QgsLayoutSize(74.5,54.5, QgsUnitTypes.LayoutMillimeters))
        map2.attemptMove(QgsLayoutPoint(213,8, QgsUnitTypes.LayoutMillimeters))
        
        
        #MAP NAME
        rectangle_namemap = QgsLayoutItemShape(layout)
        rectangle_namemap.setShapeType(QgsLayoutItemShape.Rectangle)
        rectangle_namemap.attemptResize(QgsLayoutSize(75, 20, QgsUnitTypes.LayoutMillimeters))  
        rectangle_namemap.attemptMove(QgsLayoutPoint(212.5, 60.5 + 5, QgsUnitTypes.LayoutMillimeters))    
        layout.addLayoutItem(rectangle_namemap)
        
        label = QgsLayoutItemLabel(layout)
        label.setText(self.nameOutputFile)
        font = QFont("Arial", 16) 
        label.setFont(font)
        label.adjustSizeToText()
        label.attemptMove(QgsLayoutPoint(214.5, 68.5 + 5, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(label)
        
        #LEYEND
        rectangle_leyend = QgsLayoutItemShape(layout)
        rectangle_leyend.setShapeType(QgsLayoutItemShape.Rectangle)
        rectangle_leyend.attemptResize(QgsLayoutSize(75, 114, QgsUnitTypes.LayoutMillimeters))  
        rectangle_leyend.attemptMove(QgsLayoutPoint(212.5, 82.5 + 5, QgsUnitTypes.LayoutMillimeters))    
        layout.addLayoutItem(rectangle_leyend)
        
        # Create an instance of QgsLegendSettings
        legend_settings = QgsLegendSettings()
        layer_tree_root = QgsProject.instance().layerTreeRoot()
       
        # Iterate over the layers
        for layer in QgsProject.instance().mapLayers().values():
            layer_tree_layer = layer_tree_root.findLayer(layer.id()) 

            if layer_tree_layer and layer not in self.layersList:
                parent_group = layer_tree_layer.parent() 
                parent_group.removeChildNode(layer_tree_layer)
        
        legend = QgsLayoutItemLegend(layout)
        legend.setLinkedMap(map) # map is an instance of QgsLayoutItemMap
        legend.setTitle("Map Legend")  
        legend.attemptMove(QgsLayoutPoint(214.5, 84.5 + 5, QgsUnitTypes.LayoutMillimeters)) 
        layout.addLayoutItem(legend)
        

        
        #SCALE
        item = QgsLayoutItemScaleBar(layout)
        item.setStyle('Single Box') 
        item.setLinkedMap(map) 
        item.applyDefaultSize()
        item.setNumberOfSegments(2)
        font = item.font()
        font.setPointSize(8)  
        item.setFont(font)
        item.attemptMove(QgsLayoutPoint(160, 185, QgsUnitTypes.LayoutMillimeters))  
        layout.addLayoutItem(item)
        
     # Hide all layers in the layer tree
        for layer_node in layer_tree_root.children():
                layer_node.setItemVisibilityChecked(False)  # Hide the layer in the layer tree
        
        # Create and export the layout
        layoutItem = layoutmanager.layoutByName(layoutname)
        export = QgsLayoutExporter(layoutItem)
        output_format = self.nameOutputFile.replace(" ","")
        export.exportToImage(self.outputPath + "/" + output_format + ".png", QgsLayoutExporter.ImageExportSettings())
        
        # Show all layers in the layersList
        for layer in self.layersList:
        # Get the layer's tree layer object
            layer_tree = project.layerTreeRoot().findLayer(layer.id())
            layer_tree.setItemVisibilityChecked(True)  # Set visibility to True (visible)
