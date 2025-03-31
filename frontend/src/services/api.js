import axios from 'axios';

// API URL
const API_URL = 'http://localhost:5001/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000 // 5 seconds timeout
});

/**
 * Service for transcript-related API calls
 */
export const transcriptService = {
  /**
   * Process a YouTube video to extract transcript
   */
  processTranscript: async (data) => {
    console.log('Sending data to API:', data);
    try {
      const response = await api.post('/transcripts/process', data);
      console.log('API response:', response.data);
      return response.data;
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  },

  /**
   * Fetch a list of processed transcripts
   */
  getTranscripts: async () => {
    try {
      const response = await api.get('/transcripts');
      return response.data;
    } catch (error) {
      console.error('Error fetching transcripts:', error);
      throw error;
    }
  },
  
  /**
   * Process a YouTube video with a specific model
   */
  processWithModel: async (data) => {
    console.log('Processing with specific model:', data);
    try {
      const response = await api.post('/transcripts/process/model', data);
      console.log('API response:', response.data);
      return response.data;
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  }
};

/**
 * Service for audio-related API calls
 */
export const audioService = {
  /**
   * Generate audio from a transcript
   */
  generateAudio: async (transcriptId) => {
    try {
      const response = await api.post(`/audio/generate/${transcriptId}`);
      return response.data;
    } catch (error) {
      console.error('Error generating audio:', error);
      throw error;
    }
  }
};

/**
 * Service for prompt-related API calls
 */
export const promptService = {
  /**
   * Save a prompt to storage
   * @param {Object} data - Contains promptData and promptName
   */
  savePrompt: async (data) => {
    try {
      console.log('Saving prompt:', data);
      const response = await api.post('/prompts/save', data);
      return response.data;
    } catch (error) {
      console.error('Error saving prompt:', error);
      throw error;
    }
  },
  
  /**
   * Get all saved prompts
   */
  getAllPrompts: async () => {
    try {
      const response = await api.get('/prompts');
      return response.data;
    } catch (error) {
      console.error('Error fetching prompts:', error);
      throw error;
    }
  },
  
  /**
   * Get a specific prompt by ID
   * @param {string} promptId - The unique identifier of the prompt
   */
  getPrompt: async (promptId) => {
    try {
      const response = await api.get(`/prompts/${promptId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching prompt ${promptId}:`, error);
      throw error;
    }
  },
  
  /**
   * Delete a specific prompt by ID
   * @param {string} promptId - The unique identifier of the prompt to delete
   */
  deletePrompt: async (promptId) => {
    try {
      const response = await api.delete(`/prompts/${promptId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting prompt ${promptId}:`, error);
      throw error;
    }
  }
};

/**
 * Service for project management API calls
 */
export const projectService = {
  /**
   * Get all projects
   */
  getAllProjects: async () => {
    try {
      const response = await api.get('/projects');
      return response.data;
    } catch (error) {
      console.error('Error fetching projects:', error);
      throw error;
    }
  },
  
  /**
   * Get transcript text for a project
   * @param {string} projectId - The ID of the project
   */
  getTranscript: async (projectId) => {
    try {
      const response = await api.get(`/projects/${projectId}/transcript`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching transcript for project ${projectId}:`, error);
      throw error;
    }
  },
  
  /**
   * Download transcript file
   * @param {string} projectId - The ID of the project
   */
  downloadTranscript: (projectId) => {
    // Create download link and trigger it
    const downloadUrl = `${API_URL}/projects/${projectId}/transcript/download`;
    window.open(downloadUrl, '_blank');
  },
  
  /**
   * Download audio file
   * @param {string} projectId - The ID of the project
   * @param {string} filename - The name of the audio file
   */
  downloadAudio: (projectId, filename) => {
    // Create download link and trigger it
    const downloadUrl = `${API_URL}/projects/${projectId}/audio/${filename}`;
    window.open(downloadUrl, '_blank');
  },
  
  /**
   * Delete a project
   * @param {string} projectId - The ID of the project to delete
   */
  deleteProject: async (projectId) => {
    try {
      const response = await api.delete(`/projects/${projectId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting project ${projectId}:`, error);
      throw error;
    }
  }
};

/**
 * Service for configuration management API calls
 */
export const configService = {
  /**
   * Get configuration of API keys (which ones are set)
   */
  getApiKeys: async () => {
    try {
      const response = await api.get('/config/apikeys');
      return response.data;
    } catch (error) {
      console.error('Error fetching API keys configuration:', error);
      throw error;
    }
  },
  
  /**
   * Save an API key for a specific service
   * @param {Object} data - Contains provider and key
   */
  saveApiKey: async (data) => {
    try {
      const response = await api.post('/config/apikeys', data);
      return response.data;
    } catch (error) {
      console.error('Error saving API key:', error);
      throw error;
    }
  },
  
  /**
   * Delete an API key for a specific service
   * @param {string} provider - The service provider (openai, gemini, etc.)
   */
  deleteApiKey: async (provider) => {
    try {
      const response = await api.delete(`/config/apikeys/${provider}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting API key for ${provider}:`, error);
      throw error;
    }
  },
  
  /**
   * Get the current default model
   */
  getDefaultModel: async () => {
    try {
      const response = await api.get('/config/defaultmodel');
      return response.data;
    } catch (error) {
      console.error('Error fetching default model:', error);
      throw error;
    }
  },
  
  /**
   * Save the default model
   * @param {Object} data - Contains model name
   */
  saveDefaultModel: async (data) => {
    try {
      const response = await api.post('/config/defaultmodel', data);
      return response.data;
    } catch (error) {
      console.error('Error saving default model:', error);
      throw error;
    }
  },
  
  /**
   * Get all available models with availability status
   */
  getAvailableModels: async () => {
    try {
      const response = await api.get('/config/models');
      return response.data;
    } catch (error) {
      console.error('Error fetching available models:', error);
      throw error;
    }
  }
};

export default api;