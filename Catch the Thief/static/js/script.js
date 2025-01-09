// Variables globales
let nodoSeleccionado = null;
const nodosSalida = ["N1", "N2", "N3"]; // Nodos de salida

// Configuración inicial
const nodos = {
    N1: { x: 125, y: 50 },
    N2: { x: 250, y: 25 },
    N3: { x: 375, y: 50 },
    N4: { x: 175, y: 200 },
    N5: { x: 250, y: 200 },
    N6: { x: 325, y: 200 },
    N7: { x: 125, y: 350 },
    N8: { x: 250, y: 350 },
    N9: { x: 375, y: 350 },
    N10: { x: 250, y: 450 }
};

const conexiones = [
    ['N1', 'N2'], ['N1', 'N4'], ['N1', 'N5'],
    ['N2', 'N3'], ['N2', 'N5'],
    ['N3', 'N5'], ['N3', 'N6'],
    ['N4', 'N5'], ['N4', 'N7'],
    ['N5', 'N6'], ['N5', 'N7'], ['N5', 'N8'], ['N5', 'N9'],
    ['N6', 'N9'],  
    ['N7', 'N8'], ['N7', 'N10'],
    ['N8', 'N9'], ['N8', 'N10'],
    ['N9', 'N10']
];

// Estado inicial del juego
const estadoInicial = {
    ladron: "N8",
    policias: ["N1", "N2", "N3"]
};

let estado = { ...estadoInicial };

// Crear mapa visual
function crearMapa() {
    const mapa = document.getElementById("game-map");
    mapa.innerHTML = ''; // Limpiar el mapa existente

    // Crear conexiones
    conexiones.forEach(([nodoA, nodoB]) => {
        const linea = document.createElementNS("http://www.w3.org/2000/svg", "line");
        linea.setAttribute("x1", nodos[nodoA].x);
        linea.setAttribute("y1", nodos[nodoA].y);
        linea.setAttribute("x2", nodos[nodoB].x);
        linea.setAttribute("y2", nodos[nodoB].y);
        linea.classList.add("linea");
        mapa.appendChild(linea);
    });

    // Crear nodos
    for (const [id, { x, y }] of Object.entries(nodos)) {
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", x);
        circle.setAttribute("cy", y);
        circle.setAttribute("r", 20);
        circle.setAttribute("id", id);
        circle.classList.add("nodo");
        if (nodosSalida.includes(id)) {
            circle.classList.add("salida");
        }
        circle.addEventListener("click", () => manejarClickNodo(id));
        mapa.appendChild(circle);
    }

    actualizarMapa(estado);
}

// Función para reiniciar el juego
function reiniciarEstado() {
    fetch('/reiniciar', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensaje === "Juego reiniciado") {
            estado = data.estado;
            console.log("Estado después de reiniciar:", estado);
            actualizarMapa(estado); // Actualiza el mapa
        }
    });
}

// Manejar la selección y el movimiento de los policías
function manejarClickNodo(id) {
    if (nodoSeleccionado) {
        if (estado.policias.includes(nodoSeleccionado) &&
            !estado.policias.includes(id) && 
            !estado.policias.includes(estado.ladron) && 
            conexiones.some(con => con.includes(nodoSeleccionado) && 
            con.includes(id))) {
            moverPolicia(nodoSeleccionado, id);
            nodoSeleccionado = null;
            verificarCondiciones(); // Verificar condiciones de fin del juego
        } else {          
            nodoSeleccionado = null;
        }
    } else if (estado.policias.includes(id)) {
        nodoSeleccionado = id;
    }
    actualizarMapa(estado);
}

// Mover policía (interacción del usuario)
function moverPolicia(origen, destino) {
    const indice = estado.policias.indexOf(origen);
    estado.policias[indice] = destino;
    turnoLadron();
}




