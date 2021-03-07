#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
import shutil
import ntpath
from xml.dom import minidom
from zipfile import ZipFile
import validators

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5 import uic

cwd = os.getcwd()
description_filename = ''
icon_filename = ''


class CreatorDialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi("extensioncreator.ui", self) 
        self.ui.DescriptionFileDialog.clicked.connect(self.copy_description_file)
        self.ui.IconFileDialog.clicked.connect(self.copy_icon_file)
        self.ui.buttonBox.button(0x00000400).clicked.connect(self.createextension)
        
    def copy_description_file(self):
        global description_filename
        extensionname = self.ui.ExtensionName.text().replace(' ', '')
        description_filename, _ = QFileDialog.getOpenFileName(
            caption="Choose description / documenation file", filter="Plain text (*.txt)"
            )
        if description_filename:
            os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'description'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory', extensionname, 'description')
            shutil.copy(description_filename, path)
            
    def copy_icon_file(self):
        global icon_filename
        extensionname = self.ui.ExtensionName.text().replace(' ', '')
        icon_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose an icon file for your extension', filter='Image (*.png)'
            )
        if icon_filename:
            os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'images'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory', extensionname, 'images')
            shutil.copy(icon_filename, path)
 
        
    def createextension(self):
        extensionname = self.ui.ExtensionName.text().replace(' ', '')
        identifier = self.ui.Identifier.text().strip()
        author = self.ui.Author.text().strip()
        extensionversion = self.ui.ExtensionVersion.text().strip()
        displayedname = self.ui.DisplayedName.text().strip()
        platform = self.ui.Platform.currentText()
        libreofficeversion = self.ui.LibreOfficeVersion.currentText()
        accepted_by = self.ui.Accepted_by.currentText()
        extension_license = self.ui.License.currentText().lower().split(' (')[0]
        licensefilename = extension_license + '.' + 'txt'
        licenserellink = os.path.join('registration', licensefilename)
        wb = self.ui.Website.text().strip()
        if validators.url(wb):
            website = wb
        else:
            website = None
 
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
        tag_identifier = descriptionfile.createElement('identifier')
        tag_identifier.setAttribute('value', identifier)
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
        if website != None:
            tag_name.setAttribute('xlink:href', website)
        tag_author = descriptionfile.createTextNode(author)
        if icon_filename != '':
            iconname = ntpath.basename(icon_filename)
            iconrellink = os.path.join('images', iconname)
            tag_icon = descriptionfile.createElement('icon')
            tag_icon_default = descriptionfile.createElement('default')
            tag_icon_default.setAttribute('xlink:href', iconrellink)
        tag_dependencies = descriptionfile.createElement('dependencies')
        tag_dependencies.setAttribute('xmlns:lo', 'http://libreoffice.org/extensions/description/2011')
        tag_minimal_version = descriptionfile.createElement('lo:LibreOffice-minimal-version')
        tag_minimal_version.setAttribute('name', 'LibreOffice ' + libreofficeversion)
        tag_minimal_version.setAttribute('value', libreofficeversion)
        if description_filename != '':
            name = ntpath.basename(description_filename)
            rellink = os.path.join('description', name)
            tag_extension_description = descriptionfile.createElement('extension-description')
            tag_src = descriptionfile.createElement('src')
            tag_src.setAttribute('xlink:href', rellink)
            tag_src.setAttribute('lang', 'en')
        tag_registration = descriptionfile.createElement('registration')
        tag_simple_license = descriptionfile.createElement('simple-license')
        tag_simple_license.setAttribute('accept-by', accepted_by)
        if self.ui.suppress_on_update.isChecked() == True:
            tag_simple_license.setAttribute('suppress-on-update', 'True')
        if self.ui.suppress_if_required.isChecked() == True:
            tag_simple_license.setAttribute('suppress-if-required', 'True')
        tag_license_text = descriptionfile.createElement('license-text')
        tag_license_text.setAttribute('lang', 'en')
        tag_license_text.setAttribute('xlink:href', licenserellink)
        tag_description.appendChild(tag_identifier)
        tag_description.appendChild(tag_version)
        tag_description.appendChild(tag_platform)
        tag_dp_name.appendChild(tag_dp_name_data)
        tag_display_name.appendChild(tag_dp_name)
        tag_description.appendChild(tag_display_name)
        tag_name.appendChild(tag_author)
        tag_publisher.appendChild(tag_name)
        tag_description.appendChild(tag_publisher)
        if icon_filename != '':
            tag_icon.appendChild(tag_icon_default)
            tag_description.appendChild(tag_icon)
        tag_dependencies.appendChild(tag_minimal_version)
        tag_description.appendChild(tag_dependencies)
        if description_filename != '':
            tag_extension_description.appendChild(tag_src)
            tag_description.appendChild(tag_extension_description)
        tag_simple_license.appendChild(tag_license_text)
        tag_registration.appendChild(tag_simple_license)
        tag_description.appendChild(tag_registration)
        descriptionfile.appendChild(tag_description)
        
        
        os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'META-INF'), exist_ok=True)
        os.makedirs(os.path.join(cwd, 'working_directory', extensionname, 'registration'), exist_ok=True)

        path = os.path.join(cwd, 'working_directory', extensionname)
        licenseinputpath = os.path.join(cwd, 'license_files', licensefilename)
        licenseoutputpath = os.path.join(cwd, 'working_directory', extensionname, 'registration', licensefilename)
        
        shutil.copy(licenseinputpath, licenseoutputpath)
        
        with open(os.path.join(path, 'description.xml'), 'w') as f:
            descriptionfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'META-INF', 'manifest.xml'), 'w') as f:
            manifestfile.writexml(f, "", "\t", "\n")
            
        with open(os.path.join(path, 'path.xcu'), 'w') as f:
            path_xcu_file.writexml(f, "", "\t", "\n")
            
        
        with ZipFile(extensionname + '.' + 'oxt', 'w') as liboextensionzip:
            os.chdir(path)
            for root, dirs, files in os.walk('.'):
                for name in files:
                    if not name == extensionname:
                        liboextensionzip.write(os.path.join(root, name)) 
        

app = QApplication(sys.argv)
dialog = CreatorDialog()
dialog.show()
sys.exit(app.exec_())
