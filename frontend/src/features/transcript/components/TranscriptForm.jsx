import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useTranscriptManagement } from "../hooks";

export function TranscriptForm() {
  const { url, setUrl, title, setTitle, duration, setDuration, isProcessing } =
    useTranscriptManagement();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Video Information</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="url">YouTube URL</Label>
          <Input
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            disabled={isProcessing}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="title">Title (Optional)</Label>
          <Input
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter a title for this transcript"
            disabled={isProcessing}
          />
          <p className="text-sm text-muted-foreground">
            If left blank, a title will be generated from the video ID
          </p>
        </div>

        <div className="space-y-2">
          <Label htmlFor="duration">Duration (minutes)</Label>
          <Input
            id="duration"
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            max="180"
            disabled={isProcessing}
          />
          <p className="text-sm text-muted-foreground">
            Maximum length of the video to process (up to 180 minutes, leave
            empty for no limit)
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
