import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import Sidebar from '../components/Sidebar.jsx'
import ScoreBar from '../components/ScoreBar.jsx'
import { useAuth } from '../context/AuthContext.jsx'

export default function Dashboard() {
  const { student, setStudent } = useAuth()
  const [skills, setSkills] = useState([])
  const [roles, setRoles] = useState([])
  const [loading, setLoading] = useState(true)
  const [settingRole, setSettingRole] = useState(false)

  async function load() {
    const [skillsRes, rolesRes] = await Promise.all([
      api.get('/students/me/skills'),
      api.get('/roles'),
    ])
    setSkills(skillsRes.data)
    setRoles(rolesRes.data)
    setLoading(false)
  }

  useEffect(() => {
    load()
  }, [])

  async function chooseRole(roleId) {
    setSettingRole(true)
    const { data } = await api.post('/students/me/target-role', { role_id: roleId })
    setStudent(data)
    setSettingRole(false)
  }

  const currentRole = roles.find((r) => r.id === student?.target_role_id)

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar />
      <main className="flex-1 px-6 md:px-12 py-10 max-w-3xl">
        <h1 className="font-display text-3xl mb-1">Your Skill DNA</h1>
        <p className="text-ink/60 mb-8">
          Every skill you've been assessed on, in one place. This updates automatically each time you retake the
          assessment or add verified evidence.
        </p>

        <section className="mb-12">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg">Target role</h2>
            <Link to="/skill-gap" className="text-sm underline underline-offset-2 text-ink/60 hover:text-ink">
              View skill gap →
            </Link>
          </div>

          {currentRole ? (
            <div className="border border-line rounded-sm p-4 flex items-center justify-between">
              <div>
                <p className="font-medium">{currentRole.name}</p>
                <p className="text-sm text-ink/50">{currentRole.description}</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-ink/50 mb-3">Pick a target career so we can find your skill gaps.</p>
          )}

          <div className="flex flex-wrap gap-2 mt-3">
            {roles.map((r) => (
              <button
                key={r.id}
                onClick={() => chooseRole(r.id)}
                disabled={settingRole}
                className={`tag-chip border ${
                  r.id === student?.target_role_id
                    ? 'border-ink bg-ink text-paper'
                    : 'border-line hover:border-ink/40'
                }`}
              >
                {r.name}
              </button>
            ))}
          </div>
        </section>

        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg">Skill profile</h2>
            <Link to="/assessment" className="text-sm underline underline-offset-2 text-ink/60 hover:text-ink">
              Retake assessment →
            </Link>
          </div>

          {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

          {!loading && skills.length === 0 && (
            <div className="border border-dashed border-line rounded-sm p-6 text-center">
              <p className="text-ink/60 mb-3">You haven't been assessed yet.</p>
              <Link to="/assessment" className="btn-primary inline-flex">Take the skill assessment</Link>
            </div>
          )}

          {!loading && skills.length > 0 && (
            <div>
              {skills.map((s) => (
                <div key={s.skill.id} className="ledger-row">
                  <div>
                    <p>{s.skill.name}</p>
                    <p className="text-xs text-ink/40 font-mono">{s.skill.category} · {s.source}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <ScoreBar score={s.score} have={s.score >= 60} />
                    <span className="font-mono text-sm w-10 text-right">{s.score}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
