import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <h1>IP Segment Manager</h1>
          <p>Inventario y validación NOC</p>
        </div>
        <nav className="menu">
          <Link className={location.pathname === "/" ? "active" : ""} to="/">
            Dashboard
          </Link>
          <Link className={location.pathname.startsWith("/segments") ? "active" : ""} to="/segments">
            Segmentos
          </Link>
        </nav>
        <div className="sidebar-footer">
          <div>
            <strong>{user?.full_name}</strong>
            <span>{user?.role}</span>
          </div>
          <button type="button" className="secondary" onClick={logout}>
            Salir
          </button>
        </div>
      </aside>
      <main className="content">{children}</main>
    </div>
  );
}
