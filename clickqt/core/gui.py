import click
from typing import Any
from clickqt.widgets.multivaluewidget import MultiValueWidget
from PySide6.QtWidgets import QApplication, QSplitter, QWidget, QVBoxLayout, QPushButton, QTabWidget
from PySide6.QtGui import QColor, Qt
from clickqt.widgets.checkbox import CheckBox
from clickqt.widgets.textfield import TextField
from clickqt.widgets.passwordfield import PasswordField
from clickqt.widgets.numericfields import IntField, RealField
from clickqt.widgets.combobox import ComboBox, CheckableComboBox
from clickqt.widgets.datetimeedit import DateTimeEdit
from clickqt.widgets.tuplewidget import TupleWidget
from clickqt.widgets.filepathfield import FilePathField
from clickqt.widgets.filefield import FileField
from clickqt.widgets.nvaluewidget import NValueWidget
from clickqt.widgets.confirmationwidget import ConfirmationWidget
from clickqt.widgets.messagebox import MessageBox
from clickqt.core.output import OutputStream, TerminalOutput
import sys

class GUI:
    """ GUI class responsible for setting up the components for the GUI that is used to navigate through the different kind of commands and their execution"""
    def __init__(self):
        self.window = QWidget()
        self.window.setLayout(QVBoxLayout())
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.setChildrenCollapsible(False) # Child widgets can't be resized down to size 0
        self.window.layout().addWidget(self.splitter)
        
        self.main_tab = QTabWidget()
        self.splitter.addWidget(self.main_tab)
 
        self.run_button = QPushButton("&Run")  # Shortcut Alt+R
        self.splitter.addWidget(self.run_button)

        self.terminal_output = TerminalOutput()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setToolTip("Terminal output")
        self.splitter.addWidget(self.terminal_output)
        sys.stdout = OutputStream(self.terminal_output, sys.stdout)
        sys.stderr = OutputStream(self.terminal_output, sys.stderr, QColor("red"))

    def __call__(self):
        self.window.show()
        QApplication.instance().exec()

    def create_widget(self, otype:click.ParamType, param:click.Parameter, *args, **kwargs):
        """ Function to return the widget object of the correct widget class determined by the param.type"""
        typedict = {
            click.types.BoolParamType: MessageBox if hasattr(param, "is_flag") and param.is_flag and hasattr(param, "prompt") and param.prompt else CheckBox,
            click.types.IntParamType: IntField,
            click.types.FloatParamType: RealField,
            click.types.StringParamType: PasswordField if hasattr(param, "hide_input") and param.hide_input else TextField,
            click.types.UUIDParameterType: TextField,
            click.types.UnprocessedParamType: TextField,
            click.types.DateTime: DateTimeEdit,
            click.types.Tuple: TupleWidget,
            click.types.Choice: ComboBox,
            click.types.Path: FilePathField,
            click.types.File: FileField
        }

        def get_multiarg_version(otype:click.ParamType):
            if isinstance(otype, click.types.Choice):
                return CheckableComboBox
            return NValueWidget

        if hasattr(param, "confirmation_prompt") and param.confirmation_prompt:
            return ConfirmationWidget(otype, param, *args, **kwargs)
        if param.multiple:
            return get_multiarg_version(otype)(otype, param, *args, **kwargs)
        if param.nargs > 1:
            if isinstance(otype, click.types.Tuple):
                return TupleWidget(otype, param, *args, **kwargs)
            return MultiValueWidget(otype, param, *args, **kwargs)

        for t, widgetclass in typedict.items():
            if isinstance(otype, t):
                return widgetclass(otype, param, *args, **kwargs)
            
        return TextField(otype, param, *args, **kwargs) # Custom types are mapped to TextField