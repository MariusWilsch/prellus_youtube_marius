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

function App() {
  const [count, setCount] = useState(0);

  // Use the config data hook
  const {
    apiKeys,
    isLoadingApiKeys,
    apiKeysError,
    saveApiKey,
    deleteApiKey,
    isSavingApiKey,
    isDeletingApiKey,
  } = useConfigData();

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
            <div className="flex items-center justify-center">
              <Button
                onClick={() => setCount((count) => count + 1)}
                className="mr-2"
              >
                Count: {count}
              </Button>
            </div>

            <div className="flex items-center justify-center">
              <Button onClick={testUtils} className="mr-2">
                Test Utils
              </Button>
              <Button
                onClick={() => toast.success("This is a test notification!")}
                className="mr-2"
              >
                Test Toast
              </Button>
            </div>

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
                  API Keys fetched successfully! Check console for details.
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
