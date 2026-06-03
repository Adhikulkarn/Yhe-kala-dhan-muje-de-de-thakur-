# Yhe-kala-dhan-muje-de-de-thakur💰😏

## Anti-Money Laundering (AML) Detection System

A hybrid graph intelligence platform for detecting money laundering circles in blockchain and banking transaction networks.

### 🎯 Mission

Detect and flag suspicious financial patterns including:
- **Smurfing Networks**: Fund splitting across multiple wallets to avoid thresholds
- **Peeling Chains**: Sequential value forwarding with minimal reduction
- **Mule Accounts**: Temporary pass-through intermediaries
- **Money Funneling**: Convergence of funds to collection points
- **Aggregation Rings**: Coordinated incoming transactions

### 🏗️ Architecture

```
Frontend (React + D3.js)  →  Backend (Django REST API)  →  Analysis Pipeline
  Graph Visualization       Risk Scoring & Patterns      Feature Extraction
  Risk Dashboard            Result Caching               ML Detection
```

### 🚀 Key Features

- **Dual AML Modes**: Crypto and Banking transaction analysis
- **Hybrid Detection**: Rule-based patterns + ML models
- **Graph Visualization**: Interactive D3.js network exploration
- **Real-time Analysis**: Fast graph processing for large datasets
- **REST API**: Scalable backend for integration

### 📊 Supported Data Formats

**Crypto Transactions:**
```
Source_Wallet_ID, Dest_Wallet_ID, Timestamp, Amount, Token_Type
```

**Banking Transactions:**
```
src_id, dst_id, amount
```

### 🔐 Security

- Environment-based configuration
- CORS restriction to whitelisted origins
- Input validation on all endpoints
- Request size limits
- Secure Django settings (non-production defaults)

### 🚀 Quick Start

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python server/manage.py runserver

# Frontend
cd frontend && npm install && npm run dev
```

See [SETUP.md](SETUP.md) for detailed instructions.

### 📈 Results

Analyzes transaction graphs to output:
- Risk scores per entity (0.0 - 1.0 scale)
- Detected suspicious patterns with reasoning
- Network visualization with risk coloring
- Exportable risk assessments

### 📚 Documentation

- [SETUP.md](SETUP.md) - Installation and deployment guide
- [Backend API Docs](backend/README.md) - API endpoints
- [Architecture Overview](docs/architecture.md) - System design

### 🤝 Contributing

Improvements welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

### 📄 License

[Add your license here]

---

**"Yeh Kala Dhan Mujhe De De Thakur!"** 💸
*The hidden money demands to be found!*
