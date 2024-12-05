import React, { useState } from "react";

function pagos() {
    const [status, setStatus] = useState(null);

    const procesarPago = () => {
        fetch("/pago", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ metodo: "nequi" }),
        })
            .then((response) => response.json())
            .then((data) => setStatus(data.mensaje));
    };

    return (
        <div>
            <h1>Pagos</h1>
            <button onClick={procesarPago}>Realizar Pago</button>
            {status && <p>{status}</p>}
        </div>
    );
}

export default pagos;