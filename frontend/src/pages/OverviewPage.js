import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

/**
 * API key management and model selection page
 */
const OverviewPage = () => {
  const navigate = useNavigate();
  const [apiKeys, setApiKeys] = useState({
    openai: '',
    gemini: '',
    anthropic: '',
    deepseek: '',
    qwen: ''
  });
  const [savedKeys, setSavedKeys] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [defaultModel, setDefaultModel] = useState('');

  // Available model options with the latest models
  const modelOptions = [
    // OpenAI Models
    { value: "gpt-4o", label: "OpenAI GPT-4o", provider: "openai" },
    { value: "gpt-4.5-preview", label: "OpenAI GPT-4.5 Preview", provider: "openai" },
    { value: "gpt-4-turbo", label: "OpenAI GPT-4 Turbo", provider: "openai" },
    { value: "gpt-3.5-turbo", label: "OpenAI GPT-3.5 Turbo", provider: "openai" },
    
    // Gemini Models
    { value: "gemini-2.5-pro-exp-03-25", label: "Google Gemini 2.5 Pro Exp", provider: "gemini" },
    { value: "gemini-2.0-flash", label: "Google Gemini 2.0 Flash", provider: "gemini" },
    { value: "gemini-2.0-flash-lite", label: "Google Gemini 2.0 Flash Lite", provider: "gemini" },
    { value: "gemini-1.5-pro", label: "Google Gemini 1.5 Pro", provider: "gemini" },
    { value: "gemini-1.5-flash", label: "Google Gemini 1.5 Flash", provider: "gemini" },
    
    // Anthropic Models
    { value: "claude-3-7-sonnet-20250219", label: "Anthropic Claude 3.7 Sonnet", provider: "anthropic" },
    { value: "claude-3-5-sonnet-20241022", label: "Anthropic Claude 3.5 Sonnet", provider: "anthropic" },
    { value: "claude-3-5-haiku-20241022", label: "Anthropic Claude 3.5 Haiku", provider: "anthropic" },
    { value: "claude-3-opus-20240229", label: "Anthropic Claude 3 Opus", provider: "anthropic" },
    
    // DeepSeek Models
    { value: "deepseek-r1", label: "DeepSeek R1", provider: "deepseek" }
  ];

  useEffect(() => {
    fetchApiKeys();
    fetchDefaultModel();
  }, []);

  const fetchApiKeys = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/config/apikeys');
      const keys = response.data || {};
      
      setSavedKeys(keys);
      
      // Reset the input fields
      setApiKeys({
        openai: '',
        gemini: '',
        anthropic: '',
        deepseek: '',
        qwen: ''
      });
    } catch (err) {
      setError('Failed to fetch API keys. They may not be configured yet.');
      console.error('Error fetching API keys:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDefaultModel = async () => {
    try {
      const response = await api.get('/config/defaultmodel');
      setDefaultModel(response.data.model || '');
      setSelectedModel(response.data.model || '');
    } catch (err) {
      console.error('Error fetching default model:', err);
      // If there's an error, we'll leave the model selection empty
    }
  };

  const handleInputChange = (provider, value) => {
    setApiKeys(prev => ({
      ...prev,
      [provider]: value
    }));
  };

  const saveApiKey = async (provider) => {
    if (!apiKeys[provider] || apiKeys[provider].trim() === '') {
      setError(`Please enter a valid ${provider.toUpperCase()} API key`);
      return;
    }

    setError('');
    setSuccess('');
    
    try {
      await api.post('/config/apikeys', {
        provider,
        key: apiKeys[provider]
      });
      
      // Update saved keys status
      setSavedKeys(prev => ({
        ...prev,
        [provider]: true
      }));
      
      // Clear the input field for security
      setApiKeys(prev => ({
        ...prev,
        [provider]: ''
      }));
      
      setSuccess(`${provider.toUpperCase()} API key saved successfully!`);
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess('');
      }, 3000);
    } catch (err) {
      setError(`Failed to save ${provider.toUpperCase()} API key: ${err.response?.data?.error || err.message}`);
    }
  };

  const deleteApiKey = async (provider) => {
    setError('');
    setSuccess('');
    
    try {
      await api.delete(`/config/apikeys/${provider}`);
      
      // Update saved keys status
      setSavedKeys(prev => {
        const newKeys = {...prev};
        newKeys[provider] = false;
        return newKeys;
      });
      
      setSuccess(`${provider.toUpperCase()} API key deleted successfully!`);
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess('');
      }, 3000);
    } catch (err) {
      setError(`Failed to delete ${provider.toUpperCase()} API key: ${err.response?.data?.error || err.message}`);
    }
  };

  const saveDefaultModel = async () => {
    if (!selectedModel) {
      setError('Please select a model');
      return;
    }

    setError('');
    setSuccess('');
    
    try {
      await api.post('/config/defaultmodel', {
        model: selectedModel
      });
      
      setDefaultModel(selectedModel);
      setSuccess('Default model saved successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess('');
      }, 3000);
    } catch (err) {
      setError(`Failed to save default model: ${err.response?.data?.error || err.message}`);
    }
  };

  // Check if a provider has its API key configured
  const isProviderConfigured = (provider) => {
    return savedKeys[provider] === true;
  };

  // Check if the selected model's provider is configured with an API key
  const isSelectedModelProviderConfigured = () => {
    if (!selectedModel) return false;
    
    const modelInfo = modelOptions.find(model => model.value === selectedModel);
    if (!modelInfo) return false;
    
    return isProviderConfigured(modelInfo.provider);
  };

  // Get recommended models (ones that have API keys configured)
  const getRecommendedModels = () => {
    return modelOptions.filter(model => isProviderConfigured(model.provider));
  };

  if (loading) {
    return <div className="loading">Loading API key configuration...</div>;
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>API Configuration</h1>
        <button 
          onClick={() => navigate('/')}
          style={{
            backgroundColor: '#4CAF50',
            color: 'white',
            padding: '10px 15px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Process New Video
        </button>
      </div>

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

      {success && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#d4edda', 
          color: '#155724',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {success}
        </div>
      )}

      {/* Model Selection Section */}
      <div 
        style={{
          padding: '15px',
          border: '1px solid #ddd',
          borderRadius: '4px',
          marginBottom: '30px',
          backgroundColor: '#f9f9f9'
        }}
      >
        <h2 style={{ margin: '0 0 15px 0' }}>Default Model Selection</h2>
        <p style={{ marginBottom: '15px' }}>
          Select the default AI model to use for processing transcripts. This model will be used unless overridden for a specific task.
        </p>
        
        <div style={{ marginBottom: '15px' }}>
          <label 
            htmlFor="model-select"
            style={{ 
              display: 'block', 
              fontWeight: 'bold',
              marginBottom: '5px'
            }}
          >
            Select Model
            {defaultModel && (
              <span style={{ 
                color: 'green', 
                fontSize: '0.8em',
                marginLeft: '10px'
              }}>
                (Current default: {defaultModel})
              </span>
            )}
          </label>
          
          <select
            id="model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              width: '100%',
              fontSize: '1em',
              marginBottom: '10px'
            }}
          >
            <option value="">-- Select a model --</option>
            {/* Show recommended models first if there are any configured */}
            {getRecommendedModels().length > 0 && (
              <optgroup label="Recommended Models (API Key Configured)">
                {getRecommendedModels().map(model => (
                  <option key={`rec-${model.value}`} value={model.value}>
                    {model.label}
                  </option>
                ))}
              </optgroup>
            )}
            {/* Show all models grouped by provider */}
            <optgroup label="OpenAI Models">
              {modelOptions
                .filter(model => model.provider === 'openai')
                .map(model => (
                  <option 
                    key={model.value} 
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label} {!isProviderConfigured(model.provider) ? '(API key required)' : ''}
                  </option>
                ))}
            </optgroup>
            <optgroup label="Google Gemini Models">
              {modelOptions
                .filter(model => model.provider === 'gemini')
                .map(model => (
                  <option 
                    key={model.value} 
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label} {!isProviderConfigured(model.provider) ? '(API key required)' : ''}
                  </option>
                ))}
            </optgroup>
            <optgroup label="Anthropic Claude Models">
              {modelOptions
                .filter(model => model.provider === 'anthropic')
                .map(model => (
                  <option 
                    key={model.value} 
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label} {!isProviderConfigured(model.provider) ? '(API key required)' : ''}
                  </option>
                ))}
            </optgroup>
            <optgroup label="DeepSeek Models">
              {modelOptions
                .filter(model => model.provider === 'deepseek')
                .map(model => (
                  <option 
                    key={model.value} 
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label} {!isProviderConfigured(model.provider) ? '(API key required)' : ''}
                  </option>
                ))}
            </optgroup>
          </select>
          
          {selectedModel && !isSelectedModelProviderConfigured() && (
            <div style={{ 
              color: '#856404', 
              backgroundColor: '#fff3cd', 
              padding: '8px', 
              borderRadius: '4px', 
              marginBottom: '10px',
              fontSize: '0.9em'
            }}>
              Please configure the API key for this model's provider first.
            </div>
          )}
          
          <button
            onClick={saveDefaultModel}
            disabled={!selectedModel || !isSelectedModelProviderConfigured()}
            style={{
              backgroundColor: '#2196F3',
              color: 'white',
              padding: '8px 15px',
              border: 'none',
              borderRadius: '4px',
              cursor: (!selectedModel || !isSelectedModelProviderConfigured()) ? 'not-allowed' : 'pointer',
              opacity: (!selectedModel || !isSelectedModelProviderConfigured()) ? 0.7 : 1
            }}
          >
            Save Default Model
          </button>
        </div>
      </div>

      <h2 style={{ marginBottom: '15px' }}>API Key Management</h2>
      <div style={{ marginBottom: '30px' }}>
        <p>
          Configure your API keys for various AI services. These keys are required for transcript processing and audio generation.
          The keys will be securely stored in the server's environment variables and .env file.
        </p>
      </div>

      <div>
        {Object.keys(apiKeys).map(provider => (
          <div 
            key={provider}
            style={{
              padding: '15px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              marginBottom: '15px',
              backgroundColor: '#f9f9f9'
            }}
          >
            <div style={{ marginBottom: '10px' }}>
              <label 
                htmlFor={`${provider}-api-key`}
                style={{ 
                  display: 'block', 
                  fontWeight: 'bold',
                  marginBottom: '5px'
                }}
              >
                {provider.toUpperCase()} API Key
                {savedKeys[provider] && (
                  <span style={{ 
                    color: 'green', 
                    fontSize: '0.8em',
                    marginLeft: '10px'
                  }}>
                    (Configured)
                  </span>
                )}
              </label>
              
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  id={`${provider}-api-key`}
                  type="password"
                  placeholder={savedKeys[provider] ? "••••••••••••••••••••••" : `Enter your ${provider.toUpperCase()} API key`}
                  value={apiKeys[provider]}
                  onChange={(e) => handleInputChange(provider, e.target.value)}
                  style={{
                    padding: '8px 12px',
                    borderRadius: '4px',
                    border: '1px solid #ddd',
                    flexGrow: 1,
                    fontSize: '1em'
                  }}
                />
                
                <button
                  onClick={() => saveApiKey(provider)}
                  style={{
                    backgroundColor: '#2196F3',
                    color: 'white',
                    padding: '8px 12px',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Save
                </button>
                
                {savedKeys[provider] && (
                  <button
                    onClick={() => deleteApiKey(provider)}
                    style={{
                      backgroundColor: '#f44336',
                      color: 'white',
                      padding: '8px 12px',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    Delete
                  </button>
                )}
              </div>
            </div>
            
            <div style={{ fontSize: '0.8em', color: '#666' }}>
              {provider === 'openai' && "Required for OpenAI models (GPT-4o, GPT-4.5 Preview, etc.)."}
              {provider === 'gemini' && "Required for Google's Gemini models (Gemini 2.5 Pro, 2.0 Flash, etc.)."}
              {provider === 'anthropic' && "Required for Anthropic's Claude models (Claude 3.7 Sonnet, 3.5 Opus, etc.)."}
              {provider === 'deepseek' && "Required for DeepSeek models (DeepSeek R1, etc.)."}
              {provider === 'qwen' && "Required for Alibaba's Qwen models."}
            </div>
            
            {/* Show available models for this provider */}
            {savedKeys[provider] && (
              <div style={{ marginTop: '10px', fontSize: '0.8em', color: '#666' }}>
                <strong>Available models:</strong> {' '}
                {modelOptions
                  .filter(model => model.provider === provider)
                  .map(model => model.label)
                  .join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default OverviewPage;