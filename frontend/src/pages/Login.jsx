import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await login(email, password)
      navigate('/')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not sign in. Check your details and try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <p className="font-display text-2xl mb-1">SkillBridge</p>
        <p className="text-ink/60 mb-8">Sign in to your skill profile.</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="text-sm text-ink/60">Email</label>
            <input
              type="email" required value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="field-input" placeholder="you@college.edu"
            />
          </div>
          <div>
            <label className="text-sm text-ink/60">Password</label>
            <input
              type="password" required value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="field-input" placeholder="••••••••"
            />
          </div>
          {error && <p className="text-sm text-gapcolor">{error}</p>}
          <button type="submit" disabled={busy} className="btn-primary w-full">
            {busy ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="text-sm text-ink/60 mt-6">
          New here?{' '}
          <Link to="/register" className="text-ink underline underline-offset-2">
            Create a student account
          </Link>
        </p>
      </div>
    </div>
  )
}
