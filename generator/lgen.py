"""lgen.py - tiny Logisim-evolution 4.1.0 .circ generator.

Geometry of built-in components is NOT hard-coded: every distinct
(component, attributes) combination is placed in a probe file, loaded by the
real Logisim jar (Inspect.java) and the real port offsets are cached in
geometry.json.  Sub-circuits use custom appearances whose port geometry we
define ourselves.
"""
import json, os, subprocess, hashlib
from xml.sax.saxutils import escape, quoteattr

HERE = os.path.dirname(os.path.abspath(__file__))
GEOM_FILE = os.path.join(HERE, 'geometry.json')
# Only needed when a NEW component/attribute combination appears (geometry.json is a cache).
# run.sh = java -Djava.awt.headless=true -cp <logisim.jar>:<dir of Inspect.class> Inspect "$@"
INSPECT = os.environ.get('LOGISIM_INSPECT', os.path.join(HERE, 'inspect', 'run.sh'))

LIBS = ['#Wiring', '#Gates', '#Plexers', '#Arithmetic', '#FPArithmetic', '#Memory',
        '#I/O', '#TTL', '#TCL', '#Base', '#BFH-Praktika', '#Input/Output-Extra', '#Soc']
LIB = {n: i for i, n in enumerate(LIBS)}
# component name -> library
COMP_LIB = {}
for n in ['Pin', 'Tunnel', 'Constant', 'Splitter', 'Probe', 'Clock', 'Bit Extender',
          'Ground', 'Power', 'Pull Resistor']:
    COMP_LIB[n] = '#Wiring'
for n in ['AND Gate', 'OR Gate', 'XOR Gate', 'NOT Gate', 'NAND Gate', 'NOR Gate', 'XNOR Gate', 'Buffer']:
    COMP_LIB[n] = '#Gates'
for n in ['Multiplexer', 'Demultiplexer', 'Decoder', 'Priority Encoder', 'BitSelector']:
    COMP_LIB[n] = '#Plexers'
for n in ['Adder', 'Subtractor', 'Multiplier', 'Divider', 'Negator', 'Comparator', 'Shifter', 'BitAdder', 'BitFinder']:
    COMP_LIB[n] = '#Arithmetic'
for n in ['Register', 'Counter', 'ROM', 'RAM', 'D Flip-Flop']:
    COMP_LIB[n] = '#Memory'
for n in ['TTY', 'Hex Digit Display', 'LED', 'Keyboard', 'DipSwitch', 'LedBar']:
    COMP_LIB[n] = '#I/O'
COMP_LIB['Text'] = '#Base'

NON_GEOM = {'label', 'value', 'contents', 'text', 'font', 'labelfont',
            'labelvisible', 'labelloc', 'color', 'halign', 'valign'}

_geom = json.load(open(GEOM_FILE)) if os.path.exists(GEOM_FILE) else {}
_missing = {}


def gkey(name, attrs):
    return name + '|' + json.dumps(sorted((k, str(v)) for k, v in attrs.items() if k not in NON_GEOM))


class Port:
    __slots__ = ('x', 'y', 'w', 'side', 'kind')

    def __init__(self, x, y, w, side, kind):
        self.x, self.y, self.w, self.side, self.kind = x, y, w, side, kind

    @property
    def xy(self):
        return (self.x, self.y)

    def __repr__(self):
        return f'Port({self.x},{self.y},w{self.w},{self.side})'


def _side(dx, dy, b):
    bx, by, bw, bh = b
    d = {'W': abs(dx - bx), 'E': abs(dx - (bx + bw)), 'N': abs(dy - by), 'S': abs(dy - (by + bh))}
    return min(d, key=d.get)


