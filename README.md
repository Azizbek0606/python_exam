# 🏫 Bog'cha Inventarizatsiya Boshqaruv Tizimi

**Bog‘cha Inventarizatsiya Boshqaruv Tizimi** — bu bog‘cha oshxonasida ishlatiladigan mahsulotlar, taomlar, porsiyalar va oylik hisobotlarni boshqarishga mo‘ljallangan veb-ilova. Tizim **Django** asosida ishlab chiqilgan va zamonaviy frontend, backend va asinxron xizmatlar bilan integratsiyalashgan.

---

## 📌 Funksional imkoniyatlar

### 🧺 Mahsulotlar (Ingredientlar) boshqaruvi
- Mahsulotlar zaxirasini ko‘rish va boshqarish
- Yetkazib berilgan sanani kiritish
- Kam qolgan mahsulotlar haqida ogohlantirishlar

### 🍽 Taomlar va Retseptlar boshqaruvi
- Turli xil taomlar uchun retseptlar yaratish (nonushta, tushlik, kechki ovqat)
- Retseptlarga mahsulotlarni biriktirish
- Har bir mahsulot uchun kerakli miqdorni belgilash

### 🔢 Porsiyalarni hisoblash
- Berilgan porsiyalar sonini kiritish
- Foydalanuvchilarga porsiyalarni ulash
- Mahsulotlar zaxirasini avtomatik yangilash

### 📊 Oylik Hisobotlar
- Rejalashtirilgan va haqiqiy porsiyalarni solishtirish
- Farq foizlari bo‘yicha ogohlantirishlar
- Vizual diagrammalar orqali ko‘rsatish

---

## 🛠 Texnologiyalar

| Kategoriya     | Texnologiya                              |
|----------------|------------------------------------------|
| Backend        | Django 4.2.21, Django REST Framework 3.14 |
| Frontend       | HTML, Tailwind CSS, Chart.js             |
| Ma'lumotlar ombori | SQLite3                               |
| Asinxron ishlar| Celery 5.3.7, Redis 5.0.3                |
| Server         | Gunicorn 22.0.0                          |
| Konteynerlar   | Docker, Docker Compose                   |

---

## ⚙️ O'rnatish

### 📦 Talablar
- Docker & Docker Compose
- Git
- Redis (Docker ishlatilmasa)

### 🐳 Docker bilan o'rnatish

```bash
git clone https://github.com/Azizbek0606/python_exam.git
cd kindergarten
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
