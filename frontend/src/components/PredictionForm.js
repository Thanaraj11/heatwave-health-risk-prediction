import React, { useState } from 'react';
import { predictRisk } from '../services/api';

function PredictionForm({ onPrediction, apiStatus }) {
  const [formData, setFormData] = useState({
    Age: '',
    Systolic_BP: '',
    Diastolic_BP: '',
    Heart_Disease: 0,
    Diabetes: 0,
    Respiratory_Issue: 0,
    Outdoor_Worker: 0,
    Temperature_C: '',
    Humidity_percent: '',
    Gender: 1,
    Hydration_Level: 1
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await predictRisk(formData);
      onPrediction({
        ...formData,
        risk_level: result.risk_level,
        confidence: result.confidence,
        timestamp: new Date().toLocaleString()
      });
      
      // Reset form
      setFormData({
        Age: '',
        Systolic_BP: '',
        Diastolic_BP: '',
        Heart_Disease: 0,
        Diabetes: 0,
        Respiratory_Issue: 0,
        Outdoor_Worker: 0,
        Temperature_C: '',
        Humidity_percent: '',
        Gender: 1,
        Hydration_Level: 1
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Make sure the API is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">📝 Patient Assessment</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Age</label>
            <input
              type="number"
              name="Age"
              value={formData.Age}
              onChange={handleChange}
              required
              className="w-full border rounded p-2"
              placeholder="Years"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Systolic BP</label>
            <input
              type="number"
              name="Systolic_BP"
              value={formData.Systolic_BP}
              onChange={handleChange}
              required
              className="w-full border rounded p-2"
              placeholder="mmHg"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Diastolic BP</label>
            <input
              type="number"
              name="Diastolic_BP"
              value={formData.Diastolic_BP}
              onChange={handleChange}
              required
              className="w-full border rounded p-2"
              placeholder="mmHg"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Temperature (°C)</label>
            <input
              type="number"
              step="0.1"
              name="Temperature_C"
              value={formData.Temperature_C}
              onChange={handleChange}
              required
              className="w-full border rounded p-2"
              placeholder="Celsius"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Humidity (%)</label>
            <input
              type="number"
              step="1"
              name="Humidity_percent"
              value={formData.Humidity_percent}
              onChange={handleChange}
              required
              className="w-full border rounded p-2"
              placeholder="%"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Gender</label>
            <select
              name="Gender"
              value={formData.Gender}
              onChange={handleChange}
              className="w-full border rounded p-2"
            >
              <option value={1}>Male</option>
              <option value={0}>Female</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Hydration Level</label>
            <select
              name="Hydration_Level"
              value={formData.Hydration_Level}
              onChange={handleChange}
              className="w-full border rounded p-2"
            >
              <option value={0}>Low</option>
              <option value={1}>Moderate</option>
              <option value={2}>Good</option>
            </select>
          </div>
          
          <div className="col-span-2">
            <label className="block text-sm font-medium mb-2">Medical Conditions</label>
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="Heart_Disease"
                  checked={formData.Heart_Disease === 1}
                  onChange={handleChange}
                  className="mr-2"
                />
                Heart Disease
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="Diabetes"
                  checked={formData.Diabetes === 1}
                  onChange={handleChange}
                  className="mr-2"
                />
                Diabetes
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="Respiratory_Issue"
                  checked={formData.Respiratory_Issue === 1}
                  onChange={handleChange}
                  className="mr-2"
                />
                Respiratory Issue
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="Outdoor_Worker"
                  checked={formData.Outdoor_Worker === 1}
                  onChange={handleChange}
                  className="mr-2"
                />
                Outdoor Worker
              </label>
            </div>
          </div>
        </div>
        
        {error && (
          <div className="mt-4 bg-red-100 text-red-700 p-2 rounded">
            {error}
          </div>
        )}
        
        <button
          type="submit"
          disabled={loading || apiStatus === 'offline'}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {loading ? 'Predicting...' : 'Predict Risk Level'}
        </button>
      </form>
    </div>
  );
}

export default PredictionForm;