# Minesweeper

Pet-project консольной игры **Minesweeper** на Python.  
Проект реализует классическую механику сапёра с генерацией игрового поля, обработкой ходов, установкой флагов и проверкой условий победы или поражения.  
Также проект демонстрирует применение принципов **объектно-ориентированного программирования (OOP)** для организации игровой логики и разделения ответственности между компонентами.

## Features

- **Interactive CLI Game** — игра через консольный интерфейс
- **Minefield Generation** — случайная генерация игрового поля
- **First Click Protection** — безопасный первый ход
- **Reveal & Flag Actions** — открытие клеток и установка флагов
- **Cascade Opening** — автоматическое раскрытие пустых областей
- **Game State Validation** — проверка победы и поражения
- **Solver Logic** — модуль для анализа поля и поиска безопасных ходов
- **OOP Design** — организация логики игры с использованием объектно-ориентированного подхода

## Project Structure

- `play_minesweeper.py` — запуск игры и основной игровой цикл
- `minesweeper_engine.py` — игровая логика и работа с полем
- `solver.py` — модуль анализа и логики решения

## Tech Stack

- **Language:** Python
- **Paradigm:** Object-Oriented Programming (OOP)
- **Architecture:** modular structure
- **Interface:** console / terminal
- **Game Logic:** custom Minesweeper engine

## Project Goal

Цель проекта — попрактиковаться в Python, объектно-ориентированном проектировании, декомпозиции программы на отдельные модули и реализации игровой логики.
