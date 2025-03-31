import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Import the page components
import InputPage from './pages/InputPage';
import OverviewPage from './pages/OverviewPage';
import DownloadsPage from './pages/DownloadsPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<InputPage />} />
          <Route path="/overview" element={<OverviewPage />} />
          <Route path="/downloads" element={<DownloadsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;