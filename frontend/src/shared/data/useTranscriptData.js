import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { transcriptService } from "@/core/services";
import { toast } from "sonner";

/**
 * Hook for transcript data operations
 * Provides functionality for fetching and processing transcripts
 */
export function useTranscriptData() {
  const queryClient = useQueryClient();

  // Query for storing form state that persists across route changes
  const { data: formState, isLoading: isLoadingFormState } = useQuery({
    queryKey: ["transcript-form-state"],
    queryFn: () => {
      // Return default form state if none exists
      return {
        url: "",
        title: "",
        duration: 30,
        promptName: "",
        promptData: {
          yourRole: "",
          scriptStructure: "",
          toneAndStyle: "",
          retentionAndFlow: "",
          additionalInstructions: "",
        },
      };
    },
    // Keep the data fresh for 24 hours
    staleTime: 1000 * 60 * 60 * 24,
    // Never garbage collect this data during the session
    gcTime: Infinity,
  });

  // Mutation for updating form state
  const updateFormState = useMutation({
    mutationFn: async (newState) => {
      // This is just updating the cache, no actual API call
      return newState;
    },
    onSuccess: (newState) => {
      // Update the cache with the new state
      queryClient.setQueryData(["transcript-form-state"], (oldState) => ({
        ...oldState,
        ...newState,
      }));
    },
  });

  // Query for fetching all transcripts
  const {
    data: transcripts,
    isLoading: isLoadingTranscripts,
    error: transcriptsError,
  } = useQuery({
    queryKey: ["transcripts"],
    queryFn: async () => {
      return await transcriptService.getTranscripts();
    },
  });

  // Mutation for processing a transcript
  const processTranscript = useMutation({
    mutationFn: async (data) => {
      return await transcriptService.processTranscript(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(["transcripts"]);
      toast.success("Transcript processed successfully");
    },
    onError: (error) => {
      toast.error(`Error: ${error.message || "Failed to process transcript"}`);
    },
  });

  // Mutation for processing with a specific model
  const processWithModel = useMutation({
    mutationFn: async (data) => {
      return await transcriptService.processWithModel(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(["transcripts"]);
      toast.success("Transcript processed successfully with selected model");
    },
    onError: (error) => {
      toast.error(
        `Error: ${
          error.message || "Failed to process transcript with selected model"
        }`
      );
    },
  });

  return {
    // Data
    transcripts,
    isLoadingTranscripts,
    transcriptsError,

    // Form state
    formState,
    isLoadingFormState,
    updateFormState: updateFormState.mutate,

    // Operations
    processTranscript: processTranscript.mutate,
    processWithModel: processWithModel.mutate,

    // Operation states
    isProcessing: processTranscript.isPending,
    isProcessingWithModel: processWithModel.isPending,
  };
}
