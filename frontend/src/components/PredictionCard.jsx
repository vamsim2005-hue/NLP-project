import React from 'react';
import ConfidenceBar from './ConfidenceBar';
import {
  ThumbsUp,
  ThumbsDown,
  ShieldCheck,
  ShieldAlert,
  Clock
} from 'lucide-react';

export default function PredictionCard({
  prediction,
  confidence,
  probabilities = {},
  elapsedMs = null,
  taskType = 'sentiment'
}) {
  if (!prediction) return null;

  const confidencePercent = (confidence * 100).toFixed(1);

  // Determine state based on task
  let isGood = false;
  let Icon = ThumbsUp;

  if (taskType === 'sentiment') {
    isGood = prediction.toLowerCase() === 'positive';
    Icon = isGood ? ThumbsUp : ThumbsDown;
  } else if (taskType === 'spam') {
    isGood = prediction.toUpperCase() === 'NOT SPAM' || prediction.toLowerCase() === 'ham';
    Icon = isGood ? ShieldCheck : ShieldAlert;
  }

  return (
    <div className="rounded-2xl bg-slate-900/80 border border-slate-800 p-6 space-y-6 shadow-xl relative overflow-hidden">
      {/* Glow highlight */}
      <div
        className={`absolute top-0 right-0 w-48 h-48 rounded-full blur-3xl opacity-15 pointer-events-none ${
          isGood ? 'bg-emerald-500' : 'bg-rose-500'
        }`}
      />

      {/* Header Result */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800">
        <div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Prediction Result
          </span>
          <div className="flex items-center space-x-3">
            <span
              className={`text-2xl font-extrabold tracking-tight px-4 py-1.5 rounded-xl border flex items-center space-x-2 ${
                isGood
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
              }`}
            >
              <Icon className="w-6 h-6" />
              <span className="uppercase">{prediction}</span>
            </span>
          </div>
        </div>

        <div className="text-left sm:text-right">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Model Confidence
          </span>
          <div className="text-3xl font-black font-mono text-slate-100">
            {confidencePercent}%
          </div>
          {elapsedMs !== null && (
            <div className="flex items-center sm:justify-end space-x-1 text-xs text-slate-400 mt-0.5">
              <Clock className="w-3 h-3 text-slate-400" />
              <span>Inference: {elapsedMs}ms</span>
            </div>
          )}
        </div>
      </div>

      {/* Probability Distribution */}
      {probabilities && Object.keys(probabilities).length > 0 && (
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Class Probability Distribution
          </h4>
          <div className="space-y-2">
            {Object.entries(probabilities).map(([label, prob]) => {
              let barColor = 'indigo';
              let displayLabel = label;
              let isMatch = false;

              if (taskType === 'sentiment') {
                const isPos = label.toLowerCase() === 'positive';
                barColor = isPos ? 'emerald' : 'rose';
                isMatch = label.toLowerCase() === prediction.toLowerCase();
              } else if (taskType === 'spam') {
                const isHam = label.toLowerCase() === 'ham';
                displayLabel = isHam ? 'Legitimate Message (Ham)' : 'Spam Promotion / Phishing';
                barColor = isHam ? 'emerald' : 'rose';
                isMatch =
                  (isHam && (prediction === 'NOT SPAM' || prediction === 'ham')) ||
                  (!isHam && (prediction === 'SPAM' || prediction === 'spam'));
              }

              return (
                <ConfidenceBar
                  key={label}
                  label={displayLabel}
                  value={prob}
                  color={barColor}
                  isHighlighted={isMatch}
                />
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
