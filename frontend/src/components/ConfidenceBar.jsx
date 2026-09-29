import React from 'react';

export default function ConfidenceBar({
  label,
  value, // float between 0.0 and 1.0 or percentage 0-100
  color = 'indigo', // 'emerald', 'rose', 'indigo', 'amber', 'cyan'
  isHighlighted = false
}) {
  const percentage = Math.min(100, Math.max(0, value > 1 ? value : value * 100));
  const formattedPercent = percentage.toFixed(1);

  const colorVariants = {
    emerald: {
      bar: 'bg-gradient-to-r from-emerald-500 to-teal-400',
      badge: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
    },
    rose: {
      bar: 'bg-gradient-to-r from-rose-500 to-pink-500',
      badge: 'text-rose-400 bg-rose-500/10 border-rose-500/20'
    },
    indigo: {
      bar: 'bg-gradient-to-r from-indigo-500 to-cyan-400',
      badge: 'text-indigo-300 bg-indigo-500/10 border-indigo-500/20'
    },
    amber: {
      bar: 'bg-gradient-to-r from-amber-500 to-orange-400',
      badge: 'text-amber-400 bg-amber-500/10 border-amber-500/20'
    },
    cyan: {
      bar: 'bg-gradient-to-r from-cyan-500 to-blue-400',
      badge: 'text-cyan-300 bg-cyan-500/10 border-cyan-500/20'
    }
  };

  const style = colorVariants[color] || colorVariants.indigo;

  return (
    <div className={`space-y-1.5 p-2 rounded-xl transition-colors ${isHighlighted ? 'bg-slate-800/40' : ''}`}>
      <div className="flex items-center justify-between text-xs">
        <span className={`font-semibold capitalize ${isHighlighted ? 'text-slate-100 font-bold' : 'text-slate-300'}`}>
          {label}
        </span>
        <span className={`px-2 py-0.5 rounded-md font-mono text-xs border ${style.badge}`}>
          {formattedPercent}%
        </span>
      </div>

      <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${style.bar}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
