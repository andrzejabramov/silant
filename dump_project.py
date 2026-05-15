#!/usr/bin/env python3
"""
Скрипт для создания текстового дампа исходного кода Django-проекта.
Игнорирует venv, __pycache__, .git, static, media, fixtures, базы данных.
"""

import os
from pathlib import Path


def dump_project(root_dir=".", output_file="project_dump.txt"):
    root = Path(root_dir).resolve()

    # 🔹 Папки, которые НЕ дампим
    EXCLUDE_DIRS = {
        ".git",
        "__pycache__",
        "venv",
        "env",
        ".venv",
        "node_modules",
        "static",
        "media",
        "fixtures",
        "dump",
        "backup",
    }

    # 🔹 Допустимые расширения + имена конфигов
    VALID_EXTENSIONS = {
        ".py",
        ".html",
        ".css",
        ".js",
        ".yml",
        ".yaml",
        ".json",
        ".md",
        ".txt",
        ".ini",
        ".cfg",
        ".toml",
    }
    SPECIAL_NAMES = {
        ".env",
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        ".dockerignore",
        ".gitignore",
        "Makefile",
    }

    files_found = []
    output_lines = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        # Пропускаем запрещённые папки
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue

        # Пропускаем спец. файлы и огромные логи/базы
        if path.name in (
            "db.sqlite3",
            ".DS_Store",
            "package-lock.json",
            "yarn.lock",
            "project_dump.txt",
        ):
            continue
        if path.stat().st_size > 1_500_000:  # >1.5MB пропускаем
            continue

        # Проверяем расширение или имя
        if path.suffix in VALID_EXTENSIONS or path.name in SPECIAL_NAMES:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                rel_path = path.relative_to(root)
                files_found.append(str(rel_path))

                output_lines.append(f"\n{'='*60}")
                output_lines.append(f"📄 ФАЙЛ: {rel_path}")
                output_lines.append(f"{'='*60}\n")
                output_lines.append(content)
            except Exception as e:
                output_lines.append(f"\n⚠️ Ошибка чтения {path}: {e}\n")

    # Сохраняем результат
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"📊 ДАМП ПРОЕКТА: {root}\n")
        f.write(f"📅 Найдено файлов: {len(files_found)}\n")
        f.write(f"{'='*60}\n\n")
        f.write("\n".join(output_lines))

    print(f"✅ Дамп сохранён в {output_file}")
    print(f"📦 Обработано файлов: {len(files_found)}")
    print(
        "💡 Скопируй содержимое project_dump.txt сюда или отправь частями (особенно models.py)"
    )


if __name__ == "__main__":
    dump_project()
