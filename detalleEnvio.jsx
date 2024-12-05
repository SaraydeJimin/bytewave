import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function detalleEnvio() {
    const { id } = useParams();
    const [producto, setProducto] = useState(null);

    useEffect(() => {
        fetch(`/detalleE/${id}`)
            .then((response) => response.json())
            .then((data) => setProducto(data));
    }, [id]);

    return (
        <div>
            {envio ? (
                <>
                    <h1>{envio.metodo}</h1>
                    <p>{envio.costo}</p>
                    <p>{envio.tiempoEstimado}</p>
                </>
            ) : (
                <p>Cargando...</p>
            )}
        </div>
    );
}

export default detalleEnvio;