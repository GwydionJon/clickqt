from PySide6.QtWidgets import QLineEdit, QInputDialog
from clickqt.widgets.base_widget import PathField
from typing import Tuple, Any
from PySide6.QtCore import QFile
from clickqt.core.error import ClickQtError
import sys
from io import StringIO, BytesIO
import re

class FileFild(PathField):
    widget_type = QLineEdit

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)

        self.file_type = PathField.FileType.File

    def getValue(self) -> Tuple[Any, ClickQtError]:
        if "r" in self.options["type"]["mode"] and self.widget.text() == "-":
            self.handleValid(True)

            def ret():
                old_stdin = sys.stdin
                user_input, ok = QInputDialog.getMultiLineText(self.widget, 'Stdin Input', self.label.text())
                if not ok:
                    return (None, ClickQtError(ClickQtError.ErrorType.ABORTED_ERROR))
                
                sys.stdin = BytesIO(user_input.encode(sys.stdin.encoding)) if "b" in self.options["type"]["mode"] else StringIO(user_input)
                val = super(FileFild, self).getValue()
                sys.stdin = old_stdin
                return val
            
            return (ret, ClickQtError())
        else:
            return super().getValue()
   
    def getWidgetValue(self) -> str:
        return self.widget.text()