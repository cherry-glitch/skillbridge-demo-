import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'
import ScoreBar from '../components/ScoreBar.jsx'

export default function SkillGap() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/students/me/skill-gap')
      .then(({ data }) => setData(data))
      .catch((err) => setError(err?.response?.data?.detail || 'Could not load skill gap.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Skill gap</h1>
        <p className="text-ink/60 mb-8">What's between you and being ready for your target role.</p>

        {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

        {error && (
          <div className="border border-dashed border-line rounded-sm p-6 text-center">
            <p className="text-ink/60 mb-3">{error}</p>
            <Link to="/" className="btn-primary inline-flex">Choose a target role</Link>
          </div>
        )}

        {data && (
          <>
            <div className="mb-10">
              <p className="text-sm text-ink/50">{data.role.name}</p>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-display text-5xl">{data.readiness_percent}%</span>
                <span className="text-ink/50">placement readiness</span>
              </div>
            </div>

            <section className="mb-10">
              <h2 className="text-lg mb-1 text-havecolor">Strong skills</h2>
              <p className="text-sm text-ink/50 mb-4">You've already cleared the bar here.</p>
              {data.strong_skills.length === 0 && (
                <p className="text-sm text-ink/40">None yet — take the assessment to establish your baseline.</p>
              )}
              {data.strong_skills.map((item) => (
                <div key={item.skill.id} className="ledger-row">
                  <p>{item.skill.name}</p>
                  <div className="flex items-center gap-3">
                    <ScoreBar score={item.student_score} have />
                    <span className="font-mono text-sm w-10 text-right">{item.student_score}</span>
                  </div>
                </div>
              ))}
            </section>

            <section>
              <h2 className="text-lg mb-1 text-gapcolor">Gap skills</h2>
              <p className="text-sm text-ink/50 mb-4">
                Ordered by how critical each skill is for {data.role.name}.
              </p>
              {data.gap_skills.length === 0 && (
                <p className="text-sm text-ink/40">No gaps — you're fully covered for this role.</p>
              )}
              {data.gap_skills.map((item) => (
                <div key={item.skill.id} className="ledger-row">
                  <div>
                    <p>{item.skill.name}</p>
                    <p className="text-xs text-ink/40">importance {item.required_weight}/5</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <ScoreBar score={item.student_score} have={false} />
                    <span className="font-mono text-sm w-10 text-right">{item.student_score}</span>
                  </div>
                </div>
              ))}

              {data.gap_skills.length > 0 && (
                <Link to="/roadmap" className="btn-primary inline-flex mt-6">
                  Get my learning roadmap
                </Link>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  )
}
