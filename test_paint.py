def _write_instruction2(self, asm, qp, cemu):
        s = asm.operands
        idx = 0
        qp.setPen(QtGui.QPen(QtGui.QColor(192, 192, 192), 1, QtCore.Qt.SolidLine))

        for tok in asm.lexer:
            if tok.lexpos > idx:
                cemu.write(s[idx:tok.lexpos])
                idx = tok.lexpos

            qp.save()
            if tok.type == 'REGISTER':
                qp.setPen(QtGui.QPen(QtGui.QColor('white')))

            if tok.type == 'NUMBER':
                qp.setPen(QtGui.QPen(QtGui.QColor('green')))

            cemu.write(tok.value)

            qp.restore()
            idx = tok.lexpos + len(tok.value)

        if idx < len(s):
            cemu.write(s[idx:]) 