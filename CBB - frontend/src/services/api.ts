import axios from 'axios';

// URL base del backend FastAPI. Todas las rutas del backend
// están montadas bajo el prefijo /api/v1 (ver app/main.py).
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
