#!/usr/bin/env python3
# -*- coding: utf8 -*-

''' This program creates a UI, where a user could input the necessary
    data to create a LibreOffice non-code extension. There are six
    options for different sort of such extensions available on
    tab 3 of the program.
    '''

import ntpath
import os
import shutil
import sys
from xml.dom import minidom
from zipfile import ZipFile

import validators
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QDialogButtonBox, QFileDialog, QFormLayout,
                             QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QRadioButton, QSpinBox, QTabWidget, QVBoxLayout,
                             QWidget)

cwd = os.getcwd()
description_filename = ''
icon_filename = ''
extensionname = ''
palettename = ''


class CreatorApp(QMainWindow):

    ''' Initate the main window of the application.
    '''

    def __init__(self):
        super().__init__()
        self.title = 'LibreOffice Extension Creator Dialog'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.group_widget = CreatorGroupWidget(self)
        self.setCentralWidget(self.group_widget)
        self.show()


class CreatorGroupWidget(QWidget):

    '''
    Create a group widget inside the main window. Add a top group box,
    a tab widget in the middle and a bottom group box. The group widget
    and the top and the bottom group box get a grid layout.
    '''

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.topgroupbox = QGroupBox('LibreOffice Extension Creator')
        topgridbox = QGridLayout()
        self.topgroupbox.setLayout(topgridbox)
        self.toplabel = QLabel(
            'You can use this program to create '
            'a new non-code LibreOffice extension.')
        topgridbox.addWidget(self.toplabel)
        self.tab_widget = CreatorTabWidget(self)
        self.bottomgroupbox = QGroupBox()
        bottomgridbox = QGridLayout()
        self.bottomgroupbox.setLayout(bottomgridbox)
        self.button_label = QLabel()
        self.button_label.setText(
            'Once you are finished with the data '
            'fields, you could create the extension by clicking the '
            'OK button.')
        bottomgridbox.addWidget(self.button_label, 0, 0)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setEnabled(False)
        self.buttonBox.accepted.connect(self.tab_widget.accept)
        self.buttonBox.rejected.connect(self.tab_widget.reject)
        bottomgridbox.addWidget(self.buttonBox, 0, 1)
        self.layout.addWidget(self.topgroupbox, 0, 0)

        self.layout.addWidget(self.tab_widget, 1, 0)
        self.layout.addWidget(self.bottomgroupbox, 2, 0)


class CreatorTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QFormLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(600, 800)
        self.items = []
        self.item_count = 0
        self.lineEdit = QLineEdit

        # Add tabs
        self.tabs.addTab(self.tab1, "General")
        self.tabs.addTab(self.tab2, "Registration / License")
        self.tabs.addTab(self.tab3, "Extension Content")

        # Create first tab
        formbox = QFormLayout()
        self.tab1.setLayout(formbox)
        self.nameliboext = QLineEdit()
        self.nameliboext.setObjectName('Extension Name')
        self.nameliboext.setMaxLength(30)
        QTimer.singleShot(0, self.nameliboext.setFocus)
        self.nameliboext.editingFinished.connect(
            lambda: self.no_or_toshort_text1(self.nameliboext))
        formbox.addRow(
            'Name of your LibreOffice Extension, between 8 and 30 character',
            self.nameliboext)
        self.nameextauthor = QLineEdit()
        self.nameextauthor.setObjectName('Author Name')
        self.nameextauthor.editingFinished.connect(
            lambda: self.textbox_empty(self.nameextauthor))
        formbox.addRow("Name of the extension author / publisher",
                       self.nameextauthor)
        self.authorwebsite = QLineEdit()
        formbox.addRow("URL of the author's / publisher's  "
                       'website or blog',
                       self.authorwebsite)
        self.extversion = QLineEdit()
        self.extversion.setObjectName('Extension Version')
        self.extversion.editingFinished.connect(
            lambda: self.textbox_empty(self.extversion))
        formbox.addRow("Version number of the extension (e.gl 0.1)",
                       self.extversion)
        self.extidentifier = QLineEdit()
        self.extidentifier.setObjectName('Extension Identifier')
        self.extidentifier.editingFinished.connect(
            lambda: self.textbox_empty(self.extidentifier))
        formbox.addRow("Identifier", self.extidentifier)
        self.showedname = QLineEdit()
        formbox.addRow("Displayed Name", self.showedname)
        self.platform = QLabel()
        self.platform.setText('Platform')
        self.platf = QComboBox()
        formbox.addRow(self.platform, self.platf)
        self.platf.addItem('all')
        self.platf.addItem('linux_x86')
        self.platf.addItem('linux_x86_64')
        self.platf.addItem('windows_x86')
        self.platf.addItem('macosx_x86')
        self.platf.addItem('macosx_x86_64')
        self.platf.addItem('free_bsd_x86')
        self.platf.addItem('free_bsd_x86_x64')
        self.platf.addItem('linux_arm_eabi')
        self.platf.addItem('linux_arm_oabi')
        self.platf.addItem('linux_ia64')
        self.platf.addItem('linux_mips_eb')
        self.platf.addItem('linux_mips_el')
        self.platf.addItem('linux_powerpc')
        self.platf.addItem('linux_powerpc64')
        self.platf.addItem('linux_s390')
        self.platf.addItem('linux_s390x')
        self.platf.addItem('linux_sparc')
        self.platf.addItem('macosx_powerpc')
        self.platf.addItem('os2_x86')
        self.platf.addItem('solaris_sparc')
        self.platf.addItem('solaris_x86')
        self.liboversion = QLabel()
        self.liboversion.setText('Minimal LibreOffice version')
        self.libv = QComboBox()
        formbox.addRow(self.liboversion, self.libv)
        self.libv.addItem('4.2')
        self.libv.addItem('4.3')
        self.libv.addItem('4.4')
        self.libv.addItem('5.0')
        self.libv.addItem('5.1')
        self.libv.addItem('5.2')
        self.libv.addItem('5.3')
        self.libv.addItem('5.4')
        self.libv.addItem('6.0')
        self.libv.addItem('6.1')
        self.libv.addItem('6.2')
        self.libv.addItem('6.3')
        self.libv.addItem('6.4')
        self.libv.addItem('7.0')
        self.libv.addItem('7.1')
        self.descr = QLabel()
        self.descr.setText('Description / Documentation of the '
                           'Extension (*.txt) (English Language)')
        self.descrbutton = QPushButton()
        self.descrbutton.setText('Choose File')
        self.descrbutton.setGeometry(QRect(200, 150, 93, 28))
        formbox.addRow(self.descr, self.descrbutton)
        self.descrbutton.clicked.connect(self.copy_description_file)
        self.exticon = QLabel()
        self.exticon.setText('Choose an Icon for your extension, '
                             'if you already created one.')
        self.exticonbutton = QPushButton()
        self.exticonbutton.setText('Choose an Icon')
        self.exticonbutton.setGeometry(QRect(200, 150, 93, 28))
        formbox.addRow(self.exticon, self.exticonbutton)
        self.exticonbutton.clicked.connect(self.copy_icon_file)

        # Create second tab
        gridlayout2 = QGridLayout()
        self.tab2.setLayout(gridlayout2)
        self.acceptedby = QLabel()
        self.acceptedby.setText('Accepted by:')
        self.ack = QComboBox()
        self.ack.setFixedWidth(150)
        gridlayout2.addWidget(self.acceptedby, 0, 0)
        gridlayout2.addWidget(self.ack, 0, 1)
        self.ack.addItem('admin')
        self.ack.addItem('user')
        self.extlicense = QLabel()
        self.extlicense.setText('Choose a license for your extension:')
        self.extlicense.setFixedWidth(300)
        self.eli = QComboBox()
        self.eli.setFixedWidth(300)
        gridlayout2.addWidget(self.extlicense, 1, 0)
        gridlayout2.addWidget(self.eli, 1, 1)
        self.eli.addItem('GPL-2.0 (General Public License Version 2.0)')
        self.eli.addItem('GPL-3.0 (General Public License Version 3.0)')
        self.eli.addItem('LGPL-3.0 (Lesser General Public '
                         'License Version 3.0)')
        self.eli.addItem('LGPL-2.1 (Lesser General Public '
                         'License Version 2.1)')
        self.eli.addItem('CC-BY-SA-4.0 (Creative Commons Attribution-'
                         'ShareAlike 4.0 International License')
        self.soupdbox = QCheckBox('suppress-on-update')
        self.sifreqbox = QCheckBox('suppress-if-required')
        gridlayout2.addWidget(self.soupdbox, 2, 0)
        gridlayout2.addWidget(self.sifreqbox, 3, 0)

        # Create third tab
        gridlayout3 = QGridLayout()
        self.tab3.setLayout(gridlayout3)
        self.contentkindbox = QGroupBox(
            'Which kind of content extension to build?')
        gridbox0 = QGridLayout()
        self.radiobuttonautocorrect = QRadioButton('AutoCorrect Extension')
        self.radiobuttonautocorrect.toggled.connect(
            lambda: self.autocorrectextcreation(self.radiobuttonautocorrect))
        gridbox0.addWidget(self.radiobuttonautocorrect, 0, 0)
        self.radiobuttonautotext = QRadioButton('AutoText Extension')
        self.radiobuttonautotext.toggled.connect(
            lambda: self.autotextextcreation(self.radiobuttonautotext))
        gridbox0.addWidget(self.radiobuttonautotext, 0, 1)
        self.radiobuttongallery = QRadioButton('Gallery Extension')
        self.radiobuttongallery.toggled.connect(
            lambda: self.galleryextcreation(self.radiobuttongallery))
        gridbox0.addWidget(self.radiobuttongallery, 0, 2)
        self.radiobuttoniconset = QRadioButton('IconSet Extension')
        self.radiobuttoniconset.toggled.connect(
            lambda: self.iconsetextcreation(self.radiobuttoniconset))
        gridbox0.addWidget(self.radiobuttoniconset, 1, 0)
        self.radiobuttonpalette = QRadioButton('Palette Extension')
        self.radiobuttonpalette.toggled.connect(
            lambda: self.paletteextcreation(self.radiobuttonpalette))
        gridbox0.addWidget(self.radiobuttonpalette, 1, 1)
        self.radiobuttontemplates = QRadioButton('Template Extension')
        self.radiobuttontemplates.toggled.connect(
            lambda: self.templateextcreation(self.radiobuttontemplates))
        gridbox0.addWidget(self.radiobuttontemplates, 1, 2)
        self.contentkindbox.setLayout(gridbox0)
        self.autocorbox = QGroupBox('AutoCorrect Extension')
        gridbox1 = QGridLayout()
        self.autocorbox.setLayout(gridbox1)
        self.autocorbox.setEnabled(False)
        self.autocorbox.hide()
        self.label_dat_file = QLabel(
            'Choose the *.dat file for your AutoCorrect Extension')
        self.dat_file_button = QPushButton('Choose the *.dat file')
        self.dat_file_button.clicked.connect(self.copy_dat_file)
        gridbox1.addWidget(self.label_dat_file, 0, 0)
        gridbox1.addWidget(self.dat_file_button, 0, 1)
        self.autotextbox = QGroupBox('AutoText Extension')
        gridbox2 = QGridLayout()
        self.autotextbox.setLayout(gridbox2)
        self.autotextbox.setEnabled(False)
        self.autotextbox.hide()
        self.label_bau_file = QLabel(
            'Choose the *.bau file for your AutoText Extension')
        self.bau_file_button = QPushButton('Choose the *.bau file')
        self.bau_file_button.clicked.connect(self.copy_bau_file)
        gridbox2.addWidget(self.label_bau_file, 0, 0)
        gridbox2.addWidget(self.bau_file_button, 0, 1)
        self.gallerybox = QGroupBox('Gallery Extension')
        gridbox3 = QGridLayout()
        self.gallerybox.setLayout(gridbox3)
        self.gallerybox.hide()
        self.label_sdg_file = QLabel()
        self.label_sdg_file.setText(
            'Choose the *.sdg file for your Gallery Extension')
        self.sdg_file_button = QPushButton()
        self.sdg_file_button.setText('Choose the sdg file')
        self.sdg_file_button.setGeometry(QRect(200, 150, 20, 28))
        self.sdg_file_button.clicked.connect(self.copy_sdg_file)
        self.label_sdv_file = QLabel()
        self.label_sdv_file.setText(
            'Choose the *.sdv file for your Gallery Extension')
        self.sdv_file_button = QPushButton()
        self.sdv_file_button.setText('Choose the sdv file')
        self.sdv_file_button.setGeometry(QRect(200, 150, 20, 28))
        self.sdv_file_button.clicked.connect(self.copy_sdv_file)
        self.label_thm_file = QLabel()
        self.label_thm_file.setText(
            'Choose the *.thm file for your Gallery Extension')
        self.thm_file_button = QPushButton()
        self.thm_file_button.setText('Choose the thm file')
        self.thm_file_button.setGeometry(QRect(200, 150, 20, 28))
        self.thm_file_button.clicked.connect(self.copy_thm_file)
        gridbox3.addWidget(self.label_sdg_file, 0, 0)
        gridbox3.addWidget(self.sdg_file_button, 0, 1)
        gridbox3.addWidget(self.label_sdv_file, 1, 0)
        gridbox3.addWidget(self.sdv_file_button, 1, 1)
        gridbox3.addWidget(self.label_thm_file, 2, 0)
        gridbox3.addWidget(self.thm_file_button, 2, 1)
        self.gallerybox.setEnabled(False)
        self.iconbox = QGroupBox('IconSet Extension')
        gridbox4 = QGridLayout()
        self.iconbox.setLayout(gridbox4)
        self.iconbox.setEnabled(False)
        self.iconbox.hide()
        self.palettebox = QGroupBox('Palette Extension')
        gridbox5 = QGridLayout()
        self.palettebox.setLayout(gridbox5)
        self.palettebox.setEnabled(False)
        self.palettebox.hide()
        self.labelnamepalette = QLabel('Name of the Palette')
        self.namepalette = QLineEdit()
        self.namepalette.setObjectName('Palette Name')
        self.numbercolorsbox = QGroupBox()
        gridbox5a = QGridLayout()
        self.numbercolorsbox.setLayout(gridbox5a)
        self.labelnumbercolor = QLabel(
            'Number of Colors for the Palette, up to 15.')
        self.spinboxcolors = QSpinBox()
        self.spinboxcolors.setRange(0, 15)
        self.spinboxcolors.valueChanged.connect(self.set_item_count)
        self.colorsbox = QGroupBox('')
        self.item_layout = QVBoxLayout(self.colorsbox)
        self.item_layout.addStretch(2)
        self.label_colors = QLabel(
            "Insert per box/line below 'color name, hexadecimal number' "
            "without the hash '#'")
        gridbox5a.addWidget(self.labelnumbercolor, 0, 0, 1, 2)
        gridbox5a.addWidget(self.spinboxcolors, 0, 2, 1, 1)
        gridbox5a.addWidget(self.label_colors, 3, 0, 1, 3)
        gridbox5a.addWidget(self.colorsbox, 4, 0, 5, 3)
        gridbox5.addWidget(self.labelnamepalette, 0, 0)
        gridbox5.addWidget(self.namepalette, 0, 1)
        gridbox5.addWidget(self.numbercolorsbox, 1, 0)
        self.templatebox = QGroupBox('Template Extension')
        gridbox6 = QGridLayout()
        self.templatebox.setLayout(gridbox6)
        self.templatebox.setEnabled(False)
        self.templatebox.hide()
        self.label_template_ziparchive = QLabel(
            'Choose the *.zip archive for your Template Extension')
        self.tempate_archive_button = QPushButton(
            'Choose the *.zip archive')
        self.tempate_archive_button.clicked.connect(
            self.copy_template_archive)
        gridbox6.addWidget(self.label_template_ziparchive, 0, 0)
        gridbox6.addWidget(self.tempate_archive_button, 0, 1)
        gridlayout3.addWidget(self.contentkindbox)
        gridlayout3.addWidget(self.autocorbox)
        gridlayout3.addWidget(self.autotextbox)
        gridlayout3.addWidget(self.gallerybox)
        gridlayout3.addWidget(self.iconbox)
        gridlayout3.addWidget(self.palettebox)
        gridlayout3.addWidget(self.templatebox)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def accept(self):
        # create the extension
        identifier = self.extidentifier.text().strip()
        author = self.nameextauthor.text().strip()
        extensionversion = self.extversion.text().strip()
        displayedname = self.showedname.text().strip()
        platform = self.platf.currentText()
        libreofficeversion = self.libv.currentText()
        wb = self.authorwebsite.text().strip()
        if validators.url(wb):
            website = wb
        else:
            website = None
        accepted_by = self.ack.currentText()
        extension_license = self.eli.currentText().lower().split(' (')[0]
        licensefilename = extension_license + '.' + 'txt'
        licenserellink = os.path.join('registration', licensefilename)

        # building manifest.xml
        manifestfile = minidom.Document()
        manifest_manifest = manifestfile.createElement(
            'manifest:manifest')
        manifest_manifest.setAttribute(
            'xmlns:manifest', 'http://openoffice.org/2001/manifest')
        manifest_file_entry = manifestfile.createElement(
            'manifest:file-entry')
        manifest_file_entry.setAttribute(
            'manifest:media-type',
            'application/vnd.sun.star.configuration-data')
        manifest_file_entry.setAttribute(
            'manifest:full-path', 'paths.xcu')
        manifest_manifest.appendChild(manifest_file_entry)
        manifestfile.appendChild(manifest_manifest)

        # building path.xcu
        path_xcu_file = minidom.Document()
        odc = path_xcu_file.createElement('oor:component-data')
        odc.setAttribute('oor:package', 'org.openoffice.Office')
        odc.setAttribute('oor:name', 'Paths')
        odc.setAttribute(
            'xmlns:install', 'http://openoffice.org/2004/installation')
        odc.setAttribute(
            'xmlns:oor', 'http://openoffice.org/2001/registry')
        odc.setAttribute('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        odc.setAttribute(
            'xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        if self.radiobuttonautocorrect.isChecked() is True:
            ng1 = path_xcu_file.createElement('node')
            ng1.setAttribute('oor-name', 'Paths')
            ng2 = path_xcu_file.createElement('node')
            ng2.setAttribute('oor-name', 'AutoText')
            ng2.setAttribute('oor:op', 'fuse')
            ng3 = path_xcu_file.createElement('node')
            ng3.setAttribute('oor-name', 'Internal Paths')
            ng4 = path_xcu_file.createElement('node')
            ng4.setAttribute('oor-name', '%origin%/autocorr')
            ng4.setAttribute('oor:op', 'fuse')
            ng3.appendChild(ng4)
            ng2.appendChild(ng3)
            ng1.appendChild(ng2)
            odc.appendChild(ng1)
        if self.radiobuttonautotext.isChecked() is True:
            ng1 = path_xcu_file.createElement('node')
            ng1.setAttribute('oor-name', 'Paths')
            ng2 = path_xcu_file.createElement('node')
            ng2.setAttribute('oor-name', 'AutoText')
            ng2.setAttribute('oor:op', 'fuse')
            ng3 = path_xcu_file.createElement('node')
            ng3.setAttribute('oor-name', 'Internal Paths')
            ng4 = path_xcu_file.createElement('node')
            ng4.setAttribute('oor-name', '%origin%/autotext')
            ng4.setAttribute('oor:op', 'fuse')
            ng3.appendChild(ng4)
            ng2.appendChild(ng3)
            ng1.appendChild(ng2)
            odc.appendChild(ng1)
        if self.radiobuttongallery.isChecked() is True:
            ng1 = path_xcu_file.createElement('node')
            ng1.setAttribute('oor-name', 'Paths')
            ng2 = path_xcu_file.createElement('node')
            ng2.setAttribute('oor-name', 'Gallery')
            ng2.setAttribute('oor:op', 'fuse')
            ng3 = path_xcu_file.createElement('node')
            ng3.setAttribute('oor-name', 'Internal Paths')
            ng4 = path_xcu_file.createElement('node')
            ng4.setAttribute('oor-name', '%origin%/gallery')
            ng4.setAttribute('oor:op', 'fuse')
            ng3.appendChild(ng4)
            ng2.appendChild(ng3)
            ng1.appendChild(ng2)
            odc.appendChild(ng1)
        if self.radiobuttonpalette.isChecked() is True:
            ng1 = path_xcu_file.createElement('node')
            ng1.setAttribute('oor-name', 'Paths')
            ng2 = path_xcu_file.createElement('node')
            ng2.setAttribute('oor-name', 'Palette')
            ng2.setAttribute('oor:op', 'fuse')
            ng3 = path_xcu_file.createElement('node')
            ng3.setAttribute('oor-name', 'Internal Paths')
            ng4 = path_xcu_file.createElement('node')
            ng4.setAttribute('oor-name', '%origin%/palette')
            ng4.setAttribute('oor:op', 'fuse')
            ng3.appendChild(ng4)
            ng2.appendChild(ng3)
            ng1.appendChild(ng2)
            odc.appendChild(ng1)
        if self.radiobuttontemplates.isChecked() is True:
            ng1 = path_xcu_file.createElement('node')
            ng1.setAttribute('oor-name', 'Paths')
            ng2 = path_xcu_file.createElement('node')
            ng2.setAttribute('oor-name', 'Template')
            ng2.setAttribute('oor:op', 'fuse')
            ng3 = path_xcu_file.createElement('node')
            ng3.setAttribute('oor-name', 'Internal Paths')
            ng4 = path_xcu_file.createElement('node')
            ng4.setAttribute('oor-name', '%origin%/template')
            ng4.setAttribute('oor:op', 'fuse')
            ng3.appendChild(ng4)
            ng2.appendChild(ng3)
            ng1.appendChild(ng2)
            odc.appendChild(ng1)
        path_xcu_file.appendChild(odc)

        # building the description.xml file
        descriptionfile = minidom.Document()
        tag_description = descriptionfile.createElement('description')
        tag_description.setAttribute(
            'xmlns', 'http://openoffice.org/extensions/description/2006')
        tag_description.setAttribute(
            'xmlns:xlink', 'http://www.w3.org/1999/xlink')
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
        if website is not None:
            tag_name.setAttribute('xlink:href', website)
        tag_author = descriptionfile.createTextNode(author)
        if icon_filename != '':
            iconname = ntpath.basename(icon_filename)
            iconrellink = os.path.join('images', iconname)
            tag_icon = descriptionfile.createElement('icon')
            tag_icon_default = descriptionfile.createElement('default')
            tag_icon_default.setAttribute('xlink:href', iconrellink)
        tag_dependencies = descriptionfile.createElement('dependencies')
        tag_dependencies.setAttribute(
            'xmlns:lo',
            'http://libreoffice.org/extensions/description/2011')
        tag_minimal_version = descriptionfile.createElement(
            'lo:LibreOffice-minimal-version')
        tag_minimal_version.setAttribute(
            'name', 'LibreOffice ' + libreofficeversion)
        tag_minimal_version.setAttribute('value', libreofficeversion)
        if description_filename != '':
            name = ntpath.basename(description_filename)
            rellink = os.path.join('description', name)
            tag_extension_description = descriptionfile.createElement(
                'extension-description')
            tag_src = descriptionfile.createElement('src')
            tag_src.setAttribute('xlink:href', rellink)
            tag_src.setAttribute('lang', 'en')
        tag_registration = descriptionfile.createElement('registration')
        tag_simple_license = descriptionfile.createElement('simple-license')
        tag_simple_license.setAttribute('accept-by', accepted_by)
        if self.soupdbox.isChecked() is True:
            tag_simple_license.setAttribute('suppress-on-update', 'True')
        if self.sifreqbox.isChecked() is True:
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

        # building *soc file for palette extension
        if self.radiobuttonpalette.isChecked() is True:
            global palettename
            palettename = self.namepalette.text()
            palette_soc_file = minidom.Document()
            tag_color_table = palette_soc_file.createElement('ooo:color-table')
            tag_color_table.setAttribute(
                'xmlns:office',
                'urn:oasis:names:tc:opendocument:xmlns:office:1.0')
            tag_color_table.setAttribute(
                'xmlns:draw',
                'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0')
            tag_color_table.setAttribute(
                'xmlns:xlink', 'http://www.w3.org/1999/xlink')
            tag_color_table.setAttribute(
                'xmlns:svg', 'http://www.w3.org/2000/svg')
            tag_color_table.setAttribute(
                'xmlns:ooo', 'http://openoffice.org/2004/office')
            for item in self.items[:self.spinboxcolors.value()]:
                colorkeyvalue = (item.text()).split(',')
                colorname = colorkeyvalue[0].strip()
                colorhexcode = '#' + colorkeyvalue[1].strip()
                tag_draw_color = palette_soc_file.createElement('draw:color')
                tag_draw_color.setAttribute('draw:name', colorname)
                tag_draw_color.setAttribute('draw:color', colorhexcode)
                tag_color_table.appendChild(tag_draw_color)

            palette_soc_file.appendChild(tag_color_table)

        os.makedirs(os.path.join(
            cwd, 'working_directory', extensionname,
            'META-INF'), exist_ok=True)
        os.makedirs(os.path.join(
            cwd, 'working_directory', extensionname,
            'registration'), exist_ok=True)
        path = os.path.join(cwd, 'working_directory', extensionname)
        licenseinputpath = os.path.join(cwd, 'license_files', licensefilename)
        licenseoutputpath = os.path.join(
            cwd, 'working_directory', extensionname, 'registration',
            licensefilename)

        shutil.copy(licenseinputpath, licenseoutputpath)

        with open(os.path.join(path, 'description.xml'), 'w') as f:
            descriptionfile.writexml(f, "", "\t", "\n")

        with open(os.path.join(path, 'META-INF', 'manifest.xml'), 'w') as f:
            manifestfile.writexml(f, "", "\t", "\n")

        with open(os.path.join(path, 'path.xcu'), 'w') as f:
            path_xcu_file.writexml(f, "", "\t", "\n")

        if self.radiobuttonpalette.isChecked() is True:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'palette'), exist_ok=True)
            palettfilename = (palettename + '.soc')
            with open(os.path.join(path, 'palette', palettfilename), 'w') as f:
                palette_soc_file.writexml(f, "", "\t", "\n")

        with ZipFile(
            os.path.join(
                cwd,
                extensionname + '.' + 'oxt'), 'w') as liboextensionzip:
            os.chdir(path)
            for root, dirs, files in os.walk('.'):
                for name in files:
                    if not name == extensionname:
                        liboextensionzip.write(os.path.join(root, name))

        sys.exit()

    def reject(self):
        sys.exit()

    def no_or_toshort_text1(self, widget):
        widgetname = widget.objectName()
        if not widget.text():
            QMessageBox.critical(
                self, widgetname, 'Empty value are not allowed.')
            widget.setFocus()
        elif len(widget.text()) < 8:
            QMessageBox.critical(
                self, widgetname, 'Your input is to short. '
                'You need to add more characters.')
            widget.setFocus()
        else:
            global extensionname
            extensionname = self.nameliboext.text().replace(' ', '')
            widget.setReadOnly(True)
            self.parent().buttonBox.setEnabled(True)

    def textbox_empty(self, widget):
        widgetname = widget.objectName()
        if widget.text() == '':
            QMessageBox.critical(
                self, widgetname, "Empty value are not allowed.")
        else:
            pass

    def autocorrectextcreation(self, b):
        if b.isChecked() is True:
            self.autocorbox.setEnabled(True)
            self.autocorbox.show()
        else:
            self.autocorbox.setEnabled(False)
            self.autocorbox.hide()

    def autotextextcreation(self, b):
        if b.isChecked() is True:
            self.autotextbox.setEnabled(True)
            self.autotextbox.show()
        else:
            self.autotextbox.setEnabled(False)
            self.autotextbox.hide()

    def galleryextcreation(self, b):
        if b.isChecked() is True:
            self.gallerybox.setEnabled(True)
            self.gallerybox.show()
        else:
            self.gallerybox.setEnabled(False)
            self.gallerybox.hide()

    def iconsetextcreation(self, b):
        if b.isChecked() is True:
            self.iconbox.setEnabled(True)
            self.iconbox.show()
        else:
            self.iconbox.setEnabled(False)
            self.iconbox.hide()

    def paletteextcreation(self, b):
        if b.isChecked() is True:
            self.palettebox.setEnabled(True)
            self.palettebox.show()
        else:
            self.palettebox.setEnabled(False)
            self.palettebox.hide()

    def on_clicked(self):
        print(*[item.text() for item in
                self.items[:self.spinboxcolors.value()]], sep="\n")

    def set_item_count(self, new_count: int):
        n_items = len(self.items)
        for ii in range(n_items, new_count):
            item = self.lineEdit(self)
            self.items.append(item)
            self.item_layout.insertWidget(n_items, item)
        for ii in range(self.item_count, new_count):
            self.item_layout.itemAt(ii).widget().show()
        for ii in range(new_count, self.item_count):
            self.item_layout.itemAt(ii).widget().hide()
        self.item_count = new_count

    def templateextcreation(self, b):
        if b.isChecked() is True:
            self.templatebox.setEnabled(True)
            self.templatebox.show()
        else:
            self.templatebox.setEnabled(False)
            self.templatebox.hide()

    def copy_description_file(self):
        global description_filename
        description_filename, _ = QFileDialog.getOpenFileName(
            caption="Choose description / documenation file",
            filter="Plain text (*.txt)"
            )
        if description_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'description'), exist_ok=True)
            path = os.path.join(
                cwd, 'working_directory', extensionname,
                'description')
            shutil.copy(description_filename, path)

    def copy_icon_file(self):
        global icon_filename
        icon_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose an icon file for your extension',
            filter='Image (*.png)'
            )
        if icon_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'images'), exist_ok=True)
            path = os.path.join(
                cwd, 'working_directory', extensionname, 'images')
            shutil.copy(icon_filename, path)

    def copy_dat_file(self):
        dat_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose the dat file for your AutoCorrect '
            'extension', filter='Image (*.dat)'
            )
        if dat_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'autocorr'), exist_ok=True)
            path = os.path.join(
                cwd, 'working_directory', extensionname, 'autocorr')
            shutil.copy(dat_filename, path)

    def copy_bau_file(self):
        bau_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose the bau file for your AutoText '
            'extension', filter='Image (*.bau)'
            )
        if bau_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'autotext'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory',
                                extensionname, 'autotext')
            shutil.copy(bau_filename, path)

    def copy_sdg_file(self):

        '''
        Copy the sdg file of a Gallery
        to the gallery subfolder.
        '''

        sdg_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose the sdg file for your Gallery '
            'extension', filter='Image (*.sdg)'
            )
        if sdg_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'gallery'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory',
                                extensionname, 'gallery')
            shutil.copy(sdg_filename, path)

    def copy_sdv_file(self):

        '''
        Copy the sdv file of a Gallery to the gallery
        subfolder.
        '''

        sdv_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose the sdv file for your Gallery extension',
            filter='Image (*.sdv)'
            )
        if sdv_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'gallery'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory',
                                extensionname, 'gallery')
            shutil.copy(sdv_filename, path)

    def copy_thm_file(self):

        '''
        Copy the thm file of a Gallery to the gallery
        subfolder.
        '''

        thm_filename, _ = QFileDialog.getOpenFileName(
            caption='Choose the thm file for your Gallery extension',
            filter='Image (*.thm)'
            )
        if thm_filename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'gallery'), exist_ok=True)
            path = os.path.join(cwd, 'working_directory',
                                extensionname, 'gallery')
            shutil.copy(thm_filename, path)

    def copy_template_archive(self):

        '''
        Copy the archive of the templates and it's structure
        to the template subfolder and unzip them.
        '''

        template_archivename, _ = QFileDialog.getOpenFileName(
            caption='Choose the zip archive for your Template '
            'extension', filter='Archive (*.zip)'
            )
        if template_archivename:
            os.makedirs(os.path.join(
                cwd, 'working_directory', extensionname,
                'template'), exist_ok=True)
            path = os.path.join(
                cwd, 'working_directory', extensionname, 'template')
            shutil.unpack_archive(template_archivename, path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreatorApp()
    sys.exit(app.exec_())
