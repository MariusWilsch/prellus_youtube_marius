import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { useTranscriptManagement } from "../hooks";
import { TranscriptForm } from "./TranscriptForm";
import { PromptEditor } from "./PromptEditor";
import { PromptSaveDialog } from "./PromptSaveDialog";
import { PromptListDialog } from "./PromptListDialog";
import { ModelSelector } from "./ModelSelector";
import { toast } from "sonner";

export function TranscriptPage() {
  const [activeTab, setActiveTab] = useState("basic");
  const management = useTranscriptManagement();

  const handleSubmit = () => {
    const result = management.handleProcessTranscript();
    if (!result.success) {
      toast.error(result.error);
      return;
    }

    toast.success("Processing started successfully!");
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">YouTube Transcript Processor</h1>
      </div>

      <Tabs
        defaultValue="basic"
        value={activeTab}
        onValueChange={setActiveTab}
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="basic">Basic Info</TabsTrigger>
          <TabsTrigger value="prompt">Prompt Configuration</TabsTrigger>
        </TabsList>

        <TabsContent value="basic" className="space-y-4 pt-4">
          <TranscriptForm />

          <div className="flex justify-between mt-6">
            <div>
              <Button
                onClick={handleSubmit}
                disabled={management.isProcessing}
                className="mr-2"
              >
                {management.isProcessing ? "Processing..." : "Process Video"}
              </Button>

              <ModelSelector />
            </div>

            <Button variant="outline" onClick={() => setActiveTab("prompt")}>
              Configure Prompt →
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="prompt" className="space-y-4 pt-4">
          <PromptEditor />

          <div className="flex justify-between mt-6">
            <Button variant="outline" onClick={() => setActiveTab("basic")}>
              ← Back to Basic Info
            </Button>

            <Button onClick={handleSubmit} disabled={management.isProcessing}>
              {management.isProcessing ? "Processing..." : "Process Video"}
            </Button>
          </div>
        </TabsContent>
      </Tabs>

      {management.showSavePrompt && <PromptSaveDialog />}
      {management.showPromptList && <PromptListDialog />}
    </div>
  );
}
