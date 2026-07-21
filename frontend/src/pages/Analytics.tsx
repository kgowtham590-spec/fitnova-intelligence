import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function Analytics() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get('/org/analytics').then(res => setData(res.data));
  }, []);

  if (!data) return <div className="text-slate-400">Loading deep analytics...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white">Intelligence & Trend Center</h1>
        <p className="text-slate-400">Deep analysis of customer objections, compliance breakdowns, and advisor quality metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
          <h2 className="text-xl font-bold text-white mb-4">Quality Rubric Breakdown</h2>
          <div className="space-y-4">
            {Object.entries(data.averages).map(([k, val]: [string, any]) => {
              if (k === 'overall') return null;
              return (
                <div key={k} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="capitalize text-slate-300">{k.replace(/_/g, ' ')}</span>
                    <span className="font-bold text-indigo-400">{val} / 10</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2">
                    <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${val * 10}%` }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
          <h2 className="text-xl font-bold text-white mb-4">Compliance Issues distribution</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.issues_by_type.map((i: any) => ({ name: i.type.replace(/_/g, ' '), count: i.count }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
                <Bar dataKey="count" fill="#38bdf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
