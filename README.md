# 🏗️ SkyForge Constructions — Full Stack Web App

> Production-ready Construction Business Website with Flask + MongoDB + JWT

---

## 📁 Project Structure

```
skyforge/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/
│   │   ├── __init__.py
│   │   └── db.py               # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── auth_middleware.py  # JWT middleware
│   └── routes/
│       ├── __init__.py
│       ├── auth.py             # /api/login
│       ├── leads.py            # /api/leads
│       ├── projects.py         # /api/projects
│       ├── reviews.py          # /api/reviews
│       └── analytics.py        # /api/analytics
└── frontend/
    └── index.html              # Complete SPA frontend
```

---

## ⚙️ Local Setup

### 1. Backend (Flask)

```bash
cd skyforge/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI and secret key

# Run Flask server
python app.py
# → Running on http://localhost:5000
```

### 2. Frontend

Simply open `frontend/index.html` in your browser.  
Or use Live Server (VS Code extension) for hot reload.

---

## 🌿 .env File

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
MONGO_URI=mongodb://localhost:27017/skyforge
PORT=5000
```

---

## 🍃 MongoDB Atlas Setup

1. Go to https://cloud.mongodb.com
2. Create a free cluster
3. Click **Connect → Connect your application**
4. Copy the URI and paste into `.env` as `MONGO_URI`
5. Replace `<password>` with your DB user password

**Collections created automatically:**
- `users` — Admin accounts
- `leads` — Contact form submissions
- `projects` — Construction projects
- `reviews` — Customer reviews

Create your own account from the sign-up form and choose `user` or `admin`.

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/login` | — | Admin login → returns JWT |
| GET | `/api/leads` | ✅ JWT | Get all leads |
| POST | `/api/leads` | — | Submit contact form |
| DELETE | `/api/leads/:id` | ✅ JWT | Delete a lead |
| GET | `/api/projects` | — | Get all projects |
| POST | `/api/projects` | ✅ JWT | Add project |
| PUT | `/api/projects/:id` | ✅ JWT | Update project |
| DELETE | `/api/projects/:id` | ✅ JWT | Delete project |
| GET | `/api/reviews` | — | Get approved reviews |
| GET | `/api/reviews/all` | ✅ JWT | Get all reviews |
| POST | `/api/reviews` | — | Submit review |
| PATCH | `/api/reviews/:id/approve` | ✅ JWT | Approve review |
| DELETE | `/api/reviews/:id` | ✅ JWT | Delete review |
| GET | `/api/analytics` | ✅ JWT | Dashboard stats |

---

## 🚀 Deployment

### Backend → Render.com

1. Push backend folder to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add Environment Variables:
   - `SECRET_KEY` = your secret
   - `MONGO_URI` = your Atlas URI
6. Deploy! You'll get a URL like `https://skyforge-api.onrender.com`

### Frontend → Netlify

1. Update `API` variable in `index.html` to your Render URL:
   ```js
   const API = 'https://skyforge-api.onrender.com/api';
   ```
2. Drag & drop `frontend/` folder to https://netlify.com/drop
3. Done! Your site is live.

---

## 🔧 Install Gunicorn (for production)

```bash
pip install gunicorn
# Add to requirements.txt:
echo "gunicorn==21.2.0" >> requirements.txt
```

---

## 🌐 Features

| Feature | Status |
|---------|--------|
| Home Page (Hero, Services, Projects, Reviews) | ✅ |
| Services Page with pricing | ✅ |
| Projects Gallery with filter (category/status) | ✅ |
| Cost Calculator (sq.ft × rate × quality) | ✅ |
| Contact Form + WhatsApp integration | ✅ |
| Admin Login with JWT | ✅ |
| Admin Dashboard (Analytics, Leads, Projects, Reviews) | ✅ |
| Add/Edit/Delete Projects with status | ✅ |
| Project status: pending / approved / done | ✅ |
| Approve/Delete Reviews | ✅ |
| Charts (Monthly Leads, Project Status Donut) | ✅ |
| Dark Mode | ✅ |
| Mobile Responsive | ✅ |
| Demo mode (works without backend) | ✅ |

---

## 🎨 Tech Stack

- **Backend:** Python, Flask, PyMongo, JWT, bcrypt
- **Database:** MongoDB Atlas
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS, Chart.js
- **Auth:** JWT Bearer tokens
- **Fonts:** Playfair Display + Inter
- **Deployment:** Render (backend) + Netlify (frontend)

---

## 🔐 Security

- Passwords hashed with `werkzeug.security` (bcrypt)
- JWT tokens expire in 24 hours
- All admin routes protected with `@token_required`
- CORS configured for production domains

---

*Built for SkyForge Constructions — From Blueprint to Reality*
