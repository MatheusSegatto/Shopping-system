-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: empresa
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `car_cat`
--

DROP TABLE IF EXISTS `car_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_cat` (
  `quantidade` int NOT NULL,
  `id_catalogo` int NOT NULL,
  `id_carrinho` int NOT NULL,
  `pedido` int DEFAULT '-1',
  KEY `id_catalogo` (`id_catalogo`),
  KEY `id_carrinho` (`id_carrinho`),
  CONSTRAINT `car_cat_ibfk_1` FOREIGN KEY (`id_catalogo`) REFERENCES `catalogo` (`id`),
  CONSTRAINT `car_cat_ibfk_2` FOREIGN KEY (`id_carrinho`) REFERENCES `carrinho` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_cat`
--

LOCK TABLES `car_cat` WRITE;
/*!40000 ALTER TABLE `car_cat` DISABLE KEYS */;
INSERT INTO `car_cat` VALUES (2,2,19,27),(1,2,19,28),(1,2,19,29),(1,19,19,30),(1,19,19,31),(2,2,19,32),(1,19,19,33),(2,2,19,34),(1,1,19,34),(1,2,19,35),(1,1,19,35),(1,19,19,36),(1,1,19,37),(5,2,19,38),(10,19,20,39),(51,2,20,40),(1,20,19,41);
/*!40000 ALTER TABLE `car_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrinho`
--

DROP TABLE IF EXISTS `carrinho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrinho` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_conta` int NOT NULL,
  `login_web` varchar(100) DEFAULT 'adm@adm',
  PRIMARY KEY (`id`),
  KEY `id_conta` (`id_conta`),
  KEY `login_web` (`login_web`),
  CONSTRAINT `carrinho_ibfk_1` FOREIGN KEY (`id_conta`) REFERENCES `conta` (`id`),
  CONSTRAINT `carrinho_ibfk_2` FOREIGN KEY (`login_web`) REFERENCES `usuario_web` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrinho`
--

LOCK TABLES `carrinho` WRITE;
/*!40000 ALTER TABLE `carrinho` DISABLE KEYS */;
INSERT INTO `carrinho` VALUES (3,13,'adm@adm'),(19,36,'jurair'),(20,37,'daniel'),(21,38,'matheus'),(22,39,'gabriel'),(23,40,'raissa'),(24,41,'adm@adm'),(25,42,'adm@adm');
/*!40000 ALTER TABLE `carrinho` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogo`
--

DROP TABLE IF EXISTS `catalogo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `preco` double(10,2) DEFAULT '0.00',
  `cor` varchar(16) NOT NULL,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogo`
--

LOCK TABLES `catalogo` WRITE;
/*!40000 ALTER TABLE `catalogo` DISABLE KEYS */;
INSERT INTO `catalogo` VALUES (1,2.50,'Azul','Caneta'),(2,50.00,'vermelha','cadeira'),(19,5.90,'vermelho','Feijão'),(20,5092.00,'RGB','PC Gamer'),(21,180.00,'branco','Violão');
/*!40000 ALTER TABLE `catalogo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `tel1` bigint DEFAULT NULL,
  `tel2` bigint DEFAULT NULL,
  `cpf` varchar(15) NOT NULL,
  `bairro` varchar(30) NOT NULL,
  `cidade` varchar(30) NOT NULL,
  `estado` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf` (`cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (19,'administracao',981457298,NULL,'0','Sulacap','Rio de Janeiro','RJ'),(42,'Jurair Rosa',78967896123,NULL,'23452345234','Buritis','Belo Horizonte','MG'),(43,'daniel',123456789,NULL,'12345678123','Sulacap','Rio De Janeiro','RJ'),(44,'Matheus de Mello Segatto',70891324708,1908274389,'09814723890','Sulacap','Rio De Janeiro','RJ'),(45,'Gabriel de Mello Segatto',1483904234,1908274389,'70189327490','Sulacap','Rio De Janeiro','RJ'),(46,'Raissa Mello',9743019784,NULL,'78912364987','Bangu','Rio De Janeiro','RJ'),(47,'Adenir Andrade',69481376918,1987623489,'10893724908','Bangu','Rio De Janeiro','RJ'),(48,'Marcelo Segatto',1978430189,NULL,'67164983679','Humaita','Caxambu Do Sul','SC');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conta`
--

DROP TABLE IF EXISTS `conta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `conta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conta`
--

LOCK TABLES `conta` WRITE;
/*!40000 ALTER TABLE `conta` DISABLE KEYS */;
INSERT INTO `conta` VALUES (13,19),(36,42),(37,43),(38,44),(39,45),(40,46),(41,47),(42,48);
/*!40000 ALTER TABLE `conta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagamento`
--

DROP TABLE IF EXISTS `pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamento` (
  `data` date NOT NULL,
  `forma_pagamento` varchar(30) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `valor` double(16,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `pagamento_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamento`
--

LOCK TABLES `pagamento` WRITE;
/*!40000 ALTER TABLE `pagamento` DISABLE KEYS */;
INSERT INTO `pagamento` VALUES ('2022-12-23','boleto',15,27,100.00),('2022-12-23','cartao',16,28,50.00),('2022-12-23','cartao',17,29,50.00),('2022-12-23','cartao',18,30,5.90),('2022-12-23','cartao',19,31,5.90),('2022-12-23','boleto',20,32,100.00),('2022-12-23','boleto',21,33,5.90),('2022-12-23','boleto',22,34,102.50),('2022-12-23','boleto',23,35,52.50),('2022-12-23','boleto',24,36,5.90),('2022-12-23','boleto',25,37,2.50),('2022-12-23','pix',26,38,250.00),('2022-12-23','cartao',27,39,59.00),('2022-12-24','pix',28,40,2550.00),('2022-12-25','cartao',29,41,5092.00);
/*!40000 ALTER TABLE `pagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `data` date NOT NULL,
  `valor_total` double(16,2) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `id_conta` int NOT NULL,
  `status` varchar(30) DEFAULT 'aguardando pagamento',
  `valor_a_pagar` double(16,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_conta` (`id_conta`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_conta`) REFERENCES `conta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES ('2022-12-23',100.00,27,36,'pago',0.00),('2022-11-23',50.00,28,36,'pago',0.00),('2022-10-23',50.00,29,36,'pago',0.00),('2022-09-23',5.90,30,36,'pago',0.00),('2022-08-23',5.90,31,36,'pago',0.00),('2022-07-23',100.00,32,36,'pago',0.00),('2022-06-23',5.90,33,36,'pago',0.00),('2022-05-23',102.50,34,36,'pago',0.00),('2022-04-23',52.50,35,36,'pago',0.00),('2022-03-23',5.90,36,36,'pago',0.00),('2022-02-23',2.50,37,36,'pago',0.00),('2022-01-23',250.00,38,36,'pago',0.00),('2022-12-23',59.00,39,37,'pago',0.00),('2022-12-24',2550.00,40,37,'pago',0.00),('2022-12-25',5092.00,41,36,'pago',0.00);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_web`
--

DROP TABLE IF EXISTS `usuario_web`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_web` (
  `email` varchar(100) NOT NULL,
  `senha` varchar(200) NOT NULL,
  `status` varchar(30) DEFAULT 'ativo',
  `id_conta` int NOT NULL,
  PRIMARY KEY (`email`),
  KEY `id_conta` (`id_conta`),
  CONSTRAINT `usuario_web_ibfk_1` FOREIGN KEY (`id_conta`) REFERENCES `conta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_web`
--

LOCK TABLES `usuario_web` WRITE;
/*!40000 ALTER TABLE `usuario_web` DISABLE KEYS */;
INSERT INTO `usuario_web` VALUES ('adm@adm','$2b$12$H0KLuglt231SYZdgIYMxzedY3pU3OAtNxRuP9NRb41Dq0aVM/AKwi','ativo',13),('daniel','$2b$12$yDAjiKS9NjKY9IF.pgmVlOmeZTNlMNVxY6w07kP..iulrxcEOGahe','ativo',37),('gabriel','$2b$12$DatIxsqXV4K3jm4zQzjNYez357zwCn5PfRNheKODRXtqzsCuyXOai','ativo',39),('jurair','$2b$12$MYdmAqXTv3X0soXjxj9kf.JYmYEWd/xsAO8NuomecMYL.r98tbqSS','Ativo',36),('matheus','$2b$12$w7lut5U62g0BkLjSgbQ0q.N74ZF2GYH.5fYY1xhFqdHo3Wio7wN3K','ativo',38),('raissa','$2b$12$e8eXsytBBE7Mv71972HK5e.GTN2loQqtj6TQp7oAjpzpjTw8kgrrW','Banido Temporariamente',40);
/*!40000 ALTER TABLE `usuario_web` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-25 18:54:26
