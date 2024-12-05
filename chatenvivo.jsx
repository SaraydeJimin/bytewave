import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Conexión al servidor Flask

function Soporte() {
    const [usuario, setUsuario] = useState(""); // Nombre del usuario
    const [mensaje, setMensaje] = useState("");
    const [mensajes, setMensajes] = useState([]);

    useEffect(() => {
        socket.on("respuesta", (data) => {
            setMensajes((prevMensajes) => [...prevMensajes, data]);
        });

        return () => {
            socket.off("respuesta");
        };
    }, []);

    const enviarMensaje = (e) => {
        e.preventDefault();
        if (mensaje.trim() !== "") {
            const nuevoMensaje = { usuario: usuario || "Usuario", mensaje };
            setMensajes((prevMensajes) => [...prevMensajes, nuevoMensaje]);
            socket.emit("message", nuevoMensaje);
            setMensaje("");
        }
    };

    return (
        <div>
            <h1>Soporte</h1>
            <div
                style={{
                    border: "1px solid #ccc",
                    height: "300px",
                    overflowY: "scroll",
                    padding: "10px",
                    marginBottom: "10px",
                }}
            >
                {mensajes.map((msg, index) => (
                    <div key={index}>
                        <strong>{msg.usuario}:</strong> {msg.mensaje}
                        {msg.respuesta && (
                            <p style={{ marginLeft: "20px", color: "green" }}>
                                {msg.respuesta}
                            </p>
                        )}
                    </div>
                ))}
            </div>
            {!usuario && (
                <div>
                    <input
                        type="text"
                        placeholder="Ingresa tu nombre"
                        value={usuario}
                        onChange={(e) => setUsuario(e.target.value)}
                    />
                </div>
            )}
            <form onSubmit={enviarMensaje}>
                <input
                    type="text"
                    placeholder="Escribe tu mensaje..."
                    value={mensaje}
                    onChange={(e) => setMensaje(e.target.value)}
                />
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
}

export default Soporte;