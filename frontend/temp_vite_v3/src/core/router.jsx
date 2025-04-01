import { createBrowserRouter } from "react-router-dom";
import { RootLayout, NotFound } from "@/shared/components";

// These will be implemented in future tasks
// Using placeholder components for now
const TranscriptPage = () => <div>Transcript Processing Page</div>;
const ConfigPage = () => <div>Configuration Page</div>;
const DownloadsPage = () => <div>Downloads Page</div>;

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <NotFound />,
    children: [
      {
        index: true,
        element: <TranscriptPage />,
      },
      {
        path: "config",
        element: <ConfigPage />,
      },
      {
        path: "downloads",
        element: <DownloadsPage />,
      },
    ],
  },
]);
