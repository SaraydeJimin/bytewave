import React, {useEffect, useState} from "react";

function ofertasPromociones() {
    const [ofertas, setOfertas] = useState([]);

    useEffect(() => {
        fetch("/ofertas")
        .then((response) => response.json())
        .then((data)=> setOfertas(data));
    }, []);
    
    return (
        <div>
            <h1>Ofertas y promociones</h1>
            <ul>
                {ofertas.map((oferta) => (
                    <li key={oferta.id}>
                        <h2>{oferta.titulo}</h2>
                        <p>{oferta.descripcion}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ofertasPromociones;