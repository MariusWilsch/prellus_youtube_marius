import { useState, useMemo } from "react";
import { useConfigData } from "@/shared/data/useConfigData";

/**
 * Management hook for configuration settings
 * Builds on shared data hooks to add feature-specific business logic
 */
export function useConfigManagement() {
  // Feature-specific state
  const [newApiKey, setNewApiKey] = useState({ provider: "", key: "" });
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null);

  // Use the shared data hook
  const {
    apiKeys,
    defaultModel,
    availableModels,
    saveApiKey,
    deleteApiKey,
    saveDefaultModel,
    isSavingApiKey,
    isDeletingApiKey,
    isSavingDefaultModel,
    isLoadingApiKeys,
    isLoadingDefaultModel,
    isLoadingAvailableModels,
  } = useConfigData();

  // Available providers
  const availableProviders = [
    { id: "openai", name: "OpenAI" },
    { id: "gemini", name: "Google Gemini" },
    { id: "anthropic", name: "Anthropic Claude" },
    { id: "deepseek", name: "DeepSeek" },
    { id: "qwen", name: "Qwen" },
  ];

  // Model options with provider grouping
  const modelOptions = useMemo(
    () => [
      // OpenAI Models
      { value: "gpt-4o", label: "OpenAI GPT-4o", provider: "openai" },
      {
        value: "gpt-4.5-preview",
        label: "OpenAI GPT-4.5 Preview",
        provider: "openai",
      },
      { value: "gpt-4-turbo", label: "OpenAI GPT-4 Turbo", provider: "openai" },
      {
        value: "gpt-3.5-turbo",
        label: "OpenAI GPT-3.5 Turbo",
        provider: "openai",
      },

      // Gemini Models
      {
        value: "gemini-2.5-pro-exp-03-25",
        label: "Google Gemini 2.5 Pro Exp",
        provider: "gemini",
      },
      {
        value: "gemini-2.0-flash",
        label: "Google Gemini 2.0 Flash",
        provider: "gemini",
      },
      {
        value: "gemini-2.0-flash-lite",
        label: "Google Gemini 2.0 Flash Lite",
        provider: "gemini",
      },
      {
        value: "gemini-1.5-pro",
        label: "Google Gemini 1.5 Pro",
        provider: "gemini",
      },
      {
        value: "gemini-1.5-flash",
        label: "Google Gemini 1.5 Flash",
        provider: "gemini",
      },

      // Anthropic Models
      {
        value: "claude-3-7-sonnet-20250219",
        label: "Anthropic Claude 3.7 Sonnet",
        provider: "anthropic",
      },
      {
        value: "claude-3-5-sonnet-20241022",
        label: "Anthropic Claude 3.5 Sonnet",
        provider: "anthropic",
      },
      {
        value: "claude-3-5-haiku-20241022",
        label: "Anthropic Claude 3.5 Haiku",
        provider: "anthropic",
      },
      {
        value: "claude-3-opus-20240229",
        label: "Anthropic Claude 3 Opus",
        provider: "anthropic",
      },

      // DeepSeek Models
      { value: "deepseek-r1", label: "DeepSeek R1", provider: "deepseek" },
    ],
    []
  );

  // Check if a provider has an API key configured
  const isProviderConfigured = (providerId) => {
    return (
      (Array.isArray(apiKeys) &&
        apiKeys.some((key) => key.provider === providerId)) ||
      false
    );
  };

  // Get models for a specific provider
  const getModelsForProvider = (providerId) => {
    return modelOptions.filter((model) => model.provider === providerId);
  };

  // Get recommended models (ones that have API keys configured)
  const getRecommendedModels = () => {
    return modelOptions.filter((model) => isProviderConfigured(model.provider));
  };

  // Check if the selected model's provider is configured
  const isSelectedModelProviderConfigured = () => {
    if (!selectedModel) return false;

    const modelInfo = modelOptions.find(
      (model) => model.value === selectedModel
    );
    if (!modelInfo) return false;

    return isProviderConfigured(modelInfo.provider);
  };

  // Handle API key input change
  const handleApiKeyChange = (provider, key) => {
    setNewApiKey({ provider, key });
  };

  // Save API key
  const handleSaveApiKey = (provider) => {
    if (!newApiKey.key || newApiKey.key.trim() === "") {
      return {
        success: false,
        error: `Please enter a valid ${provider.toUpperCase()} API key`,
      };
    }

    saveApiKey({
      provider,
      key: newApiKey.key,
    });

    // Clear the input field for security
    setNewApiKey({ provider: "", key: "" });
    return { success: true, error: null };
  };

  // Delete API key
  const handleDeleteApiKey = (provider) => {
    deleteApiKey(provider);
    return { success: true, error: null };
  };

  // Save default model
  const handleSaveDefaultModel = () => {
    if (!selectedModel) {
      return { success: false, error: "Please select a model" };
    }

    if (!isSelectedModelProviderConfigured()) {
      return {
        success: false,
        error: "Please configure the API key for this model's provider first",
      };
    }

    saveDefaultModel({ model: selectedModel });
    return { success: true, error: null };
  };

  return {
    // Data from shared hook
    apiKeys,
    defaultModel,
    availableModels,

    // Feature-specific state
    newApiKey,
    selectedProvider,
    setSelectedProvider,
    selectedModel,
    setSelectedModel,

    // Feature-specific data
    availableProviders,
    modelOptions,

    // Feature-specific operations
    isProviderConfigured,
    getModelsForProvider,
    getRecommendedModels,
    isSelectedModelProviderConfigured,
    handleApiKeyChange,
    handleSaveApiKey,
    handleDeleteApiKey,
    handleSaveDefaultModel,

    // Loading states
    isLoadingApiKeys,
    isLoadingDefaultModel,
    isLoadingAvailableModels,

    // Operation states
    isSavingApiKey,
    isDeletingApiKey,
    isSavingDefaultModel,
  };
}
