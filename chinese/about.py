# Modified by mentheosis@gmail.com 2020-02 for "Chinese-Text-Scanner" anki addon
#
# Copyright © 2017-2018 Joseph Lorimer <joseph@lorimer.me>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout
from aqt import mw

from ._version import __version__


CSR_GITHUB_URL = 'https://github.com/mentheosis/anki-scanner-chinese-redux'


def showAbout():
    dialog = QDialog(mw)

    label = QLabel()
    label.setStyleSheet('QLabel { font-size: 14px; }')

    contributors = [
        'Kris Winquist',
        'Rob Carr',
        'Alex Griffin',
        'Chris Hatch',
        'Roland Sieker',
        'Thomas TEMPÉ',
    ]

    text = '''
<div style="font-weight: bold">Chinese Text Scanner, based on Chinese Support Redux v%s</div><br>
<div><span style="font-weight: bold">
    Maintainer</span>: Kris Winquist &lt;mentheosis@gmail.com&gt;</div>
<div><span style="font-weight: bold">Website</span>: <a href="%s">%s</a></div>
<div>
    <br> Powered by <a href="https://github.com/luoliyan/chinese-support-redux">Chinese-Support-Redux</a> by Joseph Lorimer <joseph@lorimer.me>
    <br> which is based on the Chinese Support add-on by Thomas TEMPÉ and many others.
    <br>If your name is missing from here, please open an issue on GitHub.
    <br>
    <div>Contributors: %s</div>
</div>
''' % (__version__, CSR_GITHUB_URL, CSR_GITHUB_URL, ', '.join(contributors))

    label.setText(text)
    label.setOpenExternalLinks(True)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
    buttonBox.accepted.connect(dialog.accept)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(buttonBox)

    dialog.setLayout(layout)
    dialog.setWindowTitle('About')
    dialog.exec_()
