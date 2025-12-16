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

-- Dump completed on 2025-12-16  0:41:02
