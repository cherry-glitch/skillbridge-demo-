import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'

export default function Assessment() {
  const navigate = useNavigate()
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({}) // question_id -> 'a'|'b'|'c'|'d'
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/assessment/questions').then(({ data }) => {
      setQuestions(data)
      setLoading(false)
    })
  }, [])

  function selectAnswer(questionId, option) {
    setAnswers((prev) => ({ ...prev, [questionId]: option }))
  }

  async function handleSubmit() {
    setError('')
    const payload = {
      answers: Object.entries(answers).map(([question_id, selected_option]) => ({
        question_id: Number(question_id),
        selected_option,
      })),
    }
    if (payload.answers.length === 0) {
      setError('Answer at least one question before submitting.')
      return
    }
    setSubmitting(true)
    try {
      const { data } = await api.post('/assessment/submit', payload)
      setResults(data.results)
    } catch {
      setError('Something went wrong submitting your assessment. Try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const answeredCount = Object.keys(answers).length

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Skill assessment</h1>
        <p className="text-ink/60 mb-8">
          Answer as many as you know. Each skill is scored independently from the questions you answer for it —
          skipping a skill just leaves it unscored, it won't hurt you.
        </p>

        {loading && <p className="text-ink/50 font-mono text-sm">loading questions…</p>}

        {!loading && !results && (
          <>
            <div className="space-y-8">
              {questions.map((q, i) => (
                <div key={q.id} className="border-b border-line pb-6">
                  <p className="text-sm text-ink/40 font-mono mb-1">Q{i + 1}</p>
                  <p className="mb-3">{q.prompt}</p>
                  <div className="grid sm:grid-cols-2 gap-2">
                    {['a', 'b', 'c', 'd'].map((opt) => (
                      <button
                        key={opt}
                        type="button"
                        onClick={() => selectAnswer(q.id, opt)}
                        className={`text-left text-sm px-3 py-2 rounded-sm border transition-colors ${
                          answers[q.id] === opt
                            ? 'border-ink bg-ink text-paper'
                            : 'border-line hover:border-ink/40'
                        }`}
                      >
                        {q[`option_${opt}`]}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="sticky bottom-0 bg-paper pt-4 pb-8 mt-4">
              {error && <p className="text-sm text-gapcolor mb-3">{error}</p>}
              <div className="flex items-center gap-4">
                <button onClick={handleSubmit} disabled={submitting} className="btn-primary">
                  {submitting ? 'Scoring…' : 'Submit assessment'}
                </button>
                <p className="text-sm text-ink/50 font-mono">{answeredCount} / {questions.length} answered</p>
              </div>
            </div>
          </>
        )}

        {results && (
          <div>
            <p className="text-havecolor mb-6">Assessment scored. Here's your skill breakdown:</p>
            <div className="mb-8">
              {results.map((r) => (
                <div key={r.skill.id} className="ledger-row">
                  <div>
                    <p>{r.skill.name}</p>
                    <p className="text-xs text-ink/40">{r.correct}/{r.total} correct</p>
                  </div>
                  <p className="font-mono text-lg">{r.score}</p>
                </div>
              ))}
            </div>
            <button onClick={() => navigate('/')} className="btn-primary">
              View my skill profile
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
