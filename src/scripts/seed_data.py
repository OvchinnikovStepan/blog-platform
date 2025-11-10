# src/scripts/seed_data.py
import asyncio
import sys
import os
import hashlib

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import AsyncSessionLocal
from src.models.models import User, Article, Tag, Comment, article_tags
from sqlalchemy.future import select
from sqlalchemy import insert

def get_password_hash(password):
    """Простое хеширование пароля для тестовых данных"""
    salt = "test_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        
        if existing_users:
            print("База данных уже содержит данные. Пропускаем заполнение.")
            return

        print("Начинаем заполнение базы данных тестовыми данными...")

        # Создаем тестовых пользователей
        users_data = [
            {
                "email": "alice@example.com",
                "username": "alice_writer",
                "hashed_password": get_password_hash("password123"),
                "bio": "Писатель и блогер. Люблю делиться своими мыслями с миром.",
                "image_url": "https://example.com/images/alice.jpg"
            },
            {
                "email": "bob@example.com", 
                "username": "bob_developer",
                "hashed_password": get_password_hash("password123"),
                "bio": "Full-stack разработчик. Пишу о программировании и технологиях.",
                "image_url": "https://example.com/images/bob.jpg"
            },
            {
                "email": "carol@example.com",
                "username": "carol_designer", 
                "hashed_password": get_password_hash("password123"),
                "bio": "UI/UX дизайнер. Исследую тренды в дизайне и пользовательском опыте.",
                "image_url": "https://example.com/images/carol.jpg"
            }
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
            users.append(user)

        await session.flush()  # Получаем ID пользователей
        
        print("Создано пользователей:", len(users))

        # Создаем теги
        tags_data = [
            {"name": "Python"},
            {"name": "FastAPI"},
            {"name": "Docker"},
            {"name": "Базы данных"},
            {"name": "Веб-разработка"},
            {"name": "Дизайн"},
            {"name": "Программирование"},
            {"name": "Технологии"}
        ]

        tags = []
        for tag_data in tags_data:
            tag = Tag(**tag_data)
            session.add(tag)
            tags.append(tag)

        await session.flush()  # Получаем ID тегов
        
        print("Создано тегов:", len(tags))

        # Создаем статьи
        articles_data = [
            {
                "title": "Знакомство с FastAPI",
                "slug": "znakomstvo-s-fastapi",
                "description": "Быстрое и современное веб-фреймворк для Python",
                "body": "FastAPI - это современный, быстрый веб-фреймворк для построения API с Python 3.6+.",
                "author_id": users[1].id  # Bob - разработчик
            },
            {
                "title": "Docker для начинающих",
                "slug": "docker-dlya-nachinayushchikh",
                "description": "Основы контейнеризации приложений с Docker",
                "body": "Docker - это платформа для разработки, доставки и запуска приложений в контейнерах.",
                "author_id": users[1].id  # Bob - разработчик
            },
            {
                "title": "Принципы хорошего UI/UX дизайна",
                "slug": "printsipy-khoroshego-ui-ux-dizaina",
                "description": "Как создавать интерфейсы, которые нравятся пользователям",
                "body": "Хороший дизайн - это не только красиво, но и функционально.",
                "author_id": users[2].id  # Carol - дизайнер
            },
            {
                "title": "Мой путь в писательстве",
                "slug": "moi-put-v-pisatelstve",
                "description": "Личный опыт становления профессиональным писателем",
                "body": "Писать - это не просто складывать слова в предложения. Это искусство передачи мыслей и эмоций.",
                "author_id": users[0].id  # Alice - писатель
            }
        ]

        articles = []
        for article_data in articles_data:
            article = Article(**article_data)
            session.add(article)
            articles.append(article)

        await session.flush()  # Получаем ID статей
        
        print("Создано статей:", len(articles))

        # Добавляем связи между статьями и тегами через промежуточную таблицу
        article_tag_links = []
        
        # Статья 1: FastAPI (теги: Python, FastAPI, Веб-разработка, Программирование)
        article_tag_links.extend([
            {"article_id": articles[0].id, "tag_id": tags[0].id},  # Python
            {"article_id": articles[0].id, "tag_id": tags[1].id},  # FastAPI
            {"article_id": articles[0].id, "tag_id": tags[4].id},  # Веб-разработка
            {"article_id": articles[0].id, "tag_id": tags[6].id},  # Программирование
        ])
        
        # Статья 2: Docker (теги: Docker, Базы данных, Веб-разработка, Программирование, Технологии)
        article_tag_links.extend([
            {"article_id": articles[1].id, "tag_id": tags[2].id},  # Docker
            {"article_id": articles[1].id, "tag_id": tags[3].id},  # Базы данных
            {"article_id": articles[1].id, "tag_id": tags[4].id},  # Веб-разработка
            {"article_id": articles[1].id, "tag_id": tags[6].id},  # Программирование
            {"article_id": articles[1].id, "tag_id": tags[7].id},  # Технологии
        ])
        
        # Статья 3: Дизайн (теги: Дизайн, Технологии)
        article_tag_links.extend([
            {"article_id": articles[2].id, "tag_id": tags[5].id},  # Дизайн
            {"article_id": articles[2].id, "tag_id": tags[7].id},  # Технологии
        ])
        
        # Статья 4: Писательство (теги: Программирование, Технологии)
        article_tag_links.extend([
            {"article_id": articles[3].id, "tag_id": tags[6].id},  # Программирование
            {"article_id": articles[3].id, "tag_id": tags[7].id},  # Технологии
        ])

        # Вставляем связи в промежуточную таблицу
        if article_tag_links:
            await session.execute(insert(article_tags), article_tag_links)
        
        print("Создано связей статей с тегами:", len(article_tag_links))

        # Создаем комментарии
        comments_data = [
            {
                "body": "Отличная статья! Очень помогло разобраться с FastAPI.",
                "article_id": articles[0].id,
                "author_id": users[2].id  # Carol
            },
            {
                "body": "Спасибо за подробное объяснение! Жду продолжения.",
                "article_id": articles[0].id, 
                "author_id": users[0].id  # Alice
            },
            {
                "body": "Docker действительно упрощает разработку. Хороший обзор для новичков!",
                "article_id": articles[1].id,
                "author_id": users[0].id  # Alice
            },
            {
                "body": "Как дизайнер, полностью согласна с принципами из статьи!",
                "article_id": articles[2].id,
                "author_id": users[1].id  # Bob
            },
            {
                "body": "Вдохновляющая история! Спасибо, что делитесь опытом.",
                "article_id": articles[3].id,
                "author_id": users[1].id  # Bob
            }
        ]

        for comment_data in comments_data:
            comment = Comment(**comment_data)
            session.add(comment)

        # Сохраняем все изменения
        await session.commit()
        
        print("✅ Тестовые данные успешно добавлены в базу данных!")
        print(f"📊 Статистика:")
        print(f"   - Пользователей: {len(users)}")
        print(f"   - Статей: {len(articles)}") 
        print(f"   - Тегов: {len(tags)}")
        print(f"   - Комментариев: {len(comments_data)}")
        print(f"   - Связей статей с тегами: {len(article_tag_links)}")

async def main():
    try:
        await seed_data()
    except Exception as e:
        print(f"❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())