import React, { useEffect, useState } from "react";

function Catalogo() {
    const [productos, setProductos] = useState([]);

    useEffect(() => {
        fetch("/catalogo")
            .then((response) => response.json())
            .then((data) => setProductos(data));
    }, []);

    return (
        <div>
            <h1>Catálogo de Productos</h1>
            <ul>
                {productos.map((producto) => (
                    <li key={producto.id}>{producto.nombre} - ${producto.precio}</li>
                ))}
            </ul>
        </div>
    );
}

export default Catalogo;