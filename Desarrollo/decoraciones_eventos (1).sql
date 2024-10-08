-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 08, 2024 at 07:42 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `decoraciones_eventos`
--

-- --------------------------------------------------------

--
-- Table structure for table `banners`
--

CREATE TABLE `banners` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `primer_mensaje` varchar(255) NOT NULL,
  `segundo_mensaje` varchar(255) NOT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `banners`
--

INSERT INTO `banners` (`id`, `nombre`, `primer_mensaje`, `segundo_mensaje`, `estado`, `imagen`) VALUES
(1, 'Anillos', 'La mejor decoración para tu boda', 'Invaluable. De ensueño.', 'Activo', 'anillos.png'),
(2, 'Anillo', 'Crea momentos inolvidables', 'Decoraciones únicas para tu día especial', 'Activo', 'anillo.png'),
(4, 'Tulipanes', 'Decoraciones personalizadas para cada pareja', 'Haz realidad tus sueños', 'Activo', 'tulipanes-rosas-20-uds.png');

-- --------------------------------------------------------

--
-- Table structure for table `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `estado` enum('Activo','Inactivo') DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `estado`, `imagen`) VALUES
(8, 'Cumpleaños', 'Activo', 'images.jpg'),
(9, 'Recepciones', 'Activo', 'images.png'),
(10, 'Decoraciones', 'Activo', 'tulipanes-rosas-20-uds.png'),
(11, 'Aniversarios', 'Activo', 'anillo.png'),
(12, 'Centros de mesa', 'Activo', 'centro de mesa.png'),
(13, 'Bouquetes', 'Activo', 'bouquet.png'),
(14, 'Bodas', 'Activo', 'anillos.png');

-- --------------------------------------------------------

--
-- Table structure for table `comentario`
--

CREATE TABLE `comentario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `comentario` text NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comentario`
--

INSERT INTO `comentario` (`id`, `nombre`, `comentario`, `imagen`) VALUES
(5, 'Matrimonio Camila y Sebastián', 'El inicio de una aventura: Este día marca el comienzo de nuestra nueva vida juntos. Estamos emocionados por lo que el futuro nos depara, y nuestra boda fue solo el primer capítulo de nuestra historia.', 'matrimonio3.jpg'),
(6, 'Matrimonio Juan y Sara', 'Magia en cada rincón: Nuestra boda fue un verdadero cuento de hadas. La decoración, los invitados, la música... todo fluyó a la perfección. No hay palabras para describir lo feliz que nos sentimos.', 'matrimonio4.jpg'),
(7, 'Matrimonio Daniel y Manuela', 'Un día inolvidable: Desde la ceremonia hasta la fiesta, cada momento fue especial. Ver a nuestras familias y amigos celebrando con nosotros hizo que todo fuera aún más mágico.', 'matrimonio2.jpg'),
(8, 'Matrimonio Sara y Miguel', 'Amor desbordante: La conexión que sentimos en nuestra boda fue indescriptible. El amor en el aire, las sonrisas de nuestros seres queridos y, sobre todo, la mirada de mi pareja, hicieron que cada instante valiera la pena.', 'matrimonio1.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `estado` enum('Activo','Inactivo') DEFAULT NULL,
  `flores` varchar(100) DEFAULT NULL,
  `categorias` varchar(100) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `tamano` varchar(250) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` int(10) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `estado`, `flores`, `categorias`, `color`, `tamano`, `descripcion`, `precio`, `imagen`) VALUES
(2, 'Bouquete Primavera 1', 'Activo', 'Rosas, Jazmínes, Lírios', 'Bouquetes', 'Rojo, pastel rojo, azul', '20 x 15 x 30', 'Holaaaaaaaaaaaa', 1230000, 'bouquet.png'),
(3, 'Centro de mesa frío 2', 'Activo', 'Rosa blanca, follaje', 'Cumpleaños', 'Verde, blanco y transparente', '15 * 30 * 20', 'Funcional', 220000, 'centro_de_mesa_con_flores_y_velas.jpg'),
(4, 'Bouquete Primavera 3', 'Activo', 'Rosas, Jazmínes, Lírios', 'Bouquetes', 'Rojo, pastel rojo, azul', '20 x 15 x 30', 'Holaaaaaaaaaaaa', 1230000, 'bouquet.png'),
(5, 'Centro de mesa frío 4', 'Activo', 'Rosa blanca, follaje', 'Cumpleaños', 'Verde, blanco y transparente', '15 * 30 * 20', 'Funcional', 220000, 'centro_de_mesa_con_flores_y_velas.jpg'),
(6, 'Bouquete Primavera 5', 'Activo', 'Rosas, Jazmínes, Lírios', 'Bouquetes', 'Rojo, pastel rojo, azul', '20 x 15 x 30', 'Holaaaaaaaaaaaa', 1230000, 'bouquet.png'),
(7, 'Centro de mesa frío 6', 'Activo', 'Rosa blanca, follaje', 'Cumpleaños', 'Verde, blanco y transparente', '15 * 30 * 20', 'Funcional', 220000, 'centro_de_mesa_con_flores_y_velas.jpg'),
(8, 'Bouquete Primavera 7', 'Activo', 'Rosas, Jazmínes, Lírios', 'Bouquetes', 'Rojo, pastel rojo, azul', '20 x 15 x 30', 'Holaaaaaaaaaaaa', 1230000, 'bouquet.png'),
(9, 'Centro de mesa frío', 'Activo', 'Rosa blanca, follaje, Amarillo', 'Centros de mesa', 'Verde, blanco y transparente', '15 * 30 * 20', 'Funcional total', 2200000, 'centro de mesa.png');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `password` char(102) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `telefono` int(13) NOT NULL,
  `email` varchar(50) NOT NULL,
  `perfil` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `password`, `fullname`, `telefono`, `email`, `perfil`) VALUES
(16, 'pbkdf2:sha256:600000$bbYoAxVJS0MPxLof$0cfb22cb4a6898fac5b96c9d1a15e7747dfe691b70a526fc86d0f89cb649d595', 'Admin', 123, 'Admin@admin.com', 'Administrador');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `banners`
--
ALTER TABLE `banners`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `comentario`
--
ALTER TABLE `comentario`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `banners`
--
ALTER TABLE `banners`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `comentario`
--
ALTER TABLE `comentario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
