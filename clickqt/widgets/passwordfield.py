from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QIcon, QAction
from clickqt.widgets.textfield import TextField
from click import Parameter, ParamType

class PasswordField(TextField):
    widget_type = QLineEdit

    def __init__(self, otype:ParamType, param:Parameter, *args, **kwargs):
        super().__init__(otype, param, *args, **kwargs)

        assert hasattr(param, "hide_input") and param.hide_input, "'param.hide_input' should be True"

        self.icon_text = ((QIcon('clickqt\\images\\eye-show.png'), 'Show password'), (QIcon('clickqt\\images\\eye-hide.png'), 'Hide password'))
        self.show_hide_action = QAction(icon=self.icon_text[0][0], text=self.icon_text[0][1])
        self.widget.setEchoMode(QLineEdit.EchoMode.Password)
        self.widget.addAction(self.show_hide_action, QLineEdit.ActionPosition.TrailingPosition)
        self.show_hide_action.setCheckable(True)

        def showPassword(show):
            self.widget.setEchoMode(QLineEdit.EchoMode.Normal if show else QLineEdit.EchoMode.Password)
            self.show_hide_action.setIcon(self.icon_text[show][0])
            self.show_hide_action.setText(self.icon_text[show][1])

        self.show_hide_action.toggled.connect(showPassword)
