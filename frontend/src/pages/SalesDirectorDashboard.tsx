import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Award, ShieldAlert, Users, TrendingUp, Sparkles } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function SalesDirectorDashboard() {
  const [data, setData] = useState<any>(null);
  const [calls, setCalls] = useState<any[]>([]);

  useEffect(() => {
    api.get('/org/analytics').then(res => setData(res.data));
    api.get('/calls').then(res => setCalls(res.data.calls));
  }, []);

  if (!data) return <div className="text-slate-400">Loading Sales Director insights...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Executive Dashboard</h1>
          <p className="text-slate-400">Macro overview of FitNova's sales intelligence and quality trends.</p>
        </div>
        <div className="flex items-center space-x-2 bg-indigo-950 border border-indigo-700 px-4 py-2 rounded-lg text-indigo-200">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          <span className="text-sm font-semibold">AI Insights Active</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Avg Org Score</span>
            <div className="text-3xl font-bold text-white mt-1">{data.averages.overall} / 10</div>
          </div>
          <Award className="w-10 h-10 text-indigo-400 bg-indigo-950 p-2 rounded-lg" />
        </div>
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Total Calls</span>
            <div className="text-3xl font-bold text-white mt-1">{calls.length}</div>
          </div>
          <TrendingUp className="w-10 h-10 text-green-400 bg-green-950 p-2 rounded-lg" />
        </div>
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Compliance</span>
            <div className="text-3xl font-bold text-white mt-1">{data.averages.compliance} / 10</div>
          </div>
          <Users className="w-10 h-10 text-cyan-400 bg-cyan-950 p-2 rounded-lg" />
        </div>
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex items-center justify-between">
          <div>
            <span className="text-sm text-slate-400 font-medium">Active Flags</span>
            <div className="text-3xl font-bold text-white mt-1">
              {data.issues_by_type.reduce((acc: number, curr: any) => acc + curr.count, 0)}
            </div>
          </div>
          <ShieldAlert className="w-10 h-10 text-red-400 bg-red-950 p-2 rounded-lg" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
          <h2 className="text-xl font-bold text-white mb-4">Quality Trends</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={[
                { name: 'Week 1', score: 7.2 },
                { name: 'Week 2', score: 7.5 },
                { name: 'Week 3', score: 8.1 },
                { name: 'Week 4', score: data.averages.overall },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis domain={[0, 10]} stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
                <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] flex flex-col justify-between">
          <h2 className="text-xl font-bold text-white mb-4">Team Leaderboard</h2>
          <div className="space-y-4">
            {data.team_rankings.map((team: any, idx: number) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                <span className="font-semibold text-slate-200">{team.name}</span>
                <span className="text-indigo-400 font-bold">{team.score} / 10</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
        <h2 className="text-xl font-bold text-white mb-4">Recent Ingested Calls</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-800 text-slate-400 font-medium">
              <tr>
                <th className="p-4">Filename</th>
                <th className="p-4">Advisor</th>
                <th className="p-4">Team</th>
                <th className="p-4">Quality Score</th>
                <th className="p-4">Status</th>
                <th className="p-4">Action</th>
              </tr>
            </thead>
            <tbody>
              {calls.map((call: any) => (
                <tr key={call.id} className="border-b border-[#334155] hover:bg-slate-800/50">
                  <td className="p-4 font-semibold text-white">{call.filename}</td>
                  <td className="p-4">{call.advisor_name}</td>
                  <td className="p-4">{call.team_name}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${call.overall_score >= 8 ? 'bg-green-950 text-green-300' : 'bg-red-950 text-red-300'}`}>
                      {call.overall_score ? `${call.overall_score} / 10` : 'Pending'}
                    </span>
                  </td>
                  <td className="p-4">
                    <span className={`capitalize px-2 py-0.5 rounded text-xs ${call.status === 'completed' ? 'bg-indigo-950 text-indigo-300' : 'bg-yellow-950 text-yellow-300'}`}>
                      {call.status}
                    </span>
                  </td>
                  <td className="p-4">
                    <Link to={`/calls/${call.id}`} className="text-indigo-400 hover:text-indigo-300 font-medium">View Analysis</Link>
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
