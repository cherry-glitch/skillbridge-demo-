import { useEffect, useState } from 'react'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'

export default function Matches() {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [applyingId, setApplyingId] = useState(null)
  const [appliedIds, setAppliedIds] = useState(new Set())

  async function load() {
    setLoading(true)
    const { data } = await api.get('/internships')
    setMatches(data)
    setLoading(false)
  }

  useEffect(() => {
    load()
  }, [])

  async function apply(internshipId) {
    setApplyingId(internshipId)
    try {
      await api.post(`/internships/${internshipId}/apply`)
      setAppliedIds((prev) => new Set(prev).add(internshipId))
    } catch {
      // If already applied, just reflect that state.
      setAppliedIds((prev) => new Set(prev).add(internshipId))
    } finally {
      setApplyingId(null)
    }
  }

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Matched opportunities</h1>
        <p className="text-ink/60 mb-8">Ranked by compatibility with your current skill profile, with reasons — not just a list.</p>

        {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

        <div className="space-y-6">
          {matches.map((m) => (
            <div key={m.internship.id} className="border border-line rounded-sm p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-medium">{m.internship.title}</p>
                  <p className="text-sm text-ink/50">{m.internship.company} · {m.internship.location} · {m.internship.stipend}</p>
                </div>
                <p className="font-mono text-2xl shrink-0">{m.match_percent}%</p>
              </div>

              <p className="text-sm text-ink/60 mt-3">{m.internship.description}</p>

              <div className="flex flex-wrap gap-2 mt-4">
                {m.strong_skills.map((s) => (
                  <span key={s.skill.id} className="tag-chip bg-havecolor2 text-havecolor">
                    {s.skill.name}
                  </span>
                ))}
                {m.gap_skills.map((s) => (
                  <span key={s.skill.id} className="tag-chip bg-gapcolor2 text-gapcolor">
                    {s.skill.name}
                  </span>
                ))}
              </div>

              <button
                onClick={() => apply(m.internship.id)}
                disabled={applyingId === m.internship.id || appliedIds.has(m.internship.id)}
                className="btn-secondary mt-4"
              >
                {appliedIds.has(m.internship.id) ? 'Applied' : applyingId === m.internship.id ? 'Applying…' : 'Apply'}
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