class Comp:
    def __init__(self, circ, name, x, y, attrs, sub=None):
        self.circ, self.name, self.x, self.y, self.attrs, self.sub = circ, name, x, y, attrs, sub
        self.key = gkey(name, attrs)
        if sub is None and self.key not in _geom:
            _missing[self.key] = (name, attrs)

    def p(self, i):
        """absolute port i (index in Logisim getEnds() order, or name for subcircuits)"""
        if self.sub is not None:
            dx, dy, w, side, kind = self.sub.port_off[i]
            return Port(self.x + dx, self.y + dy, w, side, kind)
        g = _geom.get(self.key)
        if g is None:
            return Port(self.x, self.y, 1, 'E', 'o')  # placeholder during collect pass
        dx, dy, w, kind = g['ends'][i]
        return Port(self.x + dx, self.y + dy, w, _side(dx, dy, g['bounds']), kind)

    def bounds(self):
        """absolute (x, y, w, h)"""
        if self.sub is not None:
            return None
        g = _geom.get(self.key)
        if g is None:
            return (self.x, self.y, 10, 10)
        bx, by, bw, bh = g['bounds']
        return (self.x + bx, self.y + by, bw, bh)

    def nports(self):
        if self.sub is not None:
            return len(self.sub.port_off)
        g = _geom.get(self.key)
        return len(g['ends']) if g else 0

    def xml(self):
        if self.sub is not None:
            s = f'    <comp loc="({self.x},{self.y})" name={quoteattr(self.name)}>\n'
        else:
            s = f'    <comp lib="{LIB[COMP_LIB[self.name]]}" loc="({self.x},{self.y})" name={quoteattr(self.name)}>\n'
        for k, v in self.attrs.items():
            if k == 'contents':
                s += f'      <a name="contents">{escape(str(v))}</a>\n'
            else:
                s += f'      <a name={quoteattr(k)} val={quoteattr(str(v))}/>\n'
        return s + '    </comp>\n'


def missing():
    return dict(_missing)