// Turno del ladrón con movimiento aleatorio y búsqueda de salida
function turnoLadron() {
    // Filtrar los movimientos posibles del ladrón
    const movimientosPosibles = conexiones
        .filter(conexion => conexion.includes(estado.ladron)) // Conexiones con el nodo del ladrón
        .map(conexion => conexion.find(nodo => nodo !== estado.ladron && // Nodo que no sea el ladrón
            !estado.policias.includes(nodo) && // Nodo que no esté ocupado por un policía
            esNodoValido(nodo))); // Verifica si el nodo es válido

    // Buscar un movimiento prioritario hacia un nodo de salida
    let movimientoPrioritario = movimientosPosibles.find(nodo => nodosSalida.includes(nodo));

    // Si se encuentra un movimiento prioritario hacia la salida, moverse ahí
    if (movimientoPrioritario) {
        estado.ladron = movimientoPrioritario;
    } else if (movimientosPosibles.length > 0) {
        let movimientoValido = null;
    
        // Intentar encontrar un movimiento válido
        let maxAttempts = 10; // Maximum number of attempts to find a valid move
        let attempts = 0;
        while (!movimientoValido && movimientosPosibles.length > 0 && attempts < maxAttempts) {
            attempts++;
            const movimientoAleatorio = movimientosPosibles[Math.floor(Math.random() * movimientosPosibles.length)];
            console.log("Intentando movimiento aleatorio:", movimientoAleatorio);
    
            // Verificar si el nodo es válido
            if (esNodoValido(movimientoAleatorio)) {
                movimientoValido = movimientoAleatorio;
            } else {
                console.log("Movimiento inválido, reintentando...");
            }
        }
    
        // Asignar el movimiento válido al estado del ladrón
        if (movimientoValido) {
            estado.ladron = movimientoValido;
            console.log("Movimiento final del ladrón:", movimientoValido);
        } else {
            console.log("No se encontraron movimientos válidos.");
        }
    }

    // Verificar si el ladrón ha llegado a un nodo de salida
    if (nodosSalida.includes(estado.ladron)) {
        pintarNodoSalida(estado.ladron); // Pintar el nodo de salida en rojo
        console.log(`El ladrón ha llegado a una salida: ${estado.ladron}`);
    }

    // Actualizar el mapa con el nuevo estado del ladrón
    actualizarMapa(estado);
    console.log("Estado del ladrón", estado);
    verificarCondiciones();
}

// Función para pintar un nodo de salida
function pintarNodoSalida(nodo) {
    const elementoNodo = document.querySelector(`#nodo-${nodo}`); // Selector basado en el ID del nodo
    if (elementoNodo) {
        elementoNodo.style.backgroundColor = 'red'; // Cambia el color del nodo a rojo
    }
}

// Función para verificar si un nodo es válido
function esNodoValido(nodo) {
    // Verificar si el nodo no está ocupado por un policía
    return !estado.policias.includes(nodo);
}


// Actualizar el mapa con el estado actual
function actualizarMapa({ ladron, policias }) {
    document.querySelectorAll(".nodo").forEach(nodo => {
        nodo.classList.remove("ladron", "policia", "seleccionado", "salida");
    });

    const nodoLadron = document.getElementById(ladron);
    if (nodoLadron) {
        nodoLadron.classList.add("ladron");
    }

    policias.forEach(policia => {
        const nodoPolicia = document.getElementById(policia);
        if (nodoPolicia) {
            nodoPolicia.classList.add("policia");
            if (nodoPolicia.classList.contains("salida")) {
                nodoPolicia.classList.add("salida");
            }
        }
    });

    if (nodoSeleccionado) {
        const nodoSel = document.getElementById(nodoSeleccionado);
        if (nodoSel) {
            nodoSel.classList.add("seleccionado");
        }
    }

    nodosSalida.forEach(salida => {
        const nodoSalida = document.getElementById(salida);
        if (nodoSalida && !estado.policias.includes(salida)) {
            nodoSalida.classList.add("salida");
        }
    });
}

// Verificar condiciones de fin del juego
function verificarCondiciones() { 
    if (estado.policias.includes(estado.ladron)) { 
        setTimeout(() => {
            alert("¡Los policías han atrapado al ladrón! Has ganado."); 
            reiniciarEstado();
        }, 500); //Retraso para mostrar el último movimiento
    } else if (nodosSalida.includes(estado.ladron)) {
        setTimeout(() => {
            alert("¡El ladrón ha escapado por una salida! Has perdido.");
            reiniciarEstado(); // Reinicio automático al perder 
        }, 500); 
    } else if (conexiones.filter(con => con.includes(estado.ladron))
        .every(con => estado.policias.includes(con.find(nodo => nodo !== estado.ladron)))) { 
        setTimeout(() => {
            alert("¡El ladrón no tiene movimientos válidos! Has ganado.");
            reiniciarEstado();
        }, 500);
    } 
}




// Iniciar el juego
document.getElementById("start-btn").addEventListener("click", () => {
    crearMapa();
});

// Reiniciar el juego
document.getElementById("reset-btn").addEventListener("click", () => {
    reiniciarEstado();
});









/*
document.getElementById('difficulty-select').addEventListener('change', function () {
    const difficulty = this.value; // Obtiene el valor del selector
    fetch('/actualizar_dificultad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: difficulty }) // Envía un JSON con la clave 'difficulty'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar la dificultad');
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensaje); // Muestra el mensaje de éxito
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
*/