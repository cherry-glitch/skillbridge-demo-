import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProtectedRoute({ children }) {
  const { student, loading } = useAuth()

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-ink/50 font-mono text-sm">loading…</div>
  }
  if (!student) {
    return <Navigate to="/login" replace />
  }
  return children
}
