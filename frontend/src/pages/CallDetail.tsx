import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { ShieldAlert, Award, AlertTriangle } from 'lucide-react';

export default function CallDetail() {
  const { id } = useParams();
  const [call, setCall] = useState<any>(null);
  const [appealReason, setAppealReason] = useState<string>('');
  const [appealingIssueId, setAppealingIssueId] = useState<string | null>(null);

  useEffect(() => {
    api.get(`/calls/${id}`).then(res => setCall(res.data));
  }, [id]);

  const submitAppeal = async (issueId: string) => {
    if (!appealReason) return;
    try {
      await api.post('/appeals', { issue_id: issueId, reason: appealReason });
      alert('Appeal submitted successfully!');
      setAppealingIssueId(null);
      setAppealReason('');
      api.get(`/calls/${id}`).then(res => setCall(res.data));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Appeal submission failed');
    }
  };

  if (!call) return <div className="text-slate-400">Loading call metrics and transcript...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white">{call.filename}</h1>
        <p className="text-slate-400">Advisor: {call.advisor_name} | Team: {call.team_name} | Channel: {call.source}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] md:col-span-2">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <Award className="w-5 h-5 text-indigo-400 mr-2" /> Score Rubric
          </h2>
          {call.scores.map((score: any, idx: number) => (
            <div key={idx} className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-800 p-3 rounded-lg text-center">
                <div className="text-slate-400 text-xs font-semibold">Needs Discovery</div>
                <div className="text-xl font-bold text-white mt-1">{score.needs_discovery} / 10</div>
              </div>
              <div className="bg-slate-800 p-3 rounded-lg text-center">
                <div className="text-slate-400 text-xs font-semibold">Rapport</div>
                <div className="text-xl font-bold text-white mt-1">{score.rapport} / 10</div>
              </div>
              <div className="bg-slate-800 p-3 rounded-lg text-center">
                <div className="text-slate-400 text-xs font-semibold">Objection Handling</div>
                <div className="text-xl font-bold text-white mt-1">{score.objection_handling} / 10</div>
              </div>
              <div className="bg-slate-800 p-3 rounded-lg text-center">
                <div className="text-slate-400 text-xs font-semibold">Compliance</div>
                <div className="text-xl font-bold text-red-400 mt-1">{score.compliance} / 10</div>
              </div>
            </div>
          ))}
          {call.scores[0]?.comments && (
            <div className="mt-4 p-3 bg-indigo-950/40 text-indigo-300 border border-indigo-900 rounded-lg text-sm">
              <span className="font-bold">Coach Notes:</span> {call.scores[0].comments}
            </div>
          )}
        </div>

        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold text-white mb-2 flex items-center">
              <ShieldAlert className="w-5 h-5 text-red-400 mr-2" /> Call Summary
            </h2>
            <p className="text-slate-300 text-sm leading-relaxed">{call.summary || 'Summary not generated'}</p>
          </div>
          {call.recommendations && (
            <div className="mt-4 border-t border-slate-700 pt-4">
              <h3 className="font-semibold text-cyan-400 text-xs mb-1">AI Advisor Coach Recommendations</h3>
              <p className="text-slate-400 text-xs">{call.recommendations}</p>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] md:col-span-2 space-y-4">
          <h2 className="text-xl font-bold text-white">Interactive Speaker Timeline</h2>
          <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
            {call.segments.map((seg: any) => (
              <div key={seg.id} className={`flex flex-col p-3 rounded-lg max-w-[85%] ${seg.speaker === 'Advisor' ? 'bg-indigo-950/40 border border-indigo-900 ml-auto' : 'bg-slate-800 border border-slate-700'}`}>
                <span className={`text-xs font-bold mb-1 ${seg.speaker === 'Advisor' ? 'text-indigo-400' : 'text-cyan-400'}`}>
                  {seg.speaker} ({seg.start_time.toFixed(1)}s - {seg.end_time.toFixed(1)}s)
                </span>
                <p className="text-sm text-slate-200">{seg.redacted_text}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155] space-y-4 h-fit">
          <h2 className="text-xl font-bold text-white flex items-center">
            <AlertTriangle className="w-5 h-5 text-red-500 mr-2" /> Flags & Violations
          </h2>
          {call.issues.length === 0 ? (
            <div className="text-slate-400 text-sm">No compliance issues detected. Clean call!</div>
          ) : (
            <div className="space-y-4">
              {call.issues.map((issue: any) => (
                <div key={issue.id} className="p-4 bg-slate-800 rounded-lg border border-[#334155] space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-extrabold uppercase bg-red-950 text-red-400 px-2 py-0.5 rounded">
                      {issue.issue_type.replace(/_/g, ' ')}
                    </span>
                    <span className="text-xs text-slate-400">Timestamp: {issue.timestamp}s</span>
                  </div>
                  <div className="p-2 bg-slate-900 text-slate-400 text-xs italic border-l-2 border-red-500">
                    "{issue.quote}"
                  </div>
                  <p className="text-slate-300 text-xs">{issue.reason}</p>
                  
                  <div className="pt-2 flex items-center justify-between border-t border-[#334155]">
                    <span className="text-[10px] text-slate-400 capitalize">Status: <span className="font-bold text-indigo-400">{issue.status.replace(/_/g, ' ')}</span></span>
                    {issue.status === 'active' && (
                      <button onClick={() => setAppealingIssueId(issue.id)} className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold underline">Contest Flag</button>
                    )}
                  </div>
                  
                  {appealingIssueId === issue.id && (
                    <div className="mt-2 space-y-2 bg-[#1e293b] p-2 border border-slate-700 rounded">
                      <textarea value={appealReason} onChange={(e) => setAppealReason(e.target.value)} placeholder="Provide reasoning to contest this compliance issue..." className="w-full text-xs bg-slate-900 border border-slate-700 p-2 text-white outline-none rounded h-16" />
                      <div className="flex space-x-2">
                        <button onClick={() => submitAppeal(issue.id)} className="bg-indigo-600 px-3 py-1 rounded text-xs text-white font-bold hover:bg-indigo-500">Submit</button>
                        <button onClick={() => setAppealingIssueId(null)} className="bg-slate-700 px-3 py-1 rounded text-xs text-slate-300 font-bold hover:bg-slate-600">Cancel</button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
