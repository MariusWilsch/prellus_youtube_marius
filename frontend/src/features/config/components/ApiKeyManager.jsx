import { useConfigManagement } from "../hooks";
import { ProviderCard } from "./ProviderCard";

export function ApiKeyManager() {
  const { availableProviders } = useConfigManagement();

  const getProviderDescription = (provider) => {
    switch (provider) {
      case "gemini":
        return "Required for Google's Gemini models (Gemini 2.5 Pro, 2.0 Flash, etc.).";
      case "anthropic":
        return "Required for Anthropic's Claude models (Claude 3.7 Sonnet, 3.5 Haiku, etc.).";
      default:
        return "API key for AI service provider.";
    }
  };

  const getProviderDisplayName = (provider) => {
    switch (provider) {
      case "gemini":
        return "Google Gemini";
      case "anthropic":
        return "Anthropic Claude";
      default:
        return provider.toUpperCase();
    }
  };

  return (
    <div className="space-y-4">
      {availableProviders.map((provider) => (
        <ProviderCard
          key={provider.id}
          provider={provider.id}
          displayName={provider.name || getProviderDisplayName(provider.id)}
          description={getProviderDescription(provider.id)}
        />
      ))}
    </div>
  );
}
