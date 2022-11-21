from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyPDF4 import PdfFileMerger
import sys


class Ui_Dialog(QObject):
    """Main UI, also contains slot functions for button actions"""

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 450)
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setGeometry(QtCore.QRect(240, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.browse_button = QtWidgets.QPushButton(Dialog)
        self.browse_button.setGeometry(QtCore.QRect(60, 310, 121, 32))
        self.browse_button.setObjectName("browse_button")
        self.file_list_widget = ListDragWidget(Dialog)
        self.file_list_widget.setGeometry(QtCore.QRect(50, 60, 541, 241))
        self.file_list_widget.setObjectName("file_list_widget")
        self.remove_item_button = QtWidgets.QPushButton(Dialog)
        self.remove_item_button.setGeometry(QtCore.QRect(220, 310, 201, 32))
        self.remove_item_button.setObjectName("remove_item_button")
        self.clear_items_button = QtWidgets.QPushButton(Dialog)
        self.clear_items_button.setGeometry(QtCore.QRect(460, 310, 113, 32))
        self.clear_items_button.setObjectName("clear_items_button")
        self.exit_button = QtWidgets.QPushButton(Dialog)
        self.exit_button.setGeometry(QtCore.QRect(60, 400, 121, 32))
        self.exit_button.setObjectName("exit_button")
        self.merge_button = QtWidgets.QPushButton(Dialog)
        self.merge_button.setGeometry(QtCore.QRect(460, 400, 113, 32))
        self.merge_button.setObjectName("merge_button")

        self.retranslateUi(Dialog)
        self.clear_items_button.clicked.connect(self.clearItemsSlot)
        self.remove_item_button.clicked.connect(self.removeItemSlot)
        self.merge_button.clicked.connect(self.mergeDocSlot)
        self.browse_button.clicked.connect(self.browseSlot)
        self.exit_button.clicked.connect(self.exitSlot)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PDF File Merger"))
        self.title_label.setText(_translate("Dialog", "PDF File Merger"))
        self.browse_button.setText(_translate("Dialog", "Browse for Files"))
        self.remove_item_button.setText(
            _translate("Dialog", "Remove Selected Item"))
        self.clear_items_button.setText(
            _translate("Dialog", "Clear All Items"))
        self.exit_button.setText(_translate("Dialog", "Exit"))
        self.merge_button.setText(_translate("Dialog", "Merge Files"))

    @pyqtSlot()
    def clearItemsSlot(self):
        self.file_list_widget.clear()

    @pyqtSlot()
    def removeItemSlot(self):
        if self.file_list_widget.count() > 0:  # prevents crash if nothing in list
            self.file_list_widget.takeItem(self.file_list_widget.currentRow())

    @pyqtSlot()
    def browseSlot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        new_files, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Files to Merge", "", "PDF Files(*.pdf)",
                                                              options=options)  # *.pdf limits selection to pdf files only
        if new_files:  # check to make sure files were selected
            # new_files is separate from file_names in case user browses multiple times before merging
            for file_name in new_files:
                self.file_list_widget.addItem(file_name)

    @pyqtSlot()
    def mergeDocSlot(self):
        output_file_name = 'merged.pdf'  # default name for file output

        if self.file_list_widget.count() > 1:  # no merging unless there are enough documents to merge

            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            output_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File","merged", "PDF File (*.pdf)", options=options)

            for i in range(self.file_list_widget.count()):
                if output_file_name + ".pdf" == self.file_list_widget.item(i).text():
                    error_message = QtWidgets.QMessageBox.critical(None, "Error!", "Error! Your file name is already in use!")
                    return

            if output_file_name:  # check to make sure there is a name
                # user's file name won't include .pdf unless they type it in
                output_file_name = output_file_name + '.pdf'

                # create PDF merger object
                pdf_merger = PdfFileMerger(open(output_file_name, "wb"))

                for i in range(self.file_list_widget.count()):
                    # get everything from the file list
                    pdf_merger.append(self.file_list_widget.item(i).text())

                pdf_merger.write(output_file_name)
                pdf_merger.close()

                success_message = QtWidgets.QMessageBox.information(
                    None, "Files Merged", f"{output_file_name} has been successfully written!")


    @pyqtSlot()
    def exitSlot(self):
        QtCore.QCoreApplication.instance().quit()


class ListDragWidget(QtWidgets.QListWidget):
    """Creates a list widget that allows user to drag and drop PDF
    files into the widget area to add these files."""
    def __init__(self, parent):
        super(ListDragWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(ListDragWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(ListDragWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        global file_names
        if event.mimeData().hasUrls():
            for file in event.mimeData().urls():
                if file.path().endswith('.pdf'): # make sure it is a PDF file
                    self.addItem(file.toLocalFile())
        else:
            super(ListDragWidget, self).dropEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
