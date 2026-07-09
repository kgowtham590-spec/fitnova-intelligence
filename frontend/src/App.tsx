import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import SalesDirectorDashboard from './pages/SalesDirectorDashboard';
import TeamLeaderDashboard from './pages/TeamLeaderDashboard';
import AdvisorDashboard from './pages/AdvisorDashboard';
import CallDetail from './pages/CallDetail';
import Appeals from './pages/Appeals';
import Analytics from './pages/Analytics';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0f172a] text-slate-100 flex">
        <Sidebar />
        <div className="flex-1 ml-64 p-8">
          <Routes>
            <Route path="/director" element={<SalesDirectorDashboard />} />
            <Route path="/team-leader" element={<TeamLeaderDashboard />} />
            <Route path="/advisor" element={<AdvisorDashboard />} />
            <Route path="/calls/:id" element={<CallDetail />} />
            <Route path="/appeals" element={<Appeals />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="*" element={<Navigate to="/director" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
