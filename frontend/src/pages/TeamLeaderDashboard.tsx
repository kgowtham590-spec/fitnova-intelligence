import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Users, FileAudio, CheckCircle2 } from 'lucide-react';

export default function TeamLeaderDashboard() {
  const [structure, setStructure] = useState<any[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<string>('');
  const [calls, setCalls] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    api.get('/org/structure').then(res => {
      setStructure(res.data);
      if (res.data.length > 0) setSelectedTeam(res.data[0].team_id);
    });
    api.get('/org/analytics').then(res => setAnalytics(res.data));
  }, []);

  useEffect(() => {
    if (selectedTeam) {
      api.get(`/calls?team_id=${selectedTeam}`).then(res => setCalls(res.data.calls));
    }
  }, [selectedTeam]);

  if (structure.length === 0) return <div className="text-slate-400">Loading Pod structure...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white">Pod Leaderboard & Coach Control</h1>
        <p className="text-slate-400">Monitor calls, review compliance violations, and manage advisor performance.</p>
      </div>

      <div className="flex items-center space-x-4 bg-[#1e293b] p-4 rounded-lg border border-[#334155]">
        <label className="text-slate-300 font-semibold text-sm">Select Pod / Team:</label>
        <select value={selectedTeam} onChange={(e) => setSelectedTeam(e.target.value)} className="bg-slate-800 border border-[#334155] rounded px-3 py-1.5 text-white outline-none">
          {structure.map(team => (
            <option key={team.team_id} value={team.team_id}>{team.team_name}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Pod Advisors</span>
            <div className="text-2xl font-bold text-white mt-1">
              {structure.find(t => t.team_id === selectedTeam)?.advisors.length || 0} Members
            </div>
          </div>
          <Users className="w-8 h-8 text-indigo-400" />
        </div>
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Reviewed Calls</span>
            <div className="text-2xl font-bold text-white mt-1">{calls.filter(c => c.status === 'completed').length}</div>
          </div>
          <FileAudio className="w-8 h-8 text-green-400" />
        </div>
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Pod Avg Score</span>
            <div className="text-2xl font-bold text-white mt-1">
              {analytics ? `${analytics.team_rankings.find((t: any) => t.name === structure.find((st: any) => st.team_id === selectedTeam)?.team_name)?.score || '8.2'} / 10` : '8.2'}
            </div>
          </div>
          <CheckCircle2 className="w-8 h-8 text-cyan-400" />
        </div>
      </div>

      <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
        <h2 className="text-xl font-bold text-white mb-4">Pod Call Audit Logs</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-800 text-slate-400 font-medium">
              <tr>
                <th className="p-4">Advisor</th>
                <th className="p-4">Filename</th>
                <th className="p-4">Call Score</th>
                <th className="p-4">Ingestion Date</th>
                <th className="p-4">Action</th>
              </tr>
            </thead>
            <tbody>
              {calls.map((call: any) => (
                <tr key={call.id} className="border-b border-[#334155] hover:bg-slate-800/50">
                  <td className="p-4 font-semibold text-white">{call.advisor_name}</td>
                  <td className="p-4">{call.filename}</td>
                  <td className="p-4">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${call.overall_score >= 8 ? 'bg-green-950 text-green-400' : 'bg-red-950 text-red-400'}`}>
                      {call.overall_score ? `${call.overall_score} / 10` : 'Under Review'}
                    </span>
                  </td>
                  <td className="p-4">{new Date(call.created_at).toLocaleDateString()}</td>
                  <td className="p-4">
                    <Link to={`/calls/${call.id}`} className="text-indigo-400 hover:text-indigo-300 font-semibold">Audit Call</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
