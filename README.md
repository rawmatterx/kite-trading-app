# 🚀 Kite Trading App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-blue.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)

A modern web application for algorithmic trading using Zerodha Kite Connect API. This application provides a user-friendly interface for managing trades, analyzing market data, and executing algorithmic trading strategies.

## ✨ Features

- **User Authentication** - Secure JWT-based authentication system
- **Real-time Market Data** - Live market quotes and charts
- **Trading Dashboard** - Monitor account balances, margins, and positions
- **Order Management** - Place, modify, and cancel orders
- **Strategy Backtesting** - Test trading strategies with historical data
- **Paper Trading** - Practice trading without real money
- **Portfolio Analytics** - Track performance and generate reports
- **Responsive Design** - Works on desktop and mobile devices

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT
- **API Documentation**: OpenAPI/Swagger
- **Task Queue**: Celery with Redis
- **Containerization**: Docker
- **Testing**: Pytest

### Frontend
- **Framework**: React 18 with TypeScript
- **State Management**: React Query
- **UI Components**: Headless UI + Tailwind CSS
- **Data Visualization**: Chart.js
- **Form Handling**: React Hook Form
- **Routing**: React Router v6

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.9+ (for local backend development)
- Zerodha Kite Connect API credentials

### Quick Start with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kite-trading-app.git
   cd kite-trading-app
   ```

2. Copy the example environment files:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Update the environment variables in the `.env` files with your configuration.

4. Start the application:
   ```bash
   docker-compose up --build
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - pgAdmin: http://localhost:5050 (email: admin@example.com, password: admin)

### Local Development Setup

#### Backend

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

3. Set up the database:
   ```bash
   # Run migrations
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🧪 Testing

Run tests with the following commands:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=html
```

## 🛠 Development Tools

- **Code Formatting**: Black, isort
- **Linting**: flake8, mypy
- **Git Hooks**: pre-commit
- **CI/CD**: GitHub Actions

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Zerodha Kite Connect](https://kite.trade/docs/connect/v3/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

## 📧 Contact

For any questions or feedback, please open an issue or contact [your-email@example.com](mailto:your-email@example.com).

## License

This project is licensed under the MIT License - see the LICENSE file for details.