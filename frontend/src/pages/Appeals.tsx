import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Check, X } from 'lucide-react';

export default function Appeals() {
  const [appeals, setAppeals] = useState<any[]>([]);
  const [notes, setNotes] = useState<string>('');

  useEffect(() => {
    api.get('/appeals').then(res => setAppeals(res.data));
  }, []);

  const handleReview = async (id: string, status: 'approved' | 'rejected') => {
    try {
      await api.put(`/appeals/${id}`, { status, reviewer_notes: notes });
      alert(`Appeal successfully ${status}!`);
      setNotes('');
      api.get('/appeals').then(res => setAppeals(res.data));
    } catch (err: any) {
      alert('Review failed: ' + err.message);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white">Appeals Resolution Desk</h1>
        <p className="text-slate-400">Review Advisor counter-arguments on compliance flags and resolve disputes.</p>
      </div>

      <div className="bg-[#1e293b] p-6 rounded-xl border border-[#334155]">
        <h2 className="text-xl font-bold text-white mb-4">Active Appeal Requests</h2>
        {appeals.length === 0 ? (
          <div className="text-slate-400">No active appeals in queue.</div>
        ) : (
          <div className="space-y-4">
            {appeals.map(appeal => (
              <div key={appeal.id} className="p-6 bg-slate-800 rounded-lg border border-[#334155] space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-slate-200">Appeal for Issue ID: {appeal.issue_id}</h3>
                    <p className="text-xs text-slate-400">Submitted on: {new Date(appeal.created_at).toLocaleDateString()}</p>
                  </div>
                  <span className={`px-2.5 py-0.5 rounded text-xs font-bold capitalize ${appeal.status === 'pending' ? 'bg-yellow-950 text-yellow-400' : appeal.status === 'approved' ? 'bg-green-950 text-green-400' : 'bg-red-950 text-red-400'}`}>
                    {appeal.status}
                  </span>
                </div>
                <div className="bg-slate-900 p-3 rounded text-slate-300 text-sm">
                  <span className="font-semibold text-xs text-slate-400 block mb-1">Advisor Appeal Argument:</span>
                  "{appeal.reason}"
                </div>

                {appeal.status === 'pending' && (
                  <div className="space-y-3 pt-2">
                    <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Reviewer notes/reasoning..." className="w-full text-sm bg-slate-900 border border-slate-700 p-2.5 text-white outline-none rounded h-20" />
                    <div className="flex space-x-3">
                      <button onClick={() => handleReview(appeal.id, 'approved')} className="bg-green-600 hover:bg-green-500 text-white font-bold py-1.5 px-4 rounded text-sm flex items-center">
                        <Check className="w-4 h-4 mr-2" /> Approve (Remove Flag)
                      </button>
                      <button onClick={() => handleReview(appeal.id, 'rejected')} className="bg-red-600 hover:bg-red-500 text-white font-bold py-1.5 px-4 rounded text-sm flex items-center">
                        <X className="w-4 h-4 mr-2" /> Reject Appeal
                      </button>
                    </div>
                  </div>
                )}
                {appeal.status !== 'pending' && appeal.reviewer_notes && (
                  <div className="bg-indigo-950/30 border border-indigo-900/50 p-3 rounded text-indigo-300 text-xs">
                    <span className="font-bold">Reviewer Notes:</span> {appeal.reviewer_notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
