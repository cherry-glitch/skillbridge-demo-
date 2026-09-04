import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

const links = [
  { to: '/', label: 'Skill Profile' },
  { to: '/skill-gap', label: 'Skill Gap' },
  { to: '/roadmap', label: 'Roadmap' },
  { to: '/matches', label: 'Matches' },
  { to: '/applications', label: 'Applications' },
]

export default function Sidebar() {
  const { student, logout } = useAuth()

  return (
    <aside className="w-full md:w-56 shrink-0 border-b md:border-b-0 md:border-r border-line md:min-h-screen px-6 py-8 flex md:flex-col justify-between">
      <div>
        <div className="mb-10">
          <p className="font-display text-xl leading-none">SkillBridge</p>
          <p className="text-xs text-ink/50 mt-1 font-mono">student console</p>
        </div>
        <nav className="flex md:flex-col gap-1 flex-wrap">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `px-3 py-2 text-sm rounded-sm transition-colors ${
                  isActive ? 'bg-ink text-paper' : 'text-ink/70 hover:bg-ink/5'
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="hidden md:block pt-8">
        <p className="text-sm text-ink/70 truncate">{student?.name}</p>
        <button onClick={logout} className="text-xs text-ink/50 hover:text-ink underline underline-offset-2 mt-1">
          Sign out
        </button>
      </div>
    </aside>
  )
}
