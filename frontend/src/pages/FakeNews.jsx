import React from 'react';
import { Newspaper, ArrowLeft, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function FakeNews() {
  return (
    <div className="max-w-3xl mx-auto py-8 space-y-6">
      <Link to="/" className="inline-flex items-center text-xs text-slate-400 hover:text-indigo-300">
        <ArrowLeft className="w-3.5 h-3.5 mr-1" />
        Back to Dashboard
      </Link>

      <div className="rounded-3xl bg-slate-900/60 border border-slate-800 p-8 text-center space-y-5">
        <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 mx-auto flex items-center justify-center">
          <Newspaper className="w-8 h-8" />
        </div>

        <div className="space-y-2">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold">
            <Clock className="w-3 h-3" />
            <span>Scheduled for Phase 3</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Fake News Detection Module
          </h1>
          <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
            Per the project roadmap, Fake News Detection will be built in Phase 3 with headline + article body classification using Logistic Regression and TF-IDF.
          </p>
        </div>

        <div className="pt-4 border-t border-slate-800/80 max-w-md mx-auto text-left text-xs text-slate-400 space-y-2">
          <div className="font-semibold text-slate-300">Planned Specifications:</div>
          <ul className="list-disc pl-5 space-y-1">
            <li>Algorithm: Logistic Regression + TF-IDF</li>
            <li>Input: Headline + Article text</li>
            <li>Output: REAL / FAKE with disclaimer banner</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
