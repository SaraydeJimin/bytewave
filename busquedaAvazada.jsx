import React, { useState } from "react";

function busquedaAvanzada() {
    const [query, setQuery] = useState("");
    const [resultados, setResultados] = useState([]);

    const Busqueda = (e) => {
        e.preventDefault();
        fetch(`/buscar?query=${query}`)
            .then((response) => response.json())
            .then((data) => setResultados(data))
            .catch((error) => console.error("Error en la búsqueda:", error));
    };

    return (
        <div>
            <h1>Búsqueda Avanzada</h1>
            <form onSubmit={Busqueda}>
                <input
                    type="text"
                    placeholder="Buscar productos..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit">Buscar</button>
            </form>
            <ul>
                {resultados.length > 0 ? (
                    resultados.map((resultado) => (
                        <li key={resultado.id}>{resultado.nombre}</li>
                    ))
                ) : (
                    <p>No hay resultados</p>
                )}
            </ul>
        </div>
    );
}

export default busquedaAvanzada;