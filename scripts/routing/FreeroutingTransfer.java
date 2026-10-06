import app.freerouting.io.BoardReadResult;
import app.freerouting.io.specctra.DsnReader;
import app.freerouting.io.specctra.DsnWriter;
import app.freerouting.board.model.structure.FixedState;
import app.freerouting.geometry.planar.Circle;
import app.freerouting.geometry.planar.TileShape;
import com.google.gson.Gson;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.Map;

/** Calls official public file APIs; this performs no routing or DRC. */
public final class FreeroutingTransfer {
  public static void main(String[] args) throws Exception {
    if (args.length != 3) {
      throw new IllegalArgumentException("Expected input.dsn output.dsn engine-rules.json");
    }
    try (var input = Files.newInputStream(Path.of(args[0]))) {
      var result = DsnReader.readBoard(input, null, null);
      if (!(result instanceof BoardReadResult.Success success)) {
        throw new IllegalStateException("Freerouting rejected transfer: " + result);
      }
      if (!success.warnings().isEmpty()) {
        throw new IllegalStateException("Transfer has parser warnings: " + success.warnings());
      }
      try (var output = Files.newOutputStream(Path.of(args[1]))) {
        DsnWriter.write(success.board(), output, "tscircuit_native_transfer", false);
      }
      var board = success.board();
      var matrix = board.rules.clearanceMatrix;
      for (var area : board.getConductionAreas()) {
        if (area.getFixedState() != FixedState.SYSTEM_FIXED) {
          throw new IllegalStateException("Original copper region is not SYSTEM_FIXED");
        }
      }
      var constraints = new ArrayList<Map<String, Object>>();
      for (int layer = 0; layer < board.getLayerCount(); layer++) {
        for (int first = 1; first < matrix.getClassCount(); first++) {
          for (int second = first; second < matrix.getClassCount(); second++) {
            var constraint = new LinkedHashMap<String, Object>();
            constraint.put("layer", board.layerStructure.layers[layer].name);
            constraint.put("first", matrix.getName(first));
            constraint.put("second", matrix.getName(second));
            constraint.put("clearance_mm", board.communication.coordinateTransform.boardToDsn(
                matrix.getValue(first, second, layer, false)) / 1000);
            constraints.add(constraint);
          }
        }
      }
      var receipt = new LinkedHashMap<String, Object>();
      receipt.put("source_sha256", HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256")
          .digest(Files.readAllBytes(Path.of(args[0])))));
      receipt.put("clearances", constraints);
      receipt.put("system_fixed_copper_regions", board.getConductionAreas().size());
      receipt.put("engine_grid_mm", board.communication.coordinateTransform.boardToDsn(1) / 1000);
      var nets = new ArrayList<Map<String, Object>>();
      for (int number = 1; number <= board.rules.nets.maxNetNumber(); number++) {
        var net = board.rules.nets.get(number);
        var netReceipt = new LinkedHashMap<String, Object>();
        netReceipt.put("name", net.name);
        netReceipt.put("contains_plane", net.containsPlane());
        netReceipt.put("net_class", net.getNetClass().getName());
        nets.add(netReceipt);
      }
      receipt.put("nets", nets);
      var pinShapes = new ArrayList<Map<String, Object>>();
      for (var pin : board.getPins()) {
        var component = board.components.get(pin.getComponentId());
        var pinName = component.getPackage().getPin(pin.getPinIndex()).name;
        for (int layer = pin.firstLayer(); layer <= pin.lastLayer(); layer++) {
          var shape = pin.getShapeOnLayer(layer);
          var pinShape = new LinkedHashMap<String, Object>();
          pinShape.put("pin", component.name + "-" + pinName);
          pinShape.put("layer", board.layerStructure.layers[layer].name);
          if (shape instanceof Circle circle) {
            var center = board.communication.coordinateTransform.boardToDsn(circle.center.toFloat());
            pinShape.put("center_mm", new double[] {center[0] / 1000, center[1] / 1000});
            pinShape.put("radius_mm", board.communication.coordinateTransform.boardToDsn(circle.radius) / 1000);
          } else if (shape instanceof TileShape tile) {
            var corners = new ArrayList<double[]>();
            for (var corner : tile.cornerApproxArr()) {
              var point = board.communication.coordinateTransform.boardToDsn(corner);
              corners.add(new double[] {point[0] / 1000, point[1] / 1000});
            }
            pinShape.put("polygon_mm", corners);
          } else {
            throw new IllegalStateException("Unsupported engine pin geometry: " + shape.getClass());
          }
          pinShapes.add(pinShape);
        }
      }
      receipt.put("pin_shapes", pinShapes);
      receipt.put("classification", "Original input engine rules; DSN writer omits cross-class rules.");
      Files.writeString(Path.of(args[2]), new Gson().toJson(receipt) + "\n");
    }
    System.out.println("Official DSN reader/writer completed; routing and DRC were not run.");
  }
}
