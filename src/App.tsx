import { Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./context/AuthContext";
import Layout from "./components/Layout";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import SegmentDetailPage from "./pages/SegmentDetailPage";
import SegmentsPage from "./pages/SegmentsPage";

function ProtectedRoutes() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/segments" element={<SegmentsPage />} />
        <Route path="/segments/:id" element={<SegmentDetailPage />} />
      </Routes>
    </Layout>
  );
}

export default function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="page-centered">Cargando...</div>;
  }

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/*" element={user ? <ProtectedRoutes /> : <Navigate to="/login" replace />} />
    </Routes>
  );
}
