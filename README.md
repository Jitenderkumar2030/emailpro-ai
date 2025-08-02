# 🚀 EmailProAI - AI-Powered Email Automation Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)

> **World-class email automation platform with AI-powered content generation, advanced analytics, and enterprise features**

## ✨ Key Features

- 🤖 **AI Email Generation** - GPT-4 powered email writing
- 📊 **Advanced Analytics** - Real-time tracking & reporting
- 🔄 **Campaign Automation** - Bulk emails with CSV upload
- 📧 **Email Integrations** - Gmail & Outlook OAuth
- 💳 **Payment System** - Cashfree payment gateway
- 👥 **Team Collaboration** - Multi-user enterprise features
- 📱 **Mobile Ready** - Push notifications & mobile API
- 🎨 **White Label** - Custom branding support

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI + SQLAlchemy + PostgreSQL
- **AI Integration**: OpenAI GPT-4 API
- **Authentication**: OAuth 2.0 + JWT tokens
- **Email Services**: Gmail API, Outlook Graph API
- **Payments**: Cashfree payment gateway
- **Background Tasks**: APScheduler

### Frontend (Next.js)
- **Framework**: Next.js 13+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + Hooks
- **API Client**: Axios with interceptors

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📊 API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## 🔧 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost/emailproai
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
CASHFREE_APP_ID=your_cashfree_app_id
CASHFREE_SECRET_KEY=your_cashfree_secret_key
FCM_SERVER_KEY=your_fcm_server_key
```

## 📈 Features Overview

### 🤖 AI Email Generation
- Multiple tone options (Professional, Friendly, Formal)
- Context-aware email replies
- Subject line generation
- Template integration

### 📊 Campaign Management
- CSV bulk upload
- Real-time analytics
- A/B testing
- Drip campaigns

### 📧 Email Tracking
- Open tracking (1x1 pixel)
- Click tracking
- Reply detection
- Bounce handling

### 💰 Subscription Plans
- **FREE**: 3 emails/day
- **STARTER**: 100 emails/day ($9.99/month)
- **PRO**: Unlimited emails ($29.99/month)
- **LIFETIME**: Unlimited forever ($99.99)

## 🏢 Enterprise Features

- **Team Management**: Role-based access control
- **White Labeling**: Custom branding
- **API Access**: RESTful API with authentication
- **Advanced Analytics**: PDF/Excel reports
- **Audit Logs**: Complete activity tracking

## 📱 Mobile Support

- Push notifications via Firebase
- Mobile-optimized API endpoints
- Offline capability
- Quick actions

## 🔐 Security

- bcrypt password hashing
- JWT token authentication
- OAuth 2.0 integrations
- SQL injection protection
- CORS configuration
- Input validation

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Production Checklist
- [ ] Configure environment variables
- [ ] Set up SSL certificates
- [ ] Configure domain DNS
- [ ] Set up monitoring
- [ ] Configure backups

## 📊 Database Schema

- **Users**: User accounts and settings
- **Campaigns**: Email campaigns
- **Email Logs**: Individual email tracking
- **Teams**: Team management
- **Payments**: Payment processing
- **Analytics**: Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI for the amazing framework
- Next.js team for the frontend framework
- All contributors and supporters

---

**Built with ❤️ by [Jitender Kumar](https://github.com/Jitenderkumar2030)**
