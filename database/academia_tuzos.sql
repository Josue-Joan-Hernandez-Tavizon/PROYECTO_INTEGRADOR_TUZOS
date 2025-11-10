-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2025 a las 05:24:24
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `academia_tuzos`
--
CREATE DATABASE IF NOT EXISTS `academia_tuzos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `academia_tuzos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `ID_Categoria` int(11) NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`ID_Categoria`, `Nombre`) VALUES
(1, 'Sub-8'),
(2, 'Sub-10'),
(3, 'Sub-12'),
(4, 'Sub-14'),
(5, 'Sub-16'),
(6, 'Sub-18'),
(7, 'Sub-20'),
(8, 'Absoluto'),
(9, 'Femenil'),
(10, 'Veteranos'),
(11, 'total');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrenamiento`
--

CREATE TABLE `entrenamiento` (
  `Id_Entrenamiento` int(11) NOT NULL,
  `Dia` varchar(15) DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Profesor` int(11) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entrenamiento`
--

INSERT INTO `entrenamiento` (`Id_Entrenamiento`, `Dia`, `Hora`, `Profesor`, `Categoria`) VALUES
(1, 'Lunes', '16:00:00', 1, 1),
(2, 'Miercoles', '17:00:00', 2, 5),
(3, 'Viernes', '18:00:00', 3, 8),
(4, 'Jueves', '09:00:00', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `ID_Equipo` int(11) NOT NULL,
  `Nombre_Equipo` varchar(100) NOT NULL,
  `Categoria` int(11) DEFAULT NULL,
  `Color_Uniforme` varchar(50) DEFAULT NULL,
  `Anio_Fundacion` year(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipos`
--

INSERT INTO `equipos` (`ID_Equipo`, `Nombre_Equipo`, `Categoria`, `Color_Uniforme`, `Anio_Fundacion`) VALUES
(1, 'Tuzos Sub-16', 5, 'Azul y Blanco', '2020'),
(2, 'Aguilas Sub-16', 5, 'Amarillo y Azul', '2019'),
(3, 'Tuzos Absoluto', 8, 'Azul y Blanco', '2015'),
(4, 'Leones Absoluto', 8, 'Rojo y Negro', '2018');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `ID_Horario` int(11) NOT NULL,
  `Ocupacion` varchar(30) DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Dia` varchar(15) DEFAULT NULL,
  `Disponibilidad` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`ID_Horario`, `Ocupacion`, `Hora`, `Dia`, `Disponibilidad`) VALUES
(1, 'Entrenamiento', '16:00:00', 'Lunes', 0),
(2, 'Partido', '11:00:00', 'Sabado', 0),
(4, 'Partido', '13:00:00', 'Viernes', 0),
(5, 'Partido', '19:00:00', 'Miercoles', 0),
(6, 'Partido', '14:00:00', 'Jueves', 0),
(7, 'Partido', '19:00:00', 'Martes', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `ID_jugador` int(11) NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellidos` varchar(50) DEFAULT NULL,
  `CURP` varchar(18) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL,
  `Numero_jugador` int(11) DEFAULT NULL,
  `Inscripcion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `jugadores`
--

INSERT INTO `jugadores` (`ID_jugador`, `Nombre`, `Apellidos`, `CURP`, `Categoria`, `Numero_jugador`, `Inscripcion`) VALUES
(1, 'Luis', 'Martines', 'MALO950101HDFNRS01', 5, 10, '2024-01-15'),
(2, 'Ana', 'Rodriguez', 'ROAA960202MDFDNS02', 8, 7, '2024-01-20'),
(6, 'Miguel', 'Cervantes Diaz', 'mig1023549348238cd', 8, 56, '2025-12-02'),
(8, 'miguel', 'Hernandez', 'migusr4fiin341313', 2, 10, '2025-12-08');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partidos`
--

