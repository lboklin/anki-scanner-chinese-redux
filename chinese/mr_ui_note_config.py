from aqt import mw
from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QButtonGroup, QTextBrowser
from PyQt6.QtGui import QStandardItem, QColor
from PyQt6 import QtCore, QtWidgets

from .mr_async_worker_thread import TextScannerThreadAsync
from .singletons import config
from .mr_ui_scanner import MatterRabbitWindow

##########################################################
# This is the window to configure how notes will be auto-imported
##
def showConfigNoteTypes():
    #allow tracking a global var here
    mw.ChineseScannerData = {
        'ignoreFieldSelectChanges': False,
        'ignoreNoteTypeSelect': False
    }

    dev_mode = config.config['textScanner']['dev_mode']['val']

    outputText = QTextBrowser()
    def log(message, level='debug'):
        if dev_mode == True or level != 'debug':
            outputText.append(message)

    cntOuterLayout = QVBoxLayout()
    cntColLayout = QHBoxLayout()
    cntLeftLayout = QVBoxLayout()
    cntRightLayout = QVBoxLayout()

    cntTopLabel = QLabel()
    cntTopLabel.setWordWrap(True)
    cntTopLabel.setText('''<div style="font-weight: bold; font-size:24px; width: 5em; text-align:center;">
        请选择一种卡片来决定如何导入新单词</div>
        <div>Here you can configure where you want scanned words to be imported.
        Please choose which of your note types to use, and how the generated fields should map to your fields</div>
        <br>''')
    cntOuterLayout.addWidget(cntTopLabel)
    #outerLayout.addStretch()

    def updateTextOutput(text):
        if mw.mr_worker.exiting == False:
            log(text)

    # The note type selector
    selectNoteLabel = QLabel()
    selectNoteLabel.setWordWrap(True)
    selectNoteLabel.setText('<b>First select your note type:</b><br>Scanned words will be generated as notes using this note type.')
    selectNoteType = QComboBox()
    cntOuterLayout.addWidget(selectNoteLabel)
    cntOuterLayout.addWidget(selectNoteType)
    fieldsLabel = QLabel()
    fieldsLabel.setWordWrap(True)
    fieldsLabel.setText('<br><b>Next choose how to map the fields:</b><br>These are all the fields that can be generated by the scanner. You can add them to your notes or choose to skip')
    cntOuterLayout.addWidget(fieldsLabel)


    #######################################################
    # The field selectors and related functions
    fieldSelectors = {}

    def getConfigSavedTarget(noteType, mr_field):
        saved = config.config['textScanner'].get('note_target_maps')
        if saved != None and saved['val'].get(noteType) != None:
            return saved['val'][noteType].get(mr_field)

    def updateTargetMapConfig(target_data):
        if target_data != None:
            if config.config['textScanner']['note_target_maps']['val'].get(target_data['target_note_type']) == None:
                config.config['textScanner']['note_target_maps']['val'][target_data['target_note_type']] = {}

            config.config['textScanner']['note_target_maps']['val'][target_data['target_note_type']][target_data['mr_field']] \
            = target_data['target_field']
            config.save()
            log(f"saved config {config.config['textScanner']['note_target_maps']['val'][target_data['target_note_type']][target_data['mr_field']]}")

    def onFieldSelectorChanged(idx, mr_field):
        target_data = fieldSelectors[mr_field].itemData(idx)
        log(f"Hey field selector changed {idx}, {mr_field}, {target_data}")

        # set colors - not working great :/
        #if target_data != None and target_data['target_field'] != None:
        #    fieldSelectors[mr_field].setStyleSheet("color: #000000")
        #else:
        #    fieldSelectors[mr_field].setStyleSheet("color: #999999;  QAbstractItemView {color: #000000}")

        # save config if user selected a target
        if mw.ChineseScannerData['ignoreFieldSelectChanges'] == False:
            # save user choices as their config for next time.
            updateTargetMapConfig(target_data)
        else:
            log(f"ignoring field selection change {mr_field}")

    # to avoid late binding: https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
    def assignOnChangeFn(controlWidget, mr_field):
        def f(idx):
            onFieldSelectorChanged(idx, mr_field)
        controlWidget.currentIndexChanged.connect(f)

    def onNoteTypesLoaded():
        log('Notes and fields loaded.','info')
        evenOdd = 0
        for item in mw.mr_worker.nm_fields:
            label = QLabel()
            label.setText(mw.mr_worker.nm_fields[item])
            selector = QComboBox()
            selector.setToolTip(mw.mr_worker.nm_fields[item])
            #for item in mw.mr_worker.note_models:
            #    selector.addItem(mw.mr_worker.note_models[item]['name'])
            if evenOdd % 2 == 0:
                cntLeftLayout.addWidget(label)
                cntLeftLayout.addWidget(selector)
            else:
                cntRightLayout.addWidget(label)
                cntRightLayout.addWidget(selector)
            evenOdd += 1
            assignOnChangeFn(selector, item)
            fieldSelectors[item] = selector
        # do this second so that the field controls exist to be updated on init.
        mw.ChineseScannerData['ignoreNoteTypeSelect'] = True
        for item in mw.mr_worker.note_models:
            selectNoteType.addItem(mw.mr_worker.note_models[item]['name'], item)

        savedTargets = config.config['textScanner'].get('target_note_type')
        tidx = 0
        if savedTargets != None:
            configSavedNoteType = savedTargets.get('val')
            if configSavedNoteType != None:
                targetText = mw.mr_worker.note_models[configSavedNoteType]['name']
                tidx = selectNoteType.findText(targetText)
        if tidx > 0:
            log(f"setting saved note type {configSavedNoteType}")
            selectNoteType.setCurrentIndex(tidx)
        mw.ChineseScannerData['ignoreNoteTypeSelect'] = False

    def onNoteTypeSelectChanged(idx):
        log(f"\n\nHey onNoteTypeSelectChanged {idx}, {selectNoteType.itemData(idx)}")
        noteTypeSelected = selectNoteType.itemData(idx)

        if mw.ChineseScannerData['ignoreNoteTypeSelect'] == False:
            config.config['textScanner']['target_note_type']['val'] = noteTypeSelected
            config.save()
            log(f"Saved new new type selection {noteTypeSelected}")

        #dont update target field config when we are just initializing
        mw.ChineseScannerData['ignoreFieldSelectChanges'] = True
        for ctrl in fieldSelectors:
            control = fieldSelectors[ctrl]
            control.clear()
            #controlDisplay = control.model()
            #item = QStandardItem('Skip')
            #item.setForeground(QColor('gray'))
            #controlDisplay.appendRow(item)
            control.addItem('    ',{'target_note_type': noteTypeSelected, 'target_field':None, 'mr_field':ctrl})
            control.insertSeparator(1)
            for field in mw.mr_worker.note_models[noteTypeSelected]['flds']:
                control.addItem(field['name'],{'target_note_type': noteTypeSelected,'target_field':field['name'], 'mr_field':ctrl})
            configSavedTarget = getConfigSavedTarget(noteTypeSelected, ctrl)
            tidx = control.findText(configSavedTarget)
            if tidx > 1:
                log(f"setting saved default {ctrl}, {configSavedTarget}, {tidx}")
                control.setCurrentIndex(tidx)
        mw.ChineseScannerData['ignoreFieldSelectChanges'] = False


    selectNoteType.currentIndexChanged.connect(onNoteTypeSelectChanged)

    mw.mr_worker = TextScannerThreadAsync()
    mw.mr_worker.sig.connect(updateTextOutput)
    mw.mr_worker.finished.connect(onNoteTypesLoaded)
    mw.mr_worker.refresh_query(config['textScanner']['anki_db_path']['val'],None)
    mw.mr_worker.setMode('get_existing_note_types')
    mw.mr_worker.start()
    log("Gathering your note types.",'info')

    def onCancel():
        if hasattr(mw,'mr_worker'):
            mw.mr_worker.interrupt_and_quit = True
            mw.mr_worker.sig.emit("told worker to quit..")

    def onDialogClose():
        mw.mr_worker.exiting = True
        onCancel()

    leftContainer = QWidget()
    leftContainer.setFixedWidth(450)
    leftContainer.setLayout(cntLeftLayout)
    rightContainer = QWidget()
    rightContainer.setFixedWidth(450)
    rightContainer.setLayout(cntRightLayout)
    cntColLayout.addWidget(leftContainer)
    cntColLayout.addWidget(rightContainer)
    cntOuterLayout.addLayout(cntColLayout)
    cntOuterLayout.addWidget(outputText)
    dialog = MatterRabbitWindow(cntOuterLayout, onDialogClose, mw)
    dialog.resize(950,700)
    dialog.setWindowTitle('Chinese Text Scanner - Config Note Types')
    dialog.show()
