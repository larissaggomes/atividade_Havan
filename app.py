# import models
#
# departments = models.Department.get_all()
#
# for d in departments:
#     print(d.id)
#     print(d.name)

import sys

from PyQt5.QtWidgets import QApplication
from views import Main

app = QApplication(sys.argv)

main_window = Main()
main_window.showMaximized()  # Em seguida, maximiza
sys.exit(app.exec_())
