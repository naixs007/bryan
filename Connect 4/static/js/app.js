document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('game-board');
    const statusElement = document.getElementById('status');
    const resetButton = document.getElementById('reset-button');
    const winnerMessage = document.getElementById('winner-message');
    const winnerText = document.getElementById('winner-text');
    let gameOver = false;
    
    // Crear el tablero visualmente
    function createBoard() {
        for (let i = 0; i < 42; i++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.column = i % 7;
            cell.addEventListener('click', handlePlayerMove);
            boardElement.appendChild(cell);
        }
    }

    function handlePlayerMove(event) {
        if (gameOver) return;

        const column = event.target.dataset.column;

        fetch(`/move/${column}`, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateBoard(data.board);

            if (data.status === "win") {
                gameOver = true;
                setTimeout( () => {
                    showWinner(`Player ${data.winner} wins!`);    
                }, 500);  
            } else {
                winnerText.textContent = data.current_player === 1 ? "¡Tu turno!" : "Turno de la máquina...";
            }
        });
    }
   
    function handleReset() {
        fetch('/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === "reset") {
                updateBoard(data.board);
                winnerText.textContent = "Nuevo juego iniciado. ¡Tu turno!";
                gameOver = false;
            }
        });
    }

    function updateBoard(board) {
        console.log("Actualizando tablero")
        const cells = boardElement.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const row = Math.floor(index / 7);
            const col = index % 7;
            cell.style.backgroundColor = board[row][col] === 1 ? 'red' : 
                                          board[row][col] === 2 ? 'yellow' : 'lightblue';
        });
    }

    function showWinner(winner) {
        console.log("Llamando showWinner");
        winnerText.textContent = `Ganador: ${winner}`;
        winnerMessage.classList.add('show')
    }



    resetButton.addEventListener('click', handleReset);
    createBoard();
});
