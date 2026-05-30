import React, { useState, useEffect } from 'react';
import PredictionForm from './components/PredictionForm';
import RiskDashboard from './components/RiskDashboard';
import { healthCheck } from './services/api';

function App() {
  const [apiStatus, setApiStatus] = useState('checking');
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    healthCheck()
      .then(() => setApiStatus('online'))
      .catch(() => setApiStatus('offline'));
  }, []);

  const addPrediction = (prediction) => {
    setPredictions([prediction, ...predictions.slice(0, 9)]);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">🌡️ Heat Wave Health Risk Predictor</h1>
          <p className="text-sm opacity-90">Sri Lanka Early Warning System</p>
        </div>
      </header>

      <main className="container mx-auto p-4">
        {apiStatus === 'offline' && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            ⚠️ Backend API is not running. Please start the server with: <code className="bg-red-200 px-1 rounded">python -m api.main</code>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6">
          <PredictionForm onPrediction={addPrediction} apiStatus={apiStatus} />
          <RiskDashboard predictions={predictions} />
        </div>
      </main>

      <footer className="bg-gray-800 text-white text-center p-4 mt-8">
        <p>© 2024 Heat Wave Health Risk Prediction - Intern Project</p>
      </footer>
    </div>
  );
}

export default App;