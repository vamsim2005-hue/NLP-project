import React, { useEffect, useState } from 'react';
import { getAllMetrics } from '../services/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import {
  LineChart,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  TrendingUp,
  Cpu
} from 'lucide-react';

export default function ModelPerformance() {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function loadData() {
      try {
        const res = await getAllMetrics();
        if (isMounted && res && res.models) {
          setModels(res.models);
        }
      } catch (err) {
        console.warn('Failed to load performance metrics:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadData();
    return () => { isMounted = false; };
  }, []);

  const trainedModels = models.filter((m) => m.status === 'ready' && m.metrics);

  const chartData = trainedModels.map((m) => ({
    name: m.name,
    Accuracy: +(m.metrics.accuracy * 100).toFixed(1),
    Precision: +(m.metrics.precision * 100).toFixed(1),
    Recall: +(m.metrics.recall * 100).toFixed(1),
    F1: +(m.metrics.f1_score * 100).toFixed(1),
  }));

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400">
            <LineChart className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
              Model Performance & Evaluation
            </h1>
            <p className="text-sm text-slate-400">
              Verified evaluation metrics directly computed on held-out test datasets.
            </p>
          </div>
        </div>
      </div>

      {/* Performance Metrics Table */}
      <div className="rounded-2xl bg-slate-900/60 border border-slate-800 overflow-hidden shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <h2 className="font-bold text-slate-200 text-base">Benchmark Summary</h2>
          <span className="text-xs text-slate-400">
            {trainedModels.length} of {models.length || 4} models serialized & benchmarked
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800 text-xs font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3.5 px-5">Model</th>
                <th className="py-3.5 px-4">Algorithm</th>
                <th className="py-3.5 px-4">Status</th>
                <th className="py-3.5 px-4">Accuracy</th>
                <th className="py-3.5 px-4">Precision</th>
                <th className="py-3.5 px-4">Recall</th>
                <th className="py-3.5 px-4">F1 Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {models.map((m, idx) => {
                const isReady = m.status === 'ready' && m.metrics;
                return (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-4 px-5 font-semibold text-slate-200">
                      {m.name}
                    </td>
                    <td className="py-4 px-4 font-mono text-xs text-slate-400">
                      {m.algorithm || 'Classical NLP'}
                    </td>
                    <td className="py-4 px-4">
                      {isReady ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          <CheckCircle2 className="w-3 h-3 mr-1" />
                          Ready
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700">
                          Model not trained yet
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-mono">
                      {isReady ? (
                        <span className="text-emerald-400 font-bold">
                          {(m.metrics.accuracy * 100).toFixed(2)}%
                        </span>
                      ) : (
                        <span className="text-slate-500 italic text-xs">—</span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-mono">
                      {isReady ? (
                        <span className="text-slate-300">
                          {(m.metrics.precision * 100).toFixed(2)}%
                        </span>
                      ) : (
                        <span className="text-slate-500 italic text-xs">—</span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-mono">
                      {isReady ? (
                        <span className="text-slate-300">
                          {(m.metrics.recall * 100).toFixed(2)}%
                        </span>
                      ) : (
                        <span className="text-slate-500 italic text-xs">—</span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-mono">
                      {isReady ? (
                        <span className="text-indigo-300 font-bold">
                          {(m.metrics.f1_score * 100).toFixed(2)}%
                        </span>
                      ) : (
                        <span className="text-slate-500 italic text-xs">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Chart & Confusion Matrix */}
      {trainedModels.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recharts Bar Chart */}
          <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 space-y-4">
            <h3 className="font-bold text-slate-200 text-base">
              Metric Comparison (%)
            </h3>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 20, left: -10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <YAxis domain={[0, 100]} stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#334155',
                      borderRadius: '0.75rem',
                      color: '#f8fafc',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                  <Bar dataKey="Accuracy" fill="#10b981" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Precision" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Recall" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="F1" fill="#ec4899" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Confusion Matrices */}
          <div className="space-y-6">
            {/* Sentiment Confusion Matrix Card */}
            {trainedModels.find((m) => m.task === 'sentiment')?.confusion_matrix && (
              <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-slate-200 text-base">
                    Sentiment Confusion Matrix
                  </h3>
                  <span className="text-xs text-slate-400">SST-2 Test Set (1,384 samples)</span>
                </div>

                {(() => {
                  const sModel = trainedModels.find((m) => m.task === 'sentiment');
                  const cm = sModel.confusion_matrix;
                  return (
                    <div className="space-y-3">
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div></div>
                        <div className="font-semibold text-slate-400 py-1 bg-slate-800/40 rounded-lg">
                          Pred Negative
                        </div>
                        <div className="font-semibold text-slate-400 py-1 bg-slate-800/40 rounded-lg">
                          Pred Positive
                        </div>

                        <div className="font-semibold text-slate-400 flex items-center justify-center bg-slate-800/40 rounded-lg py-2">
                          Actual Negative
                        </div>
                        <div className="p-3 rounded-xl bg-indigo-950/60 border border-indigo-500/30 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-emerald-400">{cm[0][0]}</span>
                          <span className="text-[10px] text-slate-400">True Negative</span>
                        </div>
                        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-rose-400">{cm[0][1]}</span>
                          <span className="text-[10px] text-slate-400">False Positive</span>
                        </div>

                        <div className="font-semibold text-slate-400 flex items-center justify-center bg-slate-800/40 rounded-lg py-2">
                          Actual Positive
                        </div>
                        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-rose-400">{cm[1][0]}</span>
                          <span className="text-[10px] text-slate-400">False Negative</span>
                        </div>
                        <div className="p-3 rounded-xl bg-indigo-950/60 border border-indigo-500/30 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-emerald-400">{cm[1][1]}</span>
                          <span className="text-[10px] text-slate-400">True Positive</span>
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}

            {/* Spam Confusion Matrix Card */}
            {trainedModels.find((m) => m.task === 'spam')?.confusion_matrix && (
              <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-slate-200 text-base">
                    Spam Detection Confusion Matrix
                  </h3>
                  <span className="text-xs text-slate-400">SMS Spam Test Set (1,114 samples)</span>
                </div>

                {(() => {
                  const sModel = trainedModels.find((m) => m.task === 'spam');
                  const cm = sModel.confusion_matrix;
                  return (
                    <div className="space-y-3">
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div></div>
                        <div className="font-semibold text-slate-400 py-1 bg-slate-800/40 rounded-lg">
                          Pred Ham (Clean)
                        </div>
                        <div className="font-semibold text-slate-400 py-1 bg-slate-800/40 rounded-lg">
                          Pred Spam
                        </div>

                        <div className="font-semibold text-slate-400 flex items-center justify-center bg-slate-800/40 rounded-lg py-2">
                          Actual Ham
                        </div>
                        <div className="p-3 rounded-xl bg-indigo-950/60 border border-indigo-500/30 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-emerald-400">{cm[0][0]}</span>
                          <span className="text-[10px] text-slate-400">True Ham</span>
                        </div>
                        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-rose-400">{cm[0][1]}</span>
                          <span className="text-[10px] text-slate-400">False Positive</span>
                        </div>

                        <div className="font-semibold text-slate-400 flex items-center justify-center bg-slate-800/40 rounded-lg py-2">
                          Actual Spam
                        </div>
                        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-rose-400">{cm[1][0]}</span>
                          <span className="text-[10px] text-slate-400">False Negative</span>
                        </div>
                        <div className="p-3 rounded-xl bg-indigo-950/60 border border-indigo-500/30 flex flex-col justify-center">
                          <span className="text-lg font-bold font-mono text-emerald-400">{cm[1][1]}</span>
                          <span className="text-[10px] text-slate-400">True Spam</span>
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
