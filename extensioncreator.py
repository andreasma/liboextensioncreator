#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
from xml.dom import minidom

from PyQt4 import QtGui, uic

class CreatorDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = uic.loadUi("extensioncreator.ui", self)
        self.ui.buttonBox.button(0x00000400).clicked.connect(self.createextension)
        
    def createextension(self):
        extensionname = self.ui.ExtensionName.text().replace(' ', '')
        author = self.ui.Author.text().strip()
        extensionversion = self.ui.ExtensionVersion.text().strip()
        displayedname = self.ui.DisplayedName.text().strip()
        platform = self.ui.Platform.currentText()
        libreofficeversion = self.ui.LibreOfficeVersion.currentText()
        
        
        print(extensionname)
        print(author)
        print(extensionversion)
        print(displayedname)
        print(platform)
        print(libreofficeversion)
        
        # building manifest.xml
        manifestfile = minidom.Document()
        manifest_manifest = manifestfile.createElement('manifest:manifest')
        manifest_manifest.setAttribute('xmlns:manifest', 'http://openoffice.org/2001/manifest')
        manifest_file_entry = manifestfile.createElement('manifest:file-entry')
        manifest_file_entry.setAttribute('manifest:media-type', 'application/vnd.sun.star.configuration-data')
        manifest_file_entry.setAttribute('manifest:full-path', 'paths.xcu')
        manifest_manifest.appendChild(manifest_file_entry)
        manifestfile.appendChild(manifest_manifest)
        
        # building path.xcu
        path_xcu_file = minidom.Document()
        odc = path_xcu_file.createElement('oor:component-data')
        odc.setAttribute('oor:package', 'org.openoffice.Office')
        odc.setAttribute('oor:name', 'Paths')
        odc.setAttribute('xmlns:install', 'http://openoffice.org/2004/installation')
        odc.setAttribute('xmlns:oor', 'http://openoffice.org/2001/registry')
        odc.setAttribute('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        odc.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        path_xcu_file.appendChild(odc)
        
        # building the description.xml file
        descriptionfile = minidom.Document()
        tag_description = descriptionfile.createElement('description')
        tag_description.setAttribute('xmlns', 'http://openoffice.org/extensions/description/2006')
        tag_description.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        tag_version = descriptionfile.createElement('version')
        tag_version.setAttribute('value', extensionversion)
        tag_platform = descriptionfile.createElement('platform')
        tag_platform.setAttribute('value', platform)
        tag_display_name = descriptionfile.createElement('display-name')
        tag_dp_name = descriptionfile.createElement('name')
        tag_dp_name.setAttribute('lang', 'en')
        tag_dp_name_data = descriptionfile.createTextNode(displayedname)
        tag_publisher = descriptionfile.createElement('publisher')
        tag_name = descriptionfile.createElement('name')
        tag_author = descriptionfile.createTextNode(author)
        tag_icon = descriptionfile.createElement('icon')
        tag_dependencies = descriptionfile.createElement('dependencies')
        tag_dependencies.setAttribute('xmlns:lo', 'http://libreoffice.org/extensions/description/2011')
        tag_minimal_version = descriptionfile.createElement('lo:LibreOffice-minimal-version')
        tag_minimal_version.setAttribute('name', 'LibreOffice ' + libreofficeversion)
        tag_minimal_version.setAttribute('value', libreofficeversion)
        tag_description.appendChild(tag_version)
        tag_description.appendChild(tag_platform)
        tag_dp_name.appendChild(tag_dp_name_data)
        tag_display_name.appendChild(tag_dp_name)
        tag_description.appendChild(tag_display_name)
        tag_name.appendChild(tag_author)
        tag_publisher.appendChild(tag_name)
        tag_description.appendChild(tag_publisher)
        tag_dependencies.appendChild(tag_minimal_version)
        tag_description.appendChild(tag_dependencies)
        
        
        
        descriptionfile.appendChild(tag_description)
        
        cwd = os.getcwd()
        os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'META-INF'), exist_ok=True)

        path = os.path.join(cwd, 'working_directory', extensionname)
        print('Path is: ', path)
        
        with open(os.path.join(path, 'description.xml'), 'w') as f:
            descriptionfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'META-INF', 'manifest.xml'), 'w') as f:
            manifestfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'path.xcu'), 'w') as f:
            path_xcu_file.writexml(f, "", "\t", "\n")
            
        

app = QtGui.QApplication(sys.argv)
dialog = CreatorDialog()
dialog.show()
sys.exit(app.exec_())
