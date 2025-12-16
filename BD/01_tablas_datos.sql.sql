CREATE DATABASE  IF NOT EXISTS `montallantasfy1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `montallantasfy1`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: montallantasfy1
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auditoria_sesiones`
--

DROP TABLE IF EXISTS `auditoria_sesiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_sesiones` (
  `id_audit` int(11) NOT NULL AUTO_INCREMENT,
  `id_sesion` int(11) DEFAULT NULL,
  `usuario_admin_id` int(11) NOT NULL,
  `accion` varchar(100) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_audit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria_sesiones`
--

LOCK TABLES `auditoria_sesiones` WRITE;
/*!40000 ALTER TABLE `auditoria_sesiones` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria_sesiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoriaproductos`
--

DROP TABLE IF EXISTS `categoriaproductos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoriaproductos` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoriaproductos`
--

LOCK TABLES `categoriaproductos` WRITE;
/*!40000 ALTER TABLE `categoriaproductos` DISABLE KEYS */;
INSERT INTO `categoriaproductos` VALUES (1,'Llantas Radial','Llantas de construcciÃ³n radial para turismos y camionetas'),(2,'Aceites Lubricantes','Aceites para todo tipo de motores'),(3,'Filtros Vehiculares','Filtros de aire, aceite, combustible, polen'),(4,'BaterÃ­as Automotriz','BaterÃ­as de arranque para vehÃ­culos livianos y pesados'),(5,'Accesorios Taller','Accesorios para mantenimiento general');
/*!40000 ALTER TABLE `categoriaproductos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `celular` bigint(20) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(100) NOT NULL,
  `placa` varchar(7) NOT NULL,
  `modelo` varchar(40) NOT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Juan','GÃ³mez',3009988777,'juan.gomez@gmail.com','Carrera 8 # 13-45, BogotÃ¡','XYZ789','Chevrolet Onix'),(2,'Maria','Lopez',3001239999,'maria.lopez@gmail.com','Avenida 68 # 45-67, MedellÃ­n','ABC123','Mazda 2'),(3,'Pedro','Martinez',3023334455,'pedro.martineze@gmail.com','Calle 26 # 5-89, Cali','DEF456','Toyota Hilux'),(4,'Ana','Sanchez',3034445566,'ana.sancheze@gmail.com','Diagonal 45 # 10-11, Barranquilla','GHI789','Volkswagen Gol'),(5,'Luis','Diaz',3045556677,'luis.diaze@gmail.com','Calle 100 # 70-01, Cartagena','JKL012','Ford Ranger'),(6,'Sofia','Ruiz',3056667788,'sofia.ruize@gmail.com','Avenida BoyacÃ¡ # 80-20, BogotÃ¡','MNO345','Hyundai i20'),(10,'Mariana','Martines',3147824320,'marianamaritn@gmail.com','TV 94 G # 88 - 3','AKO154','toyota 2009'),(11,'Catalina','Nova',3058315169,'nccatalina0917@gmail.com','TV 94 G # 88 - 3','LIKA45','toyota 2005'),(12,'Juan Camilo','Guerrero Sierra',3002707169,'sierra9camilo9@gmail.com','Transversal 94G 88-03','TVS201','toyota 2009'),(14,'nohora','sierra',3103143185,'noridavida10@hotmail.com','TV 94 G # 88 - 3','TVS201','toyota 2009');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id_compra` int(11) NOT NULL AUTO_INCREMENT,
  `proveedor_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `fecha_pedido` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `estado` enum('Pendiente','En proceso','Recibido','Cancelado') NOT NULL DEFAULT 'Pendiente',
  `monto` decimal(10,2) GENERATED ALWAYS AS (`cantidad` * ifnull(`precio_unitario`,0)) STORED,
  PRIMARY KEY (`id_compra`),
  KEY `idx_compra_estado` (`estado`),
  KEY `idx_compra_proveedor` (`proveedor_id`),
  KEY `idx_compra_producto` (`producto_id`),
  KEY `idx_compra_fechas` (`fecha_pedido`,`fecha_entrega`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id_proveedor`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` (`id_compra`, `proveedor_id`, `producto_id`, `descripcion`, `cantidad`, `precio_unitario`, `fecha_pedido`, `fecha_entrega`, `estado`) VALUES (1,1,1,'Compra de 50 llantas actualizada por cambio de condiciones',60,280000.00,'2024-05-01','2025-10-25','En proceso'),(2,2,2,'Orden de 100 aceites Castrol 20W-50',100,37000.00,'2024-05-03','2024-05-08','Pendiente'),(3,3,3,'Compra de 25 filtros K&N para SUV',20,120000.00,'2024-05-05','2024-05-09','Pendiente'),(4,4,4,'AdquisiciÃ³n de 10 baterÃ­as MAC',10,380000.00,'2024-05-08','2024-05-12','Pendiente'),(6,1,6,'Orden de 30 llantas Michelin Primacy 4',30,450000.00,'2024-05-15','2024-05-19','Pendiente');
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_herramienta`
--

DROP TABLE IF EXISTS `control_herramienta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_herramienta` (
  `id_control` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `herramienta_total` int(11) NOT NULL,
  `herramienta_faltante` int(11) NOT NULL,
  PRIMARY KEY (`id_control`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `control_herramienta_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_herramienta`
--

LOCK TABLES `control_herramienta` WRITE;
/*!40000 ALTER TABLE `control_herramienta` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_herramienta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `descuento` decimal(5,2) DEFAULT 0.00,
  `monto_item` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id_venta`),
  CONSTRAINT `detalleventa_ibfk_3` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,1,1,5,285000.00,0.00,0.00),(5,5,5,2,2500.00,0.00,0.00),(7,34,1,1,285000.00,0.00,285000.00),(9,35,2,1,37000.00,0.00,37000.00),(10,35,3,1,120000.00,0.00,120000.00);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devoluciones`
--

DROP TABLE IF EXISTS `devoluciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devoluciones` (
  `id_devolucion` int(11) NOT NULL AUTO_INCREMENT,
  `compra_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `razon` varchar(100) NOT NULL,
  `cantidad` int(11) DEFAULT 0,
  PRIMARY KEY (`id_devolucion`),
  KEY `compra_id` (`compra_id`),
  CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id_compra`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devoluciones`
--

LOCK TABLES `devoluciones` WRITE;
/*!40000 ALTER TABLE `devoluciones` DISABLE KEYS */;
INSERT INTO `devoluciones` VALUES (1,1,'2024-05-06',1,'Producto daÃ±ado - embalaje roto',0),(2,2,'2025-05-08',1,'Error en el modelo de aceite',0),(5,5,'2024-05-15',1,'Defecto',0),(6,6,'2024-05-17',1,'Defecto de fÃ¡brica',0);
/*!40000 ALTER TABLE `devoluciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domicilio`
--

DROP TABLE IF EXISTS `domicilio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domicilio` (
  `id_domicilio` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) NOT NULL,
  `servicio_id` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id_domicilio`),
  KEY `cliente_id` (`cliente_id`),
  KEY `servicio_id` (`servicio_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `domicilio_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `domicilio_ibfk_2` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`id_servicio`),
  CONSTRAINT `domicilio_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domicilio`
--

LOCK TABLES `domicilio` WRITE;
/*!40000 ALTER TABLE `domicilio` DISABLE KEYS */;
INSERT INTO `domicilio` VALUES (1,5,5,'2024-06-05',62000.00,5),(3,4,4,'2024-06-09',58000.00,5),(4,1,1,'2024-06-11',70000.00,5);
/*!40000 ALTER TABLE `domicilio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encuesta`
--

DROP TABLE IF EXISTS `encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encuesta` (
  `id_encuesta` int(11) NOT NULL AUTO_INCREMENT,
  `calificacion` int(11) DEFAULT NULL,
  `opinion` varchar(300) DEFAULT 'Sin respuesta',
  PRIMARY KEY (`id_encuesta`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encuesta`
--

LOCK TABLES `encuesta` WRITE;
/*!40000 ALTER TABLE `encuesta` DISABLE KEYS */;
INSERT INTO `encuesta` VALUES (9,5,'Buen servicio'),(10,2,'Sin respuesta'),(11,5,'Sin respuesta'),(12,5,'Sin respuesta'),(13,5,'AAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaa'),(14,3,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),(15,3,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),(16,NULL,'a'),(17,0,'Sin respuesta'),(18,0,'Sin respuesta');
/*!40000 ALTER TABLE `encuesta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial`
--

DROP TABLE IF EXISTS `historial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial` (
  `id_historial` int(11) NOT NULL AUTO_INCREMENT,
  `tabla` varchar(50) DEFAULT NULL,
  `operacion` varchar(20) DEFAULT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `old_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`old_data`)),
  `new_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`new_data`)),
  `fecha` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_historial`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial`
--

LOCK TABLES `historial` WRITE;
/*!40000 ALTER TABLE `historial` DISABLE KEYS */;
INSERT INTO `historial` VALUES (1,'venta','INSERT',16,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"fecha_venta\": \"2025-11-21\", \"encargado_id\": 1, \"monto\": 37000.00, \"garantias\": 12}','2025-11-21 14:58:57'),(2,'producto','UPDATE',2,'{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 150, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-21 13:52:48\"}','{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 149, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-21 14:58:57\"}','2025-11-21 14:58:57'),(3,'usuario','INSERT',6,NULL,'{\"nombre\": \"Juan Camilo\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143180, \"correo\": \"sierra9camilo9@gmail.com\", \"usuario\": \"JuanCamilo\", \"rol_id\": 3}','2025-11-21 16:11:53'),(4,'usuario','INSERT',8,NULL,'{\"nombre\": \"admin\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143158, \"correo\": \"admin@gmail.com\", \"usuario\": \"admin\", \"rol_id\": 3}','2025-11-21 16:15:06'),(5,'usuario','UPDATE',8,'{\"nombre\": \"admin\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143158, \"correo\": \"admin@gmail.com\", \"usuario\": \"admin\", \"rol_id\": 3}','{\"nombre\": \"admin\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143158, \"correo\": \"admin@gmail.com\", \"usuario\": \"admin\", \"rol_id\": 1}','2025-11-21 16:15:21'),(6,'venta','INSERT',17,NULL,'{\"cliente_id\": 2, \"cantidad\": 4, \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"fecha_venta\": \"2025-11-21\", \"encargado_id\": 3, \"monto\": 148000.00, \"garantias\": 3}','2025-11-21 16:40:49'),(7,'producto','UPDATE',2,'{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 149, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-21 14:58:57\"}','{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 145, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-21 16:40:49\"}','2025-11-21 16:40:49'),(8,'venta','INSERT',18,NULL,'{\"cliente_id\": 3, \"cantidad\": 45, \"descripcion\": \"BaterÃ­a de libre mantenimiento para vehÃ­culos de alto consumo\", \"fecha_venta\": \"2025-11-21\", \"encargado_id\": 4, \"monto\": 17100000.00, \"garantias\": 4}','2025-11-21 16:44:00'),(9,'producto','UPDATE',4,'{\"nombre\": \"Bateria MAC 12V 700CCA\", \"descripcion\": \"BaterÃ­a de libre mantenimiento para vehÃ­culos de alto consumo\", \"cantidad\": 25, \"categoria_id\": 4, \"precio\": 380000, \"updated_at\": \"2025-11-21 13:52:48\"}','{\"nombre\": \"Bateria MAC 12V 700CCA\", \"descripcion\": \"BaterÃ­a de libre mantenimiento para vehÃ­culos de alto consumo\", \"cantidad\": -20, \"categoria_id\": 4, \"precio\": 380000, \"updated_at\": \"2025-11-21 16:44:00\"}','2025-11-21 16:44:00'),(10,'venta','INSERT',19,NULL,'{\"cliente_id\": 1, \"cantidad\": 12, \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 444000.00, \"garantias\": 1}','2025-11-24 17:46:53'),(11,'producto','UPDATE',2,'{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 145, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-21 16:40:49\"}','{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 133, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-24 17:46:53\"}','2025-11-24 17:46:53'),(12,'venta','INSERT',20,NULL,'{\"cliente_id\": 1, \"cantidad\": 12, \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 444000.00, \"garantias\": 1}','2025-11-24 17:47:29'),(13,'producto','UPDATE',2,'{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 133, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-24 17:46:53\"}','{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 121, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-24 17:47:29\"}','2025-11-24 17:47:29'),(14,'venta','INSERT',21,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 285000.00, \"garantias\": 1}','2025-11-24 17:49:53'),(15,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 85, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-21 13:52:48\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 84, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:49:53\"}','2025-11-24 17:49:53'),(16,'venta','INSERT',22,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 285000.00, \"garantias\": 1}','2025-11-24 17:50:34'),(17,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 84, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:49:53\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 83, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:50:34\"}','2025-11-24 17:50:34'),(18,'venta','INSERT',23,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 285000.00, \"garantias\": 1}','2025-11-24 17:51:20'),(19,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 83, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:50:34\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 82, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:51:20\"}','2025-11-24 17:51:20'),(20,'venta','INSERT',24,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 285000.00, \"garantias\": 1}','2025-11-24 17:52:10'),(21,'venta','INSERT',25,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 285000.00, \"garantias\": 1}','2025-11-24 17:52:40'),(22,'venta','INSERT',26,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 1, \"monto\": 256500.00, \"garantias\": 1}','2025-11-24 18:04:18'),(23,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 82, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 17:51:20\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 81, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 18:04:18\"}','2025-11-24 18:04:18'),(24,'venta','INSERT',27,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 8, \"monto\": 242250.00, \"garantias\": 1}','2025-11-24 18:05:51'),(25,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 81, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 18:04:18\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 80, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 18:05:51\"}','2025-11-24 18:05:51'),(26,'venta','UPDATE',27,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 8, \"monto\": 242250.00, \"garantias\": 1}','{\"cliente_id\": 1, \"cantidad\": 2, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 8, \"monto\": 484500.00, \"garantias\": 1}','2025-11-24 19:01:03'),(27,'venta','UPDATE',27,'{\"cliente_id\": 1, \"cantidad\": 2, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 8, \"monto\": 484500.00, \"garantias\": 1}','{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-11-24\", \"encargado_id\": 8, \"monto\": 242250.00, \"garantias\": 1}','2025-11-24 19:02:07'),(28,'producto','INSERT',7,NULL,'{\"nombre\": \"Aceite Total 20W50\", \"descripcion\": \"Aceite para motor gasolina\", \"cantidad\": 25, \"categoria_id\": 1, \"precio\": 32000, \"updated_at\": \"2025-11-26 00:06:01\"}','2025-11-26 00:06:01'),(29,'producto','INSERT',8,NULL,'{\"nombre\": \"Llanta Rin 13\", \"descripcion\": \"Llanta para automÃ³vil\", \"cantidad\": 10, \"categoria_id\": 2, \"precio\": 125000, \"updated_at\": \"2025-11-26 00:06:01\"}','2025-11-26 00:06:01'),(30,'producto','INSERT',9,NULL,'{\"nombre\": \"BaterÃ­a MAC 600A\", \"descripcion\": \"BaterÃ­a para carro\", \"cantidad\": 5, \"categoria_id\": 3, \"precio\": 410000, \"updated_at\": \"2025-11-26 00:06:01\"}','2025-11-26 00:06:01'),(31,'producto','INSERT',10,NULL,'{\"nombre\": \"Filtro de aire\", \"descripcion\": \"Filtro estÃ¡ndar\", \"cantidad\": 15, \"categoria_id\": 1, \"precio\": 18000, \"updated_at\": \"2025-11-26 00:06:01\"}','2025-11-26 00:06:01'),(32,'usuario','UPDATE',8,'{\"nombre\": \"admin\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143158, \"correo\": \"admin@gmail.com\", \"usuario\": \"admin\", \"rol_id\": 1}','{\"nombre\": \"admin\", \"apellido\": \"Guerrero Sierra\", \"celular\": 3103143158, \"correo\": \"admin@gmail.com\", \"usuario\": \"admin\", \"rol_id\": 1}','2025-12-13 21:06:25'),(33,'venta','INSERT',28,NULL,'{\"cliente_id\": 1, \"cantidad\": 1, \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"fecha_venta\": \"2025-12-15\", \"encargado_id\": 8, \"monto\": 282150.00, \"garantias\": 1}','2025-12-15 22:44:08'),(34,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 80, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-11-24 18:05:51\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 79, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-12-15 22:44:08\"}','2025-12-15 22:44:08'),(35,'producto','UPDATE',1,'{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 79, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-12-15 22:44:08\"}','{\"nombre\": \"Llanta Pirelli P1 Cinturato 185/65R15\", \"descripcion\": \"Llanta radial de alto rendimiento, bajo ruido\", \"cantidad\": 78, \"categoria_id\": 1, \"precio\": 285000, \"updated_at\": \"2025-12-16 00:28:25\"}','2025-12-16 00:28:25'),(36,'producto','UPDATE',3,'{\"nombre\": \"Filtro de Aire K&N para SUV\", \"descripcion\": \"Filtro de aire de alto rendimiento para SUV\", \"cantidad\": 40, \"categoria_id\": 3, \"precio\": 120000, \"updated_at\": \"2025-11-21 13:52:48\"}','{\"nombre\": \"Filtro de Aire K&N para SUV\", \"descripcion\": \"Filtro de aire de alto rendimiento para SUV\", \"cantidad\": 28, \"categoria_id\": 3, \"precio\": 120000, \"updated_at\": \"2025-12-16 00:28:25\"}','2025-12-16 00:28:25'),(37,'producto','UPDATE',2,'{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 121, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-11-24 17:47:29\"}','{\"nombre\": \"Aceite Motor CASTROL GTX 20W-50\", \"descripcion\": \"Aceite mineral premium para motores a gasolina\", \"cantidad\": 120, \"categoria_id\": 2, \"precio\": 37000, \"updated_at\": \"2025-12-16 00:30:43\"}','2025-12-16 00:30:43'),(38,'producto','UPDATE',3,'{\"nombre\": \"Filtro de Aire K&N para SUV\", \"descripcion\": \"Filtro de aire de alto rendimiento para SUV\", \"cantidad\": 28, \"categoria_id\": 3, \"precio\": 120000, \"updated_at\": \"2025-12-16 00:28:25\"}','{\"nombre\": \"Filtro de Aire K&N para SUV\", \"descripcion\": \"Filtro de aire de alto rendimiento para SUV\", \"cantidad\": 27, \"categoria_id\": 3, \"precio\": 120000, \"updated_at\": \"2025-12-16 00:30:43\"}','2025-12-16 00:30:43');
/*!40000 ALTER TABLE `historial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventarioherramientas`
--

DROP TABLE IF EXISTS `inventarioherramientas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventarioherramientas` (
  `id_herr` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `cantidad_faltante` int(11) DEFAULT 0,
  PRIMARY KEY (`id_herr`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `inventarioherramientas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventarioherramientas`
--

LOCK TABLES `inventarioherramientas` WRITE;
/*!40000 ALTER TABLE `inventarioherramientas` DISABLE KEYS */;
INSERT INTO `inventarioherramientas` VALUES (4,'Pistola NeumÃ¡tica de Impacto','Llave de impacto para aflojar tuercas de rueda',3,'Operativa',5,0);
/*!40000 ALTER TABLE `inventarioherramientas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventarioproductos`
--

DROP TABLE IF EXISTS `inventarioproductos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventarioproductos` (
  `id_inve_produ` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `categoria_id` int(11) NOT NULL,
  `rol_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_inve_produ`),
  KEY `producto_id` (`producto_id`),
  KEY `categoria_id` (`categoria_id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `inventarioproductos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id_producto`),
  CONSTRAINT `inventarioproductos_ibfk_2` FOREIGN KEY (`categoria_id`) REFERENCES `categoriaproductos` (`id_categoria`),
  CONSTRAINT `inventarioproductos_ibfk_3` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventarioproductos`
--

LOCK TABLES `inventarioproductos` WRITE;
/*!40000 ALTER TABLE `inventarioproductos` DISABLE KEYS */;
INSERT INTO `inventarioproductos` VALUES (1,1,80,1,1),(2,2,140,2,3),(3,3,38,3,3),(6,6,55,2,3);
/*!40000 ALTER TABLE `inventarioproductos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mantenimiento`
--

DROP TABLE IF EXISTS `mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mantenimiento` (
  `id_mantenimiento` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `fecha` date NOT NULL,
  `personal` varchar(80) NOT NULL,
  `maquina_id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_mantenimiento`),
  KEY `maquina_id` (`maquina_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `mantenimiento_ibfk_1` FOREIGN KEY (`maquina_id`) REFERENCES `maquinaria` (`id_maquina`),
  CONSTRAINT `mantenimiento_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mantenimiento`
--

LOCK TABLES `mantenimiento` WRITE;
/*!40000 ALTER TABLE `mantenimiento` DISABLE KEYS */;
INSERT INTO `mantenimiento` VALUES (1,'CalibraciÃ³n trimestral de balanceadora','2024-04-20','Servicio TÃ©cnico Autorizado',1,1,260000.00),(2,'RevisiÃ³n de sistema hidrÃ¡ulico desmontadora','2024-05-10','Sofia R',2,2,80000.00),(4,'Ajuste de sensores y lubricaciÃ³n alineador 3D','2024-05-25','Servicio Externo John Bean',4,1,300000.00);
/*!40000 ALTER TABLE `mantenimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maquinaria`
--

DROP TABLE IF EXISTS `maquinaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maquinaria` (
  `id_maquina` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `descripcion` text NOT NULL,
  `estado` varchar(50) NOT NULL,
  PRIMARY KEY (`id_maquina`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquinaria`
--

LOCK TABLES `maquinaria` WRITE;
/*!40000 ALTER TABLE `maquinaria` DISABLE KEYS */;
INSERT INTO `maquinaria` VALUES (1,'Balanceadora Corghi E.T.S.','MÃ¡quina profesional para balanceo con calibraciÃ³n digital','Operativa'),(2,'Desmontadora AutomÃ¡tica Hunte','Equipo para montar y desmontar neumÃ¡ticos RunâFlat y perfil bajo','Operativa'),(3,'Compresor de Tornillo Kaeser','Compresor industrial de aire comprimido para taller','Operativa'),(4,'Alineador 3D John Bean','Sistema de alineaciÃ³n tridimensional de Ãºltima tecnologÃ­a','Operativa'),(5,'Elevador de Tijera Ravaglioli','Elevador hidrÃ¡ulico de tijera para trabajos rÃ¡pidos y eficientes','Operativa');
/*!40000 ALTER TABLE `maquinaria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!50001 DROP VIEW IF EXISTS `pedido_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `pedido_detalle` AS SELECT 
 1 AS `id_compra`,
 1 AS `proveedor_id`,
 1 AS `proveedor_nombre`,
 1 AS `producto_id`,
 1 AS `producto_nombre`,
 1 AS `descripcion`,
 1 AS `cantidad`,
 1 AS `precio_unitario`,
 1 AS `monto`,
 1 AS `fecha_pedido`,
 1 AS `fecha_entrega`,
 1 AS `estado`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!50001 DROP VIEW IF EXISTS `pedidos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `pedidos` AS SELECT 
 1 AS `id_compra`,
 1 AS `proveedor_id`,
 1 AS `fecha_pedido`,
 1 AS `fecha_entrega`,
 1 AS `total`,
 1 AS `estado`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `categoria_id` int(11) NOT NULL,
  `precio` float NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_producto`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoriaproductos` (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Llanta Pirelli P1 Cinturato 185/65R15','Llanta radial de alto rendimiento, bajo ruido',78,1,285000,'2025-12-16 05:28:25'),(2,'Aceite Motor CASTROL GTX 20W-50','Aceite mineral premium para motores a gasolina',120,2,37000,'2025-12-16 05:30:43'),(3,'Filtro de Aire K&N para SUV','Filtro de aire de alto rendimiento para SUV',27,3,120000,'2025-12-16 05:30:43'),(4,'Bateria MAC 12V 700CCA','BaterÃ­a de libre mantenimiento para vehÃ­culos de alto consumo',-20,4,380000,'2025-11-21 21:44:00'),(6,'Llanta Michelin Primacy 4 205/55R16','Llanta premium para confort y durabilidad',60,1,450000,'2025-11-21 18:52:48'),(7,'Aceite Total 20W50','Aceite para motor gasolina',25,1,32000,'2025-11-26 05:06:01'),(8,'Llanta Rin 13','Llanta para automÃ³vil',10,2,125000,'2025-11-26 05:06:01'),(9,'BaterÃ­a MAC 600A','BaterÃ­a para carro',5,3,410000,'2025-11-26 05:06:01'),(10,'Filtro de aire','Filtro estÃ¡ndar',15,1,18000,'2025-11-26 05:06:01');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `producto_categoria`
--

DROP TABLE IF EXISTS `producto_categoria`;
/*!50001 DROP VIEW IF EXISTS `producto_categoria`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `producto_categoria` AS SELECT 
 1 AS `producto`,
 1 AS `cantidad`,
 1 AS `categoria`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id_proveedor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `telefono` bigint(20) NOT NULL,
  `correo` varchar(80) NOT NULL,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'ProveedurÃ­a Total',3108765432,'distrillantas.ventas@gmail.com'),(2,'Aceites Supreme S.A.',3117654321,'nuevocorreo@ejemplo.com'),(3,'Importaciones AutoPartes',3109998888,'autodealers.col@gmail.com'),(4,'Equipos Taller Colombia',3135432109,'equipos.taller@gmail.com'),(5,'TecnoBalance S.A.S',3144321098,'tecnobalance.info@gmail.com');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Administrador General'),(2,'Jefe de MecÃ¡nicos'),(3,'Vendedor'),(4,'Empleado de Taller'),(5,'Tecnico de Campo');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio`
--

DROP TABLE IF EXISTS `servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio` (
  `id_servicio` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `tipo` enum('taller','domicilio') NOT NULL,
  `fecha` date NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_servicio`),
  KEY `cliente_id` (`cliente_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `servicio_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `servicio_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio`
--

LOCK TABLES `servicio` WRITE;
/*!40000 ALTER TABLE `servicio` DISABLE KEYS */;
INSERT INTO `servicio` VALUES (1,'Cambio de 4 llantas, balanceo y alineaciÃ³n','taller','2024-06-01',1,2),(2,'Cambio de aceite y filtro de motor','taller','2024-06-02',2,2),(4,'AlineaciÃ³n de direcciÃ³n y rotaciÃ³n de neumÃ¡ticos','taller','2024-06-04',4,5),(5,'ReparaciÃ³n de pinchazo a domicilio (llanta delantera derecha)','domicilio','2024-06-07',5,5),(6,'RevisiÃ³n de suspensiÃ³n y amortiguadores','domicilio','2024-06-10',6,2);
/*!40000 ALTER TABLE `servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sesion_activa`
--

DROP TABLE IF EXISTS `sesion_activa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sesion_activa` (
  `id_sesion` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `nombre_usuario` varchar(150) DEFAULT NULL,
  `hora_inicio` datetime DEFAULT current_timestamp(),
  `ultima_actividad` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `estado` enum('activa','cerrada') DEFAULT 'activa',
  `ip` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_sesion`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `sesion_activa_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sesion_activa`
--

LOCK TABLES `sesion_activa` WRITE;
/*!40000 ALTER TABLE `sesion_activa` DISABLE KEYS */;
/*!40000 ALTER TABLE `sesion_activa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id_ticket` int(11) NOT NULL AUTO_INCREMENT,
  `problema` varchar(200) NOT NULL,
  `descripcion` text NOT NULL,
  `estado` enum('Pendiente','Atendida') DEFAULT 'Pendiente',
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_ticket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `celular` bigint(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `usuario` varchar(50) DEFAULT NULL,
  `clave` varbinary(64) DEFAULT NULL,
  `rol_id` int(11) NOT NULL DEFAULT 3,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `usuario` (`usuario`),
  UNIQUE KEY `celular` (`celular`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Sofia','Ramirez',3009998888,'sofia.ramirez@gmail.com','sofia.ramirez',_binary '1234',2),(2,'Andres','Giraldo',3023456789,'andres.giraldo@gmail.com','andres.giraldo',_binary 'Andres1458',3),(3,'Daniela','Bacheloth',3034567890,'daniela.bacheloth@gmail.com','daniela.b',_binary 'Dbache1465',4),(4,'Felipe','Fernandez',3045678901,'felipe.fernandez@gmail.com','felipe.f',_binary 'Felipe7654',5),(5,'Luisa','Fernanda',3056789012,'luisa.factualizada@gmail.com','luisa.f',_binary 'Lulu7564',4),(6,'Juan Camilo','Guerrero Sierra',3103143180,'sierra9camilo9@gmail.com','JuanCamilo',_binary '×\rÅ-µ©hðÃiurQû\ZÈ2	VJ+EF®æI´!N%',3),(8,'admin','Guerrero Sierra',3103143158,'admin@gmail.com','admin',_binary '�Wb�/\�|�ʺAhT춎��\'4`t\�R>��<\�\Z��tX#\��\�8�J&\�\���g��-<�',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id_venta` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_venta` datetime DEFAULT current_timestamp(),
  `encargado_id` int(11) DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `garantias` int(11) NOT NULL DEFAULT 0,
  `estado` enum('COMPLETADA','ANULADA') DEFAULT 'COMPLETADA',
  PRIMARY KEY (`id_venta`),
  KEY `cliente_id` (`cliente_id`),
  KEY `encargado_id` (`encargado_id`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`encargado_id`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,1,'Venta de 4 Llantas Pirelli P1 con montaje y balanceo.','2024-06-01 00:00:00',3,1250000.00,0,'COMPLETADA'),(2,2,'Venta de aceite Shell y filtro Fram actualizado','2024-06-02 00:00:00',3,185000.00,0,'COMPLETADA'),(3,3,'Venta e instalaciÃ³n de Bateria MAC 12V.','2024-06-03 00:00:00',3,450000.00,0,'COMPLETADA'),(4,4,'RevisiÃ³n y calibraciÃ³n de presiÃ³n de neumÃ¡ticos.','2024-06-07 00:00:00',3,50000.00,0,'COMPLETADA'),(6,6,'Venta de 4 Llantas Michelin Primacy 4, con alineaciÃ³n.','2024-06-06 00:00:00',3,2000000.00,0,'COMPLETADA'),(7,NULL,NULL,'2025-11-15 00:00:00',NULL,150.00,0,'COMPLETADA'),(8,NULL,NULL,'2025-11-16 00:00:00',NULL,200.00,0,'COMPLETADA'),(9,NULL,NULL,'2025-11-17 00:00:00',NULL,180.00,0,'COMPLETADA'),(10,NULL,NULL,'2025-11-18 00:00:00',NULL,220.00,0,'COMPLETADA'),(11,NULL,NULL,'2025-11-19 00:00:00',NULL,170.00,0,'COMPLETADA'),(12,NULL,NULL,'2025-11-20 00:00:00',NULL,190.00,0,'COMPLETADA'),(13,NULL,NULL,'2025-11-21 00:00:00',NULL,210.00,0,'COMPLETADA'),(14,NULL,NULL,'2025-11-20 00:00:00',NULL,190.00,0,'COMPLETADA'),(15,NULL,NULL,'2025-11-21 00:00:00',NULL,210.00,0,'COMPLETADA'),(16,1,'Aceite mineral premium para motores a gasolina','2025-11-21 00:00:00',1,37000.00,12,'COMPLETADA'),(17,2,'Aceite mineral premium para motores a gasolina','2025-11-21 00:00:00',3,148000.00,3,'COMPLETADA'),(18,3,'BaterÃ­a de libre mantenimiento para vehÃ­culos de alto consumo','2025-11-21 00:00:00',4,17100000.00,4,'COMPLETADA'),(19,1,'Aceite mineral premium para motores a gasolina','2025-11-24 00:00:00',1,444000.00,1,'COMPLETADA'),(20,1,'Aceite mineral premium para motores a gasolina','2025-11-24 00:00:00',1,444000.00,1,'COMPLETADA'),(21,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,285000.00,1,'COMPLETADA'),(22,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,285000.00,1,'COMPLETADA'),(23,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,285000.00,1,'COMPLETADA'),(24,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,285000.00,1,'COMPLETADA'),(25,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,285000.00,1,'COMPLETADA'),(26,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',1,256500.00,1,'COMPLETADA'),(27,1,'Llanta radial de alto rendimiento, bajo ruido','2025-11-24 00:00:00',8,242250.00,1,'COMPLETADA'),(28,1,'Llanta radial de alto rendimiento, bajo ruido','2025-12-15 00:00:00',8,282150.00,1,'COMPLETADA'),(34,1,'','2025-12-16 00:28:25',8,1725000.00,21,''),(35,1,'Nada','2025-12-16 00:30:43',8,157000.00,12,'');
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_domicilios`
--

DROP TABLE IF EXISTS `vista_domicilios`;
/*!50001 DROP VIEW IF EXISTS `vista_domicilios`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_domicilios` AS SELECT 
 1 AS `id_domicilio`,
 1 AS `nombre_cliente`,
 1 AS `direccion`,
 1 AS `descripcion_servicio`,
 1 AS `fecha`,
 1 AS `monto`,
 1 AS `usuario_registro`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_producto_mas_vendido`
--

DROP TABLE IF EXISTS `vista_producto_mas_vendido`;
/*!50001 DROP VIEW IF EXISTS `vista_producto_mas_vendido`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_producto_mas_vendido` AS SELECT 
 1 AS `nombre`,
 1 AS `total_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_producto_menos_vendido`
--

DROP TABLE IF EXISTS `vista_producto_menos_vendido`;
/*!50001 DROP VIEW IF EXISTS `vista_producto_menos_vendido`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_producto_menos_vendido` AS SELECT 
 1 AS `nombre`,
 1 AS `total_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_total_servicios_por_usuario`
--

DROP TABLE IF EXISTS `vista_total_servicios_por_usuario`;
/*!50001 DROP VIEW IF EXISTS `vista_total_servicios_por_usuario`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_total_servicios_por_usuario` AS SELECT 
 1 AS `id_usuario`,
 1 AS `usuario`,
 1 AS `total_servicios`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_total_vendido_productos`
--

DROP TABLE IF EXISTS `vista_total_vendido_productos`;
/*!50001 DROP VIEW IF EXISTS `vista_total_vendido_productos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_total_vendido_productos` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre`,
 1 AS `total_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_usuario_mas_servicios`
--

DROP TABLE IF EXISTS `vista_usuario_mas_servicios`;
/*!50001 DROP VIEW IF EXISTS `vista_usuario_mas_servicios`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_usuario_mas_servicios` AS SELECT 
 1 AS `usuario`,
 1 AS `total_servicios`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_usuario_mas_ventas`
--

DROP TABLE IF EXISTS `vista_usuario_mas_ventas`;
/*!50001 DROP VIEW IF EXISTS `vista_usuario_mas_ventas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_usuario_mas_ventas` AS SELECT 
 1 AS `nombre_usuario`,
 1 AS `total_ventas`,
 1 AS `total_monto_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_usuario_menos_servicios`
--

DROP TABLE IF EXISTS `vista_usuario_menos_servicios`;
/*!50001 DROP VIEW IF EXISTS `vista_usuario_menos_servicios`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_usuario_menos_servicios` AS SELECT 
 1 AS `usuario`,
 1 AS `total_servicios`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_usuario_menos_ventas`
--

DROP TABLE IF EXISTS `vista_usuario_menos_ventas`;
/*!50001 DROP VIEW IF EXISTS `vista_usuario_menos_ventas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_usuario_menos_ventas` AS SELECT 
 1 AS `nombre_usuario`,
 1 AS `total_ventas`,
 1 AS `total_monto_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_ventas_por_usuario`
--

DROP TABLE IF EXISTS `vista_ventas_por_usuario`;
/*!50001 DROP VIEW IF EXISTS `vista_ventas_por_usuario`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_ventas_por_usuario` AS SELECT 
 1 AS `usuario_id`,
 1 AS `nombre_usuario`,
 1 AS `total_ventas`,
 1 AS `total_monto_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `pedido_detalle`
--

/*!50001 DROP VIEW IF EXISTS `pedido_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pedido_detalle` AS select `c`.`id_compra` AS `id_compra`,`c`.`proveedor_id` AS `proveedor_id`,`pr`.`nombre` AS `proveedor_nombre`,`c`.`producto_id` AS `producto_id`,`p`.`nombre` AS `producto_nombre`,`c`.`descripcion` AS `descripcion`,`c`.`cantidad` AS `cantidad`,`c`.`precio_unitario` AS `precio_unitario`,`c`.`monto` AS `monto`,`c`.`fecha_pedido` AS `fecha_pedido`,`c`.`fecha_entrega` AS `fecha_entrega`,`c`.`estado` AS `estado` from ((`compra` `c` join `producto` `p` on(`p`.`id_producto` = `c`.`producto_id`)) join `proveedor` `pr` on(`pr`.`id_proveedor` = `c`.`proveedor_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `pedidos`
--

/*!50001 DROP VIEW IF EXISTS `pedidos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pedidos` AS select `c`.`id_compra` AS `id_compra`,`c`.`proveedor_id` AS `proveedor_id`,min(`c`.`fecha_pedido`) AS `fecha_pedido`,max(`c`.`fecha_entrega`) AS `fecha_entrega`,coalesce(sum(`c`.`monto`),0) AS `total`,max(`c`.`estado`) AS `estado` from `compra` `c` group by `c`.`id_compra`,`c`.`proveedor_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `producto_categoria`
--

/*!50001 DROP VIEW IF EXISTS `producto_categoria`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `producto_categoria` AS select `p`.`nombre` AS `producto`,`p`.`cantidad` AS `cantidad`,`c`.`nombre` AS `categoria` from (`producto` `p` join `categoriaproductos` `c` on(`p`.`categoria_id` = `c`.`id_categoria`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_domicilios`
--

/*!50001 DROP VIEW IF EXISTS `vista_domicilios`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_domicilios` AS select `d`.`id_domicilio` AS `id_domicilio`,`c`.`nombre` AS `nombre_cliente`,`c`.`direccion` AS `direccion`,`s`.`descripcion` AS `descripcion_servicio`,`d`.`fecha` AS `fecha`,`d`.`monto` AS `monto`,`u`.`nombre` AS `usuario_registro` from (((`domicilio` `d` join `cliente` `c` on(`d`.`cliente_id` = `c`.`id_cliente`)) join `servicio` `s` on(`d`.`servicio_id` = `s`.`id_servicio`)) join `usuario` `u` on(`d`.`usuario_id` = `u`.`id_usuario`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_producto_mas_vendido`
--

/*!50001 DROP VIEW IF EXISTS `vista_producto_mas_vendido`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_producto_mas_vendido` AS select `vista_total_vendido_productos`.`nombre` AS `nombre`,`vista_total_vendido_productos`.`total_vendido` AS `total_vendido` from `vista_total_vendido_productos` order by `vista_total_vendido_productos`.`total_vendido` desc limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_producto_menos_vendido`
--

/*!50001 DROP VIEW IF EXISTS `vista_producto_menos_vendido`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_producto_menos_vendido` AS select `vista_total_vendido_productos`.`nombre` AS `nombre`,`vista_total_vendido_productos`.`total_vendido` AS `total_vendido` from `vista_total_vendido_productos` order by `vista_total_vendido_productos`.`total_vendido` limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_total_servicios_por_usuario`
--

/*!50001 DROP VIEW IF EXISTS `vista_total_servicios_por_usuario`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_total_servicios_por_usuario` AS select `u`.`id_usuario` AS `id_usuario`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `usuario`,count(`s`.`id_servicio`) AS `total_servicios` from (`usuario` `u` left join `servicio` `s` on(`s`.`usuario_id` = `u`.`id_usuario`)) group by `u`.`id_usuario`,`u`.`nombre`,`u`.`apellido` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_total_vendido_productos`
--

/*!50001 DROP VIEW IF EXISTS `vista_total_vendido_productos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_total_vendido_productos` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre`,coalesce(sum(`d`.`cantidad`),0) AS `total_vendido` from (`producto` `p` left join `detalleventa` `d` on(`d`.`producto_id` = `p`.`id_producto`)) group by `p`.`id_producto`,`p`.`nombre` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_usuario_mas_servicios`
--

/*!50001 DROP VIEW IF EXISTS `vista_usuario_mas_servicios`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_usuario_mas_servicios` AS select `vista_total_servicios_por_usuario`.`usuario` AS `usuario`,`vista_total_servicios_por_usuario`.`total_servicios` AS `total_servicios` from `vista_total_servicios_por_usuario` order by `vista_total_servicios_por_usuario`.`total_servicios` desc limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_usuario_mas_ventas`
--

/*!50001 DROP VIEW IF EXISTS `vista_usuario_mas_ventas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_usuario_mas_ventas` AS select `vista_ventas_por_usuario`.`nombre_usuario` AS `nombre_usuario`,`vista_ventas_por_usuario`.`total_ventas` AS `total_ventas`,`vista_ventas_por_usuario`.`total_monto_vendido` AS `total_monto_vendido` from `vista_ventas_por_usuario` order by `vista_ventas_por_usuario`.`total_ventas` desc limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_usuario_menos_servicios`
--

/*!50001 DROP VIEW IF EXISTS `vista_usuario_menos_servicios`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_usuario_menos_servicios` AS select `vista_total_servicios_por_usuario`.`usuario` AS `usuario`,`vista_total_servicios_por_usuario`.`total_servicios` AS `total_servicios` from `vista_total_servicios_por_usuario` order by `vista_total_servicios_por_usuario`.`total_servicios` limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_usuario_menos_ventas`
--

/*!50001 DROP VIEW IF EXISTS `vista_usuario_menos_ventas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_usuario_menos_ventas` AS select `vista_ventas_por_usuario`.`nombre_usuario` AS `nombre_usuario`,`vista_ventas_por_usuario`.`total_ventas` AS `total_ventas`,`vista_ventas_por_usuario`.`total_monto_vendido` AS `total_monto_vendido` from `vista_ventas_por_usuario` order by `vista_ventas_por_usuario`.`total_ventas` limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_ventas_por_usuario`
--

/*!50001 DROP VIEW IF EXISTS `vista_ventas_por_usuario`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_ventas_por_usuario` AS select `u`.`id_usuario` AS `usuario_id`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `nombre_usuario`,count(`v`.`id_venta`) AS `total_ventas`,sum(`v`.`monto`) AS `total_monto_vendido` from (`usuario` `u` left join `venta` `v` on(`v`.`encargado_id` = `u`.`id_usuario`)) group by `u`.`id_usuario`,`u`.`nombre`,`u`.`apellido` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-16  0:37:55
