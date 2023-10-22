// Representación del laberinto (1: camino libre, 0: pared)
const matrix = [
  [4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4],
  [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 3, 4, 4, 4],
  [4, 4, 4, 2, 2, 4, 1, 4, 1, 1, 3, 3, 4, 1, 1],
  [4, 4, 2, 2, 2, 2, 1, 4, 1, 1, 3, 3, 1, 1, 1],
  [4, 4, 2, 2, 2, 2, 1, 4, 4, 1, 1, 3, 1, 1, 1],
  [4, 4, 4, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3],
  [4, 4, 4, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 3],
  [4, 4, 4, 1, 0, 4, 4, 1, 1, 3, 3, 3, 3, 2, 2],
  [4, 4, 4, 1, 1, 4, 4, 0, 1, 3, 3, 3, 2, 2, 2],
  [4, 4, 1, 1, 1, 1, 0, 0, 0, 3, 3, 2, 2, 2, 2],
  [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 3, 2, 2, 2, 2],
  [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2],
  [4, 4, 1, 4, 4, 1, 1, 3, 3, 3, 2, 2, 2, 2, 2],
  [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2],
  [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2]
];

const maze = [
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  // 0
  [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  // 1
  [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],  // 2
  [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],  // 3
  [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],  // 4
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // 5
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  // 6
  [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 7
  [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 8
  [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 9
  [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 10
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 11
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 12
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  // 13
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]   // 14
  //0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 2, 3, 4
];



// Definición de nodos
class Node {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.g = 0; // Costo acumulado
    this.h = 0; // Heurística
    this.f = 0; // f = g + h (prioridad)
    this.parent = null; // Nodo padre
  }
}

// Función heurística (distancia de Manhattan)
function heuristic(node, goal) {
  return Math.abs(node.x - goal.x) + Math.abs(node.y - goal.y);
}

// Implementación del algoritmo A*
function astar(maze, start, end) {
  const openList = [];
  const closedList = [];

  const startNode = new Node(start[0], start[1]);
  const endNode = new Node(end[0], end[1]);

  openList.push(startNode);

  while (openList.length > 0) {
    let currentNode = openList[0];
    let currentIndex = 0;

    // Encontrar el nodo con el valor f mínimo en la lista abierta
    openList.forEach((node, index) => {
      if (node.f < currentNode.f) {
        currentNode = node;
        currentIndex = index;
      }
    });

    // Mover el nodo actual de la lista abierta a la lista cerrada
    openList.splice(currentIndex, 1);
    closedList.push(currentNode);

    // Si hemos llegado al nodo de destino, reconstruir el camino
    if (currentNode.x === endNode.x && currentNode.y === endNode.y) {
      const path = [];
      let current = currentNode;
      while (current) {
        path.push([current.x, current.y]);
        current = current.parent;
      }
      return path.reverse();
    }

    // Generar sucesores (nodos vecinos)
    const neighbors = [];
    const x = currentNode.x;
    const y = currentNode.y;
    const potentialNeighbors = [
      [x - 1, y],
      [x, y - 1],
      [x + 1, y],
      [x, y + 1],
    ];

    potentialNeighbors.forEach(([x, y]) => {
      if (
        x >= 0 &&
        x < maze.length &&
        y >= 0 &&
        y < maze[0].length &&
        maze[x][y] === 1
      ) {
        neighbors.push(new Node(x, y));
      }
    });

    // Procesar cada sucesor
    neighbors.forEach((neighbor) => {
      if (closedList.find((node) => node.x === neighbor.x && node.y === neighbor.y)) {
        return;
      }

      neighbor.g = currentNode.g + 1;
      neighbor.h = heuristic(neighbor, endNode);
      neighbor.f = neighbor.g + neighbor.h;
      neighbor.parent = currentNode;

      if (!openList.find((node) => node.x === neighbor.x && node.y === neighbor.y)) {
        openList.push(neighbor);
      }
    });
  }

  return []; // No se encontró un camino
}

// Puntos de inicio y destino
/* const start = [0, 0];
const end = [4, 4]; */

const start = [8, 0];
const end = [1, 12];

// Encontrar el camino
const path = astar(maze, start, end);
console.log("Camino más corto:", path);
