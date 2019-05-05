-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2019-05-05 18:50:17
-- 服务器版本： 5.7.25-0ubuntu0.16.04.2
-- PHP Version: 7.0.33-0ubuntu0.16.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `OJ`
--

-- --------------------------------------------------------

--
-- 表的结构 `checker`
--

CREATE TABLE `checker` (
  `probid` int(11) NOT NULL,
  `datain` varchar(256) DEFAULT NULL COMMENT '输入文件路径',
  `dataout` varchar(256) DEFAULT NULL COMMENT '标准输出路径',
  `solution` varchar(256) DEFAULT NULL COMMENT '标程路径',
  `checker` varchar(256) DEFAULT './checker.py' COMMENT '检查器路劲',
  `limittime` int(11) DEFAULT '1000' COMMENT 'ms',
  `limitmemory` int(11) DEFAULT '524288' COMMENT 'KB'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='问题输入输出和标准程序，检查器';

--
-- 转存表中的数据 `checker`
--

INSERT INTO `checker` (`probid`, `datain`, `dataout`, `solution`, `checker`, `limittime`, `limitmemory`) VALUES
(1001, './problem/datain/1001.in', './problem/dataout/1001.out', './problem/solution/1001.cpp', './checker.py', 1000, 524288),
(1002, './problem/datain/1002.in', './problem/dataout/1002.out', './problem/solution/1002.cpp', './checker.py', 1000, 524288);

-- --------------------------------------------------------

--
-- 表的结构 `code`
--

CREATE TABLE `code` (
  `runid` int(11) NOT NULL COMMENT 'RunID',
  `judgestatus` varchar(256) DEFAULT 'Waiting' COMMENT '运行状态',
  `exetime` int(11) DEFAULT '0' COMMENT '运行时间ms',
  `exememory` int(11) DEFAULT '0' COMMENT '运行内存KB',
  `codelen` int(11) DEFAULT '0' COMMENT '代码长度B',
  `codefile` varchar(256) NOT NULL DEFAULT './A.cpp' COMMENT '代码路径',
  `warning` varchar(256) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `code`
--

INSERT INTO `code` (`runid`, `judgestatus`, `exetime`, `exememory`, `codelen`, `codefile`, `warning`) VALUES
(1, 'language_not_support', 0, 0, 0, './A.cpp', ''),
(2, 'Accept', 16, 416, 155, './code/2.cpp', ''),
(3, 'Accept', 1, 416, 148, './code/3.cpp', ''),
(4, 'Accept', 1, 416, 148, './code/4.cpp', ''),
(5, 'Illegal_2', 22, 6804, 93, './code/5.py', ''),
(6, 'Accept', 25, 6740, 93, './code/6.py', ''),
(7, 'Accept', 17, 416, 155, './code/7.cpp', ''),
(8, 'CompileError', 0, 0, 11, './code/8.cpp', 'g++: error: ./code/8.cpp: No such file or directory\ng++: fatal error: no input files\ncompilation terminated.\n'),
(9, 'CompileError', 0, 0, 9, './code/9.cpp', './code/9.cpp:1:1: error: ‘dfafdafaf’ does not name a type\n dfafdafaf\n ^~~~~~~~~\n'),
(10, 'CompileError', 0, 0, 147, './code/10.cpp', './code/10.cpp: In function ‘int main()’:\n./code/10.cpp:7:2: error: expected initializer before ‘while’\n  while(cin>>a>>b){\n  ^~~~~\n');

-- --------------------------------------------------------

--
-- 表的结构 `problem`
--

CREATE TABLE `problem` (
  `probid` int(11) NOT NULL COMMENT '问题ID',
  `probtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '问题加入时间',
  `title` varchar(128) DEFAULT NULL,
  `statement` varchar(2048) DEFAULT NULL COMMENT '题面',
  `input` varchar(2048) DEFAULT NULL COMMENT '输入格式',
  `output` varchar(2048) DEFAULT NULL COMMENT '输出格式',
  `sampleinput` varchar(2048) DEFAULT NULL COMMENT '样例输入',
  `sampleoutput` varchar(2048) DEFAULT NULL COMMENT '样例输出',
  `source` varchar(1024) DEFAULT NULL COMMENT '问题来源作者等',
  `link` varchar(1024) DEFAULT NULL COMMENT '问题链接'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `problem`
--

INSERT INTO `problem` (`probid`, `probtime`, `title`, `statement`, `input`, `output`, `sampleinput`, `sampleoutput`, `source`, `link`) VALUES
(1001, '2019-04-11 13:33:52', 'a+b', '输入a,b两个整数，输出a+b.', '多组输入，每组数据占一行,0<=a,b<=1e9', '对于每一组输出一行，该行一个整数a+b', '1 1\r\n2 3', '2\r\n5', NULL, NULL),
(1002, '2019-04-11 13:33:52', 'gcd(a,b)', '输入a,b两个整数，输出gcd(a,b),gcd表示最大公约数', '多组输入，每组数据占一行,0<=a,b<=1e7', '对于每一组输出一行，该行一个整数a+b', '2 4\r\n24 16', '2\r\n8', NULL, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `submit`
--

CREATE TABLE `submit` (
  `runid` int(11) NOT NULL,
  `uid` varchar(256) NOT NULL,
  `submtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `probid` int(11) NOT NULL,
  `language` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `submit`
--

INSERT INTO `submit` (`runid`, `uid`, `submtime`, `probid`, `language`) VALUES
(1, '__system', '2019-05-05 13:19:43', 1001, 'c+++++'),
(2, 'kangba', '2019-05-05 13:21:32', 1002, 'c++'),
(3, 'kangba', '2019-05-05 13:21:54', 1001, 'c++'),
(4, 'kangba', '2019-05-05 13:25:35', 1001, 'c++'),
(5, 'tina', '2019-05-05 14:26:32', 1001, 'python3'),
(6, 'tina', '2019-05-05 14:27:44', 1001, 'python3'),
(7, 'tina', '2019-05-05 14:36:45', 1002, 'c++'),
(8, 'kangba', '2019-05-05 15:01:35', 1001, 'c++'),
(9, 'kangba', '2019-05-05 18:28:44', 1002, 'c++'),
(10, 'kangba', '2019-05-05 18:38:26', 1001, 'c++');

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `uid` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `codeforce` varchar(256) DEFAULT NULL,
  `nationality` varchar(256) DEFAULT NULL,
  `gender` varchar(128) DEFAULT NULL,
  `motto` varchar(1024) DEFAULT NULL,
  `contact` varchar(256) DEFAULT NULL,
  `signup` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`ID`, `uid`, `password`, `codeforce`, `nationality`, `gender`, `motto`, `contact`, `signup`) VALUES
(1, 'kangba', '123', NULL, NULL, 'male', NULL, NULL, '2019-05-05 13:18:57'),
(2, 'tinasb', 'sbtina', NULL, NULL, 'female', NULL, NULL, '2019-05-05 14:23:34'),
(3, 'system', '321', NULL, NULL, 'female', NULL, NULL, '2019-05-05 14:37:44'),
(4, '__system', '321', NULL, NULL, 'male', NULL, NULL, '2019-05-05 15:11:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `checker`
--
ALTER TABLE `checker`
  ADD PRIMARY KEY (`probid`);

--
-- Indexes for table `code`
--
ALTER TABLE `code`
  ADD PRIMARY KEY (`runid`);

--
-- Indexes for table `problem`
--
ALTER TABLE `problem`
  ADD PRIMARY KEY (`probid`);

--
-- Indexes for table `submit`
--
ALTER TABLE `submit`
  ADD PRIMARY KEY (`runid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`,`uid`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `problem`
--
ALTER TABLE `problem`
  MODIFY `probid` int(11) NOT NULL AUTO_INCREMENT COMMENT '问题ID', AUTO_INCREMENT=1003;
--
-- 使用表AUTO_INCREMENT `submit`
--
ALTER TABLE `submit`
  MODIFY `runid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
