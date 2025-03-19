import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import LoadingBackdrop from './LoadingBackdrop';

const ProtectedRoute = ({
  children,
  requiredPermission,
}: {
  children: JSX.Element;
  requiredPermission?: string;
}) => {
  const { user, token, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !token) {
      navigate('/');
    }

    if (token && requiredPermission && !user?.permissions?.includes(requiredPermission)) {
      navigate('/nao-autorizado');
    }
  }, [token, loading, requiredPermission, user, navigate]);

  if (loading) {
    return <LoadingBackdrop open={true} />; // Pass `open` explicitly
  }

  if (token && (!requiredPermission || user?.permissions?.includes(requiredPermission))) {
    return children;
  }

  return null;
};

export default ProtectedRoute;