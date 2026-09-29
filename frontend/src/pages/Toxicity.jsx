import React from 'react';
import { Flame, ArrowLeft, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Toxicity() {
  return (
    <div className="max-w-3xl mx-auto py-8 space-y-6">
      <Link to="/" className="inline-flex items-center text-xs text-slate-400 hover:text-indigo-300">
        <ArrowLeft className="w-3.5 h-3.5 mr-1" />
        Back to Dashboard
      </Link>

      <div className="rounded-3xl bg-slate-900/60 border border-slate-800 p-8 text-center space-y-5">
        <div className="w-16 h-16 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 mx-auto flex items-center justify-center">
          <Flame className="w-8 h-8" />
        </div>

        <div className="space-y-2">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-semibold">
            <Clock className="w-3 h-3" />
            <span>Scheduled for Phase 4</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Toxic Comment Detection Module
          </h1>
          <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
            Per the project roadmap, Toxic Comment Detection will be built in Phase 4 featuring multi-label classification (Toxic, Severe Toxic, Obscene, Threat, Insult, Identity Hate).
          </p>
        </div>

        <div className="pt-4 border-t border-slate-800/80 max-w-md mx-auto text-left text-xs text-slate-400 space-y-2">
          <div className="font-semibold text-slate-300">Planned Specifications:</div>
          <ul className="list-disc pl-5 space-y-1">
            <li>Algorithm: One-vs-Rest Logistic Regression + TF-IDF</li>
            <li>Input: User comments / online discussions</li>
            <li>Output: Multi-label probability breakdown across 6 categories</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
