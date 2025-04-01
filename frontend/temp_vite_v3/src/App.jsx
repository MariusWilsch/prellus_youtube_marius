import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Toaster } from "@/components/ui/sonner";
import { toast } from "sonner";
import { extractYoutubeId, formatDate } from "@/lib/utils";
import { useConfigData } from "@/shared/data";
import { useTranscriptManagement } from "@/features/transcript";
import { useConfigManagement } from "@/features/config";
import { useProjectManagement } from "@/features/downloads";

function App() {
  const [count, setCount] = useState(0);
  const [activeTab, setActiveTab] = useState("transcript"); // transcript, config, project

  // Use the config data hook
  const { apiKeys, isLoadingApiKeys, apiKeysError } = useConfigData();

  // Use the management hooks
  const transcriptManagement = useTranscriptManagement();
  const configManagement = useConfigManagement();
  const projectManagement = useProjectManagement();

  // Test utility functions
  const testUtils = () => {
    const youtubeId = extractYoutubeId(
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    );
    const formattedDate = formatDate(new Date().toISOString());
    console.log("YouTube ID:", youtubeId);
    console.log("Formatted Date:", formattedDate);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <Toaster />
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Transcript Automation System</CardTitle>
          <CardDescription>Testing data hooks with React Query</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="mb-4">
            This example demonstrates that the shared data hooks are working
            correctly. We're using the useConfigData hook to fetch API keys.
          </p>

          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-center mb-4">
              <Button
                onClick={() => setActiveTab("transcript")}
                variant={activeTab === "transcript" ? "default" : "outline"}
                className="mr-2"
              >
                Transcript
              </Button>
              <Button
                onClick={() => setActiveTab("config")}
                variant={activeTab === "config" ? "default" : "outline"}
                className="mr-2"
              >
                Config
              </Button>
              <Button
                onClick={() => setActiveTab("project")}
                variant={activeTab === "project" ? "default" : "outline"}
              >
                Project
              </Button>
            </div>

            {activeTab === "transcript" && (
              <div className="p-3 bg-green-100 text-green-800 rounded-md">
                <h3 className="text-lg font-medium mb-2">
                  Transcript Management Hook:
                </h3>
                <p>URL: {transcriptManagement.url || "Not set"}</p>
                <p>Title: {transcriptManagement.title || "Not set"}</p>
                <p>Duration: {transcriptManagement.duration} minutes</p>
                <p>
                  Is Processing:{" "}
                  {transcriptManagement.isProcessing ? "Yes" : "No"}
                </p>
                <Button
                  onClick={() => {
                    transcriptManagement.setUrl(
                      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    );
                    toast.success("URL set successfully!");
                  }}
                  className="mt-2"
                  size="sm"
                >
                  Set Test URL
                </Button>
              </div>
            )}

            {activeTab === "config" && (
              <div className="p-3 bg-blue-100 text-blue-800 rounded-md">
                <h3 className="text-lg font-medium mb-2">
                  Config Management Hook:
                </h3>
                <p>
                  Default Model: {configManagement.defaultModel || "Not set"}
                </p>
                <p>
                  Selected Model:{" "}
                  {configManagement.selectedModel || "Not selected"}
                </p>
                <p>API Keys Configured: {apiKeys ? apiKeys.length : 0}</p>
                <Button
                  onClick={() => {
                    configManagement.setSelectedModel("gpt-4o");
                    toast.success("Model selected!");
                  }}
                  className="mt-2"
                  size="sm"
                >
                  Select GPT-4o
                </Button>
              </div>
            )}

            {activeTab === "project" && (
              <div className="p-3 bg-purple-100 text-purple-800 rounded-md">
                <h3 className="text-lg font-medium mb-2">
                  Project Management Hook:
                </h3>
                <p>
                  Projects:{" "}
                  {projectManagement.projects
                    ? projectManagement.projects.length
                    : 0}
                </p>
                <p>
                  Selected Project:{" "}
                  {projectManagement.selectedProject
                    ? projectManagement.getProjectDisplayName(
                        projectManagement.selectedProject
                      )
                    : "None"}
                </p>
                <p>
                  Show Transcript:{" "}
                  {projectManagement.showTranscript ? "Yes" : "No"}
                </p>
                <Button
                  onClick={() => {
                    toast.success("Project management functions are working!");
                  }}
                  className="mt-2"
                  size="sm"
                >
                  Test Project Functions
                </Button>
              </div>
            )}

            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">API Keys Status:</h3>
              {isLoadingApiKeys ? (
                <div className="p-3 bg-blue-100 text-blue-800 rounded-md">
                  Loading API keys...
                </div>
              ) : apiKeysError ? (
                <div className="p-3 bg-red-100 text-red-800 rounded-md">
                  Error:{" "}
                  {apiKeysError.message ||
                    "Failed to fetch API keys. Backend might not be running."}
                </div>
              ) : (
                <div className="p-3 bg-green-100 text-green-800 rounded-md">
                  API Keys fetched successfully!
                  {apiKeys && (
                    <pre className="mt-2 text-xs overflow-auto max-h-40">
                      {JSON.stringify(apiKeys, null, 2)}
                    </pre>
                  )}
                </div>
              )}
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline">Cancel</Button>
          <Button>Submit</Button>
        </CardFooter>
      </Card>
    </div>
  );
}

export default App;
