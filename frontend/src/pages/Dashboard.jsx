import React, { useEffect, useState } from 'react';
import { getAllMetrics } from '../services/api';
import ModelCard from '../components/ModelCard';
import {
  Smile,
  ShieldAlert,
  Newspaper,
  Flame,
  Layers,
  Sparkles,
  Gauge,
  CheckCircle,
  Clock
} from 'lucide-react';

export default function Dashboard() {
  const [modelMetrics, setModelMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function fetchMetrics() {
      try {
        const res = await getAllMetrics();
        if (isMounted && res && res.models) {
          setModelMetrics(res.models);
        }
      } catch (err) {
        console.warn('Could not load model metrics:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    fetchMetrics();
    return () => { isMounted = false; };
  }, []);

  // Compute metrics from REAL data only
  const trainedModels = modelMetrics.filter((m) => m.status === 'ready' && m.metrics);
  const totalModels = 4;
  const readyCount = trainedModels.length;

  const avgAccuracy =
    trainedModels.length > 0
      ? (
          (trainedModels.reduce((acc, curr) => acc + curr.metrics.accuracy, 0) /
            trainedModels.length) *
          100
        ).toFixed(1)
      : null;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Hero Header */}
      <div className="relative rounded-3xl p-8 bg-gradient-to-br from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 overflow-hidden shadow-2xl">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Full-Stack NLP Architecture</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
            NLP Classification Dashboard
          </h1>
          <p className="text-slate-400 text-base leading-relaxed">
            A portfolio-grade machine learning platform unifying classical NLP preprocessing,
            TF-IDF vectorization, scikit-learn classifiers, and FastAPI REST microservices
            with a modern React dashboard.
          </p>
        </div>

        {/* Decorative Grid */}
        <div className="absolute right-0 top-0 w-96 h-full bg-radial from-indigo-500/10 to-transparent pointer-events-none" />
      </div>

      {/* Overview Metric Stats (Real values only) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5 flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">Available NLP Tasks</div>
            <div className="text-2xl font-bold text-slate-100 mt-0.5">4 Tasks</div>
            <div className="text-xs text-slate-400">Sentiment, Spam, Fake News, Toxicity</div>
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5 flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <CheckCircle className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">Deployed Models</div>
            <div className="text-2xl font-bold text-slate-100 mt-0.5">
              {readyCount} of {totalModels} Ready
            </div>
            <div className="text-xs text-emerald-400 font-medium">Sentiment & Spam Online</div>
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5 flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <Gauge className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">Avg. Test Accuracy</div>
            <div className="text-2xl font-bold text-slate-100 mt-0.5">
              {avgAccuracy ? `${avgAccuracy}%` : 'Model training in progress'}
            </div>
            <div className="text-xs text-slate-400">
              {avgAccuracy ? 'Based on verified held-out test evaluation' : 'No synthetic metrics'}
            </div>
          </div>
        </div>
      </div>

      {/* Model Cards Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">
            Classification Models
          </h2>
          <span className="text-xs text-slate-400">
            Select a model to test interactive inference
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ModelCard
            title="Sentiment Analysis"
            description="Evaluates whether an opinion or review expresses positive or negative sentiment using Logistic Regression and n-gram TF-IDF vectors."
            technique="TF-IDF + Logistic Regression"
            icon={Smile}
            emoji="😊"
            path="/sentiment"
            status="ready"
            badge="Active"
          />

          <ModelCard
            title="Spam Detection"
            description="Filters unsolicited emails, phishing attempts, and SMS promotions using a Multinomial Naive Bayes classifier."
            technique="TF-IDF + Multinomial Naive Bayes"
            icon={ShieldAlert}
            emoji="🚨"
            path="/spam"
            status="ready"
            badge="Active"
          />

          <ModelCard
            title="Fake News Detection"
            description="Flags misleading or manufactured news articles based on linguistic indicators, lexical diversity, and title-to-body patterns."
            technique="TF-IDF + Logistic Regression"
            icon={Newspaper}
            emoji="📰"
            path="/fake-news"
            status="upcoming"
            badge="Phase 3"
          />

          <ModelCard
            title="Toxic Comment Detection"
            description="Multi-label moderation system predicting severe toxicity, insults, obscenity, threats, and hate speech simultaneously."
            technique="One-vs-Rest Logistic Regression"
            icon={Flame}
            emoji="☣️"
            path="/toxicity"
            status="upcoming"
            badge="Phase 4"
          />
        </div>
      </div>
    </div>
  );
}
