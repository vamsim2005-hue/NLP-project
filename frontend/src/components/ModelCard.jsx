import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Clock } from 'lucide-react';

export default function ModelCard({
  title,
  description,
  technique,
  icon: Icon,
  emoji,
  path,
  status = 'ready', // 'ready' or 'upcoming'
  badge = 'Active'
}) {
  const isReady = status === 'ready';

  return (
    <div className="relative group rounded-2xl bg-slate-900/60 border border-slate-800/80 hover:border-indigo-500/40 transition-all duration-300 p-6 flex flex-col justify-between overflow-hidden hover:shadow-xl hover:shadow-indigo-500/5">
      {/* Subtle background glow effect */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-all pointer-events-none" />

      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{emoji}</span>
            <div className="p-2.5 rounded-xl bg-slate-800/70 border border-slate-700/60 text-indigo-400">
              <Icon className="w-5 h-5" />
            </div>
          </div>
          <span
            className={`text-xs font-semibold px-2.5 py-1 rounded-full border flex items-center space-x-1 ${
              isReady
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            {isReady ? (
              <>
                <CheckCircle2 className="w-3 h-3 mr-1" />
                <span>{badge}</span>
              </>
            ) : (
              <>
                <Clock className="w-3 h-3 mr-1" />
                <span>{badge}</span>
              </>
            )}
          </span>
        </div>

        <h3 className="text-lg font-bold text-slate-100 group-hover:text-indigo-300 transition-colors">
          {title}
        </h3>
        <p className="mt-2 text-sm text-slate-400 line-clamp-2 leading-relaxed">
          {description}
        </p>

        <div className="mt-4 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
          <span className="text-slate-400">Technique:</span>
          <span className="font-mono text-indigo-300 bg-indigo-950/40 border border-indigo-800/30 px-2 py-0.5 rounded">
            {technique}
          </span>
        </div>
      </div>

      <div className="mt-6">
        <Link
          to={path}
          className={`w-full py-2.5 px-4 rounded-xl text-sm font-semibold flex items-center justify-center space-x-2 transition-all ${
            isReady
              ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/20 active:scale-[0.98]'
              : 'bg-slate-800/80 hover:bg-slate-800 text-slate-300 border border-slate-700/60'
          }`}
        >
          <span>{isReady ? 'Open Model' : 'View Module'}</span>
          <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
        </Link>
      </div>
    </div>
  );
}
