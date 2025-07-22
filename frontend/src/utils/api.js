import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (userData) => api.put('/auth/profile/update/', userData),
  getDoctors: (params) => api.get('/auth/doctors/', { params }),
  getDoctorDetail: (doctorId) => api.get(`/auth/doctors/${doctorId}/`),
};

// Diagnosis API calls
export const diagnosisAPI = {
  getSymptoms: () => api.get('/diagnosis/symptoms/'),
  predictDisease: (data) => api.post('/diagnosis/predict/', data),
  getHistory: (params) => api.get('/diagnosis/history/', { params }),
  getAnalytics: () => api.get('/diagnosis/analytics/'),
  getDiagnosisDetail: (diagnosisId) => api.get(`/diagnosis/history/${diagnosisId}/`),
};

// Appointments API calls
export const appointmentsAPI = {
  bookAppointment: (data) => api.post('/appointments/book/', data),
  getUserAppointments: (params) => api.get('/appointments/my-appointments/', { params }),
  getAppointmentDetail: (appointmentId) => api.get(`/appointments/${appointmentId}/`),
  updateAppointment: (appointmentId, data) => api.put(`/appointments/${appointmentId}/update/`, data),
  cancelAppointment: (appointmentId) => api.delete(`/appointments/${appointmentId}/cancel/`),
  getDoctorAvailability: (doctorId) => api.get(`/appointments/doctor/${doctorId}/availability/`),
  getAvailableSlots: (doctorId, date) => api.get(`/appointments/doctor/${doctorId}/slots/`, { params: { date } }),
  createReview: (appointmentId, data) => api.post(`/appointments/${appointmentId}/review/`, data),
  getDoctorReviews: (doctorId, params) => api.get(`/appointments/doctor/${doctorId}/reviews/`, { params }),
};

// Reports API calls
export const reportsAPI = {
  uploadReport: (formData) => api.post('/reports/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserReports: (params) => api.get('/reports/my-reports/', { params }),
  getReportDetail: (reportId) => api.get(`/reports/${reportId}/`),
  updateReport: (reportId, formData) => api.put(`/reports/${reportId}/update/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteReport: (reportId) => api.delete(`/reports/${reportId}/delete/`),
  getReportTypes: () => api.get('/reports/types/'),
  getReportsAnalytics: () => api.get('/reports/analytics/'),
};

export default api;

