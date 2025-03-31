import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { transcriptService, promptService } from '../services/api';
import { extractYoutubeId, formatDate } from '../utils';

/**
 * Enhanced input page with structured prompt fields for YouTube transcript processing
 */
const InputPage = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState(''); // New state for the title
  const [duration, setDuration] = useState(30);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [showSavePrompt, setShowSavePrompt] = useState(false);
  const [promptName, setPromptName] = useState('');
  const [savedPrompts, setSavedPrompts] = useState([]);
  const [showPromptList, setShowPromptList] = useState(false);
  
  // Structured prompt fields
  const [promptData, setPromptData] = useState({
    yourRole: '',
    scriptStructure: '',
    toneAndStyle: '',
    retentionAndFlow: '',
    additionalInstructions: ''
  });

  // Load saved prompts when component mounts
  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        const prompts = await promptService.getAllPrompts();
        setSavedPrompts(prompts);
      } catch (error) {
        console.error('Error fetching prompts:', error);
        setMessage('Error fetching saved prompts');
      }
    };
    
    fetchPrompts();
  }, []);

  // Auto-populate title when URL changes
  useEffect(() => {
    if (url) {
      const videoId = extractYoutubeId(url);
      if (videoId && !title) {
        // If we have a valid URL and no title yet, set a default title
        setTitle(`YouTube Transcript - ${videoId}`);
      }
    }
  }, [url, title]);

  // Handle changes to prompt fields
  const handlePromptChange = (field, value) => {
    setPromptData({
      ...promptData,
      [field]: value
    });
  };
  
  // Save the current prompt
  const handleSavePrompt = async () => {
    if (!promptName.trim()) {
      setMessage('Error: Please enter a name for your prompt');
      return;
    }
    
    try {
      setLoading(true);
      await promptService.savePrompt({
        promptData,
        promptName
      });
      
      // Refresh the prompts list
      const prompts = await promptService.getAllPrompts();
      setSavedPrompts(prompts);
      
      setMessage('Success: Prompt saved successfully');
      setShowSavePrompt(false);
      setPromptName('');
    } catch (error) {
      console.error('Error saving prompt:', error);
      setMessage('Error: Failed to save prompt');
    } finally {
      setLoading(false);
    }
  };
  
  // Load a saved prompt
  const handleLoadPrompt = async (promptId) => {
    try {
      setLoading(true);
      const result = await promptService.getPrompt(promptId);
      
      if (result && result.promptData) {
        setPromptData(result.promptData);
        setMessage(`Success: Loaded prompt "${result.metaData.prompt_name}"`);
      } else {
        setMessage('Error: Failed to load prompt data');
      }
      
      setShowPromptList(false);
    } catch (error) {
      console.error('Error loading prompt:', error);
      setMessage('Error: Failed to load prompt');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) {
      setMessage('Error: Please enter a YouTube URL');
      return;
    }
    
    // Simple validation for YouTube URL
    const videoId = extractYoutubeId(url);
    if (!videoId) {
      setMessage('Error: Please enter a valid YouTube URL');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Combine all prompt fields into a structured format
      const structuredPrompt = {
        yourRole: promptData.yourRole,
        scriptStructure: promptData.scriptStructure,
        toneAndStyle: promptData.toneAndStyle,
        retentionAndFlow: promptData.retentionAndFlow,
        additionalInstructions: promptData.additionalInstructions
      };

      // Make API call to process the transcript, now including the title
      const response = await transcriptService.processTranscript({
        url,
        title, // Include the title in the API call
        promptData: structuredPrompt,
        duration: parseInt(duration)
      });
      
      console.log('Successfully processed:', response);
      setMessage('Success! Processing started.');
      
      // Wait 1.5 seconds before redirecting to show the success message
      setTimeout(() => {
        navigate('/overview');
      }, 1500);
    } catch (err) {
      console.error('Error processing transcript:', err);
      setMessage('Error: ' + (err.message || 'Failed to process URL'));
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>YouTube Transcript Processor</h1>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            YouTube URL:
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px' 
              }}
              placeholder="https://www.youtube.com/watch?v=..."
              disabled={loading}
            />
          </label>
        </div>

        {/* Title Field - New */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Title:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px' 
              }}
              placeholder="Enter a title for this transcript"
              disabled={loading}
            />
          </label>
        </div>

        {/* Your Role Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Your Role:
            <textarea
              value={promptData.yourRole}
              onChange={(e) => handlePromptChange('yourRole', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                minHeight: '80px'
              }}
              placeholder="Define the role for the script writer (e.g., 'You are a professional scriptwriter...')"
              disabled={loading}
            />
          </label>
        </div>

        {/* Script Structure Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Script Structure:
            <textarea
              value={promptData.scriptStructure}
              onChange={(e) => handlePromptChange('scriptStructure', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                minHeight: '80px'
              }}
              placeholder="Describe how the script should be structured (intro, main sections, conclusion, etc.)"
              disabled={loading}
            />
          </label>
        </div>

        {/* Tone & Style Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Tone & Style:
            <textarea
              value={promptData.toneAndStyle}
              onChange={(e) => handlePromptChange('toneAndStyle', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                minHeight: '80px'
              }}
              placeholder="Specify the desired tone and stylistic elements for the script"
              disabled={loading}
            />
          </label>
        </div>

        {/* Retention & Flow Techniques Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Retention & Flow Techniques:
            <textarea
              value={promptData.retentionAndFlow}
              onChange={(e) => handlePromptChange('retentionAndFlow', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                minHeight: '80px'
              }}
              placeholder="Describe techniques to maintain viewer engagement and smooth flow"
              disabled={loading}
            />
          </label>
        </div>

        {/* Additional Instructions Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Additional Instructions:
            <textarea
              value={promptData.additionalInstructions}
              onChange={(e) => handlePromptChange('additionalInstructions', e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                minHeight: '80px'
              }}
              placeholder="Any other specific requirements or instructions"
              disabled={loading}
            />
          </label>
        </div>

        {/* Duration Field */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            Duration (minutes):
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px' 
              }}
              min="1"
              disabled={loading}
            />
          </label>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <div>
            <button
              type="submit"
              disabled={loading}
              style={{
                backgroundColor: '#4CAF50',
                color: 'white',
                padding: '10px 15px',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1,
                marginRight: '10px'
              }}
            >
              {loading ? 'Processing...' : 'Process Video'}
            </button>
            
            <button
              type="button"
              onClick={() => navigate('/overview')}
              style={{
                backgroundColor: '#f1f1f1',
                color: '#333',
                padding: '10px 15px',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              View Overview
            </button>
          </div>
          
          <div>
            <button
              type="button"
              onClick={() => setShowSavePrompt(true)}
              disabled={loading}
              style={{
                backgroundColor: '#2196F3',
                color: 'white',
                padding: '10px 15px',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                marginRight: '10px'
              }}
            >
              Save Prompt
            </button>
            
            <button
              type="button"
              onClick={() => setShowPromptList(true)}
              disabled={loading}
              style={{
                backgroundColor: '#ff9800',
                color: 'white',
                padding: '10px 15px',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              Load Prompt
            </button>
          </div>
        </div>
        
        {/* Save Prompt Dialog */}
        {showSavePrompt && (
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
              width: '400px'
            }}>
              <h3 style={{ marginTop: 0 }}>Save Prompt</h3>
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px' }}>
                  Prompt Name:
                  <input
                    type="text"
                    value={promptName}
                    onChange={(e) => setPromptName(e.target.value)}
                    style={{ 
                      width: '100%', 
                      padding: '8px',
                      border: '1px solid #ccc',
                      borderRadius: '4px' 
                    }}
                    placeholder="Enter a name for this prompt"
                  />
                </label>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => setShowSavePrompt(false)}
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
                  type="button"
                  onClick={handleSavePrompt}
                  style={{
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    padding: '8px 15px',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Load Prompt Dialog */}
        {showPromptList && (
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
              width: '500px',
              maxHeight: '80vh',
              overflow: 'auto'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                <h3 style={{ margin: 0 }}>Saved Prompts</h3>
                <button
                  type="button"
                  onClick={() => setShowPromptList(false)}
                  style={{
                    backgroundColor: 'transparent',
                    border: 'none',
                    fontSize: '18px',
                    cursor: 'pointer'
                  }}
                >
                  ×
                </button>
              </div>
              
              {savedPrompts.length === 0 ? (
                <p>No saved prompts found.</p>
              ) : (
                <div>
                  {savedPrompts.map((prompt) => (
                    <div
                      key={prompt.unique_id}
                      style={{
                        padding: '10px',
                        borderBottom: '1px solid #eee',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}
                      onClick={() => handleLoadPrompt(prompt.unique_id)}
                    >
                      <div>
                        <div style={{ fontWeight: 'bold' }}>{prompt.prompt_name}</div>
                        <div style={{ fontSize: '12px', color: '#777' }}>
                          {formatDate(prompt.date)}
                        </div>
                      </div>
                      <button
                        style={{
                          backgroundColor: '#2196F3',
                          color: 'white',
                          padding: '5px 10px',
                          border: 'none',
                          borderRadius: '4px'
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleLoadPrompt(prompt.unique_id);
                        }}
                      >
                        Load
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </form>


      {message && (
        <div 
          style={{ 
            marginTop: '20px', 
            padding: '10px', 
            backgroundColor: message.startsWith('Error') ? '#ffcccc' : '#ccffcc',
            borderRadius: '4px'
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
};

export default InputPage;