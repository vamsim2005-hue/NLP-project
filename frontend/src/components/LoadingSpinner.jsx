import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ text = 'Analyzing text with NLP pipeline...' }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-3 rounded-2xl bg-slate-900/40 border border-slate-800">
      <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
      <span className="text-sm font-medium text-slate-300 animate-pulse">
        {text}
      </span>
    </div>
  );
}
