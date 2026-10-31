"""Shared top-level I/O block (UART TTY + Keyboard, GPIO LEDs / hex digits / DIP switches)."""
import modules as M
from lgen import Port


def io_section(c, S, X, Y, n):
    """n: net names {'addr','wdata','MemWrite','MemRead','IsIO','ramout','memword'}"""
    io = c.inst(S['IOController'], X, Y)
    for pn, net in (('Addr', n['addr']), ('WData', n['wdata']), ('MemWrite', n['MemWrite']),
                    ('MemRead', n['MemRead']), ('IsIO', n['IsIO']), ('CLK', 'CLK'),
                    ('KbdData', 'IO_kbddata'), ('KbdAvail', 'IO_kbdavail'), ('GpioIn', 'IO_gpioin')):
        c.tun(io.p(pn), net, 30)
    for pn, net in (('IoRData', 'IO_rdata'), ('TxWE', 'IO_txwe'), ('TxData', 'IO_txdata'),
                    ('KbdRE', 'IO_kbdre'), ('GpioOut', 'IO_gpio')):
        c.tun(io.p(pn), net, 30)
    # data seen by Load/Store units: RAM word, or I/O register when the address is in the I/O region
    mw = c.add('Multiplexer', X + 290, Y - 40, width=32, select=1, enable='false')
    c.tun(mw.p(0), n['ramout'], 30)
    c.tun(mw.p(1), 'IO_rdata', 30)
    c.tun(mw.p(2), n['IsIO'], 20)
    c.tun(mw.p(3), n['memword'], 30)
    c.text(X + 180, Y - 90, 'IsIO ? I/O : RAM', size=10, color=M.TXT)
    # UART TX -> TTY
    tx, ty = X + 420, Y + 60
    tty = c.add('TTY', tx, ty, rows=8, cols=32)
    c.tun(tty.p(3), 'IO_txdata', 30)
    c.path(tty.p(1), (tx - 10, ty), (tx - 10, ty + 40))
    c.tun(Port(tx - 10, ty + 40, 1, 'S', 'i'), 'CLK', 10)
    c.tun(tty.p(2), 'IO_txwe', 80)
    c.const(tty.p(0), 0, 1, 30)
    c.text(tx, ty - 140, 'UART TX: TTY  (0xF0000000)', size=11, bold=True, color='#7c2d12')
    # UART RX <- Keyboard
    kx, ky = X + 420, Y + 220
    kb = c.add('Keyboard', kx, ky, buflen=32)
    c.tun(kb.p(1), 'CLK', 30)
    c.tun(kb.p(2), 'IO_kbdre', 30)
    c.const(kb.p(0), 0, 1, 70)
    c.tun(kb.p(3), 'IO_kbdavail', 30)
    c.tun(kb.p(4), 'IO_kbddata', 70)
    c.text(kx, ky - 24, 'UART RX: Keyboard (0xF0000004)',
           size=10, bold=True, color='#7c2d12')
    # GPIO_IN <- DIP switches
    dx, dy = X, Y + 330
    dip = c.add('DipSwitch', dx, dy, number=8)
    cm = c.splitter(dx, dy - 30, 8, [(i, i) for i in range(8)], facing='south', appear='left')
    for i in range(8):
        c.wire(cm.p(i + 1), dip.p(7 - i), first='vh')
    c.tun(cm.p(0), 'IO_gpioin', 20, side='W')
    c.text(dx, dy + 60, 'GPIO_IN: 8 DIP switch (0xF0000014), trai = bit 7', size=10, bold=True, color='#7c2d12')
    # GPIO_OUT -> 4 hex digits ([15:0]) + 8 LEDs ([23:16])
    gx, gy = X + 700, Y + 120
    gs = c.splitter(gx, gy, 32, [(12, 15), (8, 11), (4, 7), (0, 3), (16, 23)], spacing=2)
    c.tun(gs.p(0), 'IO_gpio', 30)
    for i in range(4):
        hd = c.add('Hex Digit Display', gx + 120 + 50 * i, gy - 70, decimalPoint='false')
        c.tun(hd.p(0), f'IO_hex{i}', 20)
        c.tun(gs.p(i + 1), f'IO_hex{i}', 20)
    lb = c.add('LedBar', gx + 200, gy + 60, matrixcols=8, inputtype='row')
    c.tun(lb.p(0), 'IO_led', 40)
    c.tun(gs.p(5), 'IO_led', 20)
    c.text(gx + 110, gy - 150, 'GPIO_OUT (0xF0000010): [15:0] hex, [23:16] LED', size=11, bold=True,
           color='#7c2d12')
    c.text(kx, ky + 110, 'STATUS 0xF0000008. Click vao Keyboard roi go phim', size=10, color=M.TXT)
    return io
