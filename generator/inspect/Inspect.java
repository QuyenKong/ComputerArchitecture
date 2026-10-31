import com.cburch.logisim.file.*;
import com.cburch.logisim.circuit.*;
import com.cburch.logisim.comp.*;
import com.cburch.logisim.data.*;
import com.cburch.logisim.proj.Project;
import java.io.File;
import java.util.*;

public class Inspect {
  public static void main(String[] a) { try { realMain(a); } catch (Throwable t) { t.printStackTrace(); System.exit(2);} System.exit(0);}
  static void render(LogisimFile f, Project proj, String[] a) throws Exception {
    String outdir = a[2];
    int ticks = a.length > 3 ? Integer.parseInt(a[3]) : 0;
    double scale = a.length > 4 ? Double.parseDouble(a[4]) : 1.0;
    String only = a.length > 5 ? a[5] : null;
    Circuit main = f.getMainCircuit();
    com.cburch.logisim.circuit.CircuitState root = com.cburch.logisim.circuit.CircuitState.createRootState(proj, main, Thread.currentThread());
    proj.setCircuitState(root);
    var prop = root.getPropagator();
    prop.propagate();
    for (int i = 0; i < ticks; i++) { prop.toggleClocks(); prop.propagate(); }
    javax.swing.JPanel panel = new javax.swing.JPanel();
    for (Circuit c : f.getCircuits()) {
      if (only != null && !only.equals(c.getName())) continue;
      java.awt.image.BufferedImage tmp = new java.awt.image.BufferedImage(10,10,java.awt.image.BufferedImage.TYPE_INT_RGB);
      Bounds bds = c.getBounds(tmp.getGraphics()).expand(20);
      int w = (int)Math.round(bds.getWidth()*scale), h = (int)Math.round(bds.getHeight()*scale);
      java.awt.image.BufferedImage img = new java.awt.image.BufferedImage(w, h, java.awt.image.BufferedImage.TYPE_INT_RGB);
      java.awt.Graphics base = img.getGraphics();
      java.awt.Graphics g = base.create();
      g.setColor(java.awt.Color.white); g.fillRect(0,0,w,h); g.setColor(java.awt.Color.black);
      ((java.awt.Graphics2D)g).setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
      ((java.awt.Graphics2D)g).setRenderingHint(java.awt.RenderingHints.KEY_TEXT_ANTIALIASING, java.awt.RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
      ((java.awt.Graphics2D)g).scale(scale, scale);
      g.translate(-bds.getX(), -bds.getY());
      com.cburch.logisim.circuit.CircuitState st = (c == main) ? root : findState(root, c);
      if (st == null) st = proj.getCircuitState(c);
      ComponentDrawContext ctx = new ComponentDrawContext(panel, c, st, base, g, false);
      c.draw(ctx, null);
      javax.imageio.ImageIO.write(img, "PNG", new File(outdir, c.getName() + ".png"));
      System.out.println("rendered " + c.getName() + " " + w + "x" + h);
    }
  }
  static com.cburch.logisim.circuit.CircuitState findState(com.cburch.logisim.circuit.CircuitState s, Circuit c) {
    for (var sub : s.getSubstates()) { if (sub.getCircuit() == c) return sub; var r = findState(sub, c); if (r != null) return r; }
    return null;
  }
  public static void realMain(String[] a) throws Exception {
    String mode = a[0];
    Loader loader = new Loader(null);
    LogisimFile f = loader.openLogisimFile(new File(a[1]));
    Project proj = new Project(f);
    int problems = 0;
    if (mode.equals("render")) { render(f, proj, a); return; }
    for (Circuit c : f.getCircuits()) {
      if (mode.equals("ports")) {
        for (Component comp : c.getNonWires()) {
          StringBuilder sb = new StringBuilder();
          Location L = comp.getLocation();
          Bounds b = comp.getBounds();
          sb.append("{\"circ\":\"").append(c.getName()).append("\",\"name\":\"").append(comp.getFactory().getName())
            .append("\",\"x\":").append(L.getX()).append(",\"y\":").append(L.getY())
            .append(",\"bounds\":[").append(b.getX()-L.getX()).append(",").append(b.getY()-L.getY()).append(",").append(b.getWidth()).append(",").append(b.getHeight()).append("]")
            .append(",\"ends\":[");
          boolean first=true;
          for (EndData e : comp.getEnds()) {
            Location l = e.getLocation();
            if(!first) sb.append(","); first=false;
            sb.append("[").append(l.getX()-L.getX()).append(",").append(l.getY()-L.getY()).append(",").append(e.getWidth().getWidth())
              .append(",\"").append(e.isInput()&&e.isOutput()?"io":e.isInput()?"i":"o").append("\"]");
          }
          sb.append("]}");
          System.out.println(sb);
        }
      } else {
        // lint
        Map<Location,Integer> cnt = new HashMap<>();
        for (Component comp : c.getNonWires()) for (EndData e : comp.getEnds()) cnt.merge(e.getLocation(),1,Integer::sum);
        for (Wire w : c.getWires()) { cnt.merge(w.getEnd0(),1,Integer::sum); cnt.merge(w.getEnd1(),1,Integer::sum); }
        Map<String,Integer> tun = new HashMap<>();
        for (Location l : cnt.keySet()) for (Wire w : c.getWires()) {
          if (w.contains(l) && !l.equals(w.getEnd0()) && !l.equals(w.getEnd1())) {
            System.out.println("[" + c.getName() + "] T-TOUCH point " + l + " on wire " + w.getEnd0() + "-" + w.getEnd1()); problems++; }
        }
        for (Component comp : c.getNonWires()) {
          String fn = comp.getFactory().getName();
          if (fn.equals("Tunnel")) tun.merge(comp.getAttributeSet().getValue(com.cburch.logisim.instance.StdAttr.LABEL),1,Integer::sum);
          if (fn.equals("Text")) continue;
          for (EndData e : comp.getEnds()) {
            if (cnt.get(e.getLocation()) < 2) {
              boolean outOnly = e.isOutput() && !e.isInput();
              if (outOnly && !fn.equals("Pin")) { if (System.getenv("SHOWOUT")!=null) System.out.println("[" + c.getName() + "] (unused output) " + fn + " @" + comp.getLocation() + " end " + e.getLocation()); continue; }
              System.out.println("[" + c.getName() + "] DANGLING " + fn + " @" + comp.getLocation() + " end " + e.getLocation());
              problems++;
            }
          }
        }
        for (Wire w : c.getWires()) for (Location l : new Location[]{w.getEnd0(), w.getEnd1()})
          if (cnt.get(l) < 2) { System.out.println("[" + c.getName() + "] DANGLING wire end " + l); problems++; }
        for (var e : tun.entrySet()) if (e.getValue() < 2) { System.out.println("[" + c.getName() + "] LONELY tunnel " + e.getKey()); problems++; }
        if (c.getWidthIncompatibilityData()!=null) for (var wi : c.getWidthIncompatibilityData()) {
          System.out.println("[" + c.getName() + "] WIDTH CONFLICT at " + wi.getPoint(0)); problems++; }
      }
    }
    if (mode.equals("lint")) System.out.println("LINT problems: " + problems);
    System.exit(0);
  }
}
