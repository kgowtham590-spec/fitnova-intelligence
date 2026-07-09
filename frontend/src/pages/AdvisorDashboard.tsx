import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { FileAudio, UploadCloud, Sparkles } from 'lucide-react';

export default function AdvisorDashboard() {
  const [advisors, setAdvisors] = useState<any[]>([]);
  const [selectedAdvisor, setSelectedAdvisor] = useState<string>('');
  const [calls, setCalls] = useState<any[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  useEffect(() => {
    api.get('/org/structure').then(res => {
      const allAdvs = res.data.flatMap((t: any) => t.advisors);
      setAdvisors(allAdvs);
      if (allAdvs.length > 0) setSelectedAdvisor(allAdvs[0].id);
    });
  }, []);

  useEffect(() => {
    if (selectedAdvisor) {
      api.get(`/calls?advisor_id=${selectedAdvisor}`).then(res => setCalls(res.data.calls));
    }
  }, [selectedAdvisor]);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile || !selectedAdvisor) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
      await api.post(`/upload?advisor_id=${selectedAdvisor}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Recording uploaded and queued for processing!');
      setSelectedFile(null);
      api.get(`/calls?advisor_id=${selectedAdvisor}`).then(res => setCalls(res.data.calls));
    } catch (err: any) {
      alert('Upload failed: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  if (advisors.length === 0) return <div className="text-slate-400">Loading Advisors...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Advisor Coaching Space</h1>
          <p className="text-slate-400">Review your sales metrics, access audio transcripts, and submit appeals.</p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800 p-2 rounded-lg border border-[#334155]">
          <span className="text-slate-300 text-sm font-medium mr-2">Acting As:</span>
          <select value={selectedAdvisor} onChange={(e) => setSelectedAdvisor(e.target.value)} className="bg-slate-900 border border-[#334155] rounded px-3 py-1 text-white outline-none">
            {advisors.map(adv => (
              <option key={adv.id} value={adv.id}>{adv.name}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] shadow-md flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold text-white mb-2 flex items-center">
              <UploadCloud className="w-5 h-5 text-indigo-400 mr-2" /> Upload New Call
            </h2>
            <p className="text-slate-400 text-sm mb-6">Upload a call recording (.wav, .mp3) to trigger transcription, compliance scans, and overall scoring.</p>
          </div>
          <form onSubmit={handleUpload} className="space-y-4">
            <input type="file" onChange={(e) => setSelectedFile(e.target.files?.[0] || null)} className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-950 file:text-indigo-400 hover:file:bg-indigo-900" accept="audio/*" required />
            <button type="submit" disabled={uploading || !selectedFile} className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800/50 text-white font-bold py-2 rounded-lg transition-colors flex items-center justify-center">
              {uploading ? 'Processing via Pipeline...' : 'Upload & Analyze Call'}
            </button>
          </form>
        </div>

        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold text-white mb-2 flex items-center">
              <Sparkles className="w-5 h-5 text-cyan-400 mr-2" /> Performance Overview
            </h2>
            <p className="text-slate-400 text-sm mb-4">Summarized KPI details from your successfully audited sales logs.</p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-slate-400 text-xs">Total Calls Uploaded</div>
              <div className="text-2xl font-bold text-white mt-1">{calls.length}</div>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <div className="text-slate-400 text-xs">Average Quality Rating</div>
              <div className="text-2xl font-bold text-indigo-400 mt-1">
                {calls.filter(c => c.overall_score).length > 0
                  ? (calls.reduce((sum, c) => sum + (c.overall_score || 0), 0) / calls.filter(c => c.overall_score).length).toFixed(1)
                  : 'N/A'} / 10
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
        <h2 className="text-xl font-bold text-white mb-4">Your Recent Audits</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-800 text-slate-400 font-medium">
              <tr>
                <th className="p-4">Filename</th>
                <th className="p-4">Source</th>
                <th className="p-4">Audited Score</th>
                <th className="p-4">Process Date</th>
                <th className="p-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {calls.map(call => (
                <tr key={call.id} className="border-b border-[#334155] hover:bg-slate-800/50">
                  <td className="p-4 font-semibold text-white">{call.filename}</td>
                  <td className="p-4 capitalize">{call.source}</td>
                  <td className="p-4">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${call.overall_score >= 8 ? 'bg-green-950 text-green-400' : 'bg-red-950 text-red-400'}`}>
                      {call.overall_score ? `${call.overall_score} / 10` : 'Processing'}
                    </span>
                  </td>
                  <td className="p-4">{new Date(call.created_at).toLocaleDateString()}</td>
                  <td className="p-4">
                    <Link to={`/calls/${call.id}`} className="text-indigo-400 hover:text-indigo-300 font-semibold">View Detail</Link>
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
