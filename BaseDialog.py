# -*- coding: utf-8 -*-
"""
/***************************************************************************
 **Nombre del plugin
                                 A QGIS plugin
 **Descripcion
                             -------------------
        begin                : **Fecha
        copyright            : **COPYRIGHT
        email                : **Mail de contacto
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 #   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""
import os.path


from PyQt5.QtWidgets import QDialog, QMessageBox
from qgis.core import *
from qgis.gui import *
from PyQt5 import uic
from PluginMapComposition import utils

try:
    from pydevd import *
except ImportError:
    None

#Compile the file in memory
Ui_BaseDialog, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/ui_BaseDialog.ui'),
    from_imports=True,
    import_from="PluginMapComposition.ui")


class BaseDialog(QDialog, Ui_BaseDialog):

    def __init__(self, iface):
        QDialog.__init__(self)

        self.setupUi(self)
        self.iface = iface
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.allLayersList = QgsProject.instance().mapLayers().values()
        self.layerList()
        self.mapNameTextEdit = ""
        self.selected_layers = []
        self.pathDialog = ""
        self.dataPath = ""
        
        
               
    def layerList(self):
   
        # Loop through the layers and add their names 
        for layer in self.allLayersList:
            self.layersListWidget.addItem(layer.name())
        
    def moveLayer(self, item):
        """Move the selected layer from the 1 list widget to the 2"""
        # Get the layer name clicked
        layer_name = item.text()

        # Add the layer to the 2 list widget
        self.displayedLayersListWidget.addItem(layer_name)

        # Remove the layer from 1 list widget
        row = self.layersListWidget.row(item)
        self.layersListWidget.takeItem(row)
        
    def removeLayer(self, item):
        """Move the selected layer from the 2 list widget to the 1"""
        # Get the layer name clicked
        layer_name = item.text()

        # Add the layer to the 2 list widget
        self.layersListWidget.addItem(layer_name)
        self.selected_layers = [layer for layer in self.selected_layers if layer.name() != layer_name]

        # Remove the layer from 1 list widget
        row = self.displayedLayersListWidget.row(item)
        self.displayedLayersListWidget.takeItem(row)

        
    def showLayerList(self):
        # Count the layers added
        item_count = self.displayedLayersListWidget.count()
        
        for i in range(item_count):
            item = self.displayedLayersListWidget.item(i).text()  # Get the item at index i
            layers = QgsProject.instance().mapLayersByName(item)
            if layers and layers[0] not in self.selected_layers:  # Check if the layer is not already in selected_layers
                self.selected_layers.append(layers[0])
                

                
    def updateMapNameValue(self, text):
        """Set the map Name Value"""
        self.mapNameTextEdit = text
        
    def updatePathValue(self, path):
        """Set the path Value"""
        self.pathDialog = path
        
    def updateDataPath(self, dataPath):
        """Set the path Value"""
        self.dataPath = dataPath
    
    def createComposition(self):
        if len(self.selected_layers) > 0:
            mapComposition = utils.generateMapComposition(self.selected_layers, self.allLayersList, self.pathDialog, self.mapNameTextEdit, self.dataPath)
            mapComposition.createLayout()  
            print("Layout creado")
        else:
            QMessageBox.warning(None, "No Layers Selected", "Please select at least one layer before creating the composition.")
        
    
            
