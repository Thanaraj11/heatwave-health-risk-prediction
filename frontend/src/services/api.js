import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export const predictRisk = async (patientData) => {
  // Convert string values to numbers
  const processedData = {};
  for (const [key, value] of Object.entries(patientData)) {
    if (value === '') {
      throw new Error(`Missing value for ${key}`);
    }
    processedData[key] = typeof value === 'string' ? parseFloat(value) : value;
  }
  
  const response = await api.post('/predict', processedData);
  return response.data;
};