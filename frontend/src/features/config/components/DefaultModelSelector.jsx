import { useState, useEffect } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useConfigManagement } from "../hooks";
import { toast } from "sonner";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

export function DefaultModelSelector() {
  const {
    defaultModel,
    selectedModel,
    setSelectedModel,
    modelOptions,
    getRecommendedModels,
    isProviderConfigured,
    isSelectedModelProviderConfigured,
    handleSaveDefaultModel,
    isLoadingDefaultModel,
    isSavingDefaultModel,
  } = useConfigManagement();

  const recommendedModels = getRecommendedModels();

  const onSaveDefaultModel = () => {
    const result = handleSaveDefaultModel();
    if (!result.success) {
      toast.error(result.error);
      return;
    }

    toast.success("Default model saved successfully!");
  };

  if (isLoadingDefaultModel) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-32" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label htmlFor="model-select" className="text-sm font-medium">
            Select Model
            {defaultModel && (
              <span className="ml-2 text-sm text-muted-foreground">
                (Current default: {defaultModel?.model})
              </span>
            )}
          </label>
        </div>

        <Select value={selectedModel} onValueChange={setSelectedModel}>
          <SelectTrigger id="model-select" className="w-full">
            <SelectValue placeholder="Select a model" />
          </SelectTrigger>
          <SelectContent>
            {recommendedModels.length > 0 && (
              <SelectGroup>
                <SelectLabel>
                  Recommended Models (API Key Configured)
                </SelectLabel>
                {recommendedModels.map((model) => (
                  <SelectItem key={`rec-${model.value}`} value={model.value}>
                    {model.label}
                  </SelectItem>
                ))}
              </SelectGroup>
            )}

            <SelectGroup>
              <SelectLabel>Google Gemini Models</SelectLabel>
              {modelOptions
                .filter((model) => model.provider === "gemini")
                .map((model) => (
                  <SelectItem
                    key={model.value}
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label}
                    {!isProviderConfigured(model.provider) &&
                      " (API key required)"}
                  </SelectItem>
                ))}
            </SelectGroup>

            <SelectGroup>
              <SelectLabel>Anthropic Claude Models</SelectLabel>
              {modelOptions
                .filter((model) => model.provider === "anthropic")
                .map((model) => (
                  <SelectItem
                    key={model.value}
                    value={model.value}
                    disabled={!isProviderConfigured(model.provider)}
                  >
                    {model.label}
                    {!isProviderConfigured(model.provider) &&
                      " (API key required)"}
                  </SelectItem>
                ))}
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      {selectedModel && !isSelectedModelProviderConfigured() && (
        <Alert
          variant="warning"
          className="bg-amber-50 text-amber-800 border-amber-200"
        >
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Please configure the API key for this model's provider first.
          </AlertDescription>
        </Alert>
      )}

      {selectedModel &&
        isSelectedModelProviderConfigured() &&
        defaultModel?.model === selectedModel && (
          <Alert
            variant="success"
            className="bg-green-50 text-green-800 border-green-200"
          >
            <CheckCircle2 className="h-4 w-4" />
            <AlertDescription>
              This model is already set as the default.
            </AlertDescription>
          </Alert>
        )}

      <Button
        onClick={onSaveDefaultModel}
        disabled={
          !selectedModel ||
          !isSelectedModelProviderConfigured() ||
          isSavingDefaultModel ||
          defaultModel?.model === selectedModel
        }
      >
        {isSavingDefaultModel ? "Saving..." : "Save Default Model"}
      </Button>
    </div>
  );
}
