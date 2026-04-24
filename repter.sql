-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2026. Ápr 23. 17:41
-- Kiszolgáló verziója: 10.4.32-MariaDB
-- PHP verzió: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `repter`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `jaratok`
--

CREATE TABLE `jaratok` (
  `id` int(11) NOT NULL,
  `jaratszam` varchar(20) NOT NULL,
  `repulo_id` int(11) NOT NULL,
  `jegyar_adoval` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `jaratok`
--

INSERT INTO `jaratok` (`id`, `jaratszam`, `repulo_id`, `jegyar_adoval`) VALUES
(1, 'BF101', 1, 17995),
(2, 'BF101R', 1, 18857),
(3, 'BF102', 1, 14961),
(4, 'BF102R', 1, 15978),
(5, 'BF103', 1, 22844),
(6, 'BF103R', 1, 23625),
(7, 'BF104', 1, 16270),
(8, 'BF104R', 1, 17131),
(9, 'BF105', 1, 14961),
(10, 'BF105R', 1, 15978),
(11, 'BF106', 1, 22073),
(12, 'BF106R', 1, 22844),
(13, 'BF107', 1, 17131),
(14, 'BF107R', 1, 17995),
(15, 'BF108', 1, 13957),
(16, 'BF108R', 1, 14961),
(17, 'BF109', 1, 22844),
(18, 'BF109R', 1, 22073),
(19, 'BF110', 1, 17995),
(20, 'BF110R', 1, 17131),
(21, 'KF201', 2, 75096),
(22, 'KF201R', 2, 77749),
(23, 'KF202', 2, 81365),
(24, 'KF202R', 2, 78826),
(25, 'KF203', 2, 88736),
(26, 'KF203R', 2, 88286),
(27, 'KF204', 2, 94216),
(28, 'KF204R', 2, 91850),
(29, 'KF205', 2, 98434),
(30, 'KF205R', 2, 100676),
(31, 'KF206', 2, 69797),
(32, 'KF206R', 2, 72447),
(33, 'KF207', 2, 78826),
(34, 'KF207R', 2, 81365),
(35, 'KF208', 2, 86286),
(36, 'KF208R', 2, 88736),
(37, 'KF209', 2, 91850),
(38, 'KF209R', 2, 94216),
(39, 'KF210', 2, 96194),
(40, 'KF210R', 2, 98434);

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `jaratok_excel`
--

CREATE TABLE `jaratok_excel` (
  `jaratszam` varchar(20) NOT NULL,
  `nap` varchar(20) DEFAULT NULL,
  `honnan_nev` varchar(50) DEFAULT NULL,
  `hova_nev` varchar(50) DEFAULT NULL,
  `indul_dec` decimal(18,15) DEFAULT NULL,
  `erkezik_dec` decimal(18,15) DEFAULT NULL,
  `repulogep_tipus` varchar(50) DEFAULT NULL,
  `repter_tav_km` decimal(18,2) DEFAULT NULL,
  `repulo_sebesseg_egy_ut` decimal(18,2) DEFAULT NULL,
  `jegyar_alap_atlag` decimal(18,2) DEFAULT NULL,
  `profittal` decimal(18,2) DEFAULT NULL,
  `adoval_egyutt` decimal(18,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `kapu`
--

CREATE TABLE `kapu` (
  `id` int(11) NOT NULL,
  `nev` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `kapu`
--

INSERT INTO `kapu` (`id`, `nev`) VALUES
(1, 'Kapu 1');

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `menetrend`
--

CREATE TABLE `menetrend` (
  `id` int(11) NOT NULL,
  `jarat_id` int(11) NOT NULL,
  `nap` varchar(20) NOT NULL,
  `indul` time NOT NULL,
  `erkezik` time NOT NULL,
  `kapu_id` int(11) NOT NULL,
  `jegyar_adoval` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `menetrend`
--

INSERT INTO `menetrend` (`id`, `jarat_id`, `nap`, `indul`, `erkezik`, `kapu_id`, `jegyar_adoval`) VALUES
(1, 1, 'Szerda', '08:00:00', '09:00:00', 1, 17995),
(2, 3, 'Péntek', '16:00:00', '17:15:00', 1, 16270),
(3, 5, 'Vasárnap', '15:00:00', '16:30:00', 1, 17131),
(4, 7, 'Hétfő', '13:30:00', '14:20:00', 1, 17995),
(5, 9, 'Szerda', '12:00:00', '12:45:00', 1, 14961),
(6, 11, 'Péntek', '14:00:00', '15:25:00', 1, 14961),
(7, 13, 'Vasárnap', '12:00:00', '12:55:00', 1, 13957),
(8, 15, 'Hétfő', '13:00:00', '13:40:00', 1, 22844),
(9, 17, 'Szerda', '14:00:00', '16:20:00', 1, 22073),
(10, 19, 'Péntek', '12:00:00', '13:00:00', 1, 22844),
(11, 21, 'Szerda', '06:00:00', '08:00:00', 1, 75096),
(12, 23, 'Péntek', '10:00:00', '12:15:00', 1, 69797),
(13, 25, 'Vasárnap', '18:00:00', '20:30:00', 1, 81365),
(14, 27, 'Hétfő', '06:00:00', '08:45:00', 1, 78826),
(15, 29, 'Szerda', '16:00:00', '19:00:00', 1, 88736),
(16, 31, 'Péntek', '06:00:00', '07:50:00', 1, 86286),
(17, 33, 'Vasárnap', '06:00:00', '08:10:00', 1, 91850),
(18, 35, 'Hétfő', '16:30:00', '18:55:00', 1, 94216),
(19, 37, 'Szerda', '10:00:00', '12:40:00', 1, 98434),
(20, 39, 'Péntek', '08:00:00', '10:55:00', 1, 96194),
(32, 2, 'Csütörtök', '06:55:00', '08:00:00', 1, 18857),
(33, 4, 'Szombat', '04:40:00', '06:00:00', 1, 17131),
(34, 6, 'Hétfő', '07:25:00', '09:00:00', 1, 17995),
(35, 8, 'Kedd', '05:05:00', '06:00:00', 1, 17131),
(36, 10, 'Csütörtök', '05:10:00', '06:00:00', 1, 15978),
(37, 12, 'Szombat', '14:30:00', '16:00:00', 1, 15978),
(38, 14, 'Hétfő', '14:00:00', '15:00:00', 1, 14961),
(39, 16, 'Kedd', '14:15:00', '15:00:00', 1, 23625),
(40, 18, 'Csütörtök', '12:35:00', '14:00:00', 1, 22844),
(41, 20, 'Szombat', '13:05:00', '14:00:00', 1, 22073),
(42, 22, 'Csütörtök', '07:55:00', '10:00:00', 1, 77749),
(43, 24, 'Szombat', '10:40:00', '12:00:00', 1, 72447),
(44, 26, 'Hétfő', '05:55:00', '07:30:00', 1, 78826),
(45, 28, 'Kedd', '15:10:00', '16:00:00', 1, 81365),
(46, 30, 'Csütörtök', '08:55:00', '12:00:00', 1, 86286),
(47, 32, 'Szombat', '06:05:00', '08:00:00', 1, 88736),
(48, 34, 'Hétfő', '08:15:00', '10:30:00', 1, 94216),
(49, 36, 'Kedd', '09:30:00', '12:00:00', 1, 91850),
(50, 38, 'Csütörtök', '13:15:00', '16:00:00', 1, 100676),
(51, 40, 'Szombat', '07:00:00', '10:00:00', 1, 98434);

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `napok`
--

CREATE TABLE `napok` (
  `id` tinyint(4) NOT NULL,
  `nev` varchar(20) NOT NULL,
  `sorrend` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `napok`
--

INSERT INTO `napok` (`id`, `nev`, `sorrend`) VALUES
(1, 'Hétfő', 1),
(2, 'Kedd', 2),
(3, 'Szerda', 3),
(4, 'Csütörtök', 4),
(5, 'Péntek', 5),
(6, 'Szombat', 6),
(7, 'Vasárnap', 7);

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `repulo`
--

CREATE TABLE `repulo` (
  `id` int(11) NOT NULL,
  `tipus` varchar(50) NOT NULL,
  `befogado_kepesseg` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `repulo`
--

INSERT INTO `repulo` (`id`, `tipus`, `befogado_kepesseg`) VALUES
(1, 'DHC-6 Twin Otter', 20),
(2, 'Saab 340', 34);

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `varosok`
--

CREATE TABLE `varosok` (
  `id` int(11) NOT NULL,
  `nev` varchar(50) NOT NULL,
  `tipus` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- A tábla adatainak kiíratása `varosok`
--

INSERT INTO `varosok` (`id`, `nev`, `tipus`) VALUES
(1, 'Várkút', 'belföldi'),
(2, 'Délmező', 'belföldi'),
(3, 'Kővár', 'belföldi'),
(4, 'Aérilon', 'külföldi'),
(5, 'Nordhaven', 'külföldi'),
(6, 'Solméra', 'külföldi'),
(7, 'Valderin', 'külföldi'),
(8, 'Elystria', 'külföldi'),
(9, 'Főhaven', 'belföldi');

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `jaratok`
--
ALTER TABLE `jaratok`
  ADD PRIMARY KEY (`id`),
  ADD KEY `repulo_id` (`repulo_id`);

--
-- A tábla indexei `jaratok_excel`
--
ALTER TABLE `jaratok_excel`
  ADD PRIMARY KEY (`jaratszam`);

--
-- A tábla indexei `kapu`
--
ALTER TABLE `kapu`
  ADD PRIMARY KEY (`id`);

--
-- A tábla indexei `menetrend`
--
ALTER TABLE `menetrend`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jarat_id` (`jarat_id`),
  ADD KEY `kapu_id` (`kapu_id`);

--
-- A tábla indexei `napok`
--
ALTER TABLE `napok`
  ADD PRIMARY KEY (`id`);

--
-- A tábla indexei `repulo`
--
ALTER TABLE `repulo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tipus` (`tipus`);

--
-- A tábla indexei `varosok`
--
ALTER TABLE `varosok`
  ADD PRIMARY KEY (`id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `napok`
--
ALTER TABLE `napok`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT a táblához `repulo`
--
ALTER TABLE `repulo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Megkötések a kiírt táblákhoz
--

--
-- Megkötések a táblához `jaratok`
--
ALTER TABLE `jaratok`
  ADD CONSTRAINT `jaratok_ibfk_1` FOREIGN KEY (`repulo_id`) REFERENCES `repulo` (`id`);

--
-- Megkötések a táblához `menetrend`
--
ALTER TABLE `menetrend`
  ADD CONSTRAINT `menetrend_ibfk_1` FOREIGN KEY (`jarat_id`) REFERENCES `jaratok` (`id`),
  ADD CONSTRAINT `menetrend_ibfk_2` FOREIGN KEY (`kapu_id`) REFERENCES `kapu` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
