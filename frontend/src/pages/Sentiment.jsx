import React, { useState } from 'react';
import { predictSentiment } from '../services/api';
import TextInput from '../components/TextInput';
import PredictionCard from '../components/PredictionCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { Smile, Send, Sparkles, AlertCircle } from 'lucide-react';

const SAMPLE_TEXTS = [
  {
    label: 'Great Movie (Positive)',
    text: 'A thrilling, emotional masterpiece with brilliant acting, stunning cinematography, and a heart-touching soundtrack.'
  },
  {
    label: 'Horrible Experience (Negative)',
    text: 'A dull, predictable disaster with completely uninspired dialogue, terrible pacing, and awful character development.'
  },
  {
    label: 'Subtle Praise (Positive)',
    text: 'While slow to start, the film gradually transforms into a deeply moving and unexpectedly rewarding experience.'
  },
  {
    label: 'Disappointment (Negative)',
    text: 'I was really looking forward to this release, but it failed on nearly every level and left the audience frustrated.'
  }
];

export default function Sentiment() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [elapsedMs, setElapsedMs] = useState(null);

  async function handleAnalyze(e) {
    if (e) e.preventDefault();
    if (!inputText.trim()) {
      setError('Please provide text to analyze.');
      return;
    }

    setError(null);
    setLoading(true);
    const start = performance.now();

    try {
      const response = await predictSentiment(inputText);
      const end = performance.now();
      setElapsedMs(Math.round(end - start));
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to analyze sentiment.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page Header */}
      <div className="space-y-2">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400">
            <Smile className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
              Sentiment Analysis
            </h1>
            <p className="text-sm text-slate-400">
              Analyze whether text expresses positive or negative emotion using TF-IDF n-grams and Logistic Regression.
            </p>
          </div>
        </div>
      </div>

      {/* Error alert banner */}
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {/* Input Form Card */}
      <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 space-y-5 shadow-lg">
        <TextInput
          value={inputText}
          onChange={(val) => {
            setInputText(val);
            if (error) setError(null);
          }}
          placeholder="Paste a movie review, customer feedback, tweet, or any paragraph to classify its sentiment..."
          maxLength={3000}
          examples={SAMPLE_TEXTS}
          onSelectExample={(txt) => {
            setInputText(txt);
            if (error) setError(null);
          }}
          disabled={loading}
        />

        <div className="flex items-center justify-end space-x-3 pt-2">
          <button
            type="button"
            disabled={loading || !inputText.trim()}
            onClick={handleAnalyze}
            className="py-2.5 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/25 transition-all flex items-center space-x-2 active:scale-95 cursor-pointer disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin text-indigo-200" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Analyze Sentiment</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Loading state indicator */}
      {loading && <LoadingSpinner text="Evaluating text sentiment with Logistic Regression..." />}

      {/* Prediction Result Display */}
      {result && !loading && (
        <PredictionCard
          prediction={result.prediction}
          confidence={result.confidence}
          probabilities={result.probabilities}
          elapsedMs={elapsedMs}
          taskType="sentiment"
        />
      )}

      {/* Model Information Accordion/Card */}
      <div className="rounded-2xl bg-slate-900/40 border border-slate-800/80 p-5 text-xs text-slate-400 space-y-2">
        <div className="font-semibold text-slate-300 flex items-center space-x-1.5">
          <AlertCircle className="w-4 h-4 text-indigo-400" />
          <span>Pipeline & Dataset Context</span>
        </div>
        <p className="leading-relaxed">
          Trained on the Stanford Sentiment Treebank (SST-2) binary sentiment benchmark. Text is cleaned through regex normalization, lowercased, vectorised via sublinear TF-IDF (10,000 unigrams & bigrams), and scored using an optimized Logistic Regression decision boundary.
        </p>
      </div>
    </div>
  );
}
