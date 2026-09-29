import React, { useState } from 'react';
import { predictSpam } from '../services/api';
import TextInput from '../components/TextInput';
import PredictionCard from '../components/PredictionCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { ShieldAlert, Send, Sparkles, AlertCircle } from 'lucide-react';

const SAMPLE_TEXTS = [
  {
    label: 'Prize Lottery (Spam)',
    text: 'URGENT! You have won a 1 week FREE luxury holiday or $10,000 cash! Call 09061701461 to claim your guaranteed prize now.'
  },
  {
    label: 'Casual Chat (Not Spam)',
    text: 'Hey, are we still meeting up for coffee tomorrow afternoon around 2pm at the library?'
  },
  {
    label: 'Work Update (Not Spam)',
    text: 'Hi team, please find attached the updated slides for tomorrow morning client presentation.'
  },
  {
    label: 'Phishing Urgency (Spam)',
    text: 'Your mobile account has expired! Click link http://claim-mobile-free.com to renew immediately and get 500 bonus minutes.'
  }
];

export default function Spam() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [elapsedMs, setElapsedMs] = useState(null);

  async function handleAnalyze(e) {
    if (e) e.preventDefault();
    if (!inputText.trim()) {
      setError('Please provide message text to classify.');
      return;
    }

    setError(null);
    setLoading(true);
    const start = performance.now();

    try {
      const response = await predictSpam(inputText);
      const end = performance.now();
      setElapsedMs(Math.round(end - start));
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to classify message.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
              Spam Detection
            </h1>
            <p className="text-sm text-slate-400">
              Filter unsolicited spam, lottery promotions, and phishing attempts using Multinomial Naive Bayes.
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
          placeholder="Paste an SMS message, promotional email, or suspicious text to check if it is spam..."
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
            className="py-2.5 px-6 rounded-xl bg-amber-600 hover:bg-amber-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold text-sm shadow-lg shadow-amber-600/25 transition-all flex items-center space-x-2 active:scale-95 cursor-pointer disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin text-amber-200" />
                <span>Checking...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Check Message</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Loading state indicator */}
      {loading && <LoadingSpinner text="Classifying message with Multinomial Naive Bayes..." />}

      {/* Prediction Result Display */}
      {result && !loading && (
        <PredictionCard
          prediction={result.prediction}
          confidence={result.confidence}
          probabilities={result.probabilities}
          elapsedMs={elapsedMs}
          taskType="spam"
        />
      )}

      {/* Pipeline Context Box */}
      <div className="rounded-2xl bg-slate-900/40 border border-slate-800/80 p-5 text-xs text-slate-400 space-y-2">
        <div className="font-semibold text-slate-300 flex items-center space-x-1.5">
          <AlertCircle className="w-4 h-4 text-amber-400" />
          <span>Pipeline & Model Context</span>
        </div>
        <p className="leading-relaxed">
          Trained on the UCI SMS Spam Collection benchmark ($N=5,572$). Text features are extracted with sublinear TF-IDF ($n$-gram range `(1, 2)`, 8,000 max features) and evaluated using a Multinomial Naive Bayes model ($\alpha = 0.2$), achieving <strong>98.38% test accuracy</strong>.
        </p>
      </div>
    </div>
  );
}
