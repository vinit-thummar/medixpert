# MediXpert - AI-Powered Disease Diagnosis System

A comprehensive healthcare platform that provides AI-powered disease diagnosis, doctor recommendations, appointment booking, and telemedicine features.

## Project Structure

```
medixpert/
├── backend/           # Django backend API
├── frontend/          # React frontend application
├── manage.py          # Django management script
└── README.md          # This file
```

## Features

### Core Features
- **Landing Page**: Animated hero section with call-to-action buttons
- **User Authentication**: Register/Login with role-based access (Patient/Doctor/Admin)
- **Disease Prediction**: AI-powered symptom-to-disease diagnosis using machine learning
- **Doctor Suggestions**: Location-based doctor recommendations
- **Appointment Booking**: Schedule appointments with available doctors
- **Medical Reports**: Upload and manage medical documents
- **Diagnosis History**: Track previous diagnoses and insights
- **Admin Panel**: Comprehensive management dashboard

### Advanced Features
- **Email Notifications**: Automated appointment confirmations
- **Real-time Chat**: Patient-doctor communication (optional)
- **Analytics Dashboard**: Disease trends and user insights
- **Google Sign-In**: OAuth2 authentication integration

## Technology Stack

### Backend
- **Django**: Web framework and REST API
- **Django REST Framework**: API development
- **SQLite/PostgreSQL**: Database
- **Scikit-learn**: Machine learning for disease prediction
- **Pandas/NumPy**: Data processing

### Frontend
- **React.js**: User interface framework
- **Tailwind CSS**: Styling and responsive design
- **Framer Motion**: Animations and transitions
- **Chart.js/Recharts**: Data visualization
- **React Router**: Navigation and routing

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm/pnpm

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
pnpm install
pnpm run dev
```

## API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/predict/` - Disease prediction
- `GET /api/doctors/` - Doctor suggestions
- `POST /api/appointments/` - Book appointments
- `POST /api/reports/upload/` - Upload medical reports
- `GET /api/history/` - Diagnosis history

## Development Guidelines

1. **Backend**: Follow Django best practices and REST API conventions
2. **Frontend**: Use React hooks and functional components
3. **Styling**: Utilize Tailwind CSS for consistent design
4. **Testing**: Implement unit and integration tests
5. **Documentation**: Maintain clear API documentation

## Deployment

The application is designed to be deployed with:
- Backend: Django on cloud platforms (Heroku, AWS, etc.)
- Frontend: Static hosting (Netlify, Vercel, etc.)
- Database: PostgreSQL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is developed for educational purposes as part of a comprehensive healthcare system demonstration.