CREATE TABLE `partidos` (
  `Id_Partidos` int(11) NOT NULL,
  `Dia` varchar(15) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Equipo_Local` varchar(50) DEFAULT NULL,
  `Equipo_Visitante` varchar(50) DEFAULT NULL,
  `Profesor` int(11) DEFAULT NULL,
  `Lugar` varchar(50) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `ID_Torneo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `partidos`
--

INSERT INTO `partidos` (`Id_Partidos`, `Dia`, `Fecha`, `Hora`, `Equipo_Local`, `Equipo_Visitante`, `Profesor`, `Lugar`, `Categoria`, `Tipo`, `ID_Torneo`) VALUES
(2, 'Domingo', '2025-12-21', '10:00:00', 'Tuzos Absoluto', 'Leones Absoluto', 3, 'Estadio Central', 8, 'Liga', NULL),
(3, 'Martes', '2025-12-16', '10:00:00', 'Tuzos', 'Tigres', 1, 'cancha tuzos', 10, 'Amistoso', NULL),
(4, 'Lunes', '2025-12-15', '16:00:00', 'tuzos', 'tuzomania', 2, 'tuzos field', 2, 'Torneo', 1),
(5, 'Viernes', '2025-12-12', '13:00:00', 'Tuzos', 'Tigres', 2, 'cancha tuzos', 8, 'Torneo', NULL),
(6, 'Miercoles', '2025-12-17', '19:00:00', 'pumas', 'real madrid', 3, 'TUZOMANIA', 5, 'Amistoso', NULL),
(7, 'Jueves', '2025-12-18', '14:00:00', 'MIGUELDS', 'JCNUNDC', 2, 'TUZOMAN', 8, 'Torneo', NULL);

--
-- Disparadores `partidos`
--
DELIMITER $$
CREATE TRIGGER `trg_before_delete_partidos` BEFORE DELETE ON `partidos` FOR EACH ROW BEGIN
    INSERT INTO partidos_eliminados (
        Id_Partido, Dia, Hora, Equipo_Local, Equipo_Visitante,
        Profesor, Lugar, Categoria, Tipo, Fecha_Eliminado
    )
    VALUES (
        OLD.Id_Partidos, OLD.Dia, OLD.Hora, OLD.Equipo_Local, OLD.Equipo_Visitante,
        OLD.Profesor, OLD.Lugar, OLD.Categoria, OLD.Tipo, NOW()
    );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partidos_eliminados`
--

CREATE TABLE `partidos_eliminados` (
  `Id_Partido` int(11) DEFAULT NULL,
  `Dia` varchar(15) DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Equipo_Local` varchar(50) DEFAULT NULL,
  `Equipo_Visitante` varchar(50) DEFAULT NULL,
  `Profesor` int(11) DEFAULT NULL,
  `Lugar` varchar(50) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Fecha_Eliminado` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `partidos_eliminados`
--

INSERT INTO `partidos_eliminados` (`Id_Partido`, `Dia`, `Hora`, `Equipo_Local`, `Equipo_Visitante`, `Profesor`, `Lugar`, `Categoria`, `Tipo`, `Fecha_Eliminado`) VALUES
(1, 'Sabado', '11:00:00', 'Tuzos Sub-16', 'Aguilas Sub-16', 2, 'Cancha Principal', 5, 'Amistoso', '2025-12-08 09:55:59'),
(8, 'Martes', '19:00:00', 'sdfvb', 'numi,', 2, 'tuzom', 4, 'Liga', '2025-12-09 09:44:55');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `Id_Profesores` int(11) NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellidos` varchar(50) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`Id_Profesores`, `Nombre`, `Apellidos`, `Categoria`) VALUES
(1, 'Juan', 'Perez', 1),
(2, 'Maria', 'Garcia', 5),
(3, 'Carlos', 'Lopez', 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados`
--

CREATE TABLE `resultados` (
  `Id_Resultado` int(11) NOT NULL,
  `Id_Partido` int(11) DEFAULT NULL,
  `Goles_Local` int(11) DEFAULT NULL,
  `Goles_Visitante` int(11) DEFAULT NULL,
  `Ganador` varchar(50) DEFAULT NULL,
  `Perdedor` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `resultados`
--

INSERT INTO `resultados` (`Id_Resultado`, `Id_Partido`, `Goles_Local`, `Goles_Visitante`, `Ganador`, `Perdedor`) VALUES
(1, 2, 3, 1, 'Tuzos Absoluto', 'Leones Absoluto'),
(2, 7, 0, 5, 'MIGUELDS', 'JCNUNDC'),
(3, 4, 3, 0, 'Empate', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `torneo`
--

CREATE TABLE `torneo` (
  `Id_Torneo` int(11) NOT NULL,
  `Nombre_torneo` varchar(50) DEFAULT NULL,
  `Categoria` int(11) DEFAULT NULL,
  `Cantidad_Equipos` int(11) DEFAULT NULL,
  `Duracion` varchar(20) DEFAULT NULL,
  `Fecha_Inicial` date DEFAULT NULL,
  `Fecha_Termino` date DEFAULT NULL,
  `Estado` varchar(20) DEFAULT 'Activo',
  `Equipo_Ganador` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `torneo`
--

INSERT INTO `torneo` (`Id_Torneo`, `Nombre_torneo`, `Categoria`, `Cantidad_Equipos`, `Duracion`, `Fecha_Inicial`, `Fecha_Termino`, `Estado`, `Equipo_Ganador`) VALUES
(1, 'Torneo Primavera Sub-16', 5, 8, '1 mes', '2024-03-01', '2025-12-15', 'Activo', NULL),
(2, 'Copa Absoluta 2024', 8, 12, '2 meses', '2024-04-01', '2024-05-31', 'Activo', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) DEFAULT NULL,
  `email` varchar(35) DEFAULT NULL,
  `password` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `email`, `password`) VALUES
(2, 'coach', 'coach@tuzos.com', 'coach123'),
(3, 'user', 'user@tuzos.com', 'user123'),
(4, 'Manuel', 'manuelgs@gmail.com', '123'),
(5, 'joan', 'joan@gmail.com', '123'),
(7, 'admin', 'admin@academia.com', 'admin123'),
(8, 'tavizon', 'tavizon@gmail.com', '123');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_estadisticas_equipos`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_estadisticas_equipos` (
`Nombre_Equipo` varchar(100)
,`Partidos_Jugados` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_estadisticas_equipos`
--
DROP TABLE IF EXISTS `vista_estadisticas_equipos`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_estadisticas_equipos`  AS SELECT `e`.`Nombre_Equipo` AS `Nombre_Equipo`, count(`p`.`Id_Partidos`) AS `Partidos_Jugados` FROM (`equipos` `e` left join `partidos` `p` on(`e`.`Nombre_Equipo` = `p`.`Equipo_Local` or `e`.`Nombre_Equipo` = `p`.`Equipo_Visitante`)) GROUP BY `e`.`Nombre_Equipo` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`ID_Categoria`);

--
-- Indices de la tabla `entrenamiento`
--
ALTER TABLE `entrenamiento`
  ADD PRIMARY KEY (`Id_Entrenamiento`),
  ADD KEY `Profesor` (`Profesor`),
  ADD KEY `Categoria` (`Categoria`);

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`ID_Equipo`),
  ADD KEY `Categoria` (`Categoria`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`ID_Horario`);

--
-- Indices de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD PRIMARY KEY (`ID_jugador`),
  ADD KEY `Categoria` (`Categoria`);

--
-- Indices de la tabla `partidos`
--
ALTER TABLE `partidos`
  ADD PRIMARY KEY (`Id_Partidos`),
  ADD KEY `Profesor` (`Profesor`),
  ADD KEY `Categoria` (`Categoria`),
  ADD KEY `fk_partidos_torneo` (`ID_Torneo`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`Id_Profesores`),
  ADD KEY `Categoria` (`Categoria`);

--
-- Indices de la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD PRIMARY KEY (`Id_Resultado`),
  ADD KEY `Id_Partido` (`Id_Partido`);

--
-- Indices de la tabla `torneo`
--
ALTER TABLE `torneo`
  ADD PRIMARY KEY (`Id_Torneo`),
  ADD KEY `Categoria` (`Categoria`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `ID_Categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `entrenamiento`
--
ALTER TABLE `entrenamiento`
  MODIFY `Id_Entrenamiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `ID_Equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `ID_Horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  MODIFY `ID_jugador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `partidos`
--
ALTER TABLE `partidos`
  MODIFY `Id_Partidos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `Id_Profesores` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `resultados`
--
ALTER TABLE `resultados`
  MODIFY `Id_Resultado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `torneo`
--
ALTER TABLE `torneo`
  MODIFY `Id_Torneo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `entrenamiento`
--
ALTER TABLE `entrenamiento`
  ADD CONSTRAINT `entrenamiento_ibfk_1` FOREIGN KEY (`Profesor`) REFERENCES `profesores` (`Id_Profesores`),
  ADD CONSTRAINT `entrenamiento_ibfk_2` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);

--
-- Filtros para la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD CONSTRAINT `equipos_ibfk_1` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);

--
-- Filtros para la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD CONSTRAINT `jugadores_ibfk_1` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);

--
-- Filtros para la tabla `partidos`
--
ALTER TABLE `partidos`
  ADD CONSTRAINT `fk_partidos_torneo` FOREIGN KEY (`ID_Torneo`) REFERENCES `torneo` (`Id_Torneo`) ON DELETE SET NULL,
  ADD CONSTRAINT `partidos_ibfk_1` FOREIGN KEY (`Profesor`) REFERENCES `profesores` (`Id_Profesores`),
  ADD CONSTRAINT `partidos_ibfk_2` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);

--
-- Filtros para la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);

--
-- Filtros para la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`Id_Partido`) REFERENCES `partidos` (`Id_Partidos`);

--
-- Filtros para la tabla `torneo`
--
ALTER TABLE `torneo`
  ADD CONSTRAINT `torneo_ibfk_1` FOREIGN KEY (`Categoria`) REFERENCES `categoria` (`ID_Categoria`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
