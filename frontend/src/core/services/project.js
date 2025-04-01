import api, { apiRequest } from "./api";

export const projectService = {
  /**
   * Get all projects
   */
  getAllProjects: () => {
    return apiRequest(() => api.get("/projects"));
  },

  /**
   * Get transcript text for a project
   * @param {string} projectId - The ID of the project
   */
  getTranscript: (projectId) => {
    return apiRequest(() => api.get(`/projects/${projectId}/transcript`));
  },

  /**
   * Download transcript file
   * @param {string} projectId - The ID of the project
   */
  downloadTranscript: (projectId) => {
    // Create download link and trigger it
    const downloadUrl = `${api.defaults.baseURL}/projects/${projectId}/transcript/download`;
    window.open(downloadUrl, "_blank");
  },

  /**
   * Download audio file
   * @param {string} projectId - The ID of the project
   * @param {string} filename - The name of the audio file
   */
  downloadAudio: (projectId, filename) => {
    // Create download link and trigger it
    const downloadUrl = `${api.defaults.baseURL}/projects/${projectId}/audio/${filename}`;
    window.open(downloadUrl, "_blank");
  },

  /**
   * Delete a project
   * @param {string} projectId - The ID of the project to delete
   */
  deleteProject: (projectId) => {
    return apiRequest(() => api.delete(`/projects/${projectId}`));
  },
};
