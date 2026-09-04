import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import api from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [student, setStudent] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadProfile = useCallback(async () => {
    const token = localStorage.getItem('skillbridge_token')
    if (!token) {
      setLoading(false)
      return
    }
    try {
      const { data } = await api.get('/students/me')
      setStudent(data)
    } catch {
      localStorage.removeItem('skillbridge_token')
      setStudent(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadProfile()
  }, [loadProfile])

  async function register(name, email, password) {
    await api.post('/auth/register', { name, email, password })
    await login(email, password)
  }

  async function login(email, password) {
    // The backend's OAuth2PasswordRequestForm expects form-encoded fields.
    const form = new URLSearchParams()
    form.set('username', email)
    form.set('password', password)
    const { data } = await api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    localStorage.setItem('skillbridge_token', data.access_token)
    await loadProfile()
  }

  function logout() {
    localStorage.removeItem('skillbridge_token')
    setStudent(null)
  }

  return (
    <AuthContext.Provider value={{ student, setStudent, loading, register, login, logout, refresh: loadProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
