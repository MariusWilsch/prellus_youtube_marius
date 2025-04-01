import axios from "axios";
import { toast } from "sonner";

// API URL
const API_URL = "http://localhost:5001/api";

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000, // 5 seconds timeout
});

// Helper function to handle API requests with consistent error handling
export const apiRequest = async (requestFn) => {
  try {
    const response = await requestFn();
    return response.data;
  } catch (error) {
    console.error("API error:", error);
    // Use toast from components/ui/sonner for error notifications
    toast.error(`API Error: ${error.response?.data?.message || error.message}`);
    throw error;
  }
};

export default api;
