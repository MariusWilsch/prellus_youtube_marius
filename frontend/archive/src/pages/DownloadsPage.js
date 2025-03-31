import React, { useState, useEffect } from 'react';
import { projectService } from '../services/api';

/**
 * Downloads page for accessing transcripts and audio files
 */
const DownloadsPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [showTranscript, setShowTranscript] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState(null);
  
  // Load all projects when component mounts
  useEffect(() => {
    fetchProjects();
  }, []);
  
  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await projectService.getAllProjects();
      setProjects(data);
      setError('');
    } catch (err) {
      console.error('Error fetching projects:', err);
      setError('Failed to load projects. Please try again later.');
    } finally {
      setLoading(false);
    }
  };
  
  // Load transcript when a project is selected
  const handleViewTranscript = async (project) => {
    try {
      setSelectedProject(project);
      setLoading(true);
      
      const result = await projectService.getTranscript(project.id);
      setTranscript(result.text);
      setShowTranscript(true);
      setError('');
    } catch (err) {
      console.error(`Error fetching transcript for project ${project.id}:`, err);
      setError('Failed to load transcript. Please try again later.');
      setShowTranscript(false);
    } finally {
      setLoading(false);
    }
  };
  
  // Format date for display
  const formatDate = (dateString) => {
    try {
      // If it's already a formatted date string, return it
      if (!dateString || dateString === 'Unknown') return 'Unknown';
      
      // If it's an ISO date, format it
      const date = new Date(dateString);
      if (!isNaN(date.getTime())) {
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
      }
      return dateString;
    } catch (e) {
      return dateString || 'Unknown';
    }
  };
  
  // Format YouTube URL for display
  const formatYoutubeUrl = (url) => {
    if (!url) return '';
    
    // If URL is very long, truncate it for display
    if (url.length > 50) {
      return url.substring(0, 47) + '...';
    }
    return url;
  };
  
  // Download transcript as a text file
  const downloadTranscript = (projectId) => {
    projectService.downloadTranscript(projectId);
  };
  
  // Download audio file
  const downloadAudio = (projectId, filename) => {
    projectService.downloadAudio(projectId, filename);
  };
  
  // Copy transcript to clipboard
  const copyTranscript = () => {
    if (!transcript) return;
    
    navigator.clipboard.writeText(transcript)
      .then(() => {
        alert('Transcript copied to clipboard!');
      })
      .catch(err => {
        console.error('Could not copy text: ', err);
        alert('Failed to copy transcript. Please try manually selecting and copying the text.');
      });
  };
  
  // Show delete confirmation dialog
  const confirmDelete = (project) => {
    setProjectToDelete(project);
    setShowDeleteConfirm(true);
  };
  
  // Delete project
  const handleDeleteProject = async () => {
    if (!projectToDelete) return;
    
    try {
      setLoading(true);
      await projectService.deleteProject(projectToDelete.id);
      
      // If the deleted project is currently shown in transcript view, go back to list
      if (selectedProject && selectedProject.id === projectToDelete.id) {
        setShowTranscript(false);
      }
      
      // Refresh the project list
      fetchProjects();
      
      setShowDeleteConfirm(false);
      setProjectToDelete(null);
    } catch (err) {
      console.error(`Error deleting project ${projectToDelete.id}:`, err);
      setError('Failed to delete project. Please try again later.');
      setShowDeleteConfirm(false);
    }
  };
  
  // Get display name for the project
  const getProjectDisplayName = (project) => {
    // If project has a title, use it; otherwise use the ID
    return project.name || project.id.split('_')[0];
  };
  
  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
      <h1>Downloads</h1>
      
      {loading && !showTranscript && (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          Loading...
        </div>
      )}
      
      {error && (
        <div style={{ 
          padding: '10px',
          backgroundColor: '#ffcccc',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}
      
      {!loading && projects.length === 0 && (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center',
          backgroundColor: '#f9f9f9',
          borderRadius: '4px'
        }}>
          <p>No projects found. Start by processing a YouTube video on the Process Video page.</p>
        </div>
      )}
      
      {showTranscript && selectedProject ? (
        <div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '15px'
          }}>
            <h2>
              {getProjectDisplayName(selectedProject)}
            </h2>
            <div>
              <button
                onClick={() => setShowTranscript(false)}
                style={{
                  backgroundColor: '#f1f1f1',
                  color: '#333',
                  padding: '8px 15px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  marginRight: '10px'
                }}
              >
                Back to List
              </button>
              
              <button
                onClick={copyTranscript}
                style={{
                  backgroundColor: '#2196F3',
                  color: 'white',
                  padding: '8px 15px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  marginRight: '10px'
                }}
              >
                Copy
              </button>
              
              <button
                onClick={() => downloadTranscript(selectedProject.id)}
                style={{
                  backgroundColor: '#4CAF50',
                  color: 'white',
                  padding: '8px 15px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Download
              </button>
            </div>
          </div>
          
          {selectedProject.url && (
            <div style={{ marginBottom: '15px' }}>
              <p>Source: <a href={selectedProject.url} target="_blank" rel="noopener noreferrer">{selectedProject.url}</a></p>
            </div>
          )}
          
          <div style={{
            backgroundColor: 'white',
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '15px',
            maxHeight: '500px',
            overflowY: 'auto',
            whiteSpace: 'pre-wrap',
            fontFamily: 'monospace',
            fontSize: '14px',
            lineHeight: '1.6'
          }}>
            {transcript || 'No transcript content available.'}
          </div>
        </div>
      ) : (
        <div>
          <h2>Available Projects</h2>
          <div style={{ 
            backgroundColor: 'white',
            borderRadius: '4px',
            overflow: 'hidden',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <table style={{ 
              width: '100%',
              borderCollapse: 'collapse'
            }}>
              <thead>
                <tr style={{ backgroundColor: '#f5f5f5' }}>
                  <th style={{ padding: '12px 15px', textAlign: 'left' }}>Title</th>
                  <th style={{ padding: '12px 15px', textAlign: 'left' }}>Date</th>
                  <th style={{ padding: '12px 15px', textAlign: 'center' }}>Files</th>
                  <th style={{ padding: '12px 15px', textAlign: 'center' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project, index) => (
                  <tr 
                    key={project.id}
                    style={{ 
                      borderTop: '1px solid #eee',
                      backgroundColor: index % 2 === 0 ? 'white' : '#fafafa'
                    }}
                  >
                    <td style={{ padding: '12px 15px' }}>
                      <div style={{ fontWeight: 'bold' }}>{getProjectDisplayName(project)}</div>
                      {project.url && (
                        <div style={{ fontSize: '12px', color: '#777', marginTop: '5px' }}>
                          <a 
                            href={project.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            style={{ color: '#2196F3' }}
                          >
                            {formatYoutubeUrl(project.url)}
                          </a>
                        </div>
                      )}
                    </td>
                    <td style={{ padding: '12px 15px' }}>
                      {formatDate(project.date)}
                    </td>
                    <td style={{ padding: '12px 15px', textAlign: 'center' }}>
                      <div>
                        {project.hasTranscript && (
                          <span style={{ 
                            backgroundColor: '#e8f5e9', 
                            color: '#2e7d32',
                            padding: '3px 8px',
                            borderRadius: '12px',
                            fontSize: '12px',
                            fontWeight: 'bold',
                            marginRight: '5px',
                            display: 'inline-block',
                            marginBottom: '5px'
                          }}>
                            Transcript
                          </span>
                        )}
                        
                        {project.audioFiles && project.audioFiles.length > 0 && (
                          <span style={{ 
                            backgroundColor: '#e3f2fd', 
                            color: '#1565c0',
                            padding: '3px 8px',
                            borderRadius: '12px',
                            fontSize: '12px',
                            fontWeight: 'bold',
                            display: 'inline-block'
                          }}>
                            Audio ({project.audioFiles.length})
                          </span>
                        )}
                        
                        {!project.hasTranscript && (!project.audioFiles || project.audioFiles.length === 0) && (
                          <span style={{ 
                            backgroundColor: '#ffebee', 
                            color: '#c62828',
                            padding: '3px 8px',
                            borderRadius: '12px',
                            fontSize: '12px',
                            fontWeight: 'bold'
                          }}>
                            No Files
                          </span>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: '12px 15px', textAlign: 'center' }}>
                      <div style={{ marginBottom: '8px' }}>
                        {project.hasTranscript && (
                          <button
                            onClick={() => handleViewTranscript(project)}
                            style={{
                              backgroundColor: '#4CAF50',
                              color: 'white',
                              padding: '5px 10px',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              marginRight: '5px'
                            }}
                          >
                            View Transcript
                          </button>
                        )}
                        
                        <button
                          onClick={() => confirmDelete(project)}
                          style={{
                            backgroundColor: '#f44336',
                            color: 'white',
                            padding: '5px 10px',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                          }}
                        >
                          Delete
                        </button>
                      </div>
                      
                      {project.audioFiles && project.audioFiles.length > 0 && (
                        <div style={{ marginTop: '8px' }}>
                          {project.audioFiles.map((audioFile) => (
                            <button
                              key={audioFile}
                              onClick={() => downloadAudio(project.id, audioFile)}
                              style={{
                                backgroundColor: '#2196F3',
                                color: 'white',
                                padding: '5px 10px',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                marginTop: '5px',
                                display: 'inline-block',
                                width: '100%',
                                maxWidth: '200px',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap'
                              }}
                              title={audioFile}
                            >
                              Download Audio
                            </button>
                          ))}
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* Delete Confirmation Dialog */}
      {showDeleteConfirm && projectToDelete && (
        <div style={{ 
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0, 
          backgroundColor: 'rgba(0,0,0,0.5)', 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{ 
            backgroundColor: 'white', 
            padding: '20px', 
            borderRadius: '8px',
            width: '400px',
            maxWidth: '90%'
          }}>
            <h3 style={{ marginTop: 0 }}>Delete Project</h3>
            <p>
              Are you sure you want to delete "{getProjectDisplayName(projectToDelete)}"? 
              This action cannot be undone and all associated files will be permanently removed.
            </p>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                style={{
                  backgroundColor: '#f1f1f1',
                  color: '#333',
                  padding: '8px 15px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  marginRight: '10px'
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteProject}
                style={{
                  backgroundColor: '#f44336',
                  color: 'white',
                  padding: '8px 15px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DownloadsPage;