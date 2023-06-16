from PySide6.QtWidgets import QCheckBox
from clickqt.widgets.base_widget import BaseWidget
from click import Parameter

class CheckBox(BaseWidget):
    widget_type = QCheckBox

    def __init__(self, param:Parameter, *args, **kwargs):
        super().__init__(param, *args, **kwargs)
        default = BaseWidget.getParamDefault(param, False)
        if isinstance(default, bool):
            self.setValue(default)
        
    def setValue(self, value: bool):
        self.widget.setChecked(value)
    
    def getWidgetValue(self) -> bool:
        return self.widget.isChecked()
    