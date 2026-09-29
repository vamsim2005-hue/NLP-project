const BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Standardized error message helper
 */
function handleApiError(error, defaultMsg) {
  if (error.response) {
    // Backend returned a response with an error code
    const detail = error.response.data?.detail;
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail)) {
      // Pydantic validation error list
      return detail.map(d => d.msg || 'Invalid input').join(', ');
    }
    return defaultMsg || 'Server returned an error. Please try again.';
  } else if (error.request) {
    // Request was made but no response received
    return 'Unable to connect to the NLP API. Please make sure the backend server is running.';
  } else {
    return error.message || defaultMsg || 'An unexpected error occurred.';
  }
}

async function requestJson(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });

    if (!res.ok) {
      let errData = {};
      try {
        errData = await res.json();
      } catch (_) {}
      const fakeAxiosError = {
        response: {
          status: res.status,
          data: errData
        }
      };
      throw new Error(handleApiError(fakeAxiosError));
    }

    return await res.json();
  } catch (err) {
    if (err.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError'))) {
      throw new Error('Unable to connect to the NLP API. Please make sure the backend server is running.');
    }
    throw err;
  }
}

/**
 * Checks backend health
 */
export async function checkHealth() {
  return await requestJson('/health');
}

/**
 * Predicts Sentiment for input text
 */
export async function predictSentiment(text) {
  if (!text || !text.trim()) {
    throw new Error('Please enter some text before analyzing sentiment.');
  }
  return await requestJson('/api/sentiment/predict', {
    method: 'POST',
    body: JSON.stringify({ text: text.trim() })
  });
}

/**
 * Fetches trained sentiment model metrics
 */
export async function getSentimentMetrics() {
  return await requestJson('/api/sentiment/metrics');
}

/**
 * Fetches metrics for all models in the system
 */
export async function getAllMetrics() {
  return await requestJson('/api/metrics');
}

/**
 * Spam prediction (Phase 2)
 */
export async function predictSpam(text) {
  if (!text || !text.trim()) {
    throw new Error('Please enter text to analyze for spam.');
  }
  return await requestJson('/api/spam/predict', {
    method: 'POST',
    body: JSON.stringify({ text: text.trim() })
  });
}

/**
 * Fake News prediction (Phase 3)
 */
export async function predictFakeNews(text) {
  if (!text || !text.trim()) {
    throw new Error('Please enter article text to analyze.');
  }
  return await requestJson('/api/fake-news/predict', {
    method: 'POST',
    body: JSON.stringify({ text: text.trim() })
  });
}

/**
 * Toxicity prediction (Phase 4)
 */
export async function predictToxicity(text) {
  if (!text || !text.trim()) {
    throw new Error('Please enter text to analyze for toxicity.');
  }
  return await requestJson('/api/toxicity/predict', {
    method: 'POST',
    body: JSON.stringify({ text: text.trim() })
  });
}
