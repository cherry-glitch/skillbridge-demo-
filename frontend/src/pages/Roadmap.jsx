import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'

export default function Roadmap() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/students/me/roadmap')
      .then(({ data }) => setData(data))
      .catch((err) => setError(err?.response?.data?.detail || 'Could not load roadmap.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Learning roadmap</h1>
        <p className="text-ink/60 mb-8">Recommended in priority order for {data ? data.role.name : 'your target role'}.</p>

        {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

        {error && (
          <div className="border border-dashed border-line rounded-sm p-6 text-center">
            <p className="text-ink/60 mb-3">{error}</p>
            <Link to="/" className="btn-primary inline-flex">Choose a target role</Link>
          </div>
        )}

        {data && (
          <>
            <p className="font-mono text-sm text-ink/50 mb-8">
              ~{data.total_est_hours} hours of study across {data.items.length} skill{data.items.length === 1 ? '' : 's'}
            </p>

            {data.items.length === 0 && (
              <p className="text-ink/60">No gaps to close — you're roadmap-free for this role.</p>
            )}

            <ol className="space-y-8">
              {data.items.map((item, i) => (
                <li key={item.skill.id} className="border-b border-line pb-8 last:border-b-0">
                  <div className="flex items-baseline gap-3 mb-3">
                    <span className="font-mono text-ink/40 text-sm">{String(i + 1).padStart(2, '0')}</span>
                    <h2 className="text-lg">{item.skill.name}</h2>
                  </div>
                  {item.resources.length === 0 && (
                    <p className="text-sm text-ink/40 ml-8">No resources catalogued yet for this skill.</p>
                  )}
                  <div className="ml-8 space-y-2">
                    {item.resources.map((r) => (
                      <div key={r.id} className="flex items-center justify-between text-sm">
                        <div>
                          <p>{r.title}</p>
                          <p className="text-ink/40 text-xs">{r.provider} · {r.resource_type}</p>
                        </div>
                        <span className="font-mono text-ink/50">{r.est_hours}h</span>
                      </div>
                    ))}
                  </div>
                </li>
              ))}
            </ol>
          </>
        )}
      </main>
    </div>
  )
}
