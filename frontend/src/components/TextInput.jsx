import React from 'react';
import { X, Sparkles } from 'lucide-react';

export default function TextInput({
  value,
  onChange,
  placeholder,
  maxLength = 5000,
  examples = [],
  onSelectExample,
  disabled = false
}) {
  const charCount = value ? value.length : 0;

  return (
    <div className="space-y-3">
      {/* Quick load example buttons */}
      {examples.length > 0 && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-medium text-slate-400 flex items-center mr-1">
            <Sparkles className="w-3.5 h-3.5 mr-1 text-indigo-400" />
            Try examples:
          </span>
          {examples.map((ex, idx) => (
            <button
              key={idx}
              type="button"
              disabled={disabled}
              onClick={() => onSelectExample && onSelectExample(ex.text)}
              className="text-xs py-1 px-2.5 rounded-lg bg-slate-800/80 hover:bg-indigo-600/20 text-slate-300 hover:text-indigo-300 border border-slate-700/80 hover:border-indigo-500/30 transition-all disabled:opacity-50"
            >
              {ex.label}
            </button>
          ))}
        </div>
      )}

      {/* Main Textarea Container */}
      <div className="relative rounded-2xl bg-slate-900/80 border border-slate-800 focus-within:border-indigo-500/60 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all">
        <textarea
          rows={5}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          maxLength={maxLength}
          disabled={disabled}
          className="w-full bg-transparent px-4 py-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-y rounded-2xl disabled:opacity-60"
        />

        {/* Footer controls inside textarea */}
        <div className="flex items-center justify-between px-4 py-2 border-t border-slate-800/60 text-xs text-slate-400">
          <div className="flex items-center space-x-3">
            {value && (
              <button
                type="button"
                disabled={disabled}
                onClick={() => onChange('')}
                className="flex items-center space-x-1 text-slate-400 hover:text-rose-400 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            )}
          </div>
          <span className="font-mono">
            {charCount} / {maxLength}
          </span>
        </div>
      </div>
    </div>
  );
}
