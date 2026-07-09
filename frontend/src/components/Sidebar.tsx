import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChart3, ShieldAlert, Award, FileAudio, Users } from 'lucide-react';

export default function Sidebar() {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="w-64 bg-[#1e293b] border-r border-[#334155] h-screen flex flex-col fixed left-0 top-0">
      <div className="h-16 flex items-center px-6 border-b border-[#334155]">
        <span className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">FitNova AI IQ</span>
      </div>
      <div className="flex-1 py-6 px-4 space-y-1">
        <Link to="/director" className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive('/director') ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
          <Award className="w-5 h-5 mr-3" />
          Sales Director
        </Link>
        <Link to="/team-leader" className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive('/team-leader') ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
          <Users className="w-5 h-5 mr-3" />
          Team Leader
        </Link>
        <Link to="/advisor" className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive('/advisor') ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
          <FileAudio className="w-5 h-5 mr-3" />
          Advisor Dashboard
        </Link>
        <Link to="/analytics" className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive('/analytics') ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
          <BarChart3 className="w-5 h-5 mr-3" />
          Analytics & Trends
        </Link>
        <Link to="/appeals" className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive('/appeals') ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
          <ShieldAlert className="w-5 h-5 mr-3" />
          Appeals Queue
        </Link>
      </div>
    </div>
  );
}