def probe(run=True):
    """Place every unknown component in a probe circuit, ask Logisim for real geometry."""
    if not _missing:
        return False
    for k in list(_missing):
        if k in _geom:
            del _missing[k]
    items = list(_missing.items())
    comps = []
    for i, (k, (name, attrs)) in enumerate(items):
        x = 1000 + (i % 20) * 1000
        y = 1000 + (i // 20) * 1000
        comps.append((k, x, y, Comp(None, name, x, y, attrs)))
    body = ''.join(c.xml() for _, _, _, c in comps)
    path = os.path.join(HERE, '_probe.circ')
    open(path, 'w').write(file_header('main') + '  <circuit name="main">\n' + body + '  </circuit>\n</project>\n')
    out = subprocess.run([INSPECT, 'ports', path], capture_output=True, text=True, timeout=300).stdout
    byloc = {}
    for line in out.splitlines():
        if line.startswith('{'):
            d = json.loads(line)
            byloc[(d['x'], d['y'])] = d
    for k, x, y, c in comps:
        d = byloc[(x, y)]
        _geom[k] = {'bounds': d['bounds'], 'ends': d['ends']}
    json.dump(_geom, open(GEOM_FILE, 'w'), indent=0)
    _missing.clear()
    return True


def file_header(main):
    libs = ''.join(f'  <lib desc="{d}" name="{i}"/>\n' for i, d in enumerate(LIBS))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project source="4.1.0" version="1.0">
  This file is intended to be loaded by Logisim-evolution v4.1.0(https://github.com/logisim-evolution/).

{libs}  <main name={quoteattr(main)}/>
  <options>
    <a name="gateUndefined" val="ignore"/>
    <a name="simlimit" val="1000"/>
    <a name="simrand" val="0"/>
  </options>
  <mappings>
    <tool lib="9" map="Button2" name="Poke Tool"/>
    <tool lib="9" map="Button3" name="Menu Tool"/>
    <tool lib="9" map="Ctrl Button1" name="Menu Tool"/>
  </mappings>
  <toolbar>
    <tool lib="9" name="Poke Tool"/>
    <tool lib="9" name="Edit Tool"/>
    <tool lib="9" name="Wiring Tool"/>
    <tool lib="9" name="Text Tool"/>
    <sep/>
    <tool lib="0" name="Pin"/>
    <tool lib="0" name="Pin">
      <a name="facing" val="west"/>
      <a name="output" val="true"/>
    </tool>
    <sep/>
    <tool lib="1" name="NOT Gate"/>
    <tool lib="1" name="AND Gate"/>
    <tool lib="1" name="OR Gate"/>
    <tool lib="1" name="XOR Gate"/>
    <sep/>
    <tool lib="5" name="Register"/>
  </toolbar>
'''


# ---------------------------------------------------------------------------
# Circuit builder
# ---------------------------------------------------------------------------
OUT_DIR = {'W': (-1, 0), 'E': (1, 0), 'N': (0, -1), 'S': (0, 1)}
TUN_FACING = {'W': 'east', 'E': 'west', 'N': 'south', 'S': 'north'}  # tag body away from port


def _xy(p):
    return p.xy if isinstance(p, Port) else tuple(p)


class Circuit:
    def __init__(self, name, title=None):
        self.name = name
        self.title = title or name
        self.comps = []
        self.segs = []          # list of ((x1,y1),(x2,y2))
        self.pins = {}          # label -> (Comp, 'in'|'out', width)
        self.appear = None      # (svg_body, port_off dict)
        self.port_off = {}
        self.extra_xml = ''
        self.op = 0              # drawing-operation id, used to detect accidental joins
        self.seg_op = []
        self.junctions = set()

    # -- primitives ---------------------------------------------------------
    def add(self, name, x, y, **attrs):
        attrs = {k.replace('_', '-') if k.startswith('negate') else k: v for k, v in attrs.items()}
        c = Comp(self, name, x, y, attrs)
        self.comps.append(c)
        return c

    def inst(self, sub, x, y, label=None):
        attrs = {}
        if label:
            attrs['label'] = label
        c = Comp(self, sub.name, x, y, attrs, sub=sub)
        self.comps.append(c)
        return c

    def wire(self, a, b, mid=None, first='h'):
        """Manhattan wire a->b.  first='h': horizontal, vertical, horizontal (bend at x=mid).
        first='v': vertical, horizontal, vertical (bend at y=mid)."""
        self.op += 1
        (x1, y1), (x2, y2) = _xy(a), _xy(b)
        if (x1, y1) == (x2, y2):
            return
        if x1 == x2 or y1 == y2:
            self._seg((x1, y1), (x2, y2))
            return
        if first == 'h':
            m = mid if mid is not None else (x1 + x2) // 20 * 10
            self._seg((x1, y1), (m, y1)); self._seg((m, y1), (m, y2)); self._seg((m, y2), (x2, y2))
        elif first == 'hv':  # horizontal then vertical (L shape)
            self._seg((x1, y1), (x2, y1)); self._seg((x2, y1), (x2, y2))
        elif first == 'vh':  # vertical then horizontal (L shape)
            self._seg((x1, y1), (x1, y2)); self._seg((x1, y2), (x2, y2))
        else:
            m = mid if mid is not None else (y1 + y2) // 20 * 10
            self._seg((x1, y1), (x1, m)); self._seg((x1, m), (x2, m)); self._seg((x2, m), (x2, y2))

    def path(self, *pts):
        self.op += 1
        pts = [_xy(p) for p in pts]
        for a, b in zip(pts, pts[1:]):
            if a != b:
                if _missing and not (a[0] == b[0] or a[1] == b[1]):
                    continue          # first pass: geometry not probed yet
                assert a[0] == b[0] or a[1] == b[1], (self.name, a, b)
                self._seg(a, b)

    def _seg(self, a, b):
        for v in a + b:
            assert v % 10 == 0, (self.name, a, b)
        if a == b:
            return
        self.segs.append((a, b))
        self.seg_op.append(self.op)

    def tun(self, port, label, length=20, side=None, width=None):
        """Short stub out of `port` ending in a Tunnel named `label`."""
        self.op += 1
        side = side or port.side
        dx, dy = OUT_DIR[side]
        ex, ey = port.x + dx * length, port.y + dy * length
        if length:
            self._seg(port.xy, (ex, ey))
        w = width or port.w
        self.add('Tunnel', ex, ey, facing=TUN_FACING[side], width=w, label=label,
                 labelfont='SansSerif plain 10')
        return (ex, ey)

    def const(self, port, value, width=None, length=20, side=None):
        self.op += 1
        side = side or port.side
        dx, dy = OUT_DIR[side]
        ex, ey = port.x + dx * length, port.y + dy * length
        if length:
            self._seg(port.xy, (ex, ey))
        w = width or port.w
        f = {'W': 'east', 'E': 'west', 'N': 'south', 'S': 'north'}[side]
        self.add('Constant', ex, ey, width=w, value=hex(value), facing=f)

    def probe(self, port, length=20, side=None, label=None, radix=16, facing=None, labelloc=None):
        self.op += 1
        side = side or port.side
        dx, dy = OUT_DIR[side]
        ex, ey = port.x + dx * length, port.y + dy * length
        if length:
            self._seg(port.xy, (ex, ey))
        f = facing or {'W': 'east', 'E': 'west', 'N': 'south', 'S': 'north'}[side]
        a = dict(radix=radix, facing=f, appearance='classic')
        if label:
            a['label'] = label
        if labelloc:
            a['labelloc'] = labelloc
        self.add('Probe', ex, ey, **a)

    def text(self, x, y, s, size=12, bold=False, color='#000000', halign='left', italic=False, family='SansSerif'):
        style = 'bold' if bold else ('italic' if italic else 'plain')
        self.add('Text', x, y, text=s, font=f'{family} {style} {size}', color=color,
                 halign=halign, valign='base')

    def pin_in(self, label, width, x, y, facing='east', labelloc='west'):
        c = self.add('Pin', x, y, width=width, label=label, appearance='classic', facing=facing,
                     radix=16, labelloc=labelloc)
        self.pins[label] = (c, 'in', width)
        return c.p(0) if c.nports() else Port(x, y, width, 'E', 'o')

    def pin_out(self, label, width, x, y, facing='west', labelloc='east'):
        c = self.add('Pin', x, y, width=width, label=label, appearance='classic', facing=facing,
                     output='true', radix=16, labelloc=labelloc)
        self.pins[label] = (c, 'out', width)
        return Port(x, y, width, 'W', 'i')

    def splitter(self, x, y, incoming, groups, facing='east', appear='right', spacing=1):
        """groups: list of (lo, hi) inclusive bit ranges; output i carries bits lo..hi.
        Unlisted bits are left unconnected."""
        attrs = dict(fanout=len(groups), incoming=incoming, appear=appear, facing=facing)
        if spacing != 1:
            attrs['spacing'] = spacing
        for b in range(incoming):
            attrs[f'bit{b}'] = 'none'
        for gi, (lo, hi) in enumerate(groups):
            for b in range(lo, hi + 1):
                attrs[f'bit{b}'] = gi
        return self.add('Splitter', x, y, **attrs)

    def bus_v(self, x, ys):
        """vertical bus bar at x, split into segments at every tap y so that taps connect."""
        ys = sorted(set(ys))
        for y in ys:
            self.junctions.add((x, y))
        for a, b in zip(ys, ys[1:]):
            self._seg((x, a), (x, b))

    def bus_h(self, y, xs):
        xs = sorted(set(xs))
        for x in xs:
            self.junctions.add((x, y))
        for a, b in zip(xs, xs[1:]):
            self._seg((a, y), (b, y))

    def fan_in(self, pairs, col_x):
        """Route nets (src, dst) where dst ports share an x on the right and srcs are on the
        left.  Each net is H-V-H; vertical columns are assigned right-to-left starting at
        col_x so that the bundle has no crossings."""
        down = sorted([p for p in pairs if p[0].y < p[1].y], key=lambda p: p[0].y)
        up = sorted([p for p in pairs if p[0].y > p[1].y], key=lambda p: -p[0].y)
        for s, d in pairs:
            if s.y == d.y:
                self._seg(s.xy, d.xy)
        k = 0
        for grp in (down, up):
            for i, (s, d) in enumerate(grp):
                cx = col_x - 10 * (i + k)
                self.path(s, (cx, s.y), (cx, d.y), d)
            k += len(grp)

    @staticmethod
    def pick_y(src_ys, first_off, guess, pitch=10, n=None):
        """Choose a component y so that input i (at y+first_off+i*pitch) never sits at the
        same height as the source of a *different* net (avoids collinear overlaps)."""
        n = n or len(src_ys)
        for d in range(0, 400, 10):
            for y in (guess + d, guess - d):
                dst = [y + first_off + i * pitch for i in range(n)]
                if all(src_ys[i] != dst[j] for i in range(n) for j in range(n) if i != j):
                    return y
        raise ValueError('no y')

    def fan_out(self, pairs, col_x):
        """Mirror of fan_in: one source column on the left fanning out to destinations on the
        right; columns assigned left-to-right starting at col_x."""
        down = sorted([p for p in pairs if p[0].y < p[1].y], key=lambda p: -p[1].y)
        up = sorted([p for p in pairs if p[0].y > p[1].y], key=lambda p: p[1].y)
        for s, d in pairs:
            if s.y == d.y:
                self._seg(s.xy, d.xy)
        k = 0
        for grp in (down, up):
            for i, (s, d) in enumerate(grp):
                cx = col_x + 10 * (i + k)
                self.path(s, (cx, s.y), (cx, d.y), d)
            k += len(grp)

    # -- appearance -----------------------------------------------------------
    def box(self, w, h, left=(), right=(), top=(), bottom=(), title=None, fill='#ffffff',
            title_pos='center', shape=None, extra_svg='', label_size=10, title_size=13,
            subtitle=None):
        """Custom symbol. left/right/top/bottom: list of (pin_label, offset) where offset is
        distance from box top (left/right) or box left (top/bottom); multiples of 10."""
        X0, Y0 = 50, 50
        svg = []
        if shape is None:
            svg.append(f'<rect fill="{fill}" height="{h}" stroke="#000000" stroke-width="2" '
                       f'width="{w}" x="{X0}" y="{Y0}"/>')
        else:
            pts = ' '.join(f'{X0 + px},{Y0 + py}' for px, py in shape)
            svg.append(f'<polygon fill="{fill}" points="{pts}" stroke="#000000" stroke-width="2"/>')
        tt = title or self.title
        if tt:
            if title_pos == 'center':
                ty = Y0 + h // 2
            elif title_pos == 'top':
                ty = Y0 + 14
            else:
                ty = Y0 + h - 10
            svg.append(f'<text dominant-baseline="central" font-family="SansSerif" font-size="{title_size}" '
                       f'font-weight="bold" text-anchor="middle" x="{X0 + w // 2}" y="{ty}">{escape(tt)}</text>')
            if subtitle:
                svg.append(f'<text dominant-baseline="central" font-family="SansSerif" font-size="9" '
                           f'font-style="italic" text-anchor="middle" x="{X0 + w // 2}" y="{ty + 14}">{escape(subtitle)}</text>')
        ports = []

        def add_port(lbl, x, y, side, tx, ty, anchor, show=True, text=None):
            assert x % 10 == 0 and y % 10 == 0, (self.name, lbl, x, y)
            c, d, wd = self.pins[lbl]
            ports.append(f'<circ-port dir="{d}" pin="{c.x},{c.y}" x="{x}" y="{y}"/>')
            self.port_off[lbl] = (x - X0, y - Y0, wd, side, 'i' if d == 'in' else 'o')
            if show:
                svg.append(f'<text dominant-baseline="central" font-family="SansSerif" font-size="{label_size}" '
                           f'text-anchor="{anchor}" x="{tx}" y="{ty}">{escape(text or lbl)}</text>')

        def norm(item):
            if len(item) == 2:
                return item[0], item[1], True, None
            if len(item) == 3:
                return item[0], item[1], item[2] is not False, (item[2] if isinstance(item[2], str) else None)
            return item

        for it in left:
            lbl, off, show, txt = norm(it)
            add_port(lbl, X0, Y0 + off, 'W', X0 + 4, Y0 + off, 'start', show, txt)
        for it in right:
            lbl, off, show, txt = norm(it)
            add_port(lbl, X0 + w, Y0 + off, 'E', X0 + w - 4, Y0 + off, 'end', show, txt)
        for it in top:
            lbl, off, show, txt = norm(it)
            add_port(lbl, X0 + off, Y0, 'N', X0 + off, Y0 + 9, 'middle', show, txt)
        for it in bottom:
            lbl, off, show, txt = norm(it)
            add_port(lbl, X0 + off, Y0 + h, 'S', X0 + off, Y0 + h - 8, 'middle', show, txt)
        svg.append(extra_svg)
        svg.extend(ports)
        svg.append(f'<circ-anchor facing="east" x="{X0}" y="{Y0}"/>')
        self.appear = '    <appear>\n' + ''.join('      ' + s + '\n' for s in svg if s) + '    </appear>\n'
        missing_pins = set(self.pins) - set(self.port_off)
        assert not missing_pins, (self.name, missing_pins)

    def check(self):
        """Logisim joins a wire end that lies inside another wire (T-junction) and merges
        overlapping collinear wires.  Our generator never wants that implicitly, so flag it."""
        segs = []
        for a, b in self.segs:
            k = (min(a, b), max(a, b))
            if k not in segs:
                segs.append(k)
        pts = set()
        for a, b in segs:
            pts.add(a); pts.add(b)
        for c in self.comps:
            if c.name == 'Text':
                continue
            keys = list(c.sub.port_off) if c.sub is not None else range(c.nports())
            for i in keys:
                pts.add(c.p(i).xy)
        errs = []
        for (a, b) in segs:
            for p in pts:
                if p == a or p == b:
                    continue
                if a[0] == b[0] == p[0] and a[1] < p[1] < b[1]:
                    errs.append((p, a, b))
                if a[1] == b[1] == p[1] and a[0] < p[0] < b[0]:
                    errs.append((p, a, b))
        # endpoints shared by wires drawn in different operations = accidental join
        ops_at, ends = {}, {}
        for (a, b), op in zip(self.segs, self.seg_op):
            for p in (a, b):
                ops_at.setdefault(p, set()).add(op)
                ends[p] = ends.get(p, 0) + 1
        for p, ops in ops_at.items():
            if len(ops) > 1 and ends[p] >= 3 and p not in self.junctions:
                errs.append((p, 'join of', tuple(sorted(ops))))
        return errs

    # -- output -----------------------------------------------------------------
    def xml(self):
        s = f'  <circuit name={quoteattr(self.name)}>\n'
        s += f'    <a name="appearance" val="{"custom" if self.appear else "logisim_evolution"}"/>\n'
        s += f'    <a name="circuit" val={quoteattr(self.name)}/>\n'
        s += '    <a name="circuitnamedboxfixedsize" val="true"/>\n'
        s += '    <a name="simulationFrequency" val="1.0"/>\n'
        if self.appear:
            s += self.appear
        for c in self.comps:
            s += c.xml()
        seen = set()
        for a, b in self.segs:
            k = (min(a, b), max(a, b))
            if k in seen:
                continue
            seen.add(k)
            s += f'    <wire from="({a[0]},{a[1]})" to="({b[0]},{b[1]})"/>\n'
        return s + '  </circuit>\n'


def write_project(path, circuits, main):
    bad = False
    for c in circuits:
        for e in c.check():
            print(f'[{c.name}] wiring problem at {e[0]}: {e[1]} {e[2]}')
            bad = True
    if bad:
        raise SystemExit('geometry errors')
    data = file_header(main) + ''.join(c.xml() for c in circuits) + '</project>\n'
    open(path, 'w').write(data)


def build(fn):
    """Run builder fn() -> (circuits, main) twice: first to discover geometry, then for real."""
    for _ in range(6):
        _missing.clear()
        res = fn()
        if not _missing:
            return res
        probe()
    raise AssertionError(_missing)
