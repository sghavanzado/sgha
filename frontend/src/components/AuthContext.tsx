import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance'; // Usar la instancia configurada

interface AuthContextType {
    user: any;
    token: string | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
    user: null,
    token: null,
    loading: true,
    login: async () => {},
    logout: () => {}
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<any>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const verifyToken = async () => {
            if (token) {
                try {
                    // Usar la instancia de axios configurada
                    const response = await fetch('/users/profile', {
                        headers: {
                          'Authorization': `Bearer ${token}`
                        }
                      })
                      if (!response.ok) throw new Error('Token inválido')

                      const userData = await response.json()
                      setUser(userData)
                } catch (error) {
                    logout();
                } finally {
                    setLoading(false);
                }
            } else {
                setLoading(false);
            }
        };
        verifyToken();
    }, [token]);

    const login = async (email: string, password: string) => {
        try {
          setLoading(true);
          const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          })

          const data = await response.json()

          localStorage.setItem('jwt', data.access_token)
          setToken(data.access_token)
          setUser(data.user)
          navigate('/dashboard');
        } catch (error) {
          console.error('Login error:', error);
          throw error;
        } finally {
          setLoading(false);
        }
      };

    const logout = () => {
        localStorage.removeItem('jwt')
        setToken(null);
        setUser(null);
        navigate('/');
    };

    return (
        <AuthContext.Provider value={{ user, token, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);