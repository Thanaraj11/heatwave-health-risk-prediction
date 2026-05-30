import React from 'react';

function RiskDashboard({ predictions }) {
  const getRiskColor = (risk) => {
    switch(risk) {
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">📊 Recent Predictions</h2>
      
      {predictions.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          No predictions yet. Submit the form to see results.
        </div>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {predictions.map((pred, idx) => (
            <div key={idx} className={`border rounded p-3 ${getRiskColor(pred.risk_level)}`}>
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-medium">Age: {pred.Age}</span>
                  <span className="text-gray-600 ml-2">
                    BP: {pred.Systolic_BP}/{pred.Diastolic_BP}
                  </span>
                </div>
                <div className="px-3 py-1 rounded-full text-sm font-bold bg-white shadow">
                  {pred.risk_level} Risk
                </div>
              </div>
              <div className="text-sm mt-1">
                Temp: {pred.Temperature_C}°C | Humidity: {pred.Humidity_percent}%
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Confidence: {(pred.confidence * 100).toFixed(1)}% | {pred.timestamp}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RiskDashboard;