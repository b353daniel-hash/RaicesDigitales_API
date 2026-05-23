<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tarjeta de Identidad Criptográfica</title>
    <style>
        /* Estilos generales de resistencia digital */
        body {
            background-color: #1a1d1a; /* Fondo oscuro */
            color: #e0e0e0; /* Texto claro */
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }

        /* Contenedor estilo 'Card' */
        .card-container {
            background-color: #2c302c; /* Un oscuro ligeramente más claro para la tarjeta */
            border: 1px solid #4a4d4a; /* Borde sutil */
            border-radius: 8px;
            padding: 30px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3); /* Sombra verde de resistencia */
            text-align: center;
        }

        /* Título del huerto */
        h1 {
            color: #00ff00; /* Verde brillante para el título */
            font-size: 2.2em;
            margin-bottom: 20px;
            text-shadow: 0 0 5px #00ff00; /* Efecto de brillo */
        }

        /* Párrafo de kilos disponibles */
        p {
            font-size: 1.1em;
            margin-bottom: 25px;
            line-height: 1.5;
        }

        /* Caja de texto estilo terminal para el Hash */
        .terminal-box {
            background-color: #000000; /* Fondo negro puro */
            color: #00ff00; /* Texto verde terminal */
            text-align: left;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            overflow-x: auto; /* Para hashes largos */
            font-size: 0.9em;
            line-height: 1.4;
            border: 1px solid #00ff00; /* Borde verde */
            box-shadow: inset 0 0 8px rgba(0, 255, 0, 0.5); /* Brillo interno */
            word-break: break-all; /* Asegura que el hash se rompa correctamente */
        }

        .terminal-box .prompt {
            color: #00ff00; /* Color para el prompt */
        }

        .terminal-box .command {
            color: #ffffff; /* Color para el comando */
        }

        .terminal-box .output {
            color: #00ff00; /* Color para la salida */
        }

        /* Botón verde de alto contraste */
        .action-button {
            background-color: #00cc00; /* Verde vibrante */
            color: #1a1d1a; /* Texto oscuro para alto contraste */
            border: none;
            padding: 15px 30px;
            font-size: 1.2em;
            font-family: 'Courier New', Courier, monospace;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
            box-shadow: 0 0 10px rgba(0, 204, 0, 0.7); /* Sombra de brillo verde */
            text-transform: uppercase;
            font-weight: bold;
        }

        .action-button:hover {
            background-color: #00ff00; /* Verde más claro al pasar el ratón */
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(0, 255, 0, 1);
        }

        .action-button:active {
            transform: translateY(0);
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
        }

        /* Responsividad */
        @media (max-width: 600px) {
            .card-container {
                padding: 20px;
                margin: 10px;
            }

            h1 {
                font-size: 1.8em;
            }

            p {
                font-size: 1em;
            }

            .action-button {
                padding: 12px 25px;
                font-size: 1em;
            }
        }
    </style>
</head>
<body>
    <div class="card-container">
        <h1>Huerto Urbano Resistencia</h1>
        <p>Kilos disponibles: 15.7 KG</p>
        <div class="terminal-box">
            <span class="prompt">$ </span><span class="command">generar_hash_cosecha --id HUERTO_RESISTENCIA_2023_Q4</span><br>
            <span class="output">SHA-256: 7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b</span>
        </div>
        <button class="action-button">Coordinar envío por DiDi Food</button>
    </div>
</body>
</html>
