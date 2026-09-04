import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'

const STATUS_STYLES = {
  applied: 'text-ink/60',
  shortlisted: 'text-havecolor',
  selected: 'text-havecolor',
  rejected: 'text-gapcolor',
}

export default function Applications() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/students/me/applications').then(({ data }) => {
      setApplications(data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Your applications</h1>
        <p className="text-ink/60 mb-8">Track status across everything you've applied to.</p>

        {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

        {!loading && applications.length === 0 && (
          <div className="border border-dashed border-line rounded-sm p-6 text-center">
            <p className="text-ink/60 mb-3">You haven't applied to anything yet.</p>
            <Link to="/matches" className="btn-primary inline-flex">See matched opportunities</Link>
          </div>
        )}

        {applications.map((a) => (
          <div key={a.id} className="ledger-row">
            <div>
              <p>{a.internship.title}</p>
              <p className="text-xs text-ink/40">{a.internship.company} · applied {new Date(a.applied_at).toLocaleDateString()}</p>
            </div>
            <div className="text-right">
              <p className={`text-sm font-medium capitalize ${STATUS_STYLES[a.status] || 'text-ink/60'}`}>{a.status}</p>
              <p className="text-xs text-ink/40 font-mono">{a.match_score}% match</p>
            </div>
          </div>
        ))}
      </main>
    </div>
  )
}
