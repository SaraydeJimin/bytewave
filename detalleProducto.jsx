import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function detalleProducto() {
    const { id } = useParams();
    const [producto, setProducto] = useState(null);

    useEffect(() => {
        fetch(`/producto/${ id }`)
            .then((response) => response.json())
            .then((data) => setProducto(data));
    }, [id]);

    return (
        <div>
            {producto ? (
                <>
                    <h1>{producto.nombre}</h1>
                    <p>{producto.descripcion}</p>
                    <p>Precio: ${producto.precio}</p>
                </>
            ) : (
                <p>Cargando...</p>
            )}
        </div>
    );
}

export default detalleProducto;