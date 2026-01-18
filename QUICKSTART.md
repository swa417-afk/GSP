# GSP Quick Start Guide

Get up and running with the Glass Substrate Protocol project in under 5 minutes.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- curl and jq (for testing)

## 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/swa417-afk/GSP.git
cd GSP

# Install backend dependencies
npm install

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## 2. Configure Environment

The `.env` file is already configured with defaults:

```env
PORT=4000
DB_PATH=./gsp.sqlite
JWT_SECRET=your-super-secret-key-change-this
APP_NAME=GSP Reference App
ATTESTATION_MODE=simulated
```

⚠️ **Important**: Change `JWT_SECRET` before deploying to production!

## 3. Start Backend Server

```bash
# From project root
npm start
```

The server will start on `http://localhost:4000`

### Verify Backend is Running

```bash
curl http://localhost:4000/health
```

Expected response:
```json
{
  "ok": true,
  "app": "GSP Reference App",
  "time": "2026-01-18T..."
}
```

## 4. Start Frontend Development Server

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

## 5. Test the API

Run the included test script:

```bash
./test_api.sh
```

This will test:
- ✅ Health check
- ✅ User registration
- ✅ User authentication
- ✅ Receipt submission
- ✅ Receipt retrieval
- ✅ Receipt listing

## API Quick Reference

### Health Check
```bash
GET /health
```

### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: { "ok": true, "token": "jwt_token_here" }
```

### Submit GSP Receipt
```bash
POST /api/gsp/submit
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "modelId": "gpt-4",
  "inputHash": "abc123",
  "outputHash": "xyz789",
  "policyId": "policy-001"
}
```

### Get Receipt
```bash
GET /api/gsp/receipt/:id
Authorization: Bearer <your_jwt_token>
```

### List All User Receipts
```bash
GET /api/gsp/receipts
Authorization: Bearer <your_jwt_token>
```

## Project Structure

```
GSP/
├── server.js              # Backend entry point
├── package.json           # Backend dependencies
├── .env                   # Environment configuration
├── test_api.sh           # API test script
├── STATUS.md             # Detailed project status
├── frontend/             # React frontend
│   ├── App.tsx          # Main app component
│   ├── components/      # UI components
│   └── package.json     # Frontend dependencies
└── metadata/            # Protocol files
    ├── Status
    └── *.gsp files
```

## Common Commands

### Backend
```bash
npm start          # Start server
npm install        # Install dependencies
```

### Frontend
```bash
cd frontend
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
```

## Troubleshooting

### Backend won't start
- Check if port 4000 is already in use: `lsof -i :4000`
- Verify dependencies are installed: `npm install`

### Database issues
- The SQLite database is created automatically on first run
- Database file: `./gsp.sqlite`
- To reset: `rm gsp.sqlite` and restart server

### Frontend issues
- Clear node_modules: `rm -rf frontend/node_modules && cd frontend && npm install`
- Clear Vite cache: `rm -rf frontend/.vite`

## Next Steps

1. Review [STATUS.md](./STATUS.md) for comprehensive project status
2. Read the metadata files in `/metadata` for protocol details
3. Explore the codebase and API endpoints
4. Consider addressing the known security vulnerabilities

## Getting Help

- Check the [STATUS.md](./STATUS.md) for known issues
- Review the API test script: `./test_api.sh`
- Consult the repository README: [README.md](./README.md)

## Development Notes

- **Authentication**: JWT tokens expire in 7 days
- **Database**: SQLite, automatically initialized
- **Attestation**: Currently in "simulated" mode
- **CORS**: Enabled for all origins (development only)

---

Happy coding! 🚀
