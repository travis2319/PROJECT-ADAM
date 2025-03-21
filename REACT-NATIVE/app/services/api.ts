import axios from 'axios';
import { EmissionsData, HealthMonitoringData, PredictiveMaintenanceData } from '../types/analysis';

// Configure base URL in a central place
const baseURL = 'http://192.168.251.63:8000';

// Create a base axios instance with common configuration
const apiClient = axios.create({
  baseURL,
  auth: {
    username: 'user',
    password: 'password'
  }
});

export const analysisService = {
  fetchEmissionsData: async (): Promise<EmissionsData> => {
    const response = await apiClient.get('/emissions/compliance-and-plot-data');
    return response.data;
  },
  
  fetchHealthMonitoringData: async (): Promise<HealthMonitoringData> => {
    const response = await apiClient.get('/engine-health/diagnose');
    return response.data;
  },
  
  fetchPredictiveMaintenanceData: async (): Promise<PredictiveMaintenanceData> => {
    const response = await apiClient.get('/predictive-maintenance/diagnose');
    return response.data;
  }
};