import { useState, useEffect } from "react";
import { useTranscriptData } from "@/shared/data/useTranscriptData";
import { usePromptData } from "@/shared/data/usePromptData";
import { extractYoutubeId } from "@/lib/utils";

/**
 * Management hook for transcript processing functionality
 * Builds on shared data hooks to add feature-specific business logic
 */
export function useTranscriptManagement() {
  // Feature-specific state
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [duration, setDuration] = useState(30);
  const [promptName, setPromptName] = useState("");
  const [showSavePrompt, setShowSavePrompt] = useState(false);
  const [showPromptList, setShowPromptList] = useState(false);

  // Structured prompt fields
  const [promptData, setPromptData] = useState({
    yourRole: "",
    scriptStructure: "",
    toneAndStyle: "",
    retentionAndFlow: "",
    additionalInstructions: "",
  });

  // Use the shared data hooks
  const { transcripts, processTranscript, processWithModel, isProcessing } =
    useTranscriptData();

  const { prompts, savePrompt, getPrompt, isSaving } = usePromptData();

  // Auto-populate title when URL changes
  useEffect(() => {
    if (url) {
      const videoId = extractYoutubeId(url);
      if (videoId && !title) {
        setTitle(`YouTube Transcript - ${videoId}`);
      }
    }
  }, [url, title]);

  // Handle changes to prompt fields
  const handlePromptChange = (field, value) => {
    setPromptData({
      ...promptData,
      [field]: value,
    });
  };

  // Reset form
  const resetForm = () => {
    setUrl("");
    setTitle("");
    setDuration(30);
    setPromptData({
      yourRole: "",
      scriptStructure: "",
      toneAndStyle: "",
      retentionAndFlow: "",
      additionalInstructions: "",
    });
  };

  // Validate form
  const validateForm = () => {
    if (!url) {
      return { valid: false, error: "Please enter a YouTube URL" };
    }

    const videoId = extractYoutubeId(url);
    if (!videoId) {
      return { valid: false, error: "Please enter a valid YouTube URL" };
    }

    return { valid: true, error: null };
  };

  // Process transcript
  const handleProcessTranscript = () => {
    const validation = validateForm();
    if (!validation.valid) {
      return { success: false, error: validation.error };
    }

    processTranscript({
      url,
      title,
      promptData,
      duration: parseInt(duration),
    });

    return { success: true, error: null };
  };

  // Process with specific model
  const handleProcessWithModel = (modelId) => {
    const validation = validateForm();
    if (!validation.valid) {
      return { success: false, error: validation.error };
    }

    processWithModel({
      url,
      title,
      promptData,
      duration: parseInt(duration),
      modelId,
    });

    return { success: true, error: null };
  };

  // Save prompt template
  const handleSavePrompt = () => {
    if (!promptName.trim()) {
      return { success: false, error: "Please enter a name for your prompt" };
    }

    savePrompt({
      promptData,
      promptName,
    });

    setShowSavePrompt(false);
    return { success: true, error: null };
  };

  // Load prompt template
  const handleLoadPrompt = async (promptId) => {
    try {
      const result = await getPrompt(promptId).refetch();

      if (result.data && result.data.promptData) {
        setPromptData(result.data.promptData);
        return { success: true, error: null };
      } else {
        return { success: false, error: "Failed to load prompt data" };
      }
    } catch (error) {
      return { success: false, error: "Failed to load prompt" };
    } finally {
      setShowPromptList(false);
    }
  };

  return {
    // Form state
    url,
    setUrl,
    title,
    setTitle,
    duration,
    setDuration,
    promptData,
    handlePromptChange,

    // Prompt management
    promptName,
    setPromptName,
    showSavePrompt,
    setShowSavePrompt,
    showPromptList,
    setShowPromptList,
    prompts,

    // Operations
    handleProcessTranscript,
    handleProcessWithModel,
    handleSavePrompt,
    handleLoadPrompt,
    resetForm,
    validateForm,

    // Operation states
    isProcessing,
    isSaving,
  };
}
