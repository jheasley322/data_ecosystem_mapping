import sys
import yaml
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF

# Load YAML configurations
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load configs
main_config = load_yaml("primary_config/main_config.yaml")
branded_nodes = load_yaml("primary_config/branded_nodes.yaml")
project_config = load_yaml("projects/project_template.yaml")

class Node(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, label=None):
        super().__init__(0, 0, 80, 80)  # Fixed node size
        self.setBrush(QBrush(QColor("#4285F4")))  # Default color
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable | QGraphicsEllipseItem.ItemIsSelectable)
        self.node_id = node_id
        self.label = label
        self.text = QGraphicsTextItem(label, self)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setPos(20, 30)  # Centered label

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print(f"Node {self.node_id} moved to: {self.pos()}")

class Connection(QGraphicsLineItem):
    def __init__(self, node1, node2):
        super().__init__()
        self.setPen(QPen(Qt.black, 2))
        self.node1 = node1
        self.node2 = node2
        self.update_position()
    
    def update_position(self):
        pos1 = self.node1.scenePos() + QPointF(40, 40)  # Middle of node1
        pos2 = self.node2.scenePos() + QPointF(40, 40)  # Middle of node2
        self.setLine(pos1.x(), pos1.y(), pos2.x(), pos2.y())

class EcosystemGraph(QGraphicsScene):
    def __init__(self, config):
        super().__init__()
        self.nodes = {}
        self.connections = []
        self.load_nodes(config["nodes"])
        self.load_connections(config["connections"])

    def load_nodes(self, nodes):
        for node in nodes:
            n = Node(node["id"], node["position"]["x"], node["position"]["y"], node.get("label"))
            self.addItem(n)
            n.setPos(node["position"]["x"], node["position"]["y"])  # Initial positioning
            self.nodes[node["id"]] = n
    
    def load_connections(self, connections):
        for conn in connections:
            if conn["from"] in self.nodes and conn["to"] in self.nodes:
                line = Connection(self.nodes[conn["from"]], self.nodes[conn["to"]])
                self.addItem(line)
                self.connections.append(line)

class MainView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(self.renderHints())
        self.setScene(scene)
        self.setSceneRect(0, 0, 800, 600)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = EcosystemGraph(project_config)
    view = MainView(scene)
    view.show()
    sys.exit(app.exec_())
