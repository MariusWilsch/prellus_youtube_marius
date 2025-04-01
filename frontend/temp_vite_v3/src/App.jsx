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

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Transcript Automation System</CardTitle>
          <CardDescription>
            Scaffolding with shadcn/ui components
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="mb-4">
            This is a simple example using shadcn/ui components to verify that
            everything is working correctly.
          </p>
          <div className="flex items-center justify-center">
            <Button
              onClick={() => setCount((count) => count + 1)}
              className="mr-2"
            >
              Count: {count}
            </Button>
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
