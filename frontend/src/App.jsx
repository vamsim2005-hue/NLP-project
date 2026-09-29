import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Sentiment from './pages/Sentiment';
import Spam from './pages/Spam';
import FakeNews from './pages/FakeNews';
import Toxicity from './pages/Toxicity';
import ModelPerformance from './pages/ModelPerformance';

export default function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
        {/* Navigation Sidebar */}
        <Sidebar />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <Navbar />

          <main className="flex-1 overflow-y-auto p-6 md:p-8 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/sentiment" element={<Sentiment />} />
              <Route path="/spam" element={<Spam />} />
              <Route path="/fake-news" element={<FakeNews />} />
              <Route path="/toxicity" element={<Toxicity />} />
              <Route path="/performance" element={<ModelPerformance />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}
