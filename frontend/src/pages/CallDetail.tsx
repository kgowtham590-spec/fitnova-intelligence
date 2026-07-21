import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ShieldAlert, Award, AlertTriangle, ArrowLeft, Clock, User, PhoneCall, Volume2, Sparkles, CheckCircle2 } from 'lucide-react';

export default function CallDetail() {
  const { id } = useParams();
  const [call, setCall] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [appealReason, setAppealReason] = useState<string>('');
  const [appealingIssueId, setAppealingIssueId] = useState<string | null>(null);
  const [submittingAppeal, setSubmittingAppeal] = useState<boolean>(false);

  const fetchCallDetails = () => {
    setLoading(true);
    api.get(`/calls/${id}`)
      .then(res => {
        setCall(res.data);
        setError(null);
      })
      .catch(err => {
        setError('Failed to fetch call details. Please try again.');
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCallDetails();
  }, [id]);

  const submitAppeal = async (issueId: string) => {
    if (!appealReason.trim()) return;
    setSubmittingAppeal(true);
    try {
      await api.post('/appeals', { issue_id: issueId, reason: appealReason });
      alert('Appeal submitted successfully!');
      setAppealingIssueId(null);
      setAppealReason('');
      fetchCallDetails();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Appeal submission failed');
    } finally {
      setSubmittingAppeal(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        <p className="text-slate-400 font-medium animate-pulse">Loading call metrics and transcript...</p>
      </div>
    );
  }

  if (error || !call) {
    return (
      <div className="bg-red-950/20 border border-red-900/50 p-6 rounded-xl text-center max-w-xl mx-auto space-y-4">
        <AlertTriangle className="w-12 h-12 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-white">Error Loading Call</h2>
        <p className="text-slate-300 text-sm">{error || 'Call not found'}</p>
        <Link to="/" className="inline-flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-semibold text-sm transition">
          <ArrowLeft className="w-4 h-4" /> <span>Back to Dashboard</span>
        </Link>
      </div>
    );
  }

  const audioUrl = `${api.defaults.baseURL}/calls/${id}/audio`;
  const scores = call.scores[0] || {
    needs_discovery: 0,
    rapport: 0,
    product_knowledge: 0,
    objection_handling: 0,
    compliance: 0,
    trial_booking: 0,
    closing: 0,
    overall_score: 0,
    comments: ''
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-emerald-400 bg-emerald-950/50 border-emerald-900/50';
    if (score >= 5) return 'text-amber-400 bg-amber-950/50 border-amber-900/50';
    return 'text-rose-400 bg-rose-950/50 border-rose-900/50';
  };

  const getProgressBarColor = (score: number) => {
    if (score >= 8) return 'bg-emerald-500';
    if (score >= 5) return 'bg-amber-500';
    return 'bg-rose-500';
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 md:px-0 pb-12">
      {/* Header & Back Action */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <div>
          <Link to="/" className="inline-flex items-center space-x-1 text-xs text-indigo-400 hover:text-indigo-300 transition font-semibold mb-2">
            <ArrowLeft className="w-3.5 h-3.5" /> <span>Back to Dashboard</span>
          </Link>
          <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <PhoneCall className="w-8 h-8 text-indigo-400" />
            <span>{call.filename}</span>
          </h1>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-2 text-sm text-slate-400">
            <span className="flex items-center gap-1"><User className="w-4 h-4" /> Advisor: <strong className="text-white">{call.advisor_name}</strong></span>
            <span className="h-4 w-px bg-slate-700 hidden sm:inline" />
            <span>Team: <strong className="text-white">{call.team_name}</strong></span>
            <span className="h-4 w-px bg-slate-700 hidden sm:inline" />
            <span className="flex items-center gap-1 font-mono text-xs"><Clock className="w-4 h-4" /> {call.duration ? `${Math.floor(call.duration / 60)}m ${Math.floor(call.duration % 60)}s` : 'Unknown'}</span>
            <span className="h-4 w-px bg-slate-700 hidden sm:inline" />
            <span className="bg-slate-800 text-slate-300 text-xs px-2.5 py-0.5 rounded-full border border-slate-700 uppercase">{call.source}</span>
          </div>
        </div>
        
        {/* Overall Score Badge */}
        <div className={`p-4 rounded-xl border flex flex-col items-center justify-center min-w-[120px] ${getScoreColor(scores.overall_score)}`}>
          <span className="text-[10px] uppercase font-bold tracking-wider opacity-75">Overall Score</span>
          <span className="text-3xl font-black mt-0.5">{scores.overall_score.toFixed(1)}</span>
          <span className="text-[10px] opacity-50 mt-0.5">out of 10</span>
        </div>
      </div>

      {/* Audio Player Card */}
      <div className="bg-[#1e293b] p-6 rounded-2xl border border-[#334155] shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Volume2 className="w-5 h-5 text-indigo-400" /> Play Recording
          </h2>
          <span className="text-xs text-slate-400 font-mono">Stream secure MP3</span>
        </div>
        <audio src={audioUrl} controls className="w-full focus:outline-none rounded-lg accent-indigo-500" />
      </div>

      {/* Scores and Summary Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Score Rubric Details */}
        <div className="bg-[#1e293b] p-6 rounded-2xl border border-[#334155] shadow-xl lg:col-span-2 space-y-6">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-400" /> Performance Breakdown
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
            {[
              { label: 'Needs Discovery', score: scores.needs_discovery, desc: 'Budget, goals & current status exploration' },
              { label: 'Rapport Building', score: scores.rapport, desc: 'Tone, active listening & empathy' },
              { label: 'Product Knowledge', score: scores.product_knowledge, desc: 'Fitness programs & pricing explanations' },
              { label: 'Objection Handling', score: scores.objection_handling, desc: 'Resolving pricing & schedule hesitations' },
              { label: 'Compliance & Ethics', score: scores.compliance, desc: 'Accuracy & high pressure avoidance' },
              { label: 'Trial Booking', score: scores.trial_booking, desc: 'Effort to secure trial slot' },
              { label: 'Closing & Next Steps', score: scores.closing, desc: 'Securing follow-up agreements' },
            ].map((item, idx) => (
              <div key={idx} className="space-y-1.5 p-3 rounded-xl bg-slate-900/30 border border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold text-slate-200">{item.label}</span>
                  <span className="text-sm font-bold text-white">{item.score.toFixed(1)}/10</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${getProgressBarColor(item.score)}`} 
                    style={{ width: `${item.score * 10}%` }}
                  />
                </div>
                <p className="text-[11px] text-slate-400 leading-tight">{item.desc}</p>
              </div>
            ))}
          </div>

          {scores.comments && (
            <div className="p-4 bg-indigo-950/30 border border-indigo-900/50 rounded-xl space-y-2">
              <div className="flex items-center gap-1.5 text-indigo-300 font-bold text-sm">
                <Sparkles className="w-4 h-4" /> QA Auditor Feedback & Sentiment
              </div>
              <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">{scores.comments}</p>
            </div>
          )}
        </div>

        {/* Call Summary & Coach recommendations */}
        <div className="bg-[#1e293b] p-6 rounded-2xl border border-[#334155] shadow-xl flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-indigo-400" /> AI Executive Summary
            </h2>
            <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800">
              <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">{call.summary || 'Summary generation processing...'}</p>
            </div>
          </div>
          
          {call.recommendations && (
            <div className="border-t border-[#334155] pt-4 space-y-3">
              <h3 className="font-bold text-cyan-400 text-sm flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" /> Actionable Coaching Tips
              </h3>
              <div className="bg-slate-900/20 p-4 rounded-xl border border-slate-800/50">
                <p className="text-slate-300 text-xs leading-relaxed whitespace-pre-wrap">{call.recommendations}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Timeline & Compliance Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Interactive Timeline */}
        <div className="bg-[#1e293b] p-6 rounded-2xl border border-[#334155] shadow-xl lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span>Interactive Speaker Transcript</span>
            </h2>
            <span className="text-xs bg-indigo-950 text-indigo-400 px-2.5 py-0.5 rounded-full border border-indigo-900 font-medium">Diarized</span>
          </div>

          <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-800">
            {call.segments.map((seg: any) => {
              const isAdvisor = seg.speaker === 'Advisor';
              return (
                <div key={seg.id} className={`flex items-start gap-3 max-w-[85%] ${isAdvisor ? 'ml-auto flex-row-reverse' : ''}`}>
                  {/* Speaker Initials Icon */}
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-black shrink-0 ${isAdvisor ? 'bg-indigo-600 text-white' : 'bg-cyan-600 text-white'}`}>
                    {isAdvisor ? 'AD' : 'CU'}
                  </div>
                  
                  {/* Bubble */}
                  <div className={`p-4 rounded-2xl shadow-sm border ${isAdvisor ? 'bg-indigo-950/30 border-indigo-900 text-slate-100' : 'bg-slate-900/50 border-slate-800 text-slate-200'}`}>
                    <div className="flex items-center gap-2 mb-1 justify-between">
                      <span className={`text-xs font-bold ${isAdvisor ? 'text-indigo-400' : 'text-cyan-400'}`}>
                        {isAdvisor ? 'Advisor' : 'Customer'}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {seg.start_time.toFixed(1)}s - {seg.end_time.toFixed(1)}s
                      </span>
                    </div>
                    <p className="text-sm leading-relaxed break-words">{seg.redacted_text}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Flags & Compliance Violations */}
        <div className="bg-[#1e293b] p-6 rounded-2xl border border-[#334155] shadow-xl space-y-4 h-fit">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-rose-500" /> Flags & Violations
          </h2>
          
          {call.issues.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-8 bg-slate-900/30 border border-slate-800 rounded-xl space-y-3">
              <CheckCircle2 className="w-12 h-12 text-emerald-500" />
              <div className="text-emerald-400 text-sm font-semibold text-center">Clean Compliance Score!</div>
              <p className="text-slate-400 text-xs text-center">No compliance violations or sales warnings detected on this call.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {call.issues.map((issue: any) => {
                const getSeverityStyle = (sev: string) => {
                  if (sev === 'high') return 'bg-red-950 text-red-400 border-red-900/30';
                  if (sev === 'medium') return 'bg-amber-950 text-amber-400 border-amber-900/30';
                  return 'bg-blue-950 text-blue-400 border-blue-900/30';
                };
                return (
                  <div key={issue.id} className="p-4 bg-slate-900/50 rounded-xl border border-slate-800 space-y-3 shadow-inner">
                    <div className="flex items-center justify-between">
                      <span className={`text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full border ${getSeverityStyle(issue.severity)}`}>
                        {issue.issue_type.replace(/_/g, ' ')}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">Timestamp: {issue.timestamp.toFixed(1)}s</span>
                    </div>
                    
                    <div className="p-3 bg-slate-950/60 text-slate-300 text-xs italic border-l-2 border-rose-500 rounded-r-lg font-mono">
                      "{issue.quote}"
                    </div>
                    
                    <p className="text-slate-400 text-xs leading-relaxed">{issue.reason}</p>
                    
                    <div className="pt-2 flex items-center justify-between border-t border-[#334155]">
                      <span className="text-[10px] text-slate-500 capitalize">
                        Status: <span className="font-bold text-indigo-400">{issue.status.replace(/_/g, ' ')}</span>
                      </span>
                      {issue.status === 'active' && (
                        <button 
                          onClick={() => setAppealingIssueId(issue.id)} 
                          className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold underline hover:no-underline transition"
                        >
                          Contest Flag
                        </button>
                      )}
                    </div>
                    
                    {appealingIssueId === issue.id && (
                      <div className="mt-3 space-y-2 bg-[#1e293b] p-3 border border-slate-800 rounded-xl">
                        <textarea 
                          value={appealReason} 
                          onChange={(e) => setAppealReason(e.target.value)} 
                          placeholder="Provide reasoning to contest this compliance issue..." 
                          className="w-full text-xs bg-slate-900 border border-slate-800 p-2.5 text-white outline-none rounded-lg h-20 focus:border-indigo-500" 
                        />
                        <div className="flex space-x-2 justify-end">
                          <button 
                            onClick={() => submitAppeal(issue.id)} 
                            disabled={submittingAppeal}
                            className="bg-indigo-600 px-4 py-1.5 rounded-lg text-xs text-white font-bold hover:bg-indigo-500 transition disabled:opacity-50"
                          >
                            {submittingAppeal ? 'Submitting...' : 'Submit'}
                          </button>
                          <button 
                            onClick={() => setAppealingIssueId(null)} 
                            className="bg-slate-800 px-4 py-1.5 rounded-lg text-xs text-slate-300 font-bold hover:bg-slate-700 transition"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
