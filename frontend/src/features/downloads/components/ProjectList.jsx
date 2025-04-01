import { useProjectManagement } from "../hooks";
import { ProjectCard } from "./ProjectCard";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

export function ProjectList() {
  const { projects, isLoadingProjects, showTranscript } =
    useProjectManagement();

  if (isLoadingProjects) {
    return null; // Loading state is handled by the parent component
  }

  if (!projects || projects.length === 0) {
    return (
      <Alert className="bg-muted">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No projects found. Start by processing a YouTube video on the Process
          Video page.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div
      className={`grid gap-4 ${
        showTranscript ? "" : "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
      }`}
    >
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}
