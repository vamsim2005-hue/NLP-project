import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Smile,
  ShieldAlert,
  Newspaper,
  Flame,
  LineChart,
  Sparkles
} from 'lucide-react';

const NAV_ITEMS = [
  {
    path: '/',
    label: 'Dashboard',
    icon: LayoutDashboard,
    badge: null
  },
  {
    path: '/sentiment',
    label: 'Sentiment Analysis',
    icon: Smile,
    badge: 'Active'
  },
  {
    path: '/spam',
    label: 'Spam Detection',
    icon: ShieldAlert,
    badge: 'Active'
  },
  {
    path: '/fake-news',
    label: 'Fake News Detection',
    icon: Newspaper,
    badge: 'Phase 3'
  },
  {
    path: '/toxicity',
    label: 'Toxic Comments',
    icon: Flame,
    badge: 'Phase 4'
  },
  {
    path: '/performance',
    label: 'Model Performance',
    icon: LineChart,
    badge: null
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/40 backdrop-blur-xl flex flex-col justify-between shrink-0">
      <div className="p-4 space-y-6">
        <div className="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Classification Modules
        </div>

        <nav className="space-y-1.5">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600/15 text-indigo-300 border border-indigo-500/30 shadow-sm shadow-indigo-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`
                }
              >
                <div className="flex items-center space-x-3">
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded-md ${
                      item.badge === 'Active'
                        ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                        : 'bg-slate-800 text-slate-400 border border-slate-700'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer Info Box */}
      <div className="p-4 border-t border-slate-800/80 m-3 rounded-2xl bg-slate-900/80 border border-slate-800">
        <div className="flex items-center space-x-2 text-xs font-semibold text-indigo-400 mb-1">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Classical NLP Baseline</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          TF-IDF + Logistic Regression & Naive Bayes models serialized with scikit-learn.
        </p>
      </div>
    </aside>
  );
}
